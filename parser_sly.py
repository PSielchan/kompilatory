from sly import Parser
from scanner_sly import Scanner
from AST import *


class Mparser(Parser):
    tokens = Scanner.tokens

    debugfile = 'parser.out'

    precedence = (
        ("nonassoc", IFX),
        ("nonassoc", ELSE),
        ("nonassoc", ':'),
        ("nonassoc", LESEQ, GRTEQ, EQ, NEQ, ">", "<"),
        ("left", '+', '-', DOTADD, DOTSUB),
        ("left", '*', DOTMUL, '/', DOTDIV),
        ("right", UMINUS),
        ("right", '\''),
    )

    @_('instructions')
    def program(self, p):
        return Block(p[0],0)

    @_('')
    def instructions(self, p):
        return []

    @_('instruction instructions')
    def instructions(self, p):
        return [p[0]] + p[1]

    @_('"{" instructions "}"')
    def instruction(self, p):
        return Block(p[1],p.lineno)

    @_('assignment ";"')
    def instruction(self, p):
        return Instruction(p[0], p.lineno)

    @_('conditional')
    def instruction(self, p):
        return Instruction(p[0], p.lineno)

    @_('loop')
    def instruction(self, p):
        return Instruction(p[0], p.lineno)

    @_('PRINT list ";"')
    def instruction(self, p):
        return Print(p[1], p.lineno)

    @_('BREAK ";"')
    def instruction(self, p):
        return Break(p.lineno)

    @_('CONTINUE ";"')
    def instruction(self, p):
        return Continue(p.lineno)

    @_('RETURN list ";"')
    def instruction(self, p):
        return Return(p[1], p.lineno)

    # @_('"{" instructions "}"')
    # def instructions(self, p):
    #     return p[1]

    # @_('"{" instructions "}"')
    # def block(self, p):
    #     return Block(p.instructions, p.lineno)
    #
    # @_('instruction')
    # def block(self, p):
    #     return Block([p.instruction], p.lineno)

    @_('"-" expression %prec UMINUS')
    def expression(self, p):
        return UnMinus(p[1], p.lineno)

    @_('expression "\'"')
    def expression(self, p):
        return Transpose(p[0], p.lineno)

    @_('INTNUM')
    def expression(self, p):
        return IntNum(p[0], p.lineno)

    @_('FLOATNUM')
    def expression(self, p):
        return FloatNum(p[0], p.lineno)

    @_('STRING')
    def expression(self, p):
        return String(p[0], p.lineno)

    @_('ID')
    def variable(self, p):
        return Variable(p[0], p.lineno)

    @_('reference')
    def variable(self, p):
        return p[0]

    @_('variable')
    def expression(self, p):
        return p[0]

    @_('variable "=" expression',
       'variable ADDASSIGN expression',
       'variable SUBASSIGN expression',
       'variable MULASSIGN expression',
       'variable DIVASSIGN expression',
       )
    def assignment(self, p):
        return Assign(p[1], p[0], p[2], p.lineno)

    # @_('reference "=" expression',
    #    'reference ADDASSIGN expression',
    #    'reference SUBASSIGN expression',
    #    'reference MULASSIGN expression',
    #    'reference DIVASSIGN expression',
    #    )
    # def assignment(self, p):
    #     return Assign(p[1],p[0],p[2],p.lineno)

    @_('expression DOTADD expression',
       'expression DOTSUB expression',
       'expression DOTMUL expression',
       'expression DOTDIV expression')
    def expression(self, p):
        return RelExpr(p[1], p[0], p[2], p.lineno)

    @_('expression "+" expression',
       'expression "-" expression',
       'expression "*" expression',
       'expression "/" expression', )
    def expression(self, p):
        return BinExpr(p[1], p[0], p[2], p.lineno)

    @_('expression "[" expression "," expression "]"')
    def reference(self, p):
        return Reference(p[0], p[2], p[4], p.lineno)

    @_('matrix_function')
    def expression(self, p):
        return p[0]

    @_('"(" expression ")"')
    def expression(self, p):
        return p[1]

    @_('"[" list "]"')
    def expression(self, p):
        return List(p[1], p.lineno)

    @_('expression "," list')
    def list(self, p):
        return [p[0]] + p[2]

    @_('expression')
    def list(self, p):
        return [p[0]]

    @_('expression "<" expression',
       'expression ">" expression',
       'expression LESEQ expression',
       'expression GRTEQ expression',
       'expression EQ expression',
       'expression NEQ expression')
    def expression(self, p):
        return Comparason(p[1], p[0], p[2], p.lineno)

    @_('ZEROS "(" list ")"',
       'ONES "(" list ")"',
       'EYE "(" list ")"')
    def matrix_function(self, p):
        return MatrixFunc(p[0], p[2], p.lineno)

    @_('IF "(" expression ")"  instruction ELSE instruction')
    def conditional(self, p):
        return IfElseStatement(p[2], p[4], p[6], p.lineno)

    @_('IF "(" expression ")" instruction %prec IFX')
    def conditional(self, p):
        return IfStatement(p[2], p[4], p.lineno)

    @_('WHILE "(" expression ")" instruction')
    def loop(self, p):
        return WhileLoop(p[2], p[4], p.lineno)

    @_('FOR variable "=" range instruction')
    def loop(self, p):
        return ForLoop(p[1], p[3], p[4], p.lineno)

    @_('expression ":" expression')
    def range(self, p):
        return Range(p[0], p[2], p.lineno)

    def error(self, p):
        if p:
            print(f"Syntax error at line {p.lineno}: unexpected token '{p.value}'")
        else:
            print("Syntax error: unexpected end of input")