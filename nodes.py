from tokens import *

class Node:

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self):
        pass

class BinOp(Node):

    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,st):
        child_L = self.children[0].evaluate(st)
        child_R = self.children[1].evaluate(st)
        op = self.value

        if type(child_L[0]) == int and type(child_R[0]) == int:
            if op == "+":
                result = int(child_L[0] + child_R[0])
            elif op == "-":
                result = int(child_L[0] - child_R[0])
            elif op == "*":
                result = int(child_L[0] * child_R[0])
            elif op == "/":
                result = int(child_L[0] / child_R[0])
            elif op == ">":
                result = int(child_L[0] > child_R[0])
            elif op == "<":
                result = int(child_L[0] < child_R[0])
            elif op == ".":
                result = int(str(child_L[0]) + str(child_R[0]))
            elif op == "==":
                result = int(child_L[0] == child_R[0])
            elif op == "&&":
                result = int(child_L[0] and child_R[0])
            elif op == "||":
                result = int(child_L[0] or child_R[0])
            return (result, "i32")
        elif type(child_L[0]) == str and type(child_R[0]) == str or type(child_L[0]) == str and type(child_R[0]) == int or type(child_L[0]) == int and type(child_R[0]) == str:
            if op == "+":
                result = str(child_L[0]) + str(child_R[0])
                tipo = "String"
            elif op == ".":
                result = str(child_L[0]) + str(child_R[0])
                tipo = "String"
            elif op == "==":
                result = (int(str(child_L[0]) == str(child_R[0])))
                tipo = "i32"
            elif op == ">":
                result = int(str(child_L[0]) > str(child_R[0]))
                tipo = "i32"
            elif op == "<":
                result = int(str(child_L[0]) < str(child_R[0]))
                tipo = "i32"
            return (result, tipo)
        else:
            raise Exception("Operacão entre tipos inválidos")

class UnOp(Node):

    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,st):
        child = self.children[0].evaluate(st)
        op = self.value

        if op == "+":
            result = int(child[0])
        elif op == "!":
            result = int(not child[0])
        else:
            result = int(-child[0])

        return (result, "i32")

class IntVal(Node):

    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,st):
        value = int(self.value)

        return (value,"i32")

class StrVal(Node):

    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,st):
        value = self.value

        return (value, "String")

class NoOp(Node):

    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,st):
        pass

class Print(Node):

    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,st):
        value = self.value
        print(value.evaluate(st)[0])

class Identifier(Node):

    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,st):
        value = self.value

        return (st.getter(value)[0],st.getter(value)[1])

class Assignment(Node):

    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,st):
        child_L = self.children[0]
        child_R = self.children[1].evaluate(st)
        st.setter(child_L,child_R)

class VarDec(Node):

    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,st):
        vars = self.children[0]
        type = self.children[1]

        for var in vars:
            st.creator(var,type)

class Read(Node):

    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,st):
        value = input()
        if value.isnumeric():
            return [int(value),"i32"]
        else:
            raise Exception("Input must be an integer")
            #return [value,"String"]

class If(Node):

    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,st):
        child_L = self.children[0]
        child_M = self.children[1]

        if child_L.evaluate(st)[0]:
            child_M.evaluate(st)

        elif len(self.children) > 2:
            child_R = self.children[2]
            child_R.evaluate(st)

class While(Node):

    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,st):
        child_L = self.children[0]
        child_R = self.children[1]

        while(child_L.evaluate(st)[0]==True):
            child_R.evaluate(st)

class Return(Node):

    def __init__(self, value, children):
        super().__init__(value, children)
        
    def evaluate(self,st):
        result = self.value

        return result.evaluate(st)

class Block(Node):

    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,st):
        for child in self.children:
            if type(child) == Return:
                return child.evaluate(st)
            child.evaluate(st)

class RelExpression(Node):

    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,st):
        for child in self.children:
            child.evaluate(st)

class FuncDec(Node):

    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,st):
        vardec = self.value
        statements = self.children
        
        FuncTable.create(vardec[0], statements, vardec[1])
class FuncCall(Node):

    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,st):
        funcName = self.value
        parametros = self.children
        statements, tipo = FuncTable.getter(funcName)
        func_st = SimbolTable()
        if parametros != []:
            for i in range(1,len(statements)-1):
                statements[i].evaluate(func_st)
                func_st.setter(statements[i].children[0], parametros[i-1].evaluate(st))
        nodeBlock = statements[-1].evaluate(func_st)
        return nodeBlock