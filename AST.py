
class Node(object):
    def __init__(self,lineno):
        self.lineno = lineno
    pass

class Block(Node):
    def __init__(self, instructions,lineno):
        super().__init__(lineno)
        self.instructions = instructions

class Instruction(Node):
    def __init__(self, instruction,lineno):
        super().__init__(lineno)
        self.instruction = instruction

class IntNum(Node):
    def __init__(self, value,lineno):
        super().__init__(lineno)
        self.value = value

class FloatNum(Node):
    def __init__(self, value,lineno):
        super().__init__(lineno)
        self.value = value

class String(Node):
    def __init__(self, value,lineno):
        super().__init__(lineno)
        self.value = value

class Variable(Node):
    def __init__(self, name,lineno):
        super().__init__(lineno)
        self.name = name

class Constant(Node):
    def __init__(self, name,lineno):
        super().__init__(lineno)
        self.name = name

class BinExpr(Node):
    def __init__(self, op, left, right,lineno):
        super().__init__(lineno)
        self.op = op
        self.left = left
        self.right = right

class RelExpr(Node):
    def __init__(self, op, left, right,lineno):
        super().__init__(lineno)
        self.op = op
        self.left = left
        self.right = right

class Assign(Node):
    def __init__(self, op, left, right,lineno):
        super().__init__(lineno)
        self.op = op
        self.left = left
        self.right = right

class Comparason(Node):
    def __init__(self, op, left, right,lineno):
        super().__init__(lineno)
        self.op = op
        self.left = left
        self.right = right

class WhileLoop(Node):
    def __init__(self, con, inst,lineno):
        super().__init__(lineno)
        self.con =  con
        self.inst = inst

class ForLoop(Node):
    def __init__(self,itr, range, inst,lineno):
        super().__init__(lineno)
        self.itr = itr
        self.range = range
        self.inst = inst

class  IfStatement(Node):
    def __init__(self, con, expr,lineno):
        super().__init__(lineno)
        self.con =  con
        self.expr = expr

class  IfElseStatement(Node):
    def __init__(self, con, expr1, expr2,lineno):
        super().__init__(lineno)
        self.con =  con
        self.expr1 = expr1
        self.expr2 = expr2


class Range(Node):
    def __init__(self,start,end,lineno):
        super().__init__(lineno)
        self.start = start
        self.end = end

class Reference(Node):
    def __init__(self,expr,x, y,lineno):
        super().__init__(lineno)
        self.expr = expr
        self.x = x
        self.y = y

class Print(Node):
    def __init__(self,list,lineno):
        super().__init__(lineno)
        self.list = list

class Return(Node):
    def __init__(self,list,lineno):
        super().__init__(lineno)
        self.list = list

class Break(Node):
    def __init__(self,lineno):
        super().__init__(lineno)

class Continue(Node):
    def __init__(self,lineno):
        super().__init__(lineno)

class List(Node):
    def __init__(self,list,lineno):
        super().__init__(lineno)
        self.list = list

class MatrixFunc(Node):
    def __init__(self,func,matrix,lineno):
        super().__init__(lineno)
        self.func = func
        self.matrix = matrix

class Transpose(Node):
    def __init__(self,num,lineno):
        super().__init__(lineno)
        self.num = num

class UnMinus(Node):
    def __init__(self,num,lineno):
        super().__init__(lineno)
        self.num = num



# ...
# fill out missing classes
# ...

class Error(Node):
    def __init__(self,lineno):
        super().__init__(lineno)
        pass
