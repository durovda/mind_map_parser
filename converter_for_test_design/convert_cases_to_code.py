

def convert_cases_to_code(cases):
    tab = "    "
    s = list()
    for case in cases:
        s.append(f"")
        s.append(f"")
        s.append(f"@allure.feature('{case.feature}')")
        s.append(f"@allure.story('{case.story}')")
        s.append(f"@allure.title('{case.name}')")
        s.append(f"def {case.method}(app):")
        if len(case.steps) == 0:
            s.append(f"{tab}pass")
        else:
            for step in case.steps:
                s.append(f"")
                s.append(f"{tab}with allure.step('{step.name}'):")
                for comment in step.comments:
                    s.append(f"{tab}{tab}# {comment}")
                s.append(f"{tab}{tab}pass")
    s.append(f"")
    return s


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
