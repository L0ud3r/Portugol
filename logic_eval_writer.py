# logic_eval_writer.py

import math
from pprint import PrettyPrinter
from copy import deepcopy
from symbol_table import SymbolTable


class LogicEvalWriter:

    # Tabela de operadores
    operators = {
        "or": lambda args: str(LogicEvalWriter._return_value_of_var(args[0])) + "||" +  str(LogicEvalWriter._return_value_of_var(args[1])),
        "and": lambda args: str(LogicEvalWriter._return_value_of_var(args[0])) + "&&" +  str(LogicEvalWriter._return_value_of_var(args[1])),
        "xor": lambda args: str(LogicEvalWriter._return_value_of_var(args[0])) + "^" +  str(LogicEvalWriter._return_value_of_var(args[1])),
        "not": lambda args: str(LogicEvalWriter._return_value_of_var(args[0])) + "!" +  str(LogicEvalWriter._return_value_of_var(args[1])),
        #
        "+": lambda args: str(LogicEvalWriter._return_value_of_var(args[0])) + "+" +  str(LogicEvalWriter._return_value_of_var(args[1])),
        "-": lambda args: str(LogicEvalWriter._return_value_of_var(args[0])) + "-" +  str(LogicEvalWriter._return_value_of_var(args[1])),
        "*": lambda args: str(LogicEvalWriter._return_value_of_var(args[0])) + "*" +  str(LogicEvalWriter._return_value_of_var(args[1])),
        "/": lambda args: str(LogicEvalWriter._return_value_of_var(args[0])) + "/" +  str(LogicEvalWriter._return_value_of_var(args[1])),

        "<": lambda args: str(LogicEvalWriter._return_value_of_var(args[0])) + "<" +  str(LogicEvalWriter._return_value_of_var(args[1])),
        "<=": lambda args: str(LogicEvalWriter._return_value_of_var(args[0])) + "<=" +  str(LogicEvalWriter._return_value_of_var(args[1])),
        ">": lambda args: str(LogicEvalWriter._return_value_of_var(args[0])) + ">" +  str(LogicEvalWriter._return_value_of_var(args[1])),
        ">=": lambda args: str(LogicEvalWriter._return_value_of_var(args[0])) + ">=" +  str(LogicEvalWriter._return_value_of_var(args[1])),

        "=": lambda args: str(LogicEvalWriter._return_value_of_var(args[0])) + "==" +  str(LogicEvalWriter._return_value_of_var(args[1])),
        "!=": lambda args: str(LogicEvalWriter._return_value_of_var(args[0])) + "!=" +  str(LogicEvalWriter._return_value_of_var(args[1])),

        "declarar": lambda args: LogicEvalWriter._declarar(*args), #done
        "assign": lambda args: LogicEvalWriter._changeValue(*args), #fix funcoes
        "escreva": lambda args: LogicEvalWriter._escreva(*args), #done
        "leia": lambda args: LogicEvalWriter._leia(*args), #done
        "para": lambda args: LogicEvalWriter._para(*args), #done
        "enquanto": lambda args: LogicEvalWriter._enquanto(*args), #done
        "se": lambda args: LogicEvalWriter._se(*args), #done
        "funcao": lambda args: LogicEvalWriter._funcao(args), #done
        "call": lambda args: LogicEvalWriter._funcao2(*args), #done

    }
    # Symbol Table (Tabela de Símbolos)
    symbols = SymbolTable()

    f = open("main.c", "w")
    c_code = ""

    @staticmethod
    def _write_operation_to_file(value1, op, value2):
        value1 = LogicEvalWriter._return_value_of_var(value1)
        value2 = LogicEvalWriter._return_value_of_var(value2)
        LogicEvalWriter._write_to_file(value1, op, value2)

    @staticmethod
    def _write_to_file(*args):
        for a in args:
            a = str(a)
            LogicEvalWriter.c_code += a
        LogicEvalWriter.c_code+=";\n"


    # Função para retornar o valor de uma variável
    # Com a implementação da stack e dos vartypes, uma variável é guardada da seguinte forma
    # key = "x", value = [inteiro, "1"] ou no caso de vários: key = "x", value = [inteiro, "1", "2"]
    @staticmethod
    def _return_value_of_var(value):
        while isinstance(value, list):
            value = value[-1]
        return value


    # Procedimento para declarar uma variável
    # Presume-se que declarar uma variável é criá-la na memória mas não atribuir um valor
    @staticmethod
    def _declarar(*args):

        vartype = args[-1]

        if vartype == "inteiro":
            vartype = "int"
        elif vartype == "logico":
            vartype = "bool"
        elif vartype == "real":
            vartype = "float"
        elif vartype == "caracter":
            vartype = "char*"

        i = 0
        for arg in args:
            if i < len(args)-1:
                #args = varname or varnames, vartype
                LogicEvalWriter.c_code += f"{vartype} {arg};\n\t"
                LogicEvalWriter._assign(arg, vartype, None)
            i += 1


    # Função para chamar uma função
    @staticmethod
    def _call(args): #TODO: fix
        print(args)

        name, values = args
        finalString = ""
        #LogicEvalWriter.c_code += f"{name}("
        finalString += f"{name}("
        i = 0
        for value in values:
            if i < len(values)-1:
                #LogicEvalWriter.c_code += f"{value},"
                finalString += f"{value},"
            else:
                #LogicEvalWriter.c_code += f"{value});\n\t"
                finalString += f"{value})"
            i+=1

        return finalString

    @staticmethod
    def _funcao2(*args):
        # print(args)
        LogicEvalWriter.eval(LogicEvalWriter._call(args))

    # Procedimento para declarar uma função
    # (não é executada, apenas armazenada em memória para ser chamada futuramente)
    @staticmethod
    def _funcao(args):

        name, vars, code = args

        LogicEvalWriter.c_code += f"int {name}("

        i = 0

        for var in vars:
            if i == len(vars)-1:
                LogicEvalWriter.c_code += f"int {var})"
            else:
                LogicEvalWriter.c_code += f"int {var},"
            i+=1

        LogicEvalWriter.c_code += "{\n\t"
        LogicEvalWriter.eval(code)
        LogicEvalWriter.c_code += f"return {args[-1][-1]['var']};\n\t"
        LogicEvalWriter.c_code += "}\n\t"


    # Procedimento para escrever no escrever dados (variáveis, números, strings, etc.) no ecrã
    @staticmethod
    def _escreva(*args):
        for arg in args:
            if arg in LogicEvalWriter.symbols:
                LogicEvalWriter.c_code += f'printf("'
                if LogicEvalWriter.symbols[arg][0] == "int":
                    LogicEvalWriter.c_code += "%d"
                elif LogicEvalWriter.symbols[arg][0] == "bool":
                    LogicEvalWriter.c_code += "%b"
                elif LogicEvalWriter.symbols[arg][0] == "float":
                    LogicEvalWriter.c_code += "%f"
                elif LogicEvalWriter.symbols[arg][0] == "char*":
                    LogicEvalWriter.c_code += "%s"
                LogicEvalWriter.c_code += f'", {arg});\n\t'
            else:
                LogicEvalWriter.c_code += f'printf("{arg}");\n\t'



    # Procedimento para interpretar o código do ciclo para (for)
    @staticmethod
    def _para(var, lower, higher, code):
        lower = LogicEvalWriter._return_value_of_var(lower)
        higher = LogicEvalWriter._return_value_of_var(higher)
        LogicEvalWriter.c_code += f"for({var} = {lower}; {var} <= {higher}; {var}++)" + "{\n"
        LogicEvalWriter.eval(code)
        LogicEvalWriter.c_code += "}\n"




    # Procedimento para interpretar o código do ciclo enquanto (while)
    @staticmethod
    def _enquanto(*args):
        LogicEvalWriter.c_code += f"while({args[0]['args'][0]['var']} {args[0]['op']}  {args[0]['args'][1]['var']}) " + "{\n"
        LogicEvalWriter.eval(args[1])
        LogicEvalWriter.c_code += "}\n"


    # Procedimento para interpretar o código da condição se (e senão)
    @staticmethod
    def _se(*args):

        if len(args) == 2: # caso não tenha senão
            LogicEvalWriter.c_code += f"if ({args[0]})" + "{\n"

            LogicEvalWriter.eval(args[1])
            LogicEvalWriter.c_code += "}\n"
        if len(args) == 3:
            LogicEvalWriter.c_code += f"if ({args[0]})" + "{\n"

            LogicEvalWriter.eval(args[1])
            LogicEvalWriter.c_code += "}\n"
            LogicEvalWriter.c_code += "else {\n\t"
            LogicEvalWriter.eval(args[2])
            LogicEvalWriter.c_code += "}\n\t"







    # Procedimento para declarar variáveis
    @staticmethod
    def _assign(var, vartype, value):
        LogicEvalWriter.symbols[var] = [vartype, value]

    # Procedimento para atribuir valores a variáveis
    @staticmethod
    def _changeValue(var, value):

        LogicEvalWriter.c_code += f"{var} = {LogicEvalWriter.eval(value)};\n\t"


    # Procedimento para ler dados do input do utilizador para uma variável
    @staticmethod
    def _leia(*args):
        for arg in args:
            if arg in LogicEvalWriter.symbols:
                LogicEvalWriter.c_code += f'scanf("'
                if LogicEvalWriter.symbols[arg][0] == "int":
                    LogicEvalWriter.c_code += "%d"
                elif LogicEvalWriter.symbols[arg][0] == "bool":
                    LogicEvalWriter.c_code += "%b"
                elif LogicEvalWriter.symbols[arg][0] == "float":
                    LogicEvalWriter.c_code += "%f"
                elif LogicEvalWriter.symbols[arg][0] == "char*":
                    LogicEvalWriter.c_code += "%s"
                LogicEvalWriter.c_code += f'", &{arg});\n\t'


    #TODO: documentar
    @staticmethod
    def eval(ast):
        if type(ast) in (float, bool, str):
            ast2 = str(ast)
            if ast2 == "inicio":
                LogicEvalWriter.c_code += "int main(){" + "\n\t"
            elif ast2 == "fim":
                LogicEvalWriter.c_code += "}"
                LogicEvalWriter.f.write(LogicEvalWriter.c_code)
                LogicEvalWriter.f.close()
            return ast
        if type(ast) is dict:
            return LogicEvalWriter._eval_dict(ast)
        if type(ast) is list:
            ans = None
            for c in ast:
                ans = LogicEvalWriter.eval(c)
            return ans
        raise Exception(f"Eval called with weird type: {type(ast)}")

    #TODO: documentar
    @staticmethod
    def _eval_dict(ast):
        if "op" in ast:
            op = ast["op"]
            args = list(map(LogicEvalWriter.eval, ast["args"]))
            if "data" in ast:
                args += ast["data"]

            if op in LogicEvalWriter.operators:
                func = LogicEvalWriter.operators[op]
                return func(args)
            else:
                raise Exception(f"Operador desconhecido: {op}")
        elif "var" in ast:
            return ast["var"]
        else:
            raise Exception("Weird dict on eval")

