from mind_map_parser import TextUtils, launch_parser


def test_one():
    launch_parser('sample_mind_map.txt')
    expected_lines = TextUtils.getFileAsLines("expected_test_cases.xml")
    actual_lines = TextUtils.getFileAsLines("test_cases.xml")
    assert expected_lines == actual_lines
