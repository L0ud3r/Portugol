# logic_eval.py

import math
from pprint import PrettyPrinter
from copy import deepcopy
from symbol_table import SymbolTable


class LogicEval:

    # Tabela de operadores
    operators = {
        "or": lambda args: LogicEval._return_value_of_var(args[0]) or LogicEval._return_value_of_var(args[1]),
        "and": lambda args: LogicEval._return_value_of_var(args[0]) and LogicEval._return_value_of_var(args[1]),
        "xor": lambda a: LogicEval._return_value_of_var(a[0]) ^ LogicEval._return_value_of_var(a[1]),
        "not": lambda a: not LogicEval._return_value_of_var(a[0]),
        #
        "+": lambda args: LogicEval._return_value_of_var(args[0]) + LogicEval._return_value_of_var(args[1]),
        "-": lambda args: LogicEval._return_value_of_var(args[0]) - LogicEval._return_value_of_var(args[1]),
        "*": lambda args: LogicEval._return_value_of_var(args[0]) * LogicEval._return_value_of_var(args[1]),
        "/": lambda args: LogicEval._return_value_of_var(args[0]) / LogicEval._return_value_of_var(args[1]),

        "<": lambda args: LogicEval._return_value_of_var(args[0]) < LogicEval._return_value_of_var(args[1]),
        "<=": lambda args: LogicEval._return_value_of_var(args[0]) <= LogicEval._return_value_of_var(args[1]),
        ">": lambda args: LogicEval._return_value_of_var(args[0]) > LogicEval._return_value_of_var(args[1]),
        ">=": lambda args: LogicEval._return_value_of_var(args[0]) >= LogicEval._return_value_of_var(args[1]),

        "=": lambda args: LogicEval._return_value_of_var(args[0]) == LogicEval._return_value_of_var(args[1]),
        "!=": lambda args: LogicEval._return_value_of_var(args[0]) != LogicEval._return_value_of_var(args[1]),

        "declarar": lambda args: LogicEval._declarar(*args),
        "assign": lambda args: LogicEval._changeValue(*args),
        "escreva": lambda args: LogicEval._escreva(*args),
        "leia": lambda args: LogicEval._leia(*args),
        "para": lambda args: LogicEval._para(*args),
        "enquanto": lambda args: LogicEval._enquanto(*args),
        "se": lambda args: LogicEval._se(*args),
        "funcao": lambda args: LogicEval._funcao(args),
        "call": lambda args: LogicEval._call(args),

    }
    # Symbol Table (Tabela de Símbolos)
    symbols = SymbolTable()

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
        i = 0
        for arg in args:
            if i < len(args)-1:
                #args = varname, vartype, None
                LogicEval._assign(arg, args[-1], None)
            i += 1


    # Função para chamar uma função
    @staticmethod
    def _call(args):
        name, values = args
        name = f"{name}/{len(values)}" # funcao/0, funcao/1, etc. consoante numero de args
        if name in LogicEval.symbols:
            code = LogicEval.symbols[name]["code"]
            var_list = LogicEval.symbols[name]["vars"]

            for var_name, value in zip(var_list, values): # definir parâmetros recebidos
                LogicEval._assign(var_name, None, value)
                LogicEval.symbols.re_set(var_name, LogicEval.eval(value))

            result = LogicEval.eval(code) # avaliar código

            for var in var_list: # apagar variáveis "locais" ("locais", pois apenas são apagadas as dos parâmetros)
                del LogicEval.symbols[var]
            return result

        else:
            raise Exception(f"Função {name} não está definida") # função não está definida


    # Procedimento para declarar uma função
    # (não é executada, apenas armazenada em memória para ser chamada futuramente)
    @staticmethod
    def _funcao(args):
        name, var, code = args
        name = f"{name}/{len(var)}"    # factorial/1
        LogicEval.symbols[name] = {"vars": var, "code": code}

    # Procedimento para escrever no escrever dados (variáveis, números, strings, etc.) no ecrã
    @staticmethod
    def _escreva(*args):
        if type(args) == tuple or type(args) == list: # se tuplo ou lista
            for x in args: # percorrer argumentos
                if type(x) != tuple and type(x) != list: #caso já não seja tuplo nem lista
                    print(x)
                else: #caso ainda seja tuplo ou lista
                    x_in_list = list(x)
                    while isinstance(x_in_list, list):
                        x_in_list = x_in_list[-1]
                    print(x_in_list)
        else: # caso não seja nem tuplo nem lista
            print(args)


    # Procedimento para interpretar o código do ciclo para (for)
    @staticmethod
    def _para(var, lower, higher, code):
        lower = LogicEval._return_value_of_var(lower)
        higher = LogicEval._return_value_of_var(higher)
        value = lower
        LogicEval._assign(var, "real", value)
        while value <= higher:
            LogicEval.eval(code)
            value += 1
            LogicEval._changeValue(var, value)


    # Procedimento para interpretar o código do ciclo enquanto (while)
    @staticmethod
    def _enquanto(*args):
        while (LogicEval.eval(args[0])):
            LogicEval.eval(args[1])


    # Procedimento para interpretar o código da condição se (e senão)
    @staticmethod
    def _se(*args):
        if len(args) == 2: # caso não tenha senão
            if args[0]: # caso exp = true
                return LogicEval.eval(args[1])
        if len(args) == 3: # caso tenha senão
            if args[0]: # caso exp = true
                return LogicEval.eval(args[1])
            else: # correr código do senão
                return LogicEval.eval(args[2])


    # Procedimento para declarar variáveis
    @staticmethod
    def _assign(var, vartype, value):
        LogicEval.symbols[var] = [vartype, value]


    # Procedimento para atribuir valores a variáveis
    @staticmethod
    def _changeValue(var, value):
        value = LogicEval._return_value_of_var(value) #se entrar uma lista em value (stack stuff)
        if var in LogicEval.symbols:
            var_type = LogicEval.symbols[var][0]

            # var_type pode ser inteiro, logico, caracter, real

            # verificações!
            if (type(value) == str and var_type == "caracter"):
                LogicEval.symbols[var][-1] = value
            elif (type(value) == bool and var_type == "logico"):
                LogicEval.symbols[var][-1] = value

            elif(type(value) == float and var_type == "real"):
                LogicEval.symbols[var][-1] = value

            elif (type(value) == float and var_type == "inteiro"):
                if value.is_integer() == False:
                    #2.5
                    value = math.trunc(value)
                    #2.0
                LogicEval.symbols[var][-1] = value

            else:
                raise Exception (f"Variável {var} é do tipo {var_type}. {type(value)} não é suportado.")
        else:
            raise Exception(f"Variável {var} não existe.")


    # Procedimento para ler dados do input do utilizador para uma variável
    @staticmethod
    def _leia(*args):
        for var in args: # Por cada variável em argumentos
            if var in LogicEval.symbols: # Caso esteja em símbolos, lê o input
                value = input()
                try:
                    value = float(value) # passa para float caso consiga
                except: # pode ser retirado?
                    value = value # pode ser retirado?
                LogicEval._changeValue(var, value)
            else: # Não está em símbolos (não foi declarada)
                raise Exception(f"Variável {var} não existe.") #caso nao queiramos que sejam declaradas variaveis automaticamente


    #TODO: documentar
    @staticmethod
    def eval(ast):
        if type(ast) in (float, bool, str):
            return ast
        if type(ast) is dict:
            return LogicEval._eval_dict(ast)
        if type(ast) is list:
            ans = None
            for c in ast:
                ans = LogicEval.eval(c)
            return ans
        raise Exception(f"Eval called with weird type: {type(ast)}")

    #TODO: documentar
    @staticmethod
    def _eval_dict(ast):
        if "op" in ast:
            op = ast["op"]
            args = list(map(LogicEval.eval, ast["args"]))
            if "data" in ast:
                args += ast["data"]

            if op in LogicEval.operators:
                func = LogicEval.operators[op]
                return func(args)
            else:
                raise Exception(f"Operador desconhecido: {op}")
        elif "var" in ast:
            if ast["var"] in LogicEval.symbols:
                return LogicEval.symbols[ast["var"]]
            raise Exception(f"Variável {ast['var']} não existe.")
        else:
            raise Exception("Weird dict on eval")

