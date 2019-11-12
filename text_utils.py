

def strToHtmlFormat(string):
    string = string.strip()
    string = string.replace(r'''<''', '&lt;')
    string = string.replace(r'''>''', '&gt;')
    string = _double_stars_to_html(string)
    string = string.replace("'", '&quot;')
    return string


def _double_stars_to_html(text):
    current_tag = ''
    count = text.count('**')
    for x in range(count):
        a, b, c = text.partition('**')
        if b != '':
            if x % 2 == 0:
                current_tag = '<strong>'
                text = a + current_tag + c
            else:
                current_tag = '</strong>'
                text = a + current_tag + c
    if current_tag == '<strong>':
        text = text + '</strong>'
    return text


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


def getFileAsLines(fileName):
    lines = []
    with open(fileName, encoding='utf8') as file:
        line = file.readline()
        lines.append(line[:-1])
        while line:
            line = file.readline()
            lines.append(line[:-1])
    return lines


def replace_spaces_to_tabs(raw_lines):
    lines = []
    for line in raw_lines:
        line = line.replace('    ', '\t')
        lines.append(line)
    return lines
