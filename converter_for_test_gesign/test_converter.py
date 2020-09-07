from converter_for_test_gesign.case import Case, Step
from converter_for_test_gesign.convert_test_design_to_code import get_file_as_lines, convert_lines_to_cases, is_case_name, \
    get_case_name, is_method_name, get_method_name, is_step_name, get_step_name


def test_read_file():
    lines = get_file_as_lines('file_with_two_lines.txt')
    assert 2 == len(lines)
    assert "Тест: Название теста" == lines[0]
    assert "Метод: Имя метода" == lines[1]


def test_is_case_name():
    assert is_case_name("Тест: Первый тест")


def test_get_case_name():
    assert "Первый тест" == get_case_name("Тест: Первый тест")


def test_is_method_name():
    assert is_method_name("Метод: test_one")


def test_get_method_name():
    assert "test_one" == get_method_name("Метод: test_one")


def test_is_step_name():
    assert is_step_name("Шаг: Первый шаг 1-го теста")


def test_get_step_name():
    assert "Первый шаг 1-го теста" == get_step_name("Шаг: Первый шаг 1-го теста")


def test_add_step_to_case():
    case = Case("Тест")
    case.steps.append(Step("Первый шаг"))
    assert "Первый шаг" == case.steps[0].name


def test_convert_one_test():
    lines = get_file_as_lines('simple_test_design.txt')
    cases = convert_lines_to_cases(lines)
    case = cases[0]
    assert "Первый тест" == case.name
    assert "test_one" == case.method_name
    assert "Первый шаг 1-го теста" == case.steps[0].name
    assert "Второй шаг 1-го теста" == case.steps[1].name


def test_convert_test_suite():
    lines = get_file_as_lines('simple_test_design.txt')
    cases = convert_lines_to_cases(lines)
    case = cases[0]
    assert "Первый тест" == case.name
    assert "test_one" == case.method_name
    assert "Первый шаг 1-го теста" == case.steps[0].name
    assert "Второй шаг 1-го теста" == case.steps[1].name
    case = cases[1]
    assert "Второй тест" == case.name
    assert "test_two" == case.method_name
    assert "Первый шаг 2-го теста" == case.steps[0].name
