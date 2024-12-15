from sly import Parser
from scanner_sly import Scanner
from AST import *

class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = 'parser.out'

    precedence = (
        ("nonassoc",IFX),
        ("nonassoc",ELSE),
        ("nonassoc", LESEQ, GRTEQ, EQ, NEQ, ">", "<"),
        ("left", '+', '-', DOTADD, DOTSUB),
        ("left", '*', DOTMUL, '/', DOTDIV),
        ("nonassoc", ':'),
        ("right", UMINUS),
        ("right", '\''),
    )

    @_('instructions_opt')
    def program(self,p):
        return Block(p[0])

    @_('instructions')
    def instructions_opt(self,p):
        return p[0]

    @_('')
    def instructions_opt(self,p):
        return []

    @_('instructions instruction')
    def instructions(self,p):
        return p.instructions + [p.instruction]

    @_('instruction')
    def instructions(self,p):
        return [p.instruction]

    @_('assignment ";"')
    def instruction(self,p):
        return Instruction(p[0])

    @_('conditional')
    def instruction(self,p):
        return Instruction(p[0])

    @_('loop')
    def instruction(self,p):
        return Instruction(p[0])

    @_('PRINT list ";"')
    def instruction(self,p):
        return Print(p[1])

    @_('BREAK ";"')
    def instruction(self,p):
        return Break()

    @_('CONTINUE ";"')
    def instruction(self,p):
        return Continue()

    @_('RETURN list ";"')
    def instruction(self,p):
        return Return(p[1])

    @_('"{" instructions "}"')
    def instructions(self, p):
        return p[1]

    @_('"{" instructions "}"')
    def block(self, p):
        return Block(p.instructions)

    @_('instruction')
    def block(self, p):
        return Block([p.instruction])

    @_('"-" expression %prec UMINUS')
    def expression(self,p):
        return UnMinus(p[1])

    @_('expression "\'"')
    def expression(self,p):
        return Transpose(p[0])

    @_('INTNUM')
    def expression(self,p):
        return IntNum(p[0])

    @_('FLOATNUM')
    def expression(self,p):
        return FloatNum(p[0])

    @_('STRING')
    def expression(self,p):
        return String(p[0])

    @_('ID')
    def expression(self,p):
        return Variable(p[0])

    @_('expression "=" expression',
       'expression ADDASSIGN expression',
       'expression SUBASSIGN expression',
       'expression MULASSIGN expression',
       'expression DIVASSIGN expression',
       )
    def assignment(self, p):
        return Assign(p[1],p[0],p[2])

    @_('reference "=" expression',
       'reference ADDASSIGN expression',
       'reference SUBASSIGN expression',
       'reference MULASSIGN expression',
       'reference DIVASSIGN expression',
       )
    def assignment(self, p):
        return Assign(p[1],p[0],p[2])

    @_('expression DOTADD expression',
       'expression DOTSUB expression',
       'expression DOTMUL expression',
       'expression DOTDIV expression')
    def expression(self,p):
        return RelExpr(p[1],p[0],p[2])

    @_('expression "+" expression',
       'expression "-" expression',
       'expression "*" expression',
       'expression "/" expression',)
    def expression(self,p):
        return BinExpr(p[1],p[0],p[2])

    @_('expression "[" expression "," expression "]"')
    def reference(self, p):
        return Reference(p[0],p[2],p[4])

    @_('matrix_function')
    def expression(self,p):
        return p[0]

    @_('"(" expression ")"')
    def expression(self, p):
        return p[1]

    @_('"[" list "]"')
    def expression(self, p):
        return List(p[1])

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
        return Comparason(p[1],p[0],p[2])

    @_('ZEROS "(" expression ")"',
       'ONES "(" expression ")"',
       'EYE "(" expression ")"')
    def matrix_function(self,p):
        return MatrixFunc(p[0],p[2])


    @_('IF "(" expression ")"  block ELSE block')
    def conditional(self,p):
        return IfElseStatement(p[2],p[4],p[6])

    @_('IF "(" expression ")" block %prec IFX')
    def conditional(self,p):
        return IfStatement(p[2],p[4])

    @_('WHILE "(" expression ")" block')
    def loop(self,p):
        return WhileLoop(p[2],p[4])

    @_('FOR expression "=" range block')
    def loop(self,p):
        return ForLoop(p[1],p[3],p[4])

    @_('expression ":" expression')
    def range(self,p):
        return Range(p[0],p[2])
    
    def error(self, p):
        if p:
            print(f"Syntax error at line {p.lineno}: unexpected token '{p.value}'")
        else:
            print("Syntax error: unexpected end of input")