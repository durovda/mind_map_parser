from mind_map_parser import TextUtils, launch_parser


def test_real_test_suite():
    launch_parser('mind_map_01.txt', 'results/test_cases_01.xml')
    expected_lines = TextUtils.getFileAsLines("expected_test_cases_01.xml")
    actual_lines = TextUtils.getFileAsLines("results/test_cases_01.xml")
    assert expected_lines == actual_lines
