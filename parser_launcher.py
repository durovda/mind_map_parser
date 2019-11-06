from mind_map_parser import launch_parser, long_names_to_file

launch_parser('mind_map.txt', 'test_cases.xml')
long_names_to_file('mind_map.txt', 'long_names.txt')

print('Ok')
input('Для завершения нажмите "Enter"')
