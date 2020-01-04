"""Test functionality in srctools.__init__."""
import pytest

from srctools import EmptyMapping
import srctools


class FalseObject:
    """Test object which is always False."""
    def __bool__(self):
        return False


class TrueObject:
    """Test object which is always True."""
    def __bool__(self):
        return True

true_vals = [1, 1.0, True, 'test', [2], (-1, ), TrueObject(), object()]
false_vals = [0, 0.0, False, '', [], (), FalseObject()]

ints = [
    ('0', 0),
    ('-0', -0),
    ('1', 1),
    ('12352343783', 12352343783),
    ('24', 24),
    ('-4784', -4784),
    ('28', 28),
    (1, 1),
    (-2, -2),
    (3783738378, 3783738378),
    (-23527, -23527),
]

floats = [
    ('0.0', 0.0),
    ('-0.0', -0.0),
    ('-4.5', -4.5),
    ('4.5', 4.5),
    ('1.2', 1.2),
    ('12352343783.189', 12352343783.189),
    ('24.278', 24.278),
    ('-4784.214', -4784.214),
    ('28.32', 28.32),
    (1.35, 1.35),
    (-2.26767, -2.26767),
    (338378.3246, 338378.234),
    (-23527.9573, -23527.9573),
]

false_strings = ['0', 'false', 'no', 'faLse', 'False', 'No', 'NO', 'nO']
true_strings = ['1', 'true', 'yes', 'True', 'trUe', 'Yes', 'yEs', 'yeS']

non_ints = ['-23894.0', '', 'hello', '5j', '6.2', '0.2', '6.9', None, object()]
non_floats = ['5j', '', 'hello', '6.2.5', '4F', '100-', None, object(), float]

# We want to pass through all object types unchanged as defaults.
def_vals = [
    1, 0, True, False, None, object(),
    TrueObject(), FalseObject(), 456.9,
    -4758.97
]


def check_empty_iterable(obj, name, item: object='x'):
    """Check the given object is iterable, and is empty."""
    try:
        iterator = iter(obj)
    except TypeError:
        raise AssertionError(name + ' is not iterable!')
    else:
        assert item not in obj
        with pytest.raises(StopIteration):
            next(iterator)
        with pytest.raises(StopIteration):
            next(iterator)


def test_bool_as_int():
    """Test result of srctools.bool_as_int."""
    for val in true_vals:
        assert srctools.bool_as_int(val) == '1', repr(val)
    for val in false_vals:
        assert srctools.bool_as_int(val) == '0', repr(val)


def test_conv_int():
    for string, result in ints:
        assert srctools.conv_int(string) == result, string

    # Check that float values fail
    marker = object()
    for string, result in floats:
        if isinstance(string, str):  # We don't want to check float-rounding
            assert srctools.conv_int(string, marker) is marker, repr(string)

    # Check non-integers return the default.
    for string in non_ints:
        assert srctools.conv_int(string) == 0
        for default in def_vals:
            # Check all default values pass through unchanged
            assert srctools.conv_int(string, default) is default, repr(string)


def test_conv_bool():
    """Test srctools.conv_bool()"""
    for val in true_strings:
        assert srctools.conv_bool(val)
    for val in false_strings:
        assert not srctools.conv_bool(val)

    # Check that bools pass through
    assert srctools.conv_bool(True)
    assert not srctools.conv_bool(False)

    # None passes through the default
    for val in def_vals:
        assert srctools.conv_bool(None, val) is val


def test_conv_float():
    # Float should convert integers too
    for string, result in ints:
        assert srctools.conv_float(string) == float(result)
        assert srctools.conv_float(string) == result

    for string in non_floats:
        # Default default value
        assert srctools.conv_float(string) == 0.0
        for default in def_vals:
            # Check all default values pass through unchanged
            assert srctools.conv_float(string, default) is default


def test_EmptyMapping():
    marker = object()
    
    # It should be possible to 'construct' an instance..
    assert EmptyMapping() is EmptyMapping

    # Must be passable to dict()
    assert dict(EmptyMapping) == {}

    # EmptyMapping['x'] raises in various forms.
    assert 'x' not in EmptyMapping
    with pytest.raises(KeyError):
        EmptyMapping['x']
    with pytest.raises(KeyError):
        del EmptyMapping['x']

    EmptyMapping['x'] = 4  # Shouldn't fail

    assert 'x' not in EmptyMapping  # but it's a no-op
    with pytest.raises(KeyError):
        EmptyMapping['x']

    # Check it's all empty
    check_empty_iterable(EmptyMapping, 'EmptyMapping')
    check_empty_iterable(EmptyMapping.keys(), 'keys()')
    check_empty_iterable(EmptyMapping.values(), 'values()')
    check_empty_iterable(EmptyMapping.items(), 'items()', item=('x', 'y'))

    # Dict methods 
    assert EmptyMapping.get('x') is None
    assert EmptyMapping.setdefault('x') is None

    assert EmptyMapping.get('x', marker) is marker
    assert EmptyMapping.setdefault('x', marker) is marker
    assert EmptyMapping.pop('x', marker) is marker

    with pytest.raises(KeyError):
        EmptyMapping.popitem()
    with pytest.raises(KeyError):
        EmptyMapping.pop('x')

    assert not EmptyMapping

    assert len(EmptyMapping) == 0

    # Should work, but do nothing and return None.
    assert EmptyMapping.update({1: 23, 'test': 34, }) is None
    assert EmptyMapping.update(other=5, a=1, b=3) is None

    # Can't give more than one mapping as a positional argument,
    # though.
    with pytest.raises(TypeError):
        EmptyMapping.update({3: 4}, {1: 2})

    # Check it's registered in ABCs.
    from collections import abc
    assert isinstance(EmptyMapping, abc.Container)
    assert isinstance(EmptyMapping, abc.Sized)
    assert isinstance(EmptyMapping, abc.Mapping)
    assert isinstance(EmptyMapping, abc.MutableMapping)


def test_quote_escape():
    """Test escaping various quotes"""
    assert srctools.escape_quote_split('abcdef') ==['abcdef']
    # No escapes, equivalent to str.split
    assert (
        srctools.escape_quote_split('"abcd"ef""  " test') ==
        '"abcd"ef""  " test'.split('"')
    )

    assert (
        srctools.escape_quote_split(r'"abcd"ef\""  " test') ==
        ['', 'abcd', 'ef"', '  ', ' test']
    )
    # Check double-quotes next to others, and real quotes
    assert (
        srctools.escape_quote_split(r'"test\"\"" blah"') ==
        ['', 'test""', ' blah', '']
    )
