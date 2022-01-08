# logic_eval

from pprint import PrettyPrinter as pp
from copy import deepcopy
from symbol_table import SymbolTable


class LogicEval:

    # Dispatch Table (Design Pattern)
    operators = {
        "or": lambda args: args[0] or args[1],
        "and": lambda args: args[0] and args[1],
        "xor": lambda a: a[0] ^ a[1],
        "not": lambda a: not a[0],
        "+": lambda args: args[0] + args[1],
        "-": lambda args: args[0] - args[1],
        "*": lambda args: args[0] * args[1],
        "/": lambda args: args[0] / args[1],

        "declarar": lambda args: LogicEval._declarar(*args),
        "assign": lambda args: LogicEval._changeValue(*args),
        "escreva": lambda args: LogicEval._escreva(*args),
        "leia": lambda args: LogicEval._leia(*args),
        "para": lambda args: LogicEval._para(*args),
        "funcao": lambda args: LogicEval._funcao(args),
        "call": lambda args: LogicEval._call(args)
    }
    # Symbol Table (Tabela de Símbolos)
    symbols = SymbolTable()

    #@staticmethod
    #def check_float(x):
    #    assert type(x) is float, "operando nao é float"
    #    return x

    @staticmethod
    def _declarar(*args):
        i = 0
        for arg in args:
            if i < len(args)-1:
                LogicEval._assign(arg, args[-1], None)
            i += 1



    @staticmethod
    def _call(args):
        name, values = args
        name = f"{name}/{len(values)}"
        if name in LogicEval.symbols:
            code = LogicEval.symbols[name]["code"]
            var_list = LogicEval.symbols[name]["vars"]
            # 1. Definir as variaveis recebidas  [[DANGER]]
            for var_name, value in zip(var_list, values):
                LogicEval.symbols.re_set(var_name, LogicEval.eval(value))
            # 2. Avaliar Codigo
            result = LogicEval.eval(code)
            # 3. Apagar as variaveis "locais"/recebidas
            for var in var_list:
                del LogicEval.symbols[var]
            return result

        else:
            raise Exception(f"Function {name} not defined")

    @staticmethod
    def _funcao(args):
        name, var, code = args
        name = f"{name}/{len(var)}"    # factorial/1
        LogicEval.symbols[name] = {"vars": var, "code": code}

    def _escreva(args):
        i = 0
        for arg in args:
            if i == len(args)-1:
                print(arg)
            i+=1

    @staticmethod
    def _para(var, lower, higher, code):
        inc, comp = (1, lambda a, b: a <= b) \
            if lower < higher else (-1, lambda a, b: a >= b)
        value = lower
        LogicEval._assign(var, None, value)
        while comp(value, higher):
            LogicEval.eval(code)
            value += inc
            LogicEval._assign(var, None, value)

    @staticmethod
    def _assign(var, vartype, value):
        LogicEval.symbols[var] = [vartype, value]

    def _changeValue(var, value):
        if var in LogicEval.symbols:
            var_type = LogicEval.symbols[var][0]
            if (type(value) == str) and (var_type == "caracter"):
                LogicEval.symbols[var][1] = value
            elif (type(value) != str) and (var_type != "caracter"):
                LogicEval.symbols[var][1] = value
            else:
                raise Exception(f"Variável {var} é do tipo {var_type}. Esse não é suportado.")
        else:
            raise Exception(f"Variável {var} não existe.")

    @staticmethod
    def _leia(*args):
        for var in args:
            if var in LogicEval.symbols:
                value = input("Escreva valor: ")
                try:
                    value = float(value)
                except:
                    value = value
                LogicEval._assign(var, None, value)
            else:
                raise Exception(f"Variable {var} does not exist.") #caso nao queiramos que sejam declaradas variaveis automaticamente

                #declara automaticamente
                #LogicEval._assign(var, None)
                #LogicEval._leia(var)



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

    @staticmethod
    def _eval_dict(ast):
        if "op" in ast:
            op = ast["op"]
            # args = [LogicEval.eval(x) for x in ast["args"]]
            args = list(map(LogicEval.eval, ast["args"]))
            if "data" in ast:
                args += ast["data"]

            if op in LogicEval.operators:
                func = LogicEval.operators[op]
                return func(args)
            else:
                raise Exception(f"Unknown operator: {op}")
        elif "var" in ast:
            if ast["var"] in LogicEval.symbols:
                return LogicEval.symbols[ast["var"]]
            raise Exception(f"Variável {ast['var']} não existe.")
        else:
            raise Exception("Weird dict on eval")

