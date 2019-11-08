import text_utils
from mind_map_parser import pars_map_to_xml


def test_real_suite():
    pars_map_to_xml('fixture/01_mind_map.txt', 'results/01_test_cases.xml')
    expected_lines = text_utils.getFileAsLines("fixture/01_expected_test_cases.xml")
    actual_lines = text_utils.getFileAsLines("results/01_test_cases.xml")
    assert expected_lines == actual_lines
