__author__ = 'Phase (Jadon Fowler)'

tokens = []
symbols = {}

def open_file(filename):
    data = open(filename, "r").read()
    data += "<EOF>"
    return data


def lex(contents):
    tok = ""
    state = 0
    string = ""
    expr = ""
    n = ""
    isexpr = 0
    varstarted = 0
    var = ""
    comment = 0

    contents = list(contents)
    for char in contents:
        tok += char
        if comment == 0 and tok == ";":
            comment = 1
        elif comment == 1:
            if tok == "\n" or tok == "<EOF>":
                comment = 0
            tok = ""
        elif tok == " " and state == 0:
            tok = ""
        elif tok == "\n" or tok == "<EOF>":
            if comment == 1:
                comment = 0
            elif expr != "" and isexpr == 1:
                tokens.append("EXPR:" + expr)
                expr = ""
                isexpr = 0
            elif expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            elif var != "":
                tokens.append("VAR:" + var)
                var = ""
                varstarted = 0
            tok = ""
        elif tok == "=" and state == 0:
            if var != "":
                tokens.append("VAR:" + var)
                var = ""
                varstarted = 0
            tokens.append("EQUALS")
            tok = ""
        elif tok == "@" and state == 0 and isexpr == 0:
            varstarted = 1
            var += tok
            tok = ""
        elif tok == "echo":
            tokens.append("ECHO")
            tok = ""
        elif varstarted == 1:
            if tok == "<" or tok == ">":
                if var != "":
                    tokens.append("VAR:" + var)
                    var = ""
                    varstarted = 0
                    tok = ""
            if varstarted == 1:
                var += tok
                tok = ""
        elif tok == "in":
            tokens.append("IN")
            tok = ""
        elif tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9":
            expr += tok
            tok = ""
        elif tok == "+" or tok == "-" or tok == "/" or tok == "*" or tok == "(" or tok == ")":
            isexpr = 1
            expr += tok
            tok = ""
        elif isexpr == 1:
            expr += tok
            tok = ""
        elif tok == "\"" or tok == " \"":
            if state == 0:
                state = 1
            elif state == 1:
                tokens.append("STRING:" + string + "\"")
                string = ""
                state = 0
                tok = ""
        elif state == 1:
            string += tok
            tok = ""
    print(tokens)
    return tokens

def echo(p):
    if p[0:6] == "STRING":
        p = p[8:]
        p = p[:-1]
    elif p[0:3] == "NUM":
        p = p[4:]
    elif p[0:4] == "EXPR":
        p = eval(p[5:])
    print(p)

def assignVariable(varname, value):
    symbols[varname[4:]] = value

def getVariable(varname):
    varname = varname[4:]
    if varname in symbols:
        return symbols[varname]
    else:
        return "Undefined:" + varname

def getInput(prompt, var):
    i = input(prompt + " ")
    symbols[var] = "STRING:\"" + i + "\""

def evaluate(s):
    for v in symbols.keys():
        if s.find(v) != -1:
            s.replace(v, str(getVariable("VAR:" + v)).split(":")[1])
            s
            print(s)
    return eval(s)

def parse(toks):
    i = 0
    while i < len(toks):
        if toks[i] == "ECHO":
            if toks[i+1][0:3] == "VAR":
                echo(getVariable(toks[i+1]))
            else:
                echo(toks[i + 1])
            i += 2
        elif len(toks) >= i + 2 and toks[i][0:3] + " " + toks[i+1] == "VAR EQUALS":
            if toks[i+2][0:3] == "VAR":
                assignVariable(toks[i], getVariable(toks[i+2]))
            if toks[i+2][0:4] == "EXPR":
                assignVariable(toks[i], "NUM:" + str(evaluate(toks[i+2][5:])))
            else:
                assignVariable(toks[i], toks[i + 2])
            i += 3
        elif toks[i] == "IN" and len(toks) > i+2:
            getInput(toks[i+1][8:-1], toks[i+2][4:])
            i += 3

def run():
    data = open_file("helloworld.flow")
    toks = lex(data)
    parse(toks)


run()
