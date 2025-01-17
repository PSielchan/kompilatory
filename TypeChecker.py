#!/usr/bin/python

from SymbolTable import SymbolTable, VariableSymbol
import AST

class TypeError(Exception):
    pass


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            #print(node.__class__.__name__)
            children = node.instructions if hasattr(node, 'instructions') else []
            for child in children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #     for child in node.children:
    #         self.visit(child)

class TypeChecker(NodeVisitor):

    def __init__(self):
        self.symbol_table = SymbolTable(None, 'program')
        self.error_flag = False

    def visit_Block(self, node):
        self.visit(node.instructions)

    def visit_Instruction(self,node):
        self.visit(node.instruction)

    def visit_Assign(self, node):
        type1 = self.visit(node.right)
        op = node.op
        if op == '=':
            this=self.visit(node.left)
            if this=='gref':
                rettype=self.visit(node.left.expr)
                return rettype[int(node.left.x.value)][int(node.left.y.value)]
            if this=='bref':
                return
            #print(node.left.name,"=",end=" ")
            #print(type1)
            self.symbol_table.put(node.left.name, VariableSymbol(node.left.name, type1))
        elif op in ['+=', '-=', '*=', '/=']:
            type2 = self.visit(node.left)
            if type1 != type2:
                print(f"Type error at line {node.lineno}: Incompatible types in assignment")
                self.error_flag = True
                return
        return type1

    def visit_Comparason(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op
        if type1 != type2:
            print(f"Type error at line {node.lineno}:Incompatible types in comparison: {type1} and {type2}")
            self.error_flag = True
        return 'bool'

    def visit_RelExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op

        # Check if the operands are matrices or scalars
        is_matrix1 = isinstance(type1, list)
        is_matrix2 = isinstance(type2, list)

        if is_matrix1 and is_matrix2:
            # Both are matrices
            if len(type1) != len(type2) or any(len(row1) != len(row2) for row1, row2 in zip(type1, type2)):
                print(f"Type error at line {node.lineno}: Matrix dimensions do not match for operation")
                self.error_flag = True
            elif op in ['.+', '.-', '.*', './']:
                f = False
                for row in type1:
                    for val in row:
                        if val!='int' and val!='float':
                            print(f"Type error at line {node.lineno}: Non-numeric values found in matrix 1")
                            self.error_flag = True
                            f = True
                            break
                    if f:
                        break
                f = False
                for row in type2:
                    for val in row:
                        if val != 'int' and val != 'float':
                            print(f"Type error at line {node.lineno}: Non-numeric values found in matrix 2")
                            self.error_flag = True
                            f = True
                            break
                    if f:
                        break
        else:
            if op in ['+', '-']:
                if not isinstance(type1 if not is_matrix1 else type2, (int, float)):
                    print(f"Type error at line {node.lineno}: Matrix +- scalar operation")
                    self.error_flag = True

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op
        if ((isinstance(type1, list) and (type2 == "int" or type2 == "float")) ):
            return type1
        if ((type1 == "int" or type1 == "float") and isinstance(type2, list)):
            return type2
        if ((type1 == "string" and type2 == "int") or (type1 == "int" and type2 == "string")) and op == "*":
            return "string"
        elif (type1 == "int" and type2 == "float") or (type1 == "float" and type2 == "int"):
            return "float"
        if type1 != type2:
            print(f"Type error at line {node.lineno}: Incompatible types in relational expression: {type1} and {type2}")
            self.error_flag = True
        return type1

    def visit_WhileLoop(self, node):
        self.symbol_table.pushNesting()
        self.symbol_table.pushScope('while')
        self.visit(node.con)
        self.visit(node.inst)
        self.symbol_table.popScope()
        self.symbol_table.popNesting()

    def visit_ForLoop(self, node):
        self.symbol_table.pushNesting()
        self.symbol_table.pushScope('for')
        self.visit(node.range)
        self.symbol_table.put(node.itr.name, VariableSymbol(node.itr.name, 'int'))
        self.visit(node.inst)
        self.symbol_table.popScope()
        self.symbol_table.popNesting()

    def visit_IfStatement(self, node):
        self.symbol_table.pushScope('if')
        self.visit(node.con)
        self.visit(node.expr)
        self.symbol_table.popScope()

    def visit_IfElseStatement(self, node):
        self.symbol_table.pushScope('if')
        self.visit(node.con)
        self.visit(node.expr1)
        self.symbol_table.popScope()
        self.symbol_table.pushScope('else')
        self.visit(node.expr2)
        self.symbol_table.popScope()

    def visit_Range(self, node):
        start_type = self.visit(node.start)
        end_type = self.visit(node.end)
        #print(start_type)
        #print(end_type)
        if start_type != end_type:
            print(f"Type error at line {node.lineno}: Start and end types in range are incompatible")
            self.error_flag = True
        return start_type

    def visit_Print(self, node):
        for argument in node.list:
            self.visit(argument)

    def visit_Return(self, node):
        for value in node.list:
            self.visit(value)

    def visit_Break(self, node):
        if self.symbol_table.nesting == 0:
            print(f"Type error at line {node.lineno}: Break outside of loop")
            self.error_flag = True

    def visit_Continue(self, node):
        if self.symbol_table.nesting == 0:
            print(f"Type error at line {node.lineno}: Continue outside of loop")
            self.error_flag = True

    def visit_Reference(self, node):
        type1=self.visit(node.x)
        type2=self.visit(node.x)
        if type1 != 'int' or type2 != 'int':
            print(f"Type error at line {node.lineno}: bad reference")
            self.error_flag = True
            return 'bref'
        else:
            #print("siema")
            #print(node.expr)
            type3=self.visit(node.expr)
            if not isinstance(type3,list):
                print(f"Type error at line {node.lineno}: matrix do not exist")
                self.error_flag = True
                return 'bref'
            elif int(node.x.value)>len(type3) or int(node.y.value)>len(type3[0]):
                print(f"Type error at line {node.lineno}: matrix index out of range")
                self.error_flag = True
                return 'bref'
        return 'gref'

    def visit_Transpose(self, node):
        type1 = self.visit(node.num)
        if type!='int' and type!='string' and type!='float':
            return [[type1[j][i] for i in range(len(type1))] for j in range(len(type1[0]))]
        else:
            print(f"Type error at line {node.lineno}: Cannot transpose something that is not a matrix or vector")
            self.error_flag = True

    def visit_UnMinus(self, node):
        type1 = self.visit(node.num)
        if type1 != 'string':
            return type1
        else:
            print(f"Type error at line {node.lineno}: Bad type for unary minus!")
            self.error_flag = True

    def visit_List(self, node):
        elements = [self.visit(item) for item in node.list]
        
        if all(isinstance(el, list) for el in elements):
            row_lengths = {len(row) for row in elements}
            if len(row_lengths) > 1:
                print(f"Type error at line {node.lineno}: Matrix rows have inconsistent lengths")
                self.error_flag = True
                return None
            element_types = {type(item) for row in elements for item in row}
            if len(element_types) > 1:
                print(f"Type error at line {node.lineno}: Matrix elements have inconsistent types")
                self.error_flag = True
                return None
            return elements  # Return the validated matrix structure
        elif all(not isinstance(el, list) for el in elements):
            # Flat list: Ensure all elements have the same type
            element_types = {type(item) for item in elements}
            if len(element_types) > 1:
                print(f"Type error at line {node.lineno}: List elements have inconsistent types")
                self.error_flag = True
                return None
            return elements  # Return the validated flat list
        else:
            print(f"Type error at line {node.lineno}: Mixed matrix and scalar elements")
            self.error_flag = True
            return None


    def visit_MatrixFunc(self, node):
        if len(node.matrix)>2:
            print(f"Type error at line {node.lineno}: Bad number of arguments for matirx function")
            self.error_flag = True
            return None
        if len(node.matrix) == 2 and node.func == 'eye':
            print(f"Type error at line {node.lineno}: Bad number of arguments for EYE function")
            self.error_flag = True
            return None
        type = self.visit(node.matrix[0])
        if type != 'int':
            print(f"Type error at line {node.lineno}: Bad type of parameter for matrix function")
            self.error_flag = True
            return None
        dl=int(node.matrix[0].value)
        return [['int' for _ in range(dl)] for _ in range(dl)]
        

    def visit_IntNum(self, node):
        return 'int'

    def visit_FloatNum(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Variable(self, node):
        symbol = self.symbol_table.get(node.name)
        return symbol.type if symbol else None

    def visit_Constant(self, node):
        return self.visit(node.name)

    def visit_Error(self, node):
        print(f"Error at line {node.lineno}: Error in AST structure.")
        return None