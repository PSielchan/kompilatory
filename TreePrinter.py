import AST

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
        print("|  " * indent + self.value)

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print("|  " * indent + self.value)

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print("|  " * indent + self.value)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print("|  " * indent + self.name)

    @addToClass(AST.Constant)
    def printTree(self, indent=0):
        print("|  " * indent + self.name)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print("|  " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.RelExpr)
    def printTree(self, indent=0):
        print("|  " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Comparason)
    def printTree(self, indent=0):
        print("|  " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Assign)
    def printTree(self, indent=0):
        print("|  " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.WhileLoop)
    def printTree(self, indent=0):
        print("|  " * indent + "WHILE")
        self.con.printTree(indent + 1)
        self.inst.printTree(indent + 1)

    @addToClass(AST.ForLoop)
    def printTree(self, indent=0):
        print("|  " * indent + "FOR")
        self.itr.printTree(indent + 1)
        self.range.printTree(indent + 1)
        self.inst.printTree(indent + 1)

    @addToClass(AST.IfStatement)
    def printTree(self, indent=0):
        print("|  " * indent + "IF")
        self.con.printTree(indent + 1)
        self.expr.printTree(indent + 1)

    @addToClass(AST.IfElseStatement)
    def printTree(self, indent=0):
        print("|  " * indent + "IF")
        self.con.printTree(indent + 1)
        print("|  " * indent + "THEN")
        self.expr1.printTree(indent + 1)
        print("|  " * indent + "ELSE")
        self.expr2.printTree(indent + 1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        print("|  " * indent + "PRINT")
        for expr in self.list:
            expr.printTree(indent + 1)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        print("|  " * indent + "RETURN")
        for expr in self.list:
            expr.printTree(indent + 1)

    @addToClass(AST.List)
    def printTree(self, indent=0):
        print("|  " * indent + "VECTOR")
        for expr in self.list:
            expr.printTree(indent+1)

    @addToClass(AST.MatrixFunc)
    def printTree(self, indent=0):
        print("|  " * indent + self.func)
        self.matrix.printTree(indent + 1)

    @addToClass(AST.Transpose)
    def printTree(self, indent=0):
        print("|  " * indent + "TRANSPOSE")
        self.num.printTree(indent + 1)

    @addToClass(AST.UnMinus)
    def printTree(self, indent=0):
        print("|  " * indent + "-")
        self.num.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        print("|  " * indent + "RANGE")
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)

    @addToClass(AST.Reference)
    def printTree(self, indent=0):
        print("|  " * indent + "REF")
        self.expr.printTree(indent + 1)
        self.x.printTree(indent + 1)
        self.y.printTree(indent + 1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        print("|  " * indent + "BREAK")

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        print("|  " * indent + "CONTINUE")


    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass
        # fill in the body


    # define printTree for other classes
    # ...

