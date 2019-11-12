from enum import Enum
from text_utils import strToHtmlFormat, getFileAsLines, printLinesToFile, replace_spaces_to_tabs

__author__ = 'DDA'


class NodeType(Enum):
    Section = 1
    TestCase = 2


class Node:

    def __init__(self, text):
        text = text.replace("«", "'")
        text = text.replace("»", "'")
        text = text.replace('"', "'")
        self._text = text
        self._level = self._calculateLevel(text)
        self._text = self._text[self._level:]
        self._children = []

    def asText(self):
        return self._text

    def getLevel(self):
        return self._level

    def getIndent(self):
        if self._level == 0:
            return ''
        return '\t' * self._level

    def addChild(self, childNode):
        self._children.append(childNode)

    def getChildren(self):
        return self._children

    def addNodeAsPatternTo(self, nodes, pattern, level, indent):
        node = pattern.format(str(level * indent), strToHtmlFormat(self.asText()))
        nodes.append(node)
        children = self.getChildren()
        if len(children) > 0:
            for child in children:
                child.addNodeAsPatternTo(nodes, pattern, level + 1, 40)

    def print(self):
        print(self.getIndent() + self.asText())
        for child in self._children:
            child.print()

    def addNodesTo(self, lines):
        lines.append(self.getIndent() + self.asText())
        for child in self._children:
            child.addNodesTo(lines)

    @staticmethod
    def _calculateLevel(text):
        count = 0
        for symbol in text:
            if symbol == '\t':
                count += 1
            else:
                return count
        return count


class TParser:

    def __init__(self):
        self._nodes = []

    def parse_mind_map_to_node_tree(self, fileName):
        lines = getFileAsLines(fileName)
        return self._parse_lines_to_node_tree(lines)

    def _parse_lines_to_node_tree(self, lines):
        raw_lines = self._remove_mysterious_initial_symbol(lines)
        raw_lines = replace_spaces_to_tabs(raw_lines)
        raw_nodes = self._convert_lines_to_linear_list_of_nodes(raw_lines)
        result_nodes = self._convert_linear_list_to_hierarchy(raw_nodes)
        return result_nodes

    @staticmethod
    def _convert_lines_to_linear_list_of_nodes(raw_lines):
        headlineLevel = 0
        raw_nodes = []
        for line in raw_lines:
            lineWithoutTabs = line.replace('\t', '')
            if lineWithoutTabs[:1] == '+':
                line = line.replace(' + ', '$$$')
                line = line.replace('+ ', '')
                line = line.replace('$$$', ' + ')
                raw_nodes.append(Node('\t' * headlineLevel + line))
            elif lineWithoutTabs[:1] == '*':
                line = line.replace('**', '$$')
                line = line.replace(' * ', '$$$')
                line = line.replace('* ', '')
                line = line.replace('$$', '**')
                line = line.replace('$$$', ' * ')
                raw_nodes.append(Node('\t' * headlineLevel + line))
        return raw_nodes

    def _convert_linear_list_to_hierarchy(self, raw_nodes):
        maxLevel = self._get_max_level(raw_nodes)
        result_nodes = []
        for raw_node in raw_nodes:
            if raw_node.getLevel() == 0:
                result_nodes.append(raw_node)
        for level in range(maxLevel):
            currentNode = None
            for node in raw_nodes:
                if node.getLevel() == level:
                    currentNode = node
                elif node.getLevel() == level + 1:
                    if currentNode is not None:
                        currentNode.addChild(node)
        return result_nodes

    @staticmethod
    # Иногда в самом начале файла присутствует 'таинственный' символ...
    # Этот метод удаляет его (если он есть)
    def _remove_mysterious_initial_symbol(raw_lines):
        if raw_lines[0][:1] not in ('*', '+', ' ', '\t'):
            raw_lines[0] = raw_lines[0][1:]
        return raw_lines

    @staticmethod
    def _get_max_level(nodes):
        maxLevel = 0
        for node in nodes:
            currentLevel = node.getLevel()
            if currentLevel > maxLevel:
                maxLevel = currentLevel
        return maxLevel


class TestSuite:

    def __init__(self, rawNodes=None):
        if rawNodes is None:
            self.rawNodes = []
        self.rawNodes = rawNodes
        self.testSuiteElements = []
        self.children = []
        for node in self.rawNodes:
            text = node.asText().strip()
            if text[:2] == 'ТК':
                element = TestCase(node.getLevel(), text, node.getChildren(), self.testSuiteElements)
                self.testSuiteElements.append(element)
                self.children.append(element)
            elif text[:3] != 'ДДА':
                element = TSection(node.getLevel(), text, node.getChildren(), self.testSuiteElements)
                self.testSuiteElements.append(element)
                self.children.append(element)

    def addAsXmlTo(self, nodes):
        nodes.append(r'''<?xml version="1.0" encoding="UTF-8"?>''')
        haveSections = False
        for node in self.children:
            if node.getType() == NodeType.Section:
                haveSections = True
        if not haveSections:
            nodes.append('<testcases>')
        for node in self.children:
            node.addAsXmlTo(nodes)
        if not haveSections:
            nodes.append('</testcases>')

    def getTestCases(self):
        testCases = []
        for element in self.testSuiteElements:
            if element.getType() == NodeType.TestCase:
                testCases.append(element)
        return testCases


class TSection:

    def __init__(self, level, rawText, rawNodes, testSuiteElements, parent=None):
        self.type = NodeType.Section
        self.level = level
        self.rawText = rawText
        self.rawNodes = rawNodes
        self.parent = parent
        self.testSuiteElements = testSuiteElements
        self.children = []
        for node in self.rawNodes:
            text = node.asText()
            if text[:2] == 'ТК':
                element = TestCase(node.getLevel(), text, node.getChildren(), self.testSuiteElements, self)
                self.testSuiteElements.append(element)
                self.children.append(element)
            elif text[:3] != 'ДДА':
                element = TSection(node.getLevel(), text, node.getChildren(), self.testSuiteElements, self)
                self.testSuiteElements.append(element)
                self.children.append(element)

    def getType(self):
        return self.type

    def getName(self):
        text = self.rawText.replace('*', '')
        text = text.strip()
        return strToHtmlFormat(text)

    def getStoryNumber(self):
        if self.getName()[:9].lower() == 'inrights-':
            return self.getName()[:13]
        elif self.parent is not None:
            return self.parent.getStoryNumber()
        else:
            return None

    def addParentsTo(self, parents):
        if self.parent is not None:
            parents.append(self.parent.getName())
            self.parent.addParentsTo(parents)

    def addAsXmlTo(self, nodes):
        pattern = r'''<testsuite id="" name="{0}">'''
        nodes.append(pattern.format(self.getName()))
        nodes.append(r'''<node_order><![CDATA[]]></node_order>''')
        nodes.append(r'''<details><![CDATA[]]></details>''')
        for node in self.children:
            node.addAsXmlTo(nodes)
        nodes.append(r'''</testsuite>''')


class TestCase:

    def __init__(self, level, rawText, rawNodes, testSuiteElements, parent=None):
        self.type = NodeType.TestCase
        self.level = level
        self.rawText = rawText
        self.rawNodes = rawNodes
        self.parent = parent
        self.testSuiteElements = testSuiteElements
        self.name = self.makeName()
        self.children = []
        self.idea = []
        self.preconditions = []
        self.steps = []
        currentStepNumber = 1
        for node in self.rawNodes:
            text = node.asText()
            if text[:4] == 'КРТ:':
                self.name = text[5:].strip()
            elif text[:12].lower() == 'предусловия:':
                self.preconditions = node.getChildren()
            elif text[:5].lower() == 'шаги:':
                sNodes = node.getChildren()
                currentStep = None
                for sNode in sNodes:
                    sNodeText = sNode.asText()
                    if sNodeText[:3].lower() == 'ор:':
                        currentStep.result = sNode.getChildren()
                    else:
                        currentStep = TestCaseStep(sNode, currentStepNumber)
                        currentStepNumber += 1
                        self.steps.append(currentStep)
            else:
                self.idea.append(node)

    def getType(self):
        return self.type

    def getRawText(self):
        return self.rawText

    def makeName(self):
        text = self.rawText.replace('*', '')
        text = text[7:].strip()
        return strToHtmlFormat(text)

    def getName(self):
        return self.name

    def addDescriptionAsXmlTo(self, nodes):
        if self.parent is not None:
            pattern = r'''<span style="color:#a9a9a9;"><p>{0}</p></span>'''
            chainOfParents = pattern.format(strToHtmlFormat(self.getParentsAsText()))
            nodes.append(chainOfParents)
        fullName = '<p>' + strToHtmlFormat(self.rawText) + '</p>'
        nodes.append(fullName)
        if len(self.idea) > 0:
            nodes.append('<p>Идея:</p>')
            pattern = r'''<p style="margin-left: {0}px;">{1}</p>'''
            for node in self.idea:
                strOfIdea = pattern.format('40', strToHtmlFormat(node.asText()))
                nodes.append(strOfIdea)
                children = node.getChildren()
                if len(children) > 0:
                    for child in children:
                        child.addNodeAsPatternTo(nodes, pattern, 2, 40)

    def addPreconditionsAsXmlTo(self, nodes):
        if len(self.preconditions) > 0:
            pattern = r'''<p style="margin-left: {0}px;">{1}</p>'''
            for node in self.preconditions:
                nodes.append('<p>' + strToHtmlFormat(node.asText()) + '</p>')
                children = node.getChildren()
                if len(children) > 0:
                    for child in children:
                        child.addNodeAsPatternTo(nodes, pattern, 1, 40)

    def addStepsAsXmlTo(self, nodes):
        if len(self.steps) > 0:
            for node in self.steps:
                node.addAsXmlTo(nodes)

    def addStoryNumberAsXmlTo(self, nodes):
        if self.parent is not None:
            storyNumber = self.parent.getStoryNumber()
            if storyNumber is not None:
                nodes.append(r'''<custom_fields><custom_field>''')
                nodes.append(r'''<name><![CDATA[UserStory]]></name>''')
                pattern = r'''<value><![CDATA[{0}]]></value>'''
                nodes.append(pattern.format(storyNumber))
                nodes.append(r'''</custom_field></custom_fields>''')

    def getParentsAsText(self):
        parents = [self.parent.getName()]
        self.parent.addParentsTo(parents)
        parents.reverse()
        return " -> ".join(parents)

    def addAsXmlTo(self, nodes):
        pattern = r'''<testcase internalid="" name="{0}">'''
        nodes.append(pattern.format(self.getName()))
        nodes.append(r'''<node_order><![CDATA[]]></node_order>''')
        nodes.append(r'''<externalid><![CDATA[]]></externalid>''')
        nodes.append(r'''<version><![CDATA[]]></version>''')
        nodes.append(r'''<summary><![CDATA[''')
        self.addDescriptionAsXmlTo(nodes)
        nodes.append(''']]></summary>''')
        nodes.append(r'''<preconditions><![CDATA[''')
        self.addPreconditionsAsXmlTo(nodes)
        nodes.append(r''']]></preconditions>''')
        nodes.append(r'''<execution_type><![CDATA[1]]></execution_type>''')
        nodes.append(r'''<importance><![CDATA[2]]></importance>''')
        nodes.append(r'''<steps>''')
        self.addStepsAsXmlTo(nodes)
        nodes.append(r'''</steps>''')
        self.addStoryNumberAsXmlTo(nodes)
        nodes.append(r'''</testcase>''')


class TestCaseStep:

    def __init__(self, step, stepNumber, result=None):
        if result is None:
            result = []
        self.step = step
        self.stepNumber = stepNumber
        self.result = result

    def addAsXmlTo(self, nodes):
        pattern = r'''<step><step_number><![CDATA[{0}]]></step_number>'''
        nodes.append(pattern.format(str(self.stepNumber)))
        nodes.append('''<actions><![CDATA[''')
        nodes.append('<p>' + strToHtmlFormat(self.step.asText()) + '</p>')
        pattern = r'''<p style="margin-left: {0}px;">{1}</p>'''
        children = self.step.getChildren()
        if len(children) > 0:
            for child in children:
                child.addNodeAsPatternTo(nodes, pattern, 1, 40)
        nodes.append(r''']]></actions>''')
        nodes.append(r'''<expectedresults><![CDATA[''')
        resultNodes = self.result
        if len(resultNodes) > 0:
            for resultNode in resultNodes:
                nodes.append('<p>' + strToHtmlFormat(resultNode.asText()) + '</p>')
                children = resultNode.getChildren()
                if len(children) > 0:
                    for child in children:
                        child.addNodeAsPatternTo(nodes, pattern, 1, 40)
        nodes.append(r''']]></expectedresults>''')
        nodes.append(r'''</step>''')


def pars_map_to_xml(mind_map_file, test_cases_file):
    prs = TParser()
    node_tree = prs.parse_mind_map_to_node_tree(mind_map_file)
    ts = TestSuite(node_tree)
    lines = []
    ts.addAsXmlTo(lines)
    printLinesToFile(lines, test_cases_file)


def long_names_to_file(mind_map_file, long_names_file):
    prs = TParser()
    node_tree = prs.parse_mind_map_to_node_tree(mind_map_file)
    ts = TestSuite(node_tree)
    tks = ts.getTestCases()
    lines = []
    count = 0
    for tk in tks:
        name = tk.getName().strip()
        if len(name) > 100:
            lines.append(tk.getRawText()[:5])
            lines.append(name)
            lines.append(name[:100])
            lines.append('\n')
            count += 1
    lines.append('Длинных имён: ' + str(count))
    printLinesToFile(lines, long_names_file)
