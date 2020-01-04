import pytest
from srctools.property_parser import Property, KeyValError, NoKeyError
from srctools.tokenizer import C_Tokenizer, Py_Tokenizer
from srctools import property_parser as pp_mod

if C_Tokenizer is not None:
    parms = [C_Tokenizer, Py_Tokenizer]
    ids = ['Cython tokenizer', 'Python tokenizer']
else:
    pytest.fail('No _tokenizer')
    parms = [Py_Tokenizer]
    ids = ['Python tokenizer']


@pytest.fixture(params=parms, ids=ids)
def py_c_token(request):
    """Run the test twice, for the Python and C versions of Tokenizer."""
    orig_tok = pp_mod.Tokenizer
    try:
        pp_mod.Tokenizer = request.param
        yield None
    finally:
        pp_mod.Tokenizer = orig_tok


def assert_tree(first, second):
    """Check that two property trees match exactly (including case)."""
    assert first.name == second.name
    assert first.real_name == second.real_name
    assert first.has_children() == second.has_children()
    if first.has_children():
        for child1, child2 in zip(first, second):
            assert_tree(child1, child2)
    else:
        assert first.value == second.value


def test_constructor():
    """Test the constructor for Property objects."""
    Property(None, [])
    Property('Test', 'value with spaces and ""')
    block = Property('Test_block', [
        Property('Test', 'value\0'),
        Property('Test', [
            Property('leaf', 'data'),
        ]),
        Property('Test2', 'other'),
        Property('Block', []),
    ])
    assert block.real_name == 'Test_block'
    children = list(block)
    assert children[0].real_name == 'Test'
    assert children[1].real_name == 'Test'
    assert children[2].real_name == 'Test2'
    assert children[3].real_name == 'Block'

    assert children[0].value == 'value\0'
    assert children[2].value, 'other'
    assert list(children[3]) == []

    sub_children = list(children[1])
    assert sub_children[0].real_name == 'leaf'
    assert sub_children[0].value == 'data'
    assert len(sub_children) == 1


def test_names():
    """Test the behaviour of Property.name."""
    prop = Property('Test1', 'value')
    
    # Property.name casefolds the argument.
    assert prop.name == 'test1'
    assert prop.real_name == 'Test1'
    
    # Editing name modifies both values
    prop.name = 'SECOND_test'
    assert prop.name == 'second_test'
    assert prop.real_name == 'SECOND_test'
    
    # It can also be set to None.
    prop.name = None
    assert prop.name is prop.real_name is None

# If edited, update test_parse() and tokeniser check too!
parse_test = '''

// """"" should be ignored

"Root1"
    {
        

    "Key" "Value"
        "Extra"        "Spaces"
    // "Commented" "out"
    "Block"  {
        "Empty"
             {
             } }
    "Block" // "with value"
  {
 bare
    {   "block" "he\\tre"
          }
            }
       }
    "Root2"
    {
    "Name with \\" in it" "Value with \\" inside"
    "multiline" "text
\tcan continue
for many \\"lines\\" of
  possibly indented

text"
    "Escapes" "\\t \\n \\d"
    "Oneliner" { "name" "value" }
    }
    "CommentChecks"
        {
        "after " "value" //comment [ ] ""
        "FlagBlocks" "This" [test_disabled]
        "Flag" "allowed" [!test_disabled]
        "FlagAllows" "This" [test_enabled]
        "Flag" "blocksthis" [!test_enabled]

        "Replaced" "shouldbe"
        "Replaced" "toreplace" [test_enabled]
        "Replaced" "alsothis"  [test_enabled]
        
        "Replaced" "shouldbe2"
        "Replaced" "toreplace2" [!test_disabled]
        "Replaced" "alsothis2"  [!test_disabled]

        "Replaced"
            {
            "shouldbe3" "replaced3"
            "prop2" "blah"
            }
        "Replaced" [test_enabled]
            {
            "lambda" "should"
            "replace" "above"
            }
        
        "Replaced"
            {
            "shouldbe4" "replaced4"
            "prop2" "blah"
            }
        "Replaced" [!test_disabled]
            {
            "lambda2" "should2"
            "replace2" "above2"
            }
        }
'''

P = Property
parse_result = P(None, [
    P('Root1', [
        P("Key", "Value"),
        P("Extra", "Spaces"),
        P("Block", [
            P('Empty', []),
        ]),
        P('Block', [
            P('bare', [
                P('block', 'he\tre'),
            ]),
        ]),
    ]),
    P('Root2', [
        P('Name with " in it', 'Value with \" inside'),
        P('multiline',
          'text\n\tcan continue\nfor many "lines" of\n  possibly indented\n\ntext'
          ),
        # Note, invalid = unchanged.
        P('Escapes', '\t \n \\d'),
        P('Oneliner', [Property('name', 'value')]),
    ]),
    P('CommentChecks', [
        P('after ', 'value'),
        P('Flag', 'allowed'),
        P('FlagAllows', 'This'),
        P('Replaced', 'toreplace'),
        P('Replaced', 'alsothis'),
        P('Replaced', 'toreplace2'),
        P('Replaced', 'alsothis2'),
        P('Replaced', [
            P('lambda', 'should'),
            P('replace', 'above'),
        ]),
        P('Replaced', [
            P('lambda2', 'should2'),
            P('replace2', 'above2'),
        ])
    ])
])
del P


def test_parse(py_c_token):
    """Test parsing strings."""
    result = Property.parse(
        # iter() ensures sequence methods aren't used anywhere.
        iter(parse_test.splitlines()),
        # Check active and inactive flags are correctly treated.
        flags={
            'test_enabled': True,
            'test_disabled': False,
        }
    )
    assert_tree(parse_result, result)

    # Test the whole string can be passed too.
    result = Property.parse(
        parse_test,
        flags={
            'test_enabled': True,
            'test_disabled': False,
        },
    )
    assert_tree(parse_result, result)

    # Check export roundtrips.
    assert_tree(parse_result, Property.parse(parse_result.export()))
    
def test_build():
    """Test the .build() constructor."""
    prop = Property(None, [])

    with prop.build() as b:
        with b.Root1:
            b.Key("Value")
            b.Extra("Spaces")
            with b.Block:
                with b.Empty:
                    pass
            with b.Block:
                with b.bare:
                    b.block('he\tre')
        with b.Root2:
            b['Name with " in it']('Value with \" inside')
            b.multiline(
              'text\n\tcan continue\nfor many "lines" of\n  possibly '
              'indented\n\ntext'
            )
            # Note invalid = unchanged.
            b.Escapes('\t \n \\d')
            with b.Oneliner:
                b.name('value')
        
        with b.CommentChecks:
            b['after ']('value')
            b.Flag('allowed')
            b.FlagAllows('This')
            b.Replaced('toreplace')
            b.Replaced('alsothis')
            b.Replaced('toreplace2')
            b.Replaced('alsothis2')
            with b.Replaced:
                b.lambda_('should')
                b.replace('above')
            with b.Replaced:
                b['lambda2']('should2')
                b.replace2('above2')

    assert_tree(parse_result, prop)
    

def test_parse_fails(py_c_token):
    """Test various forms of invalid syntax to ensure they indeed fail."""
    def t(text):
        """Test a string to ensure it fails parsing."""
        try:
            result = Property.parse(text)
        except KeyValError:
            pass
        else:
            pytest.fail("Successfully parsed bad text ({!r}) to {!r}".format(
                text,
                result,
            ))
    # Bare text at end of file
    t('''\
regular text. with sentences.
    ''')
    # Bare text in the middle
    t('''\
regular text. with sentences.
    "blah" "value"
    ''')
    t('''\
"Ok block"
    {
    "missing" //value
    }
''')

    # Test block without a block
    t('''\
"block1"
"no_block" 
''')

    # Test block expecting a {
    t('''\
"block"
    {
    "blsh" "Val"
    }
"block1"
''')

    # Test characters before a keyvalue
    t('''\
bbhf  "text before"
    "key" "value
''')
    t('''
  "text" bl "between"
    "key" "value
''')
    # Test text after the keyvalue
    t('''\
    "text" "value" blah
    "key" "value
    ''')
    # Test quotes after the keyvalue
    t('''
    "text" "with extra" "
''')

    t('''
    "multi" "line
text with
  multiple
  quotes" "
''')

    # Test a flag without ] at end
    t('''
    "Name" "value" [flag
    ''')

    # Test a flag with values after the bracket.
    t('''
    "Name" "value" [flag ] hi
    ''')

    # Test too many closing brackets
    t('''
    "Block"
        {
        "Opened"
            {
            "Closed" "value"
            }
            }
        }
    "More text" "value"
    ''')

    # Test property with a value and block
    t('''
    "Block" "value"
        {
        "Name" "value"
        }
    ''')

    # Test '/' in text by itself (not a comment!)
    t('''\
    "Block"
        {
        "Name" / "Value"
            {
            }
        }
    ''')

    # Test unterminated strings
    t('''\
    "Block"
        {
        "blah
        }
    ''')

    # Test unterminated string with '\' at the end
    t('''"Blah \\''')

    # Test too many open brackets
    t('''\
    "Block"
        {
        "Key" "Value"
        "Block"
            {
            {
            "Key" "value"
            }
        }
    ''')

    # Too many open blocks.
    t('''\
    "Block"
        {
        "Key" "Value"
        "Block2"
            {
            "Key" "Value"
            }
    ''')

    t('''\
    "Key" "value
    which is multi-line
    and no ending.
    ''')

    # Test a key and value split over a line.
    t('''\
    "block"
        {
        "key" "value"
        "key"
        "value"
        }
    ''')


def test_edit():
    """Check functionality of Property.edit()"""
    test_prop = Property('Name', 'Value')

    def check(prop: Property, name, value):
        """Check the property was edited, and has the given value."""
        nonlocal test_prop
        assert prop is test_prop
        assert prop.real_name == name
        assert prop.value == value
        test_prop = Property('Name', 'Value')

    check(test_prop.edit(), 'Name', 'Value')
    check(test_prop.edit(name='new_name',), 'new_name', 'Value')
    check(test_prop.edit(value='new_value'), 'Name', 'new_value')

    # Check converting a block into a keyvalue
    test_prop = Property('Name', [
        Property('Name', 'Value')
    ])
    check(test_prop.edit(value='Blah'), 'Name', 'Blah')

    # Check converting a keyvalue into a block.
    child_1 = Property('Key', 'Value')
    new_prop = test_prop.edit(value=[child_1, Property('Key2', 'Value')])
    assert test_prop is new_prop
    assert list(test_prop)[0] is child_1


def test_bool():
    """Check bool(Property)."""
    assert bool(Property('Name', '')) is False
    assert bool(Property('Name', 'value')) is True
    assert bool(Property('Name', [])) is False
    assert bool(Property('Name', [
        Property('Key', 'Value')
    ])) is True
