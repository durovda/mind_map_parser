from converter_for_test_gesign.case import Case, Step


def is_case_name(line):
    return line[:4].lower() == "тк -"


def get_case_name(line):
    return line[4:].strip()


def is_method_name(line):
    return line[:6].lower() == "метод:"


def get_method_name(line):
    return line[6:].strip()


def is_step_name(line):
    return line[:4].lower() == "шаг:"


def get_step_name(line):
    return line[4:].strip()


def is_story_name(line):
    return line[:4].lower() == "бк -"


def get_story_name(line):
    return line[4:].strip()


def is_feature_name(line):
    return line[:7].lower() == "раздел:"


def get_feature_name(line):
    return line[7:].strip()


def convert_lines_to_cases(lines):
    cases = []
    current_feature = "???"
    current_story = "???"
    current_case = None
    current_step = None
    current_obj_type = None
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        if is_feature_name(line):
            current_feature = get_feature_name(line)
            current_obj_type = "feature"
        elif is_story_name(line):
            current_story = get_story_name(line)
            current_obj_type = "story"
        elif is_case_name(line):
            case = Case(get_case_name(line))
            case.feature = current_feature
            case.story = current_story
            cases.append(case)
            current_case = case
            current_obj_type = "test"
        elif is_method_name(line):
            current_case.method_name = get_method_name(line)
        elif is_step_name(line):
            step = Step(get_step_name(line))
            current_case.steps.append(step)
            current_step = step
            current_obj_type = "step"
        elif line != "":
            if current_obj_type == "test":
                current_case.add_comment(line)
            if current_obj_type == "step":
                current_step.add_comment(line)
    return cases


def get_file_as_lines(file_name):
    with open(file_name, encoding='utf-8') as file:
        lines = file.read().rstrip().split('\n')
    return lines
