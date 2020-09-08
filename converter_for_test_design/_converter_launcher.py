from converter_for_test_design.convert_cases_to_code import convert_cases_to_code, printLinesToFile
from converter_for_test_design.convert_design_to_cases import convert_lines_to_cases, get_file_as_lines

cases = convert_lines_to_cases(get_file_as_lines('_test_design.txt'))
lines = convert_cases_to_code(cases)
printLinesToFile(lines, "_result.txt")
