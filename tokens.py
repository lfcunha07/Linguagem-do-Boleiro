myAlpha = ["+","-","/","*","(",")","{","}","=",";","<",">","&&","==","||",".",",",":","->"]

class SimbolTable():
    def __init__(self):
        self.alphabet = dict()

    def getter(self, key):
        return (self.alphabet[key])

    def setter(self, key, num):
        value = num[0]
        tipo = (self.alphabet[key])[1]
        if tipo == "i32" and type(value) == int:
            self.alphabet[key] = [value, tipo]
        elif tipo == "String" and type(value) == str:
            self.alphabet[key] = [value, tipo]
        else:
            raise Exception("Type Err")

    def creator(self, key, tipo):
        if key in self.alphabet:
            raise KeyError("Variável já existe")
        default_str = ""
        default_int = 0
        if tipo == "i32":
            self.alphabet[key] = [default_int, tipo]
        elif tipo == "String":
            self.alphabet[key] = [default_str, tipo]

class FuncTable:
    functions = dict()

    @staticmethod
    def create(funct, value, tipo): 
        if funct in FuncTable.functions:
            raise Exception("Invalid casting or more than one declaration of a function")
        else:
            FuncTable.functions[funct] = [value, tipo]

    @staticmethod
    def getter(chave):
        return (FuncTable.functions[chave][0],FuncTable.functions[chave][1])

class Token:

    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:

    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None

    def selectNext(self):

        # Pega o primeiro caracter
        if self.position < len(self.source):
            number = self.source[self.position]
        # Ignora espaço
        while self.position < len(self.source) and self.source[self.position] == " ":
            self.position += 1
            number = self.source[self.position]
            
        # Checa EOF
        if self.position == len(self.source):
            self.next = Token("EOF", None)
            return

        # Checa If
        elif self.source[self.position] == "r" and self.source[self.position+1] == "e" and self.source[self.position+2] == "s" and self.source[self.position+3] == "e" and self.source[self.position+4] == "n" and self.source[self.position+5] == "h" and self.source[self.position+6] == "a":
            self.next = Token("IF", None)
            self.position += 7

        # Checa ->
        elif self.source[self.position] == "-" and self.source[self.position+1] == ">":
            self.next = Token("->", None)
            self.position += 2

        # Checa Else
        elif self.source[self.position] == "r" and self.source[self.position+1] == "a" and self.source[self.position+2] == "m" and self.source[self.position+3] == "e" and self.source[self.position+4] == "l" and self.source[self.position+5] == "o" and self.source[self.position+6] == "u":
            self.next = Token("ELSE", None)
            self.position += 7

        # Checa Var
        elif self.source[self.position] == "j" and self.source[self.position+1] == "o" and self.source[self.position+2] == "g" and self.source[self.position+3] == "a" and self.source[self.position+4] == "d" and self.source[self.position+5] == "o" and self.source[self.position+6] == "r":
            self.next = Token("VAR", None)
            self.position += 7

        # Checa I32
        elif self.source[self.position] == "i" and self.source[self.position+1] == "3" and self.source[self.position+2] == "2":
            self.next = Token("I32", None)
            self.position += 3
            
        # Checa Func
        elif self.source[self.position] == "r" and self.source[self.position+1] == "e" and self.source[self.position+2] == "g" and self.source[self.position+3] == "u" and self.source[self.position+4] == "l" and self.source[self.position+5] == "a" and self.source[self.position+6] == "m" and self.source[self.position+7] == "e" and self.source[self.position+8] == "n" and self.source[self.position+9] == "t" and self.source[self.position+10] == "o":
            self.next = Token("FN", None)
            self.position += 11

        # Checa String
        elif self.source[self.position] == "n" and self.source[self.position+1] == "o" and self.source[self.position+2] == "m" and self.source[self.position+3] == "e":
            self.next = Token("STRING", None)
            self.position += 4

        # Checa Print
        elif self.source[self.position] == "e" and self.source[self.position+1] == "x" and self.source[self.position+2] == "p" and self.source[self.position+3] == "l" and self.source[self.position+4] == "a" and self.source[self.position+5] == "n" and self.source[self.position+6] == "a":
            self.next = Token("PRINT", None)
            self.position += 7

        # Checa While
        elif self.source[self.position] == "e" and self.source[self.position+1] == "n" and self.source[self.position+2] == "q" and self.source[self.position+3] == "u" and self.source[self.position+4] == "a" and self.source[self.position+5] == "n" and self.source[self.position+6] == "t" and self.source[self.position+7] == "o":
            self.next = Token("WHILE", None)
            self.position += 8

        # Checa Return
        elif self.source[self.position] == "r" and self.source[self.position+1] == "e" and self.source[self.position+2] == "c" and self.source[self.position+3] == "u" and self.source[self.position+4] == "a":
            self.next = Token("RET", None)
            self.position += 5

        # Checa Read
        elif self.source[self.position] == "f" and self.source[self.position+1] == "a" and self.source[self.position+2] == "z" and self.source[self.position+3] == "_" and self.source[self.position+4] == "t" and self.source[self.position+5] == "e" and self.source[self.position+6] == "u" and self.source[self.position+7] == "_" and self.source[self.position+8] == "n" and self.source[self.position+9] == "o" and self.source[self.position+10] == "m" and self.source[self.position+11] == "e":
            self.next = Token("READ", None)
            self.position += 12

        # Checa operações boleanas
        elif self.source[self.position] == "&":
            self.position += 1
            if self.source[self.position] == "&":
                self.next = Token("AND", None)
                self.position += 1
            else:
                self.position -= 2
        elif self.source[self.position] == "|":
            self.position += 1
            if self.source[self.position] == "|":
                self.next = Token("OR", None)
                self.position += 1
            else:
                self.position -= 2
        elif self.source[self.position] == "=":
            self.position += 1
            if self.source[self.position] == "=":
                self.next = Token("SAME", None)
                self.position += 1
            else:
                self.next = Token("EQUAL", None)
        elif self.source[self.position] == ">":
            self.next = Token("MORE", None)
            self.position += 1
        elif self.source[self.position] == "<":
            self.next = Token("LESS", None)
            self.position += 1

        # Checa concatenação
        elif self.source[self.position] == ".":
            self.next = Token("CONCAT", None)
            self.position += 1

        # Checa operações
        elif self.source[self.position] == "!":
            self.next = Token("NOT", None)
            self.position += 1
        elif self.source[self.position] == "+":
            self.next = Token("PLUS", None)
            self.position += 1
        elif self.source[self.position] == "-":
            self.next = Token("MINUS", None)
            self.position += 1
        elif self.source[self.position] == "*":
            self.next = Token("MULT", None)
            self.position += 1
        elif self.source[self.position] == "/":
            self.next = Token("DIV", None)
            self.position += 1

        # Checa parenteses
        elif self.source[self.position] == "(":
            self.next = Token("LS", None)
            self.position += 1
        elif self.source[self.position] == ")":
            self.next = Token("RS", None)
            self.position += 1

        # Checa Block
        elif self.source[self.position] == "{":
            self.next = Token("LC", None)
            self.position += 1
        elif self.source[self.position] == "}":
            self.next = Token("RC", None)
            self.position += 1
        elif self.source[self.position] == ";":
            self.next = Token("SC", None)
            self.position += 1
        elif self.source[self.position] == ":":
            self.next = Token("COLON", None)
            self.position += 1
        elif self.source[self.position] == ",":
            self.next = Token("COMMA", None)
            self.position += 1

        # Se for numero, loopa ate chegar ao fim da sequencia numerica
        elif number.isdigit() == True:
            value = ''
            # Concatena os números até enquanto for dígito
            while number.isdigit() and self.position < len(self.source):
                self.position += 1
                value += number
                if self.position < len(self.source):
                    number = self.source[self.position]
            self.next = Token("INT", int(value))        

        # Se for aspas, loopa ate chegar ao fim da sequencia alfabetica
        elif self.source[self.position] == '"':
            value = ''
            self.position += 1
            number = self.source[self.position]
            # Concatena os números até enquanto for dígito
            while number != '"' and self.position < len(self.source):
                self.position += 1
                value += number
                if self.position < len(self.source):
                    number = self.source[self.position]
            self.position += 1
            self.next = Token("NAME", value)

        # Se for letra, loopa ate chegar ao fim da sequencia alfabetica
        elif number.isalpha() == True:
            value = ''
            # Concatena as letras até enquanto for caracter
            while number not in myAlpha and self.position < len(self.source):
                self.position += 1
                value += number
                if self.position < len(self.source):
                    number = self.source[self.position]
            self.next = Token("ID", value)
        else:
            raise Exception("Formato Inválido")