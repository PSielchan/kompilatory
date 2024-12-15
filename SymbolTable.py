#!/usr/bin/python

class Symbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type

class VariableSymbol(Symbol):
    def __init__(self, name, type):
        self.name = name
        self.type = type

class SymbolTable:
    def __init__(self, parent=None, name=""):
        self.parent = parent
        self.name = name
        self.symbols = {}
        self.nesting = 0

    def put(self, name, symbol):
        self.symbols[name] = symbol

    def get(self, name):
        symbol = self.symbols.get(name)
        if symbol is not None:
            return symbol
        if self.parent is not None:
            return self.parent.get(name)
        return None

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        return SymbolTable(parent=self, name=name)

    def popScope(self):
        return self.parent
    
    def pushNesting(self):
        self.nesting += 1

    def popNesting(self):
        self.nesting -= 1
    




