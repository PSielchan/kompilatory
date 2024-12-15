import sys
from sly import Lexer


class Scanner(Lexer):
    reserved = { 'BREAK','CONTINUE' ,'IF' ,'ELSE' ,'FOR',
    'WHILE','RETURN','ZEROS','ONES','EYE','PRINT'}
    literals={'+','-','*','/',';',':','(',')','[',']','{','}','\'',';','=','<','>',','}
    tokens = [
        "ID", "INTNUM", "FLOATNUM", "STRING",
        "DOTADD", "DOTSUB", "DOTMUL", "DOTDIV",
        "ADDASSIGN", "SUBASSIGN", "MULASSIGN", "DIVASSIGN",
        "LESEQ", "GRTEQ", "NEQ", "EQ"
    ] + list(reserved)
    
    ignore = ' \t'
    ignore_comment = r'\#.*'

    DOTADD = r'\.\+'
    DOTSUB = r'\.-'
    DOTMUL = r'\.\*'
    DOTDIV = r'\./'

    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'/='

    LESEQ = r'<='
    GRTEQ = r'>='
    NEQ = r'!='
    EQ = r'=='

    FLOATNUM = r'(\d+\.\d*|\.\d+)([Ee][+-]?\d+)?'
    INTNUM = r'\d+'

    STRING = r'\".*?\"'

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['break'] = 'BREAK'
    ID['continue'] = 'CONTINUE'
    ID['if'] = 'IF'
    ID['else'] = 'ELSE'
    ID['for'] = 'FOR'
    ID['while'] = 'WHILE'
    ID['return'] = 'RETURN'
    ID['zeros'] = 'ZEROS'
    ID['ones'] = 'ONES'
    ID['eye'] = 'EYE'
    ID['print'] = 'PRINT'

    @_(r'\n+')
    def newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print(f'Błąd leksykalny w linii {self.lineno}: Nieznany znak "{t.value[0]}"')

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()
    
    for tok in lexer.tokenize(text):
        print(f"({tok.lineno}): {tok.type}({tok.value})")

  