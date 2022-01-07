# logic_eval

from pprint import PrettyPrinter as pp


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

        "assign": lambda a: LogicEval._assign(*a),
        "escreva": lambda a: print(*a),
        "leia": lambda args: LogicEval._leia(*args),
        "para": lambda args: LogicEval._para(*args),
        "fun": lambda args: LogicEval._fun(args),
        "call": lambda args: LogicEval._call(args)
    }
    # Symbol Table (Tabela de Símbolos)
    symbols = {}

    @staticmethod
    def check_float(x):
        assert type(x) is float, "operando nao é float"
        return x

    @staticmethod
    def _call(args):
        name, values = args
        name = f"{name}/{len(values)}"
        if name in LogicEval.symbols:
            code = LogicEval.symbols[name]["code"]
            var_list = LogicEval.symbols[name]["vars"]
            # 1. Definir as variaveis recebidas  [[DANGER]]
            for var_name, value in zip(var_list, values):
                LogicEval._assign(var_name, LogicEval.eval(value))
            # 2. Avaliar Codigo
            result = LogicEval.eval(code)
            # 3. Apagar as variaveis "locais"
            for var in var_list:
                del LogicEval.symbols[var]
            return result

        else:
            raise Exception(f"Function {name} not defined")

    @staticmethod
    def _fun(args):
        name, var, code = args
        name = f"{name}/{len(var)}"    # factorial/1
        LogicEval.symbols[name] = {"vars": var, "code": code}

    @staticmethod
    def _para(var, lower, higher, code):
        inc, comp = (1, lambda a, b: a <= b) \
            if lower < higher else (-1, lambda a, b: a >= b)
        value = lower
        LogicEval._assign(var, value)
        while comp(value, higher):
            LogicEval.eval(code)
            value += inc
            LogicEval._assign(var, value)

    @staticmethod
    def _assign(var, value):
        LogicEval.symbols[var] = value

    @staticmethod
    def _leia(*args):
        for var in args:
            if var in LogicEval.symbols:
                value = input("Escreva valor: ")
                try:
                    value = float(value)
                except:
                    value = value
                LogicEval._assign(var, value)
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
            raise Exception(f"Unknown variable {ast['var']}")
        else:
            raise Exception("Weird dict on eval")

