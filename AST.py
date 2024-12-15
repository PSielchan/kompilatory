
class Node(object):
    pass


class Block(Node):
    def __init__(self, instructions):
        self.instructions = instructions

class Instruction(Node):
    def __init__(self, instruction):
        self.instruction = instruction

class IntNum(Node):
    def __init__(self, value):
        self.value = value

class FloatNum(Node):
    def __init__(self, value):
        self.value = value

class String(Node):
    def __init__(self, value):
        self.value = value

class Variable(Node):
    def __init__(self, name):
        self.name = name

class Constant(Node):
    def __init__(self, name):
        self.name = name

class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class RelExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class Assign(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class Comparason(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class WhileLoop(Node):
    def __init__(self, con, inst):
        self.con =  con
        self.inst = inst

class ForLoop(Node):
    def __init__(self,itr, range, inst):
        self.itr = itr
        self.range = range
        self.inst = inst

class  IfStatement(Node):
    def __init__(self, con, expr):
        self.con =  con
        self.expr = expr

class  IfElseStatement(Node):
    def __init__(self, con, expr1, expr2):
        self.con =  con
        self.expr1 = expr1
        self.expr2 = expr2


class Range(Node):
    def __init__(self,start,end):
        self.start = start
        self.end = end

class Reference(Node):
    def __init__(self,expr,x, y):
        self.expr = expr
        self.x = x
        self.y = y

class Print(Node):
    def __init__(self,list):
        self.list = list

class Return(Node):
    def __init__(self,list):
        self.list = list

class Break(Node):
    def __init__(self):
        pass

class Continue(Node):
    def __init__(self):
        pass

class List(Node):
    def __init__(self,list):
        self.list = list

class MatrixFunc(Node):
    def __init__(self,func,matrix):
        self.func = func
        self.matrix = matrix

class Transpose(Node):
    def __init__(self,num):
        self.num = num

class UnMinus(Node):
    def __init__(self,num):
        self.num = num



# ...
# fill out missing classes
# ...

class Error(Node):
    def __init__(self):
        pass
