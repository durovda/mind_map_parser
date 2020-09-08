from converter_for_test_design.convert_cases_to_code import convert_cases_to_code
from converter_for_test_design.convert_design_to_cases import convert_lines_to_cases, get_file_as_lines


def test_convert_cases_to_code_and_print():
    lines = get_file_as_lines('complete_test_design.txt')
    cases = convert_lines_to_cases(lines)
    lines = convert_cases_to_code(cases)
    for line in lines:
        print(line)
