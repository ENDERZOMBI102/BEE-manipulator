from dataclasses import dataclass
from enum import IntEnum, auto
from os import PathLike
from pathlib import Path
from typing import Union, Tuple, List, Dict, Any, Type, Optional, Callable


class TokType( IntEnum ):
	Word = auto()
	Semicolon = auto()
	Dot = auto()

	Padding = auto()
	Newline = auto()
	EOF = auto()

	Comment = auto()
	Key = auto()
	Value = auto()
	Class = auto()


Loc = Tuple[ str, int, int ]
TokValue = Union[str, int, None]


@dataclass
class Token:
	typ: TokType
	value: TokValue
	loc: Loc


def eof( last: Token ) -> Token:
	return Token( TokType.EOF, None, last.loc )


def _tokenizeString( data: str, file: str ) -> List[ Token ]:
	tokens: List[ Token ] = [ ]
	line: int = 1
	char: int = 1
	i = 0

	def getChar( offset=0 ) -> str:
		return data[ i + offset ]

	def add(typ: TokType, value: TokValue, loc: Loc = None ) -> None:
		tokens.append( Token( typ, value, loc or (file, line, char) ) )

	while len( data ) > i:
		# print(data[i])
		# comment
		if getChar() == '#':
			# print('comment')
			string = ''
			while getChar() != '\n':
				string += getChar()
				i += 1
			# print( string )
			add( TokType.Comment, string, ( file, line, char + len( string ) ) )
		# padding
		elif getChar() == '\t':
			# print('padding')
			count = 1
			while getChar(1) == '\t':
				count += 1
				i += 1
			add( TokType.Padding, count )
			i += 1
			char += 1 + count
		# semicolon
		elif getChar() == ':':
			# print('semicolon')
			add( TokType.Semicolon, None )
			i += 1
			char += 1
		# newline
		elif getChar() == '\n':
			# print('newline')
			add( TokType.Newline, None )
			line += 1
			char = 1
			i += 1
		# dot
		elif getChar() == '.':
			# print('dot')
			add( TokType.Dot, None )
			i += 1
			char += 1
		# space
		elif getChar() == ' ':
			i += 1
			char += 1
		# word
		else:
			# print('word')
			string = getChar()
			while len(data) - 1 > i and getChar(1) not in ( ':', '\n', '\0', '#' ):
				i += 1
				string += getChar()
			add( TokType.Word, string )
			i += 1
			char += len(string) + 1

	add( TokType.EOF, None, ( file, line + 1, 0 ) )

	return tokens


def _parseTokens( tokList: List[Token ] ) -> List[Token ]:
	processedTokens: List[Token] = []
	i = 0

	def peek( offset=1 ) -> Token:
		return tokList[ i + offset ] if len(tokList) > i + offset else tokList[-1]

	def consume() -> Token:
		nonlocal i
		i += 1
		return tokList[ i - 1 ]

	def peekType( offset=1 ) -> TokType:
		return peek(offset).typ

	def peekIsType( offset, typ: TokType ) -> bool:
		return peekType(offset) == typ

	def discard() -> None:
		consume()

	def add( typ: TokType, tok: Token ) -> None:
		processedTokens.append( Token( typ, tok.value, tok.loc ) )

	while len(tokList) > i:
		# key
		if peekIsType( 0, TokType.Word ) and peekIsType( 1, TokType.Semicolon ):
			tok = consume()
			# print( 'key:', tok )
			add( TokType.Key, tok )
		# value
		elif ( peekIsType( 0, TokType.Semicolon ) or peekIsType(0, TokType.Padding) ) and peekIsType( 1, TokType.Word ) and not peekIsType( 2, TokType.Semicolon ):
			prev = consume()
			if prev.typ == TokType.Padding:
				processedTokens.append( prev )
			tok = consume()
			# print( 'value:', tok )
			add( TokType.Value, tok )
		# class
		elif peekIsType( 0, TokType.Dot ) and peekIsType( 1, TokType.Word ) and peekIsType( 2, TokType.Semicolon ):
			discard()
			tok = consume()
			discard()
			# print( 'class:', tok )
			add( TokType.Class, tok )
		# padding|newline|eof
		elif peekType(0) in ( TokType.Padding, TokType.Newline, TokType.EOF ):
			processedTokens.append( consume() )
			# print( f'{processedTokens[-1].typ.name.lower()}:', processedTokens[-1] )
		# discarded
		elif peekType(0) in ( TokType.Semicolon, TokType.Comment ):
			# print( 'discarding', peek(0) )
			discard()
		else:
			# print( 'invalid', peek(0) )
			discard()

	return processedTokens


@dataclass
class Context:
	typ: str  # 'dict', 'class', 'list'
	klass: Optional[ Type ]


EMPTY = Context( 'dict', None )


def _toObject( parsedTokens: List[Token ], classes: List[Type ], ctx: Context = EMPTY ) -> Union[ Dict[ Any, Any ], List[Any ] ]:
	# 1: dict 2: list 3: class
	result = [] if ctx.typ == 'list' else {}
	klasses: Dict[str, Type] = { klass.__name__: klass for klass in classes }
	i = 0

	def peek( offset=1 ) -> Token:
		return parsedTokens[ i + offset ] if len(parsedTokens) > i + offset else parsedTokens[-1]

	def consume() -> Token:
		nonlocal i
		i += 1
		return parsedTokens[ i - 1 ]

	def peekType( offset=1 ) -> TokType:
		return peek(offset).typ

	def peekIsType( offset, typ: TokType ) -> bool:
		return peekType(offset) == typ

	def discard() -> None:
		consume()

	while len(parsedTokens) > i:
		# print( peek(0), peek() )
		# key-value
		if peekIsType( 0, TokType.Key ) and peekIsType( 1, TokType.Value ):
			key = consume()
			value = consume().value
			# print(key, value)
			if ctx.typ == 'class':
				typ = ctx.klass.__annotations__[key.value]
				value = typ( value )
			result[key.value] = value
		# value
		elif peekIsType(0, TokType.Value) and ctx.typ == 'list':
			result.append( consume().value )
			# print( result[-1] )
		# list|dict|class
		elif ( peekIsType(0, TokType.Key) or peekIsType(0, TokType.Class) ) and peekIsType( 1, TokType.Newline ):
			key = consume()
			# discard() # newline
			level = peek().value
			startIndex = endIndex = i

			# get object end index
			while True:
				if endIndex >= len(parsedTokens):
					endIndex -= 1
					break
				elif parsedTokens[endIndex].typ == TokType.Padding and parsedTokens[endIndex].value < level:
					break
				elif parsedTokens[endIndex].typ == TokType.Newline and parsedTokens[endIndex + 1].typ != TokType.Padding:
					break
				elif parsedTokens[endIndex].typ == TokType.EOF:
					break
				endIndex += 1

			# print( parsedTokens[startIndex:endIndex] )
			# create object
			obj: Union[object, list, dict]
			if key.typ == TokType.Class:
				# print( key )
				toObj = _toObject(
						parsedTokens[ startIndex : endIndex ] + [ eof( parsedTokens[ endIndex ] ) ],
						classes,
						Context( 'class', klasses[ key.value ] )
					)
				obj = klasses[key.value](
					**toObj
				)
			elif peekIsType( 2, TokType.Key ):
				obj = _toObject(
					parsedTokens[ startIndex : endIndex ] + [ eof( parsedTokens[ endIndex ] ) ],
					classes
				)
			else:
				obj = _toObject(
					parsedTokens[ startIndex: endIndex ] + [ eof( parsedTokens[ endIndex ] ) ],
					classes,
					Context( 'list', None )
				)
			# add obj to result
			if ctx.typ == 'list':
				result.append( obj )
			else:
				result[key.value] = obj
			# finalize
			i = endIndex
		elif peekIsType(0, TokType.EOF):
			break
		else:
			# print( 'unknown token:', peek(0) )
			discard()
	return result


Types = List[Type]


def loads( data: str, file: str, classes: Types = [] ) -> dict:
	return _toObject( _parseTokens( _tokenizeString( data, file ) ), classes )


def load( fp: Union[ PathLike, str ], classes: Types = [] ) -> dict:
	return loads( Path(fp).read_text(), str( fp ), classes )


def dumps( obj: object ) -> str:
	def dumpl( obj: object ) -> List[str]:
		parts: List[str] = []
		if hasattr( obj, '__toe__' ) and isinstance( getattr( obj, '__toe__', None ), Callable ):
			return obj.__toe__().split('\n')

		if obj.__class__ == list:
			obj: list
			for value in obj:
				p = dumpl( value )
				if len( p ) == 2 and p[1] is None:
					parts += [ f'\t{p[ 0 ]}' ]
				else:
					if value.__class__ not in (int, str, float, complex, list, dict, None.__class__):
						parts.append( f'.{value.__class__.__name__}:' )
					parts += [ '\t' + line for line in p ]

		elif obj.__class__ == dict:
			obj: dict
			for key, value in obj.items():
				p = dumpl( value )
				if len(p) == 2 and p[1] is None:
					parts.append(f'{key}: {p[0]}')
				else:
					parts.append( f'{key}:' )
					parts += [ '\t' + line for line in p ]

		elif obj.__class__ in (int, str, float, complex):
			parts += [ str( obj ), None ]
		elif obj.__class__ in (bool, None.__class__):
			parts += [ str(obj).lower(), None ]
		else:
			for attr in dir( obj ):
				# ignore privates, dunders and functions
				if attr.startswith('_') or isinstance( getattr( obj, attr ), Callable ):
					continue
				attribute = getattr( obj, attr )
				if attribute.__class__ == str:
					parts.append(f'{attr}: {attribute}')
				elif attribute.__class__ in (int, float, complex, bool, None.__class__):
					parts.append(f'{attr}: { str(attribute).lower() }')
				else:
					parts.append(f'{attr}:')
					parts += [ '\t' + line for line in dumpl(attribute) ]

		return parts

	return '\n'.join( dumpl( obj ) )


def dump( fp: Union[PathLike, str], obj: object ) -> None:
	Path(fp).write_text( dumps(obj) )

