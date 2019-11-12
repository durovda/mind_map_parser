import pytest
import text_utils

fixture = [('**01**', '<strong>01</strong>'),
           ('**01**\n', '<strong>01</strong>'),
           ('**01 02**', '<strong>01 02</strong>'),
           ('**01 02** 03', '<strong>01 02</strong> 03'),
           ('**01** **02 03**', '<strong>01</strong> <strong>02 03</strong>'),
           ('**01**02', '<strong>01</strong>02'),
           ('**01 02** 03 04, 05 **06 07**, 08 **09 10**',
            '<strong>01 02</strong> 03 04, 05 <strong>06 07</strong>, 08 <strong>09 10</strong>'),
           ("**'01'**", '<strong>&quot;01&quot;</strong>'),
           ("'**01**'", '&quot;<strong>01</strong>&quot;'),
           ('01 **02**', '01 <strong>02</strong>'),
           ('01 **02 03**', '01 <strong>02 03</strong>'),
           ('01 **02 03** 04', '01 <strong>02 03</strong> 04'),
           ('01**02**', '01<strong>02</strong>'),
           ('01**02**03', '01<strong>02</strong>03'),
           ('01**02**03**', '01<strong>02</strong>03<strong></strong>'),
           ("'01'", '&quot;01&quot;')
           ]


@pytest.mark.parametrize('tpl', fixture, ids=[x[0] for x in fixture])
def test_01(tpl):
    result = text_utils.strToHtmlFormat(tpl[0])
    print('\t', result)
    assert tpl[1] == result


def test():
    lst = ['01', '   + 3 symbols', '    + 4 symbols']
    exp = ['01', '   + 3 symbols', '\t+ 4 symbols']
    res = text_utils.replace_spaces_to_tabs(lst)
    assert exp == res
