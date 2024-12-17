import AST

def prints(text,indent):
    print("|  " * indent + text)

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Block)
    def printTree(self, indent=0):
        for inst in self.instructions:
            inst.printTree(indent)

    @addToClass(AST.Instruction)
    def printTree(self, indent=0):
        self.instruction.printTree(indent)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        prints(self.value,indent)

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        prints(self.value, indent)

    @addToClass(AST.String)
    def printTree(self, indent=0):
        prints(self.value, indent)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        prints(self.name, indent)

    @addToClass(AST.Constant)
    def printTree(self, indent=0):
        prints(self.name, indent)
    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        prints(self.op, indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.RelExpr)
    def printTree(self, indent=0):
        prints(self.op, indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Comparason)
    def printTree(self, indent=0):
        prints(self.op, indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Assign)
    def printTree(self, indent=0):
        prints(self.op, indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.WhileLoop)
    def printTree(self, indent=0):
        prints("WHILE", indent)
        self.con.printTree(indent + 1)
        self.inst.printTree(indent + 1)

    @addToClass(AST.ForLoop)
    def printTree(self, indent=0):
        prints("FOR", indent)
        self.itr.printTree(indent + 1)
        self.range.printTree(indent + 1)
        self.inst.printTree(indent + 1)

    @addToClass(AST.IfStatement)
    def printTree(self, indent=0):
        prints("IF", indent)
        self.con.printTree(indent + 1)
        self.expr.printTree(indent + 1)

    @addToClass(AST.IfElseStatement)
    def printTree(self, indent=0):
        prints("IF", indent)
        self.con.printTree(indent + 1)
        prints("THEN", indent)
        self.expr1.printTree(indent + 1)
        prints("ELSE", indent)
        self.expr2.printTree(indent + 1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        prints("PRINT", indent)
        for expr in self.list:
            expr.printTree(indent + 1)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        prints("RETURN", indent)
        for expr in self.list:
            expr.printTree(indent + 1)

    @addToClass(AST.List)
    def printTree(self, indent=0):
        prints("VECTOR", indent)
        for expr in self.list:
            expr.printTree(indent+1)

    @addToClass(AST.MatrixFunc)
    def printTree(self, indent=0):
        prints(self.func, indent)
        for expr in self.matrix:
            expr.printTree(indent + 1)
        # self.matrix.printTree(indent + 1)

    @addToClass(AST.Transpose)
    def printTree(self, indent=0):
        prints("TRANSPOSE", indent)
        self.num.printTree(indent + 1)

    @addToClass(AST.UnMinus)
    def printTree(self, indent=0):
        prints("-", indent)
        self.num.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        prints("RANGE", indent)
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)

    @addToClass(AST.Reference)
    def printTree(self, indent=0):
        prints("REF", indent)
        self.expr.printTree(indent + 1)
        self.x.printTree(indent + 1)
        self.y.printTree(indent + 1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        prints("BREAK", indent)

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        prints("CONTINUE", indent)


    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass
        # fill in the body


    # define printTree for other classes
    # ...

