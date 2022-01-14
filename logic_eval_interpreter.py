# logic_eval_interpreter.py

import math
from pprint import PrettyPrinter
from copy import deepcopy
from symbol_table import SymbolTable


class LogicEvalInterpreter:

    # Tabela de operadores
    operators = {
        "or": lambda args: LogicEvalInterpreter._return_value_of_var(args[0]) or LogicEvalInterpreter._return_value_of_var(args[1]),
        "and": lambda args: LogicEvalInterpreter._return_value_of_var(args[0]) and LogicEvalInterpreter._return_value_of_var(args[1]),
        "xor": lambda a: LogicEvalInterpreter._return_value_of_var(a[0]) ^ LogicEvalInterpreter._return_value_of_var(a[1]),
        "not": lambda a: not LogicEvalInterpreter._return_value_of_var(a[0]),
        #
        "+": lambda args: LogicEvalInterpreter._return_value_of_var(args[0]) + LogicEvalInterpreter._return_value_of_var(args[1]),
        "-": lambda args: LogicEvalInterpreter._return_value_of_var(args[0]) - LogicEvalInterpreter._return_value_of_var(args[1]),
        "*": lambda args: LogicEvalInterpreter._return_value_of_var(args[0]) * LogicEvalInterpreter._return_value_of_var(args[1]),
        "/": lambda args: LogicEvalInterpreter._return_value_of_var(args[0]) / LogicEvalInterpreter._return_value_of_var(args[1]),

        "<": lambda args: LogicEvalInterpreter._return_value_of_var(args[0]) < LogicEvalInterpreter._return_value_of_var(args[1]),
        "<=": lambda args: LogicEvalInterpreter._return_value_of_var(args[0]) <= LogicEvalInterpreter._return_value_of_var(args[1]),
        ">": lambda args: LogicEvalInterpreter._return_value_of_var(args[0]) > LogicEvalInterpreter._return_value_of_var(args[1]),
        ">=": lambda args: LogicEvalInterpreter._return_value_of_var(args[0]) >= LogicEvalInterpreter._return_value_of_var(args[1]),

        "=": lambda args: LogicEvalInterpreter._return_value_of_var(args[0]) == LogicEvalInterpreter._return_value_of_var(args[1]),
        "!=": lambda args: LogicEvalInterpreter._return_value_of_var(args[0]) != LogicEvalInterpreter._return_value_of_var(args[1]),

        "declarar": lambda args: LogicEvalInterpreter._declarar(*args),
        "assign": lambda args: LogicEvalInterpreter._changeValue(*args),
        "escreva": lambda args: LogicEvalInterpreter._escreva(*args),
        "leia": lambda args: LogicEvalInterpreter._leia(*args),
        "para": lambda args: LogicEvalInterpreter._para(*args),
        "enquanto": lambda args: LogicEvalInterpreter._enquanto(*args),
        "se": lambda args: LogicEvalInterpreter._se(*args),
        "funcao": lambda args: LogicEvalInterpreter._funcao(args),
        "call": lambda args: LogicEvalInterpreter._call(args),

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
                LogicEvalInterpreter._assign(arg, args[-1], None)
            i += 1


    # Função para chamar uma função
    @staticmethod
    def _call(args):
        name, values = args
        name = f"{name}/{len(values)}" # funcao/0, funcao/1, etc. consoante numero de args
        if name in LogicEvalInterpreter.symbols:
            code = LogicEvalInterpreter.symbols[name]["code"]
            var_list = LogicEvalInterpreter.symbols[name]["vars"]

            for var_name, value in zip(var_list, values): # definir parâmetros recebidos
                LogicEvalInterpreter._assign(var_name, None, value)
                LogicEvalInterpreter.symbols.re_set(var_name, LogicEvalInterpreter.eval(value))

            result = LogicEvalInterpreter.eval(code) # avaliar código

            for var in var_list: # apagar variáveis "locais" ("locais", pois apenas são apagadas as dos parâmetros)
                del LogicEvalInterpreter.symbols[var]
            return result

        else:
            raise Exception(f"Função {name} não está definida") # função não está definida


    # Procedimento para declarar uma função
    # (não é executada, apenas armazenada em memória para ser chamada futuramente)
    @staticmethod
    def _funcao(args):
        name, var, code = args
        name = f"{name}/{len(var)}"    # factorial/1
        LogicEvalInterpreter.symbols[name] = {"vars": var, "code": code}

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
        lower = LogicEvalInterpreter._return_value_of_var(lower)
        higher = LogicEvalInterpreter._return_value_of_var(higher)
        value = lower
        LogicEvalInterpreter._assign(var, "real", value)
        while value <= higher:
            LogicEvalInterpreter.eval(code)
            value += 1
            LogicEvalInterpreter._changeValue(var, value)


    # Procedimento para interpretar o código do ciclo enquanto (while)
    @staticmethod
    def _enquanto(*args):
        while (LogicEvalInterpreter.eval(args[0])):
            LogicEvalInterpreter.eval(args[1])


    # Procedimento para interpretar o código da condição se (e senão)
    @staticmethod
    def _se(*args):
        if len(args) == 2: # caso não tenha senão
            if args[0]: # caso exp = true
                return LogicEvalInterpreter.eval(args[1])
        if len(args) == 3: # caso tenha senão
            if args[0]: # caso exp = true
                return LogicEvalInterpreter.eval(args[1])
            else: # correr código do senão
                return LogicEvalInterpreter.eval(args[2])


    # Procedimento para declarar variáveis
    @staticmethod
    def _assign(var, vartype, value):
        LogicEvalInterpreter.symbols[var] = [vartype, value]


    # Procedimento para atribuir valores a variáveis
    @staticmethod
    def _changeValue(var, value):
        value = LogicEvalInterpreter._return_value_of_var(value) #se entrar uma lista em value (stack stuff)
        if var in LogicEvalInterpreter.symbols:
            var_type = LogicEvalInterpreter.symbols[var][0]

            # var_type pode ser inteiro, logico, caracter, real

            # verificações!
            if (type(value) == str and var_type == "caracter"):
                LogicEvalInterpreter.symbols[var][-1] = value
            elif (type(value) == bool and var_type == "logico"):
                LogicEvalInterpreter.symbols[var][-1] = value

            elif(type(value) == float and var_type == "real"):
                LogicEvalInterpreter.symbols[var][-1] = value

            elif (type(value) == float and var_type == "inteiro"):
                if value.is_integer() == False:
                    #2.5
                    value = math.trunc(value)
                    #2.0
                LogicEvalInterpreter.symbols[var][-1] = value

            else:
                raise Exception (f"Variável {var} é do tipo {var_type}. {type(value)} não é suportado.")
        else:
            raise Exception(f"Variável {var} não existe.")


    # Procedimento para ler dados do input do utilizador para uma variável
    @staticmethod
    def _leia(*args):
        for var in args: # Por cada variável em argumentos
            if var in LogicEvalInterpreter.symbols: # Caso esteja em símbolos, lê o input
                value = input()
                try:
                    value = float(value) # passa para float caso consiga
                except: # pode ser retirado?
                    value = value # pode ser retirado?
                LogicEvalInterpreter._changeValue(var, value)
            else: # Não está em símbolos (não foi declarada)
                raise Exception(f"Variável {var} não existe.") #caso nao queiramos que sejam declaradas variaveis automaticamente


    #TODO: documentar
    @staticmethod
    def eval(ast):
        if type(ast) in (float, bool, str):
            return ast
        if type(ast) is dict:
            return LogicEvalInterpreter._eval_dict(ast)
        if type(ast) is list:
            ans = None
            for c in ast:
                ans = LogicEvalInterpreter.eval(c)
            return ans
        raise Exception(f"Eval called with weird type: {type(ast)}")

    #TODO: documentar
    @staticmethod
    def _eval_dict(ast):
        if "op" in ast:
            op = ast["op"]
            args = list(map(LogicEvalInterpreter.eval, ast["args"]))
            if "data" in ast:
                args += ast["data"]

            if op in LogicEvalInterpreter.operators:
                func = LogicEvalInterpreter.operators[op]
                return func(args)
            else:
                raise Exception(f"Operador desconhecido: {op}")
        elif "var" in ast:
            if ast["var"] in LogicEvalInterpreter.symbols:
                return LogicEvalInterpreter.symbols[ast["var"]]
            raise Exception(f"Variável {ast['var']} não existe.")
        else:
            raise Exception("Weird dict on eval")

