from nodes import *
from tokens import *

class ExpressionParser:
    tokenizer = None

    @staticmethod
    def parseFactor():

        # Operações
        if ExpressionParser.tokenizer.next.type == "INT":       # Checa para numero
            value = IntVal(ExpressionParser.tokenizer.next.value, None)
            ExpressionParser.tokenizer.selectNext()
            return value
        elif ExpressionParser.tokenizer.next.type == "NAME":       # Checa para numero
            value = StrVal(ExpressionParser.tokenizer.next.value, None)
            ExpressionParser.tokenizer.selectNext()
            return value
        elif ExpressionParser.tokenizer.next.type == "PLUS":    # Checa para PLUS
            ExpressionParser.tokenizer.selectNext()
            value = UnOp("+", [ExpressionParser.parseFactor()])
            return value
        elif ExpressionParser.tokenizer.next.type == "MINUS":   # Checa para MINUS
            ExpressionParser.tokenizer.selectNext()
            value = UnOp("-", [ExpressionParser.parseFactor()])
            return value     
        elif ExpressionParser.tokenizer.next.type == "NOT":    # Checa para NOT
            ExpressionParser.tokenizer.selectNext()
            value = UnOp("!", [ExpressionParser.parseFactor()])
            return value   
        elif ExpressionParser.tokenizer.next.type == "ID":   # Checa para ID
            funcName = ExpressionParser.tokenizer.next.value
            ExpressionParser.tokenizer.selectNext()
            if ExpressionParser.tokenizer.next.type == "LS": 
                ExpressionParser.tokenizer.selectNext()
                value = []
                while ExpressionParser.tokenizer.next.type != "RS":
                    value.append(ExpressionParser.parseRelExpression())
                    if ExpressionParser.tokenizer.next.type == "COMMA":
                        ExpressionParser.tokenizer.selectNext()
                ExpressionParser.tokenizer.selectNext()
                return FuncCall(funcName, value)
            else:
                value = Identifier(funcName, "[]")
            return value
        elif ExpressionParser.tokenizer.next.type == "READ":   # Checa para READ
            value = Read(None, None)
            ExpressionParser.tokenizer.selectNext()
            if ExpressionParser.tokenizer.next.type == "LS":    # Checa para LS
                ExpressionParser.tokenizer.selectNext()
                if ExpressionParser.tokenizer.next.type == "RS":    # Checa para RS
                    ExpressionParser.tokenizer.selectNext()
                    return value
                else:
                    raise Exception("Formato invalido")
            else:
                raise Exception("Formato invalido")
        elif ExpressionParser.tokenizer.next.type == "LS":      # Checa para LS
            ExpressionParser.tokenizer.selectNext()
            value = ExpressionParser.parseRelExpression()
            if ExpressionParser.tokenizer.next.type == "RS":    # Checa para RS
                ExpressionParser.tokenizer.selectNext()
                return value
            else:
                raise Exception("Formato invalido")

    @staticmethod
    def parseTerm():

        # Inicializa metodo com o valor
        value = ExpressionParser.parseFactor()

        # Lida com operacoes
        while ExpressionParser.tokenizer.next.type == "MULT" or ExpressionParser.tokenizer.next.type == "DIV" or ExpressionParser.tokenizer.next.type == "AND":
            if ExpressionParser.tokenizer.next.type == "MULT":
                ExpressionParser.tokenizer.selectNext()
                value = BinOp("*", [value, ExpressionParser.parseFactor()])
            elif ExpressionParser.tokenizer.next.type == "DIV":
                ExpressionParser.tokenizer.selectNext()
                value = BinOp("/", [value, ExpressionParser.parseFactor()])
            elif ExpressionParser.tokenizer.next.type == "AND":
                ExpressionParser.tokenizer.selectNext()
                value = BinOp("&&", [value, ExpressionParser.parseFactor()])
        return value

    @staticmethod
    def parseExpression():

        # Inicializando metodo
        value = ExpressionParser.parseTerm()

        # Loop principal, apenas soma e divide
        while ExpressionParser.tokenizer.next.type == "PLUS" or ExpressionParser.tokenizer.next.type == "MINUS" or ExpressionParser.tokenizer.next.type == "OR":
            if ExpressionParser.tokenizer.next.type == "PLUS":
                ExpressionParser.tokenizer.selectNext()
                value = BinOp("+", [value, ExpressionParser.parseTerm()])
            elif ExpressionParser.tokenizer.next.type == "MINUS":
                ExpressionParser.tokenizer.selectNext()
                value = BinOp("-", [value, ExpressionParser.parseTerm()])
            elif ExpressionParser.tokenizer.next.type == "OR":
                ExpressionParser.tokenizer.selectNext()
                value = BinOp("||", [value, ExpressionParser.parseTerm()])
        return value

    @staticmethod
    def parseRelExpression():

        # Inicializa metodo com o valor
        value = ExpressionParser.parseExpression()

        # Lida com operacoes
        while ExpressionParser.tokenizer.next.type == "SAME" or ExpressionParser.tokenizer.next.type == "LESS" or ExpressionParser.tokenizer.next.type == "MORE" or ExpressionParser.tokenizer.next.type == "CONCAT":
            if ExpressionParser.tokenizer.next.type == "SAME":
                ExpressionParser.tokenizer.selectNext()
                value = BinOp("==", [value, ExpressionParser.parseExpression()])
            elif ExpressionParser.tokenizer.next.type == "LESS":
                ExpressionParser.tokenizer.selectNext()
                value = BinOp("<", [value, ExpressionParser.parseExpression()])
            elif ExpressionParser.tokenizer.next.type == "MORE":
                ExpressionParser.tokenizer.selectNext()
                value = BinOp(">", [value, ExpressionParser.parseExpression()])
            elif ExpressionParser.tokenizer.next.type == "CONCAT":
                ExpressionParser.tokenizer.selectNext()
                value = BinOp(".", [value, ExpressionParser.parseExpression()])
        return value

    @staticmethod
    def parseStatement():

        node = NoOp(None, [])

        # Checa para SEMICOLON
        if ExpressionParser.tokenizer.next.type == "SC":
            ExpressionParser.tokenizer.selectNext()
            return node
            
        # Checa para RETURN
        elif(ExpressionParser.tokenizer.next.type == "RET"):
            ExpressionParser.tokenizer.selectNext()
            return Return(ExpressionParser.parseRelExpression(), None)

        # Checa para IDENTIFIER
        elif ExpressionParser.tokenizer.next.type == "ID":
            var = ExpressionParser.tokenizer.next.value
            ExpressionParser.tokenizer.selectNext()

            if ExpressionParser.tokenizer.next.type == "EQUAL":
                ExpressionParser.tokenizer.selectNext()
                op = ExpressionParser.parseRelExpression()
                node = Assignment(None, [var,op])

            elif ExpressionParser.tokenizer.next.type == "LS" :
                parametros= []
                ExpressionParser.tokenizer.selectNext()

                while ExpressionParser.tokenizer.next.type != "RS":
                    parametros.append(ExpressionParser.parseRelExpression())
                    if ExpressionParser.tokenizer.next.type == "COMMA":
                        ExpressionParser.tokenizer.selectNext()
                    else:
                        raise Exception("Parâmetros para função inválidos")

                ExpressionParser.tokenizer.selectNext()
                node = FuncCall(var, parametros)
            else:
                raise Exception("Formato Inválido para Identifier")

        # Checa para PRINT
        elif ExpressionParser.tokenizer.next.type == "PRINT":
            ExpressionParser.tokenizer.selectNext()
            if ExpressionParser.tokenizer.next.type == "LS":
                ExpressionParser.tokenizer.selectNext()
                value = ExpressionParser.parseRelExpression()
                if ExpressionParser.tokenizer.next.type == "RS":    # Checa para RS
                    ExpressionParser.tokenizer.selectNext()
                    node = Print(value,None)
                else:
                    raise Exception("Formato invalido")
            else:
                raise Exception("Formato Inválido para Print")

        # Checa para VAR
        elif ExpressionParser.tokenizer.next.type == "VAR":
            ExpressionParser.tokenizer.selectNext()   
            # Checa todos as variáveis 
            vars = []
            while ExpressionParser.tokenizer.next.type == "ID":   # Checa para ID
                value = ExpressionParser.tokenizer.next.value
                vars.append(value)
                ExpressionParser.tokenizer.selectNext()
                if ExpressionParser.tokenizer.next.type == "COMMA":
                    ExpressionParser.tokenizer.selectNext()
                elif ExpressionParser.tokenizer.next.type == "COLON":
                    ExpressionParser.tokenizer.selectNext()
                else:
                    raise Exception("Formato inválido em VAR")
            # Da um tipo
            if ExpressionParser.tokenizer.next.type == "STRING":
                node = VarDec(None, [vars,"String"])
                ExpressionParser.tokenizer.selectNext()
            elif ExpressionParser.tokenizer.next.type == "I32":
                node = VarDec(None, [vars,"i32"])
                ExpressionParser.tokenizer.selectNext()
            else:
                raise Exception("Formato inválido em VAR")

        # Checa para WHILE
        elif ExpressionParser.tokenizer.next.type == "WHILE":
            ExpressionParser.tokenizer.selectNext()
            if ExpressionParser.tokenizer.next.type == "LS":
                ExpressionParser.tokenizer.selectNext()
                value = ExpressionParser.parseRelExpression()
                if ExpressionParser.tokenizer.next.type == "RS":    # Checa para RS
                    ExpressionParser.tokenizer.selectNext()
                    var = ExpressionParser.parseStatement()
                    return While(None, [value,var])
                else:
                    raise Exception("Formato nválido em WHILE")
            else:
                raise Exception("Formato Inválido para While")

        # Checa para IF
        elif ExpressionParser.tokenizer.next.type == "IF":
            ExpressionParser.tokenizer.selectNext()
            if ExpressionParser.tokenizer.next.type == "LS":
                ExpressionParser.tokenizer.selectNext()
                value = ExpressionParser.parseRelExpression()
                if ExpressionParser.tokenizer.next.type == "RS":    # Checa para RS
                    ExpressionParser.tokenizer.selectNext()
                    child_1 = ExpressionParser.parseStatement()
                    if ExpressionParser.tokenizer.next.type == "ELSE":
                        ExpressionParser.tokenizer.selectNext()
                        return If(1, [value, child_1, ExpressionParser.parseStatement()])
                    else:
                        return If(0, [value, child_1])
                else:
                    raise Exception("Formato invalido")
            else:
                raise Exception("Formato Inválido para If")

        # Checa para BLOCK
        else:
            return ExpressionParser.parseBlock()
        
        # Checa para fim de comando
        if ExpressionParser.tokenizer.next.type == "SC":
            ExpressionParser.tokenizer.selectNext()
            return node
        else:
            raise Exception("Formato Inválido para Comando")
        
    @staticmethod
    def parseBlock():

        children = []
        ast = Block(None, children)
        # Checando se o primeiro token é "{"
        if ExpressionParser.tokenizer.next.type == "LC":
            ExpressionParser.tokenizer.selectNext()
            while ExpressionParser.tokenizer.next.type != "RC":
                node = ExpressionParser.parseStatement()
                children.append(node)
            ExpressionParser.tokenizer.selectNext()
            return ast
        else:     
            raise Exception("Formato Inválido")

    @staticmethod
    def parseDeclaration():
        
        children = []
        # Encontra método no código
        if(ExpressionParser.tokenizer.next.type == "FN"):
            ExpressionParser.tokenizer.selectNext()

            # Pega o nome do método
            if(ExpressionParser.tokenizer.next.type == "ID"):
                funcName = ExpressionParser.tokenizer.next.value
                children.append(Identifier(funcName, "[]"))
                ExpressionParser.tokenizer.selectNext()

                # Pega os parâmetros do método
                if(ExpressionParser.tokenizer.next.type == "LS"):
                    ExpressionParser.tokenizer.selectNext()

                    while (ExpressionParser.tokenizer.next.type != "RS"):
                        vars = []
                        if ExpressionParser.tokenizer.next.type == "ID":
                            value = ExpressionParser.tokenizer.next.value
                            vars.append(value)
                            ExpressionParser.tokenizer.selectNext()
                            if ExpressionParser.tokenizer.next.type == "COMMA":
                                ExpressionParser.tokenizer.selectNext()
                            elif ExpressionParser.tokenizer.next.type == "COLON":
                                ExpressionParser.tokenizer.selectNext()
                                if ExpressionParser.tokenizer.next.type == "I32":
                                    for v in vars:
                                        node = VarDec(None, [v,"i32"]) 
                                        children.append(node)
                                        ExpressionParser.tokenizer.selectNext()
                                        if ExpressionParser.tokenizer.next.type == "COMMA":
                                            ExpressionParser.tokenizer.selectNext()
                                elif ExpressionParser.tokenizer.next.type == "STRING":
                                    for v in vars:
                                        node = VarDec(None, [v,"string"]) 
                                        children.append(node)
                                        ExpressionParser.tokenizer.selectNext()
                                        if ExpressionParser.tokenizer.next.type == "COMMA":
                                            ExpressionParser.tokenizer.selectNext()
                            else:
                                raise Exception("Formato inválido em VAR")
                        else:
                            raise Exception("Declaração de parâmetros de função inválido")

                    ExpressionParser.tokenizer.selectNext()

                    # Pega tipo do método
                    funcType = ""
                    if ExpressionParser.tokenizer.next.type == "->":
                        ExpressionParser.tokenizer.selectNext()
                        if ExpressionParser.tokenizer.next.type == "I32":
                            funcType = "i32"
                            ExpressionParser.tokenizer.selectNext()
                        elif ExpressionParser.tokenizer.next.type == "String":
                            funcType = "String"
                            ExpressionParser.tokenizer.selectNext()
                    children.append(ExpressionParser.parseBlock())

                    function = FuncDec([funcName, funcType], children)
                    return function
            else:
                raise Exception("Falta identificador de função")
        else:
            raise Exception("Código não atrelado a função")
    
    @staticmethod
    def parseProgram(): 

        children = []
        while ExpressionParser.tokenizer.next.type != "EOF":     
            children.append(ExpressionParser.parseDeclaration())

        return Block("Block", children)

    @staticmethod
    def run(file):

        # Rodando programa
        code = PrePro.cleanup(file)
        code = code.replace('\n', '')
        code = code.replace(' ', '')

        ExpressionParser.tokenizer = Tokenizer(code)
        ExpressionParser.tokenizer.selectNext()
        value = ExpressionParser.parseProgram()
        value.children.append(FuncCall("Main",[]))

        if ExpressionParser.tokenizer.next.type != "EOF" or type(value) == None:
            raise Exception("Erro de Semântica")
        else:
            return value

class PrePro:

    @staticmethod
    def cleanup(code):
        comment=""
        new_code = ""
        div = False
        isComment=False
        for i in code:
            new_code += i
            # Iteração de comentário
            if isComment:
                comment+=i
                if i == "\n":
                    new_code = new_code.replace(comment,"")
                    isComment = False
                    comment=""
            # Iteração de código fonte
            if i == "/":
                if div == True:
                    comment += new_code[-2:]
                    isComment=True
                    div = False
                else:
                    div = True
            else:
                div = False
        return new_code