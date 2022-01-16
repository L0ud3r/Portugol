# eval_interpreter.py

import math
from pprint import PrettyPrinter
from symbol_table import SymbolTable


class   EvalInterpreter:

    # Tabela de operadores
    operators = {
        "or": lambda args: EvalInterpreter._return_value_of_var(args[0]) or EvalInterpreter._return_value_of_var(args[1]),
        "and": lambda args: EvalInterpreter._return_value_of_var(args[0]) and EvalInterpreter._return_value_of_var(args[1]),
        "xor": lambda a: EvalInterpreter._return_value_of_var(a[0]) ^ EvalInterpreter._return_value_of_var(a[1]),
        "not": lambda a: not EvalInterpreter._return_value_of_var(a[0]),

        "+": lambda args: EvalInterpreter._return_value_of_var(args[0]) + EvalInterpreter._return_value_of_var(args[1]),
        "-": lambda args: EvalInterpreter._return_value_of_var(args[0]) - EvalInterpreter._return_value_of_var(args[1]),
        "*": lambda args: EvalInterpreter._return_value_of_var(args[0]) * EvalInterpreter._return_value_of_var(args[1]),
        "/": lambda args: EvalInterpreter._return_value_of_var(args[0]) / EvalInterpreter._return_value_of_var(args[1]),

        "<": lambda args: EvalInterpreter._return_value_of_var(args[0]) < EvalInterpreter._return_value_of_var(args[1]),
        "<=": lambda args: EvalInterpreter._return_value_of_var(args[0]) <= EvalInterpreter._return_value_of_var(args[1]),
        ">": lambda args: EvalInterpreter._return_value_of_var(args[0]) > EvalInterpreter._return_value_of_var(args[1]),
        ">=": lambda args: EvalInterpreter._return_value_of_var(args[0]) >= EvalInterpreter._return_value_of_var(args[1]),

        "=": lambda args: EvalInterpreter._return_value_of_var(args[0]) == EvalInterpreter._return_value_of_var(args[1]),
        "!=": lambda args: EvalInterpreter._return_value_of_var(args[0]) != EvalInterpreter._return_value_of_var(args[1]),

        "declarar": lambda args: EvalInterpreter._declarar(*args),
        "assign": lambda args: EvalInterpreter._changeValue(*args),
        "escreva": lambda args: EvalInterpreter._escreva(*args),
        "leia": lambda args: EvalInterpreter._leia(*args),
        "para": lambda args: EvalInterpreter._para(*args),
        "enquanto": lambda args: EvalInterpreter._enquanto(*args),
        "se": lambda args: EvalInterpreter._se(*args),
        "funcao": lambda args: EvalInterpreter._funcao(args),
        "call": lambda args: EvalInterpreter._call(args),

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
                EvalInterpreter._assign(arg, args[-1], None)
            i += 1

    # Função para chamar uma função
    @staticmethod
    def _call(args):
        name, values = args
        # funcao/0, funcao/1, etc. consoante numero de args
        name = f"{name}/{len(values)}"
        if name in EvalInterpreter.symbols:
            code = EvalInterpreter.symbols[name]["code"]
            var_list = EvalInterpreter.symbols[name]["vars"]

            # definir parâmetros recebidos
            for var_name, value in zip(var_list, values):
                EvalInterpreter._assign(var_name, None, value)
                EvalInterpreter.symbols.re_set(var_name, EvalInterpreter.eval(value))

            # avaliar código
            result = EvalInterpreter.eval(code)

            # apagar variáveis "locais" ("locais", pois apenas são apagadas as dos parâmetros)
            for var in var_list:
                del EvalInterpreter.symbols[var]
            return result

        else:
            # função não está definida
            raise Exception(f"Função {name} não está definida")

    # Procedimento para declarar uma função
    # (não é executada, apenas armazenada em memória para ser chamada futuramente)
    @staticmethod
    def _funcao(args):
        name, var, code = args
        name = f"{name}/{len(var)}"    # factorial/1
        EvalInterpreter.symbols[name] = {"vars": var, "code": code}

    # Procedimento para escrever no escrever dados (variáveis, números, strings, etc.) no ecrã
    @staticmethod
    def _escreva(*args):
        # se tuplo ou lista
        if type(args) == tuple or type(args) == list:
            # percorrer argumentos
            for x in args:
                # caso já não seja tuplo nem lista
                if type(x) != tuple and type(x) != list:
                    print(x)

                # caso ainda seja tuplo ou lista
                else:
                    x_in_list = list(x)
                    while isinstance(x_in_list, list):
                        x_in_list = x_in_list[-1]
                    print(x_in_list)
        # caso não seja nem tuplo nem lista
        else:
            print(args)

    # Procedimento para interpretar o código do ciclo para (for)
    @staticmethod
    def _para(var, lower, higher, code):
        lower = EvalInterpreter._return_value_of_var(lower)
        higher = EvalInterpreter._return_value_of_var(higher)
        value = lower
        EvalInterpreter._assign(var, "real", value)
        while value <= higher:
            EvalInterpreter.eval(code)
            value += 1
            EvalInterpreter._changeValue(var, value)

    # Procedimento para interpretar o código do ciclo enquanto (while)
    @staticmethod
    def _enquanto(*args):
        while EvalInterpreter.eval(args[0]):
            EvalInterpreter.eval(args[1])

    # Procedimento para interpretar o código da condição se (e senão)
    @staticmethod
    def _se(*args):
        # caso não tenha senão
        if len(args) == 2:
            # caso exp = true
            if args[0]:
                return EvalInterpreter.eval(args[1])
            # caso tenha senão
        if len(args) == 3:
            # caso exp = true
            if args[0]:
                return EvalInterpreter.eval(args[1])
            # correr código do senão
            else:
                return EvalInterpreter.eval(args[2])

    # Procedimento para declarar variáveis
    @staticmethod
    def _assign(var, vartype, value):
        EvalInterpreter.symbols[var] = [vartype, value]

    # Procedimento para atribuir valores a variáveis
    @staticmethod
    def _changeValue(var, value):
        # se entrar uma lista em value (stack stuff)
        value = EvalInterpreter._return_value_of_var(value)
        if var in EvalInterpreter.symbols:
            var_type = EvalInterpreter.symbols[var][0]

            # var_type pode ser inteiro, logico, caracter, real

            # verificações!
            if type(value) == str and var_type == "caracter":
                EvalInterpreter.symbols[var][-1] = value
            elif type(value) == bool and var_type == "logico":
                EvalInterpreter.symbols[var][-1] = value

            elif type(value) == float and var_type == "real":
                EvalInterpreter.symbols[var][-1] = value

            elif type(value) == float and var_type == "inteiro":
                if value.is_integer() is False:
                    value = math.trunc(value)
                EvalInterpreter.symbols[var][-1] = value

            else:
                raise Exception(f"Variável {var} é do tipo {var_type}. {type(value)} não é suportado.")
        else:
            raise Exception(f"Variável {var} não existe.")

    # Procedimento para ler dados do input do utilizador para uma variável
    @staticmethod
    def _leia(*args):
        # Por cada variável em argumentos
        for var in args:
            # Caso esteja em símbolos, lê o input
            if var in EvalInterpreter.symbols:
                value = input()
                try:
                    # passa para float caso consiga
                    value = float(value)
                    # Except inútil? Como fixar?
                except:
                    value = value
                EvalInterpreter._changeValue(var, value)
            # Não está em símbolos (não foi declarada)
            else:
                # caso nao queiramos que sejam declaradas variaveis automaticamente
                raise Exception(f"Variável {var} não existe.")

    # TODO: documentar
    @staticmethod
    def eval(ast):
        if type(ast) in (float, bool, str):
            return ast
        if type(ast) is dict:
            return EvalInterpreter._eval_dict(ast)
        if type(ast) is list:
            ans = None
            for c in ast:
                ans = EvalInterpreter.eval(c)
            return ans
        raise Exception(f"Eval called with weird type: {type(ast)}")

    # TODO: documentar
    @staticmethod
    def _eval_dict(ast):
        if "op" in ast:
            op = ast["op"]
            args = list(map(EvalInterpreter.eval, ast["args"]))
            if "data" in ast:
                args += ast["data"]

            if op in EvalInterpreter.operators:
                func = EvalInterpreter.operators[op]
                return func(args)
            else:
                raise Exception(f"Operador desconhecido: {op}")
        elif "var" in ast:
            if ast["var"] in EvalInterpreter.symbols:
                return EvalInterpreter.symbols[ast["var"]]
            raise Exception(f"Variável {ast['var']} não existe.")
        else:
            raise Exception("Weird dict on eval")
