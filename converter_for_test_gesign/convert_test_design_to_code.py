from converter_for_test_gesign.case import Case, Step


def is_case_name(line):
    return line[0:5].lower() == "тест:"


def get_case_name(line):
    return line[5:].strip()


def is_method_name(line):
    return line[0:6].lower() == "метод:"


def get_method_name(line):
    return line[6:].strip()


def is_step_name(line):
    return line[0:4].lower() == "шаг:"


def get_step_name(line):
    return line[4:].strip()


def convert_lines_to_cases(lines):
    cases = []
    current_case = None
    current_step = None
    for line in lines:
        line = line.strip()
        if is_case_name(line):
            case = Case(get_case_name(line))
            cases.append(case)
            current_case = case
        if is_method_name(line):
            current_case.method_name = get_method_name(line)
        if is_step_name(line):
            step = Step(get_step_name(line))
            current_case.steps.append(step)
            current_step = step
    return cases


def get_file_as_lines(file_name):
    with open(file_name, encoding='utf-8') as file:
        lines = file.read().rstrip().split('\n')
    return lines
