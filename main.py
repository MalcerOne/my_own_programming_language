import sys

# =====================================
# SymbolTable
# =====================================
class SymbolTable():
    def __init__(self):
        self.table = {}

    def setter(self, key, tuple_):    
        if key in self.table:
            if tuple_[1] == self.table[key][1]:
                self.table[key][0] = tuple_[0]
            else:
                raise Exception("[X] Type mismatch")
        else:
            raise Exception("[X] Variable not declared")

    def getter(self, key):
        return self.table[key]

    def create(self, key, type):
        if key in self.table:
            raise Exception("[X] Symbol already exists")
        else:
            self.table[key] = [None, type]

# =====================================
# FuncTable
# =====================================
class FuncTable:
    func_table = {}

    @staticmethod
    def getter(func_name):
        if func_name not in FuncTable.func_table:
            raise Exception(f"[X] Function {func_name} not found")
        return FuncTable.func_table[func_name][1]

    @staticmethod
    def create(func_type, func_name, reference):
        if func_name in FuncTable.func_table:
            raise Exception(f"[X] Function {func_name} already exists")
        else:
            FuncTable.func_table[func_name] = [func_type, reference]

# =====================================
# Nodes
# =====================================
class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        pass

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.left = children[0]
        self.right = children[1]

    def Evaluate(self, symbolTable):
        left_first = self.left.Evaluate(symbolTable)
        right_first = self.right.Evaluate(symbolTable)

        if left_first[1] == "i32" and right_first[1] == "i32":
            if self.value == "+":
                return (left_first[0] + right_first[0], "i32")
            elif self.value == "-":
                return (left_first[0] - right_first[0], "i32")
            elif self.value == "*":
                return (left_first[0] * right_first[0], "i32")
            elif self.value == "/":
                return (int(left_first[0] // right_first[0]), "i32")
            elif self.value == "==":
                return (int(left_first[0] ==  right_first[0]), "i32")
            elif self.value == "<":
                return (int(left_first[0] < right_first[0]), "i32")
            elif self.value == ">":
                return (int(left_first[0] > right_first[0]), "i32")
            elif self.value == "&&":
                return (left_first[0] and right_first[0], "i32")
            elif self.value == "||":            
                return (left_first[0] or right_first[0], "i32")
            elif self.value == ".":
                res = str(left_first[0]) + str(right_first[0])
                return (str(res), "String")
            else:
                raise Exception("[X] Invalid operation")

        elif left_first[1] == "String" and right_first[1] == "String":
            if self.value == ".":
                res = str(left_first[0]) + str(right_first[0])
                return (str(res), "String")
            elif self.value == "==":
                res = str(left_first[0]) == str(right_first[0])
                return (int(res), "i32")
            elif self.value == "<":
                res = str(left_first[0]) < str(right_first[0])
                return (int(res), "i32")
            elif self.value == ">":
                res = str(left_first[0]) > str(right_first[0])
                return (int(res), "i32")
            else:
                raise Exception("[X] Invalid operation")

        elif left_first[1] == "String" or right_first[1] == "String":
            if self.value == ".":
                res = str(left_first[0]) + str(right_first[0])
                return (str(res), "String")
            elif self.value == "==":
                return (int(left_first[0] == right_first[0]), "i32")
            else:
                raise Exception("[X] Invalid operation")
        
class IntVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbolTable):
        return (int(self.value), "i32")

class StrVal(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbolTable):
        return (str(self.value), "String")

class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbolTable):
        first = self.children[0].Evaluate(symbolTable)
        if first[1] == "i32":
            if self.value == "-":
                return (-first[0], "i32")
            elif self.value == "!":
                return (int(not first[0]), "i32")
            elif self.value == "+":
                return (first[0], "i32")
            return not self.children[0].Evaluate()

class NoOp(Node):
    def __init__(self):
        pass

    def Evaluate(self, symbolTable):
        pass

class Var(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbolTable):
        return (symbolTable.getter(self.value)[0], symbolTable.getter(self.value)[1])

class VarDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbolTable):
        for i in self.children:
            symbolTable.create(i.value, self.value)

class Assign(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbolTable):
        symbolTable.setter(self.children[0], self.children[1].Evaluate(symbolTable))

class Return(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbolTable):
        return self.children.Evaluate(symbolTable)

# ============= Palavras reservadas ==================
class ShowMeWhatYouGot(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbolTable):
        print(self.children[0].Evaluate(symbolTable)[0])

class Squanch(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbolTable):
        while(self.children[0].Evaluate(symbolTable)[0]):
            self.children[1].Evaluate(symbolTable)

class If(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbolTable):
        if self.children[0].Evaluate(symbolTable):
            self.children[1].Evaluate(symbolTable)
        elif len(self.children) == 3:
            self.children[2].Evaluate(symbolTable)

class Read(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbolTable):
        return (int(input()), "i32")
# ============= Palavras reservadas ==================

# ============= Funções ==============================
class FuncDec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbolTable):
        FuncTable.create(self.value, self.children[0], self)

class FuncCall(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbolTable):
        func = FuncTable.getter(self.value)
        lenFunc = len(func.children)
        localTable = SymbolTable()
        funcName = func.children[0]
        funcBlock = func.children[-1]
        funcParams = func.children[1:lenFunc-1]

        if funcName == "Main":
            return funcBlock.Evaluate(localTable)
        else:
            if (lenFunc - 2 == len(self.children)):
                for varDeclared, attrib in zip(funcParams, self.children):
                    localTable.create(varDeclared.children[0], varDeclared.value)
                    
                    if attrib.value in symbolTable.table:
                        value = attrib.value
                        type_ = symbolTable.getter(value)[1]

                        localTable.create(value, type_)
                        localTable.setter(value, symbolTable.getter(value))
                        localTable.setter(varDeclared.children[0], symbolTable.getter(value))

                    else:
                        localTable.setter(varDeclared.children[0], attrib.Evaluate(localTable))

                return funcBlock.Evaluate(localTable)
            else:
                raise Exception("[X] Invalid number of parameters")
# ============= Funções ==============================

# =============== Block ==============================
class Block(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, symbolTable):
        for child in self.children:
            res = child.Evaluate(symbolTable)
            
            if res != None:
                return res
# =============== Block ==============================

# =====================================
# Token classes
# =====================================
class Token:
    def __init__(self, type, value):
        self.type  = type # String
        self.value = value # int or None

class PrePro:
    @staticmethod
    def filter(code):
        a = "\n".join([i for i in code.splitlines() if not '//' in i]).replace("\n", "").replace(" ", "")
        return a

class Tokenizer:
    def __init__(self, source):
        self.source = PrePro.filter(source)
        self.position = 0
        self.next = ""
        self.operators = ["+", "-", "/", "*", "(", ")", "{", "}", "=", ";", "==", "rickier_than", "mortyer_than", "!", "||", "&&", "&", "|", ".", ",", ":", "->"]
        self.stdfuncs = ["show_me_what_you_got", "if", "else", "squanch", "Read", "meeseeks", "String", "i32", "fn", "return"]
        
        # Verify for blank spaces 
        if self.source == "":
            raise Exception("[X] You can not have no operation at all.")

        if " " in self.source:
            check = self.source.replace(" ", "")
            if "{" not in check and "}" not in check and ";" not in check:
                raise Exception("[X] You can not have blank spaces in the operation.")
            self.source = check

        if ")" in self.source and "(" not in self.source:
            raise Exception("[X] You can not have a closing parenthesis without an opening one.")
        
        self.select_next()

    def select_next(self):
        hp = ""
        hp2 = ""
        flag = False
        flagVar = False
        
        #print(self.source[self.position])

        if self.position == len(self.source):
            self.next = Token("EOF", None)

        else:
            if self.source[self.position] == '"' and (self.source[self.position + 1].isdigit() or self.source[self.position + 1].isalpha()):
                hp3 = ""
                self.position += 1
                while self.source[self.position] != '"':
                    if self.position == len(self.source):
                        raise Exception("[X] You can not have a string without closing it.")
                    hp3 += self.source[self.position]
                    self.position += 1
                self.position += 1
                self.next = Token("STRING", hp3)
                return self.next

            while (self.position < len(self.source)) and (self.source[self.position].isdigit()):
                hp += self.source[self.position]
                self.position += 1
                flag = True

            if flag:
                self.next = Token("INT", int(hp))

            if self.position < len(self.source) and (self.source[self.position].isalpha()):
                while self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == "_":
                    if hp2 == "rickier_than":
                        break
                    elif hp2 == "mortyer_than":
                        break
                    elif "mortyer_than" in hp2:
                        hp2 = hp2.split("mortyer_than")[0]
                        self.position -= 12
                        break
                    elif "rickier_than" in hp2:
                        hp2 = hp2.split("rickier_than")[0]
                        self.position -= 12
                        break
                    elif hp2 == "else":
                        break
                    elif hp2 == "show_me_what_you_got":
                        break
                    elif hp2 == "if":
                        break
                    elif hp2 == "squanch":
                        break
                    elif hp2 == "Read":
                        break
                    elif hp2 == "meeseeks":
                        break
                    elif hp2 == "String":
                        break
                    elif hp2 == "i32":
                        break
                    elif hp2 == "fn":
                        break
                    elif hp2 == "return":
                        break
                    hp2 += self.source[self.position]
                    self.position += 1
                    flagVar = True

            if flag:
                self.next = Token("INT", int(hp))

            elif flagVar:
                if hp2 in self.stdfuncs:
                    self.next = Token("STDFUNCT", hp2)
                elif hp2 in self.operators:
                    if hp2 == "rickier_than":
                        self.next = Token("RICKIERTHAN", "rickier_than")
                    elif hp2 == "mortyer_than":
                        self.next = Token("MORTYERTHAN", "mortyer_than")
                else:
                    self.next = Token("VAR", hp2)

            else:
                if self.source[self.position] in self.operators:
                    if self.source[self.position] == "=" and self.source[self.position + 1] != "=":
                        self.next = Token("ASSIGN", "=")

                    if self.source[self.position] == ";":
                        self.next = Token("SEMICOL", ";")
                    
                    if self.source[self.position] == ".":
                        self.next = Token("DOT", ".")

                    if self.source[self.position] == ",":
                        self.next = Token("COMMA", ",")

                    if self.source[self.position] == ":":
                        self.next = Token("COLON", ":")

                    if self.source[self.position] == "{":
                        self.next = Token("OPEN_BRACK", "{")

                    if self.source[self.position] == "}":
                        self.next = Token("CLOSE_BRACK", "}")

                    if self.source[self.position] == "(":
                        self.next = Token("OPEN_PAREN", "(")

                    if self.source[self.position] == ")":
                        self.next = Token("CLOSE_PAREN", ")")

                    if self.source[self.position] == "!":
                        self.next = Token("NOT", "!")

                    if self.source[self.position] == "-" and self.source[self.position + 1] == ">":
                        self.position += 1
                        self.next = Token("ARROW", "->")

                    if self.source[self.position] == "=" and self.source[self.position + 1] == "=":
                        self.position += 1
                        self.next = Token("EQUAL", "==")

                    if self.source[self.position] == "|" and self.source[self.position + 1] == "|":
                        self.position += 1
                        self.next = Token("OR", "||")

                    if self.source[self.position] == "&" and self.source[self.position + 1] == "&":
                        self.position += 1 
                        self.next = Token("AND", "&&")

                    if self.source[self.position] == "+":
                        self.next = Token("PLUS", "+")

                    if self.source[self.position] == "-":
                        self.next = Token("MINUS", "-")
                    
                    if self.source[self.position] == "*":
                        self.next = Token("MULT", "*")

                    if self.source[self.position] == "/":
                        self.next = Token("DIV", "/")

                    self.position += 1
                    
# =====================================
# Parser
# =====================================
class Parser():
    tokenizer = None

    @staticmethod
    def parse_program():
        list_childrens = []

        while Parser.tokenizer.next.type != "EOF":
            res = Parser.parse_declaration()
            list_childrens.append(res)

        blockNode = Block("Block", list_childrens)
        return blockNode

    @staticmethod
    def parse_declaration():
        if Parser.tokenizer.next.type == "STDFUNCT" and Parser.tokenizer.next.value == "fn":
            Parser.tokenizer.select_next()
            childrens = []

            if Parser.tokenizer.next.type == "VAR":
                funcName = Parser.tokenizer.next.value
                childrens.append(funcName)
                Parser.tokenizer.select_next()

                if Parser.tokenizer.next.type == "OPEN_PAREN":
                    Parser.tokenizer.select_next()
                    while Parser.tokenizer.next.type != "CLOSE_PAREN":
                        if Parser.tokenizer.next.type == "VAR":
                            vars = [Parser.tokenizer.next.value]
                            Parser.tokenizer.select_next()

                            while Parser.tokenizer.next.type == "COMMA":
                                Parser.tokenizer.select_next()
                                if Parser.tokenizer.next.type == "VAR":
                                    vars.append(Parser.tokenizer.next.value)
                                    Parser.tokenizer.select_next()

                            if Parser.tokenizer.next.type == "COLON":
                                Parser.tokenizer.select_next()
                                varType = Parser.tokenizer.next.value
                                childrens.append(VarDec(varType, vars))
                            else:
                                raise Exception("[X] You can not have an argument without type.")
                            
                            if Parser.tokenizer.next.value not in ["i32", "String"]:
                                raise Exception("[X] Unrecognized type of variable.")

                            Parser.tokenizer.select_next()

                        if Parser.tokenizer.next.type == "COMMA":
                            Parser.tokenizer.select_next()

                    Parser.tokenizer.select_next()

                    if Parser.tokenizer.next.type == "ARROW":
                        Parser.tokenizer.select_next()

                        if Parser.tokenizer.next.value not in ["i32", "String"]:
                            raise Exception("[X] Unrecognized type of function.")

                        typeOfFunc = Parser.tokenizer.next.value
                        Parser.tokenizer.select_next()
                        block1 = Parser.parse_block()
                        childrens.append(block1)
                        res = FuncDec(funcName, childrens)
                        res.type = typeOfFunc
                        return res

                    block2 = Parser.parse_block()
                    childrens.append(block2)
                    res = FuncDec(funcName, childrens)
                    return res
                else:
                    raise Exception("[X] You can not have a function without a open parenthesis.")

            else:
                raise Exception("[X] You can not have a function without a name.")
        
        else:
            raise Exception("[X] You can not have a program without a function.")
            

    @staticmethod
    def parse_block():
        list_childrens = [] 

        if Parser.tokenizer.next.type == "OPEN_BRACK":
            Parser.tokenizer.select_next()
            while Parser.tokenizer.next.type != "CLOSE_BRACK":
                res = Parser.parse_statement()
                list_childrens.append(res)

            if Parser.tokenizer.next.type == "CLOSE_BRACK":
                Parser.tokenizer.select_next()
                # print("Block: ", Parser.tokenizer.next.type)
                return Block("Block", list_childrens)
            else:
                raise Exception("[X] You can not have a block without a closing bracket.")

        else:
            raise Exception("[X] You can not have a block without a open bracket.")
        
    @staticmethod
    def parse_statement():
        if Parser.tokenizer.next.type == "VAR":
            var = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "ASSIGN":
                Parser.tokenizer.select_next()
                res = Parser.parse_real_expression()
                if Parser.tokenizer.next.type == "SEMICOL":
                    Parser.tokenizer.select_next()
                    return Assign("ASSIGN", [var, res])
                else:
                    raise Exception("[X] You can not have a statement without a semicolon.")

            else:
                raise Exception("[X] You can not have a variable without an assignment.")

        elif Parser.tokenizer.next.type == "STDFUNCT" and Parser.tokenizer.next.value == "show_me_what_you_got":
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "OPEN_PAREN":
                Parser.tokenizer.select_next()
                res = Parser.parse_real_expression()
                printNode = ShowMeWhatYouGot("show_me_what_you_got", [res])
                if Parser.tokenizer.next.type == "CLOSE_PAREN":
                    Parser.tokenizer.select_next()
                    if Parser.tokenizer.next.type == "SEMICOL":
                        Parser.tokenizer.select_next()
                        return printNode
                    else:
                        raise Exception("[X] You can not have a statement without a semicolon.")
                else:
                    raise Exception("[X] You can not have a function call without a closing parenthesis.")
            else:
                raise Exception("[X] You can not have a function call without an opening parenthesis.")

        elif Parser.tokenizer.next.type == "STDFUNCT" and Parser.tokenizer.next.value == "meeseeks":
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "VAR":
                var = [Var(Parser.tokenizer.next.value, [])]
                Parser.tokenizer.select_next()
                while Parser.tokenizer.next.type != "COLON":
                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.select_next()
                        if Parser.tokenizer.next.type == "VAR":
                            var.append(Var(Parser.tokenizer.next.value, []))
                            Parser.tokenizer.select_next()
                        else:
                            raise Exception("[X] You can not have a variable without a name.")
                if Parser.tokenizer.next.type == "COLON":
                    Parser.tokenizer.select_next()
                    if Parser.tokenizer.next.type == "STDFUNCT" and Parser.tokenizer.next.value == "i32" or Parser.tokenizer.next.value == "String":
                        type_ = Parser.tokenizer.next.value
                        Parser.tokenizer.select_next()
                        if Parser.tokenizer.next.type == "SEMICOL":
                            Parser.tokenizer.select_next()
                            return VarDec(type_, var)
                        else:
                            raise Exception("[X] You can not have a statement without a semicolon.")
                else:
                    raise Exception("[X] You can not have a variable without a colon to declare the type of it.")
            else:
                raise Exception("[X] You can not have a variable without a name.")

        elif Parser.tokenizer.next.type == "SEMICOL":
            Parser.tokenizer.select_next()
            return NoOp()

        elif Parser.tokenizer.next.type == "STDFUNCT" and Parser.tokenizer.next.value == "return":
            Parser.tokenizer.select_next()
            res = Parser.parse_real_expression()
            return Return("RETURN", res)

        elif Parser.tokenizer.next.type == "STDFUNCT" and Parser.tokenizer.next.value == "squanch":
            Parser.tokenizer.select_next() 
            if Parser.tokenizer.next.type == "OPEN_PAREN":
                Parser.tokenizer.select_next()
                res = Parser.parse_real_expression()

                if Parser.tokenizer.next.type == "CLOSE_PAREN":
                    Parser.tokenizer.select_next()
                    res_aux1 = Parser.parse_statement()
                    return Squanch("SQUANCH", [res, res_aux1])
                else:
                    raise Exception("[X] You can not have a function call without a closing parenthesis.")
            else:
                raise Exception("[X] You can not have a function call without an opening parenthesis.")

        elif Parser.tokenizer.next.type == "STDFUNCT" and Parser.tokenizer.next.value == "if":  
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "OPEN_PAREN":
                Parser.tokenizer.select_next()
                res = Parser.parse_real_expression()
                
                if Parser.tokenizer.next.type == "CLOSE_PAREN":
                    Parser.tokenizer.select_next()
                    res_aux1 = Parser.parse_statement()

                    if Parser.tokenizer.next.type == "STDFUNCT" and Parser.tokenizer.next.value == "else":
                        Parser.tokenizer.select_next()
                        res_aux2 = Parser.parse_statement()
                        
                        return If("IF", [res, res_aux1, res_aux2])

                    else:
                        return If("IF", [res, res_aux1])
                else:
                    raise Exception("[X] You can not have a function call without a closing parenthesis.")
            else:
                raise Exception("[X] You can not have a function call without an opening parenthesis.")
     
        else:
            res = Parser.parse_block()
            return res

    @staticmethod
    def parse_real_expression():
        res = Parser.parse_expression()
        while Parser.tokenizer.next.type == "EQUAL" or Parser.tokenizer.next.type == "RICKIERTHAN" or Parser.tokenizer.next.type == "MORTYERTHAN" or Parser.tokenizer.next.type == "DOT":
            if Parser.tokenizer.next.type == "EQUAL":
                Parser.tokenizer.select_next()
                res = BinOp("==", [res, Parser.parse_expression()])
                continue

            elif Parser.tokenizer.next.type == "RICKIERTHAN":
                Parser.tokenizer.select_next()
                res = BinOp(">", [res, Parser.parse_expression()])
                continue

            elif Parser.tokenizer.next.type == "MORTYERTHAN":
                Parser.tokenizer.select_next()
                res = BinOp("<", [res, Parser.parse_expression()])
                continue

            elif Parser.tokenizer.next.type == "DOT":
                Parser.tokenizer.select_next()
                res = BinOp(".", [res, Parser.parse_expression()])
                continue

        if Parser.tokenizer.next.type == "EOF":
            return res
        
        return res

    @staticmethod
    def parse_expression():
        res = Parser.parse_term()
        while Parser.tokenizer.next.type == "PLUS" or Parser.tokenizer.next.type == "MINUS" or Parser.tokenizer.next.type == "OR":
            if Parser.tokenizer.next.type == "PLUS":
                Parser.tokenizer.select_next()
                res = BinOp("+", [res, Parser.parse_term()])
                continue
            elif Parser.tokenizer.next.type == "MINUS":
                Parser.tokenizer.select_next()
                res = BinOp("-", [res, Parser.parse_term()])
                continue
            elif Parser.tokenizer.next.type == "OR":
                Parser.tokenizer.select_next()
                res = BinOp("||", [res, Parser.parse_term()])
                continue

        if Parser.tokenizer.next.type == "EOF":
            return res
        
        return res

    @staticmethod
    def parse_term():
        res = Parser.parse_factor()
        while Parser.tokenizer.next.type == "MULT" or Parser.tokenizer.next.type == "DIV" or Parser.tokenizer.next.type == "AND":
            
            if Parser.tokenizer.next.type == "MULT":
                Parser.tokenizer.select_next()
                res = BinOp("*", [res, Parser.parse_factor()])
                continue
            elif Parser.tokenizer.next.type == "DIV":
                Parser.tokenizer.select_next()
                res = BinOp("/", [res, Parser.parse_factor()])
                continue
            elif Parser.tokenizer.next.type == "AND":
                Parser.tokenizer.select_next()
                res = BinOp("&&", [res, Parser.parse_factor()])
                continue

        if Parser.tokenizer.next.type == "EOF":
            return res
        
        return res

    @staticmethod
    def parse_factor():
        if Parser.tokenizer.next.type == "INT":
            res = IntVal(Parser.tokenizer.next.value, [])
            Parser.tokenizer.select_next()
            return res

        if Parser.tokenizer.next.type == "STRING":
            res = StrVal(Parser.tokenizer.next.value, [])
            Parser.tokenizer.select_next()
            return res
        
        elif Parser.tokenizer.next.type == "VAR":
            varName = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()

            if Parser.tokenizer.next.type == "OPEN_PAREN":
                arguments = []
                Parser.tokenizer.select_next()

                while Parser.tokenizer.next.type != "CLOSE_PAREN":
                    arguments.append(Parser.parse_real_expression())
                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.select_next()
                res = FuncCall(varName, arguments)
                Parser.tokenizer.select_next()
            else:
                res = Var(varName, [])
            return res
                

        elif Parser.tokenizer.next.type == "PLUS":
            Parser.tokenizer.select_next()
            res = UnOp("+", [Parser.parse_factor()])
            return res

        elif Parser.tokenizer.next.type == "MINUS":
            Parser.tokenizer.select_next()
            res = UnOp("-", [Parser.parse_factor()])
            return res

        elif Parser.tokenizer.next.type == "NOT":
            Parser.tokenizer.select_next()
            res = UnOp("!", [Parser.parse_factor()])
            return res

        elif Parser.tokenizer.next.type == "OPEN_PAREN":
            Parser.tokenizer.select_next()
            res = Parser.parse_real_expression()
            if Parser.tokenizer.next.type == "CLOSE_PAREN":
                Parser.tokenizer.select_next()
                return res
            
            else:
                raise Exception("[X] Error. Missing closing parenthesis.")
            
        elif Parser.tokenizer.next.type == "STDFUNCT" and Parser.tokenizer.next.value == "Read":
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "OPEN_PAREN":
                Parser.tokenizer.select_next()
                if Parser.tokenizer.next.type == "CLOSE_PAREN":
                    Parser.tokenizer.select_next()
                    return Read("READ", [])
                else:
                    raise Exception("[X] You can not have a function call without a closing parenthesis.")
            else:
                raise Exception("[X] You can not have a function call without an opening parenthesis.")

        else:
            raise Exception("[X] Error. Invalid syntax.") 

    @staticmethod
    def run(string):
        Parser.tokenizer = Tokenizer(string)
        result = Parser.parse_program()
        result.children.append(FuncCall("Main", []))

        if Parser.tokenizer.next.type == "EOF" and result != None:
            localSTable = SymbolTable
            result.Evaluate(localSTable)
        else:
            raise Exception("[X] Error. Invalid syntax.")

# =====================================
# Main
# =====================================
def main():
    filename = sys.argv[1]
    with open(filename, "r") as f:
        code = f.read()
        Parser.run(code)
        #print("FINAL RESULT: ", Tokenizer.next.type)
    
if __name__ == "__main__":
    main()