from enum import Enum

__author__ = 'DDA'


class NodeType(Enum):
    Section = 1
    TestCase = 2


class Node:

    def __init__(self, text):
        text = text.replace("«", "\'")
        text = text.replace("»", "\'")
        text = text.replace("\"", "\'")
        self.text = text
        self.level = self.calculateLevel(text)
        self.text = self.text[self.level:]
        self.children = []

    def asText(self):
        return self.text

    def getLevel(self):
        return self.level

    def getIndent(self):
        if self.level == 0:
            return ''
        return '\t' * self.level

    def addChild(self, childNode):
        self.children.append(childNode)

    def getChildren(self):
        return self.children

    def addNodeAsPatternTo(self, nodes, pattern, level, indent):
        node = pattern.format(str(level * indent), TextUtils.strToHtmlFormat(self.asText()))
        nodes.append(node)
        children = self.getChildren()
        if len(children) > 0:
            for child in children:
                child.addNodeAsPatternTo(nodes, pattern, level + 1, 40)

    def print(self):
        print(self.getIndent() + self.asText())
        for child in self.children:
            child.print()

    def addNodesTo(self, lines):
        lines.append(self.getIndent() + self.asText())
        for child in self.children:
            child.addNodesTo(lines)

    @staticmethod
    def calculateLevel(text):
        count = 0
        for symbol in text:
            if symbol == '\t':
                count += 1
            else:
                return count
        return count


class TParser:

    def __init__(self, fileName):
        self.fileName = fileName
        self.nodes = []
        self.testSuite = None

    def run(self):
        megaRawLines = TextUtils.getFileAsLines(self.fileName)
        rawLines = []
        rawNodes = []
        headlineLevel = 0
        for line in megaRawLines:
            if line[:1] not in ('*', '+', ' ', '\t'):
                line = line[1:]
            line = line.replace('    ', '\t')
            rawLines.append(line)
        for line in rawLines:
            lineWithoutTabs = line.replace('\t', '')
            if line[:2] == r'''# ''':
                newLine = line[2:]
                rawNodes.append(Node(newLine))
                headlineLevel = 1
            elif line[:3] == r'''## ''':
                newLine = '\t' + line[3:]
                rawNodes.append(Node(newLine))
                headlineLevel = 2
            elif line[:4] == r'''### ''':
                newLine = '\t\t' + line[4:]
                rawNodes.append(Node(newLine))
                headlineLevel = 3
            elif lineWithoutTabs[:1] == '+':
                line = line.replace(' + ', '$$$')
                line = line.replace('+ ', '')
                line = line.replace('$$$', ' + ')
                rawNodes.append(Node('\t' * headlineLevel + line))
            elif lineWithoutTabs[:1] == '*':
                line = line.replace('**', '$$')
                line = line.replace(' * ', '$$$')
                line = line.replace('* ', '')
                line = line.replace('$$', '**')
                line = line.replace('$$$', ' * ')
                rawNodes.append(Node('\t' * headlineLevel + line))
        if Config.isDebug():
            nodes = []
            for node in rawNodes:
                node.addNodesTo(nodes)
            TextUtils.printLinesToFile(nodes, 'raw_lines.txt')
        maxLevel = self.getMaxLevel(rawNodes)
        for node in rawNodes:
            if node.getLevel() == 0:
                self.nodes.append(node)
        for level in range(maxLevel):
            self.parsLevel(level, rawNodes)
        self.testSuite = TestSuite(self.nodes)
        if Config.isDebug():
            nodes = []
            for node in self.nodes:
                node.addNodesTo(nodes)
            TextUtils.printLinesToFile(nodes, 'tree.txt')

    def getTestSuite(self):
        return self.testSuite

    @staticmethod
    def parsLevel(level, nodes):
        currentNode = None
        for node in nodes:
            if node.getLevel() == level:
                currentNode = node
            elif node.getLevel() == level + 1:
                if currentNode is not None:
                    currentNode.addChild(node)

    @staticmethod
    def getMaxLevel(nodes):
        maxLevel = 0
        for node in nodes:
            currentLevel = node.getLevel()
            if currentLevel > maxLevel:
                maxLevel = currentLevel
        return maxLevel


class TestSuite:

    def __init__(self, rawNodes=None):
        if rawNodes is None:
            rawNodes = []
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
        return TextUtils.strToHtmlFormat(text)

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
        return TextUtils.strToHtmlFormat(text)

    def getName(self):
        return self.name

    def addDescriptionAsXmlTo(self, nodes):
        if self.parent is not None:
            pattern = r'''<span style="color:#a9a9a9;"><p>{0}</p></span>'''
            chainOfParents = pattern.format(TextUtils.strToHtmlFormat(self.getParentsAsText()))
            nodes.append(chainOfParents)
        fullName = '<p>' + TextUtils.strToHtmlFormat(self.rawText) + '</p>'
        nodes.append(fullName)
        if len(self.idea) > 0:
            nodes.append('<p>Идея:</p>')
            pattern = r'''<p style="margin-left: {0}px;">{1}</p>'''
            for node in self.idea:
                strOfIdea = pattern.format('40', TextUtils.strToHtmlFormat(node.asText()))
                nodes.append(strOfIdea)
                children = node.getChildren()
                if len(children) > 0:
                    for child in children:
                        child.addNodeAsPatternTo(nodes, pattern, 2, 40)

    def addPreconditionsAsXmlTo(self, nodes):
        if len(self.preconditions) > 0:
            pattern = r'''<p style="margin-left: {0}px;">{1}</p>'''
            for node in self.preconditions:
                nodes.append('<p>' + TextUtils.strToHtmlFormat(node.asText()) + '</p>')
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
        nodes.append('<p>' + TextUtils.strToHtmlFormat(self.step.asText()) + '</p>')
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
                nodes.append('<p>' + TextUtils.strToHtmlFormat(resultNode.asText()) + '</p>')
                children = resultNode.getChildren()
                if len(children) > 0:
                    for child in children:
                        child.addNodeAsPatternTo(nodes, pattern, 1, 40)
        nodes.append(r''']]></expectedresults>''')
        nodes.append(r'''</step>''')


class TextUtils:

    @staticmethod
    def strToHtmlFormat(string):
        string = string.replace(r'''<''', '&lt;')
        string = string.replace(r'''>''', '&gt;')
        string = string.replace('«', '\"')
        string = string.replace('»', '\"')
        string = string.replace('\"', '&quot;')
        string = ' ' + string + ' '
        string = string.replace(' **', ' <strong>')
        string = string.replace('** ', '</strong> ')
        string = string.replace('**.', '</strong>.')
        string = string.replace('**,', '</strong>,')
        string = string.replace('**', '</strong>')
        string = string.replace(' </strong>', ' <strong>')
        string = string.strip()
        return string

    @staticmethod
    def printLinesToFile(lines, file_name):
        file = None
        try:
            file = open(file_name, mode='w', encoding='utf8')
            for line in lines:
                file.write(line + '\n')
        finally:
            if file is not None:
                file.close()
            else:
                print('Файл не найден')

    @staticmethod
    def getFileAsLines(fileName):
        lines = []
        with open(fileName, encoding='utf8') as file:
            line = file.readline()
            lines.append(line[:-1])
            while line:
                line = file.readline()
                lines.append(line[:-1])
        return lines


class Config:

    @staticmethod
    def isDebug():
        return False


def launch_parser(mind_map_file):
    prs = TParser(mind_map_file)
    prs.run()
    ts = prs.getTestSuite()
    lines = []
    ts.addAsXmlTo(lines)
    TextUtils.printLinesToFile(lines, 'test_cases.xml')


def long_names_to_file(mind_map_file):
    prs = TParser(mind_map_file)
    prs.run()
    ts = prs.getTestSuite()
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
    TextUtils.printLinesToFile(lines, 'long_names.txt')
