from mind_map_parser import pars_map_to_xml, long_names_to_file

# launch_parser('mind_map.txt', 'test_cases.xml')
# long_names_to_file('mind_map.txt', 'long_names.txt')

pars_map_to_xml('test/fixture/01_mind_map.txt', 'test/fixture/01_expected_test_cases.xml')

print('Ok')
input('Для завершения нажмите "Enter"')
