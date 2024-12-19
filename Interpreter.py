import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import uuid
import sys

import random
import string

sys.setrecursionlimit(10000)


def mem_name(name,length=3):
    characters = string.ascii_letters + string.digits
    return name + ''.join(random.choice(characters) for _ in range(length))

class Interpreter(object):

    def __init__(self):
        self.global_mem = Memory("global")
        self.mem_stack = MemoryStack(self.global_mem)

    def print_memory(self):
        print("=========")
        for memory in self.mem_stack.stack:
            print("----" + memory.name)
            for v in memory.space.keys():
                if v is not None:
                    print(v +": " + str(memory.space[v]))
        print("=========")

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Block)
    def visit(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    @when(AST.Instruction)
    def visit(self, node):
        self.visit(node.instruction)

    @when(AST.IntNum)
    def visit(self, node):
        return int(node.value)

    @when(AST.FloatNum)
    def visit(self, node):
        return float(node.value)

    @when(AST.String)
    def visit(self, node):
        return node.value

    @when(AST.Variable)
    def visit(self, node, name = False):
        r = self.mem_stack.get(node.name)
        if r is None:
            self.mem_stack.insert(node.name, None)

        if name:
            return node.name
        else:
            return r

    @when(AST.BinExpr)
    def visit(self, node):

        r1 = self.visit(node.left)
        r2 = self.visit(node.right)

        ops = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b}
        return ops[node.op](r1,r2)

    @when(AST.RelExpr)
    def visit(self, node):
        r1 = self.visit(node.left)
        r2 = self.visit(node.right)
        ops = {
            ".+": lambda a, b: a + b,
            ".-": lambda a, b: a - b,
            ".*": lambda a, b: a * b,
            "./": lambda a, b: a / b}
        new_matrix = []
        y = 0

        for i in range(len(r1)):
            new_matrix.append([])
            for j in range(len(r1[0])):
                new_matrix[y].append(ops[node.op](r1[i][j],r2[i][j]))
            y+=1

        return new_matrix


    @when(AST.Assign)
    def visit(self, node):
        variable = self.visit(node.left, name = True)
        update_val = self.visit(node.right)
        ops = {
            "+=": lambda a, b: a + b,
            "-=": lambda a, b: a - b,
            "*=": lambda a, b: a * b,
            "/=": lambda a, b: a / b,
            "=" : lambda a, b: b}


        if(isinstance(node.left,AST.Reference)):
            id, (x,y) = variable
            matrix = self.mem_stack.get(id)
            matrix[x][y] = update_val
            self.mem_stack.set(id,matrix)
        else:
            current_val = self.mem_stack.get(variable)
            new_val = ops[node.op](current_val,update_val)
            self.mem_stack.set(node.left.name,new_val)

    @when(AST.Comparason)
    def visit(self, node):
        r1 = self.visit(node.left)
        r2 = self.visit(node.right)
        ops = {
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
            "<=": lambda a, b: a <= b,
            ">=": lambda a, b: a >= b,
            "<": lambda a, b: a < b,
            ">": lambda a, b: a> b}
        return ops[node.op](r1,r2)

    @when(AST.WhileLoop)
    def visit(self, node):
        space_name = mem_name('while')
        memory = Memory(space_name)
        self.mem_stack.push(memory)

        while self.visit(node.con):
            try:
                self.visit(node.inst)
            except BreakException:
                break
            except ReturnValueException:
                break
            except ContinueException:
                continue

        self.mem_stack.pop()

    @when(AST.ForLoop)
    def visit(self, node):
        memory = Memory(mem_name('for'))
        self.mem_stack.push(memory)

        start, end = self.visit(node.range)
        self.visit(node.itr)
        itr_name = self.visit(node.itr,name = True)
        for i in range(start,end):
            self.mem_stack.set(itr_name, i)
            try:
                self.visit(node.inst)
            except BreakException:
                break
            except ReturnValueException:
                break
            except ContinueException:
                continue
        self.mem_stack.pop()

    @when(AST.IfStatement)
    def visit(self, node):
        if self.visit(node.con):
            self.visit(node.expr)

    @when(AST.IfElseStatement)
    def visit(self, node):
        if self.visit(node.con):
            self.visit(node.expr1)
        else:
            self.visit(node.expr2)

    @when(AST.Range)
    def visit(self, node):
        return (self.visit(node.start), self.visit(node.end))

    @when(AST.Reference)
    def visit(self, node, name = False):
        if name:
            return self.visit(node.expr, name=True), (self.visit(node.x), self.visit(node.y))
        else:
            return self.visit(node.expr)[self.visit(node.x)][self.visit(node.y)]


    @when(AST.Print)
    def visit(self, node):
        for expr in node.list:
            print(self.visit(expr),end=", ")
        print()

    @when(AST.Return)
    def visit(self, node):
        val = self.visit(node.list)
        print("RETURNED VALUE : ", val)
        raise ReturnValueException(val)

    @when(AST.Break)
    def visit(self, node):
        raise BreakException()

    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException()

    @when(AST.List)
    def visit(self, node):
        return [self.visit(element) for element in node.list]

    @when(AST.MatrixFunc)
    def visit(self, node):
        size = [0,0]
        size[0] = size[1] = self.visit(node.matrix[0])
        if len(node.matrix) >1:
            size[1] = self.visit(node.matrix[1])
        ops = {
            "zeros": lambda m: [[0 for _ in range(size[1])] for _ in range(size[0])],
            "ones": lambda m: [[1 for _ in range(size[1])] for _ in range(size[0])],
            "eye": lambda m: [[1 if i == j else 0 for j in range(size[1])] for i in range(size[0])],
        }
        return ops[node.func](list)

    @when(AST.Transpose)
    def visit(self, node):
        matrix = self.visit(node.num)
        return [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]

    @when(AST.UnMinus)
    def visit(self, node):
        value = self.visit(node.num)
        if isinstance(value, List):
            return [[-v for v in row] for row in value]
        return -value




