# eval_writer.py

from symbol_table import SymbolTable


class EvalWriter:

    # Tabela de operadores
    operators = {
        "or": lambda args: str(EvalWriter._return_value_of_var(args[0])) + "||" + str(EvalWriter._return_value_of_var(args[1])),
        "and": lambda args: str(EvalWriter._return_value_of_var(args[0])) + "&&" + str(EvalWriter._return_value_of_var(args[1])),
        "xor": lambda args: str(EvalWriter._return_value_of_var(args[0])) + "^" + str(EvalWriter._return_value_of_var(args[1])),
        "not": lambda args: str(EvalWriter._return_value_of_var(args[0])) + "!" + str(EvalWriter._return_value_of_var(args[1])),

        "+": lambda args: str(EvalWriter._return_value_of_var(args[0])) + "+" + str(EvalWriter._return_value_of_var(args[1])),
        "-": lambda args: str(EvalWriter._return_value_of_var(args[0])) + "-" + str(EvalWriter._return_value_of_var(args[1])),
        "*": lambda args: str(EvalWriter._return_value_of_var(args[0])) + "*" + str(EvalWriter._return_value_of_var(args[1])),
        "/": lambda args: str(EvalWriter._return_value_of_var(args[0])) + "/" + str(EvalWriter._return_value_of_var(args[1])),

        "<": lambda args: str(EvalWriter._return_value_of_var(args[0])) + "<" + str(EvalWriter._return_value_of_var(args[1])),
        "<=": lambda args: str(EvalWriter._return_value_of_var(args[0])) + "<=" + str(EvalWriter._return_value_of_var(args[1])),
        ">": lambda args: str(EvalWriter._return_value_of_var(args[0])) + ">" + str(EvalWriter._return_value_of_var(args[1])),
        ">=": lambda args: str(EvalWriter._return_value_of_var(args[0])) + ">=" + str(EvalWriter._return_value_of_var(args[1])),

        "=": lambda args: str(EvalWriter._return_value_of_var(args[0])) + "==" + str(EvalWriter._return_value_of_var(args[1])),
        "!=": lambda args: str(EvalWriter._return_value_of_var(args[0])) + "!=" + str(EvalWriter._return_value_of_var(args[1])),

        "declarar": lambda args: EvalWriter._declarar(*args),
        "assign": lambda args: EvalWriter._changeValue(*args), #fix funcoes
        "escreva": lambda args: EvalWriter._escreva(*args),
        "leia": lambda args: EvalWriter._leia(*args),
        "para": lambda args: EvalWriter._para(*args),
        "enquanto": lambda args: EvalWriter._enquanto(*args),
        "se": lambda args: EvalWriter._se(*args),
        "funcao": lambda args: EvalWriter._funcao(args),
        "call": lambda args: EvalWriter._call(args),

    }
    # Symbol Table (Tabela de Símbolos)
    symbols = SymbolTable()

    # Abrir o ficheiro main.c
    f = open("main.c", "w")
    c_code = ""

    # Recebe uma operação e chama a função write_to_file para escrever no ficheiro a operação
    @staticmethod
    def _write_operation_to_file(value1, op, value2):
        value1 = EvalWriter._return_value_of_var(value1)
        value2 = EvalWriter._return_value_of_var(value2)
        EvalWriter._write_to_file(value1, op, value2)

    # Escreve para o c.code os argumentos
    @staticmethod
    def _write_to_file(*args):
        for a in args:
            a = str(a)
            EvalWriter.c_code += a
        EvalWriter.c_code += ";\n"

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
                # args = varname or varnames, vartype
                EvalWriter.c_code += f"{vartype} {arg};\n\t"
                EvalWriter._assign(arg, vartype, None)
            i += 1

    # TODO: fix
    # Função para chamar uma função
    @staticmethod
    def _call(args):
        name, values = args
        final_string = ""
        #LogicEvalWriter.c_code += f"{name}("
        final_string += f"{name}("
        i = 0
        for value in values:
            if i < len(values)-1:
                #LogicEvalWriter.c_code += f"{value},"
                final_string += f"{value},"
            else:
                #LogicEvalWriter.c_code += f"{value});\n\t"
                final_string += f"{value})"
            i += 1

        #LogicEvalWriter.eval(args)
        return final_string

    # Procedimento para declarar uma função
    # (não é executada, apenas armazenada em memória para ser chamada futuramente)
    @staticmethod
    def _funcao(args):
        name, varrs, code = args
        EvalWriter.c_code += f"int {name}("

        i = 0

        for var in varrs:
            if i == len(varrs)-1:
                EvalWriter.c_code += f"int {var})"
            else:
                EvalWriter.c_code += f"int {var},"
            i += 1

        EvalWriter.c_code += "{\n\t"
        EvalWriter.eval(code)
        EvalWriter.c_code += f"return {args[-1][-1]['var']};\n\t"
        EvalWriter.c_code += "}\n\t"

    # Procedimento para escrever no escrever dados (variáveis, números, strings, etc.) no ecrã
    @staticmethod
    def _escreva(*args):
        for arg in args:
            if arg in EvalWriter.symbols:
                EvalWriter.c_code += f'printf("'
                if EvalWriter.symbols[arg][0] == "int":
                    EvalWriter.c_code += "%d"
                elif EvalWriter.symbols[arg][0] == "bool":
                    EvalWriter.c_code += "%b"
                elif EvalWriter.symbols[arg][0] == "float":
                    EvalWriter.c_code += "%f"
                elif EvalWriter.symbols[arg][0] == "char*":
                    EvalWriter.c_code += "%s"
                EvalWriter.c_code += f'", {arg});\n\t'
            else:
                EvalWriter.c_code += f'printf("{arg}");\n\t'

    # Procedimento para interpretar o código do ciclo para (for)
    @staticmethod
    def _para(var, lower, higher, code):
        lower = EvalWriter._return_value_of_var(lower)
        higher = EvalWriter._return_value_of_var(higher)
        EvalWriter.c_code += f"for({var} = {lower}; {var} <= {higher}; {var}++)" + "{\n"
        EvalWriter.eval(code)
        EvalWriter.c_code += "}\n"

    # Procedimento para interpretar o código do ciclo enquanto (while)
    @staticmethod
    def _enquanto(*args):
        EvalWriter.c_code += f"while({args[0]['args'][0]['var']} {args[0]['op']}  {args[0]['args'][1]['var']}) " + "{\n"
        EvalWriter.eval(args[1])
        EvalWriter.c_code += "}\n"

    # Procedimento para interpretar o código da condição se (e senão)
    @staticmethod
    def _se(*args):
        # caso não tenha senão
        if len(args) == 2:
            EvalWriter.c_code += f"if ({args[0]})" + "{\n"

            EvalWriter.eval(args[1])
            EvalWriter.c_code += "}\n"
        if len(args) == 3:
            EvalWriter.c_code += f"if ({args[0]})" + "{\n"

            EvalWriter.eval(args[1])
            EvalWriter.c_code += "}\n"
            EvalWriter.c_code += "else {\n\t"
            EvalWriter.eval(args[2])
            EvalWriter.c_code += "}\n\t"

    # Procedimento para declarar variáveis
    @staticmethod
    def _assign(var, vartype, value):
        EvalWriter.symbols[var] = [vartype, value]

    # Procedimento para atribuir valores a variáveis
    @staticmethod
    def _changeValue(*args):
        var, value = args
        EvalWriter.c_code += f"{var} = {EvalWriter.eval(value)};\n\t"

    # Procedimento para ler dados do input do utilizador para uma variável
    @staticmethod
    def _leia(*args):
        for arg in args:
            if arg in EvalWriter.symbols:
                EvalWriter.c_code += f'scanf("'
                if EvalWriter.symbols[arg][0] == "int":
                    EvalWriter.c_code += "%d"
                elif EvalWriter.symbols[arg][0] == "bool":
                    EvalWriter.c_code += "%b"
                elif EvalWriter.symbols[arg][0] == "float":
                    EvalWriter.c_code += "%f"
                elif EvalWriter.symbols[arg][0] == "char*":
                    EvalWriter.c_code += "%s"
                EvalWriter.c_code += f'", &{arg});\n\t'

    # Função que faz o eval da AST, recebe a mesma e consoante o tipo de dados é encaminhado para diferentes funções
    @staticmethod
    def eval(ast):
        #print(type(ast))
        if type(ast) in (float, bool, str):
            ast2 = str(ast)
            if ast2 == "inicio":
                EvalWriter.c_code += "int main(){" + "\n\t"
            elif ast2 == "fim":
                EvalWriter.c_code += "}"
                EvalWriter.f.write(EvalWriter.c_code)
                EvalWriter.f.close()
            return ast
        if type(ast) is dict:
            return EvalWriter._eval_dict(ast)
        if type(ast) is list:
            ans = None
            for c in ast:
                ans = EvalWriter.eval(c)
            return ans
        raise Exception(f"Eval called with weird type: {type(ast)}")

    # Função que faz o eval de um dicionário
    @staticmethod
    def _eval_dict(ast):
        if "op" in ast:
            op = ast["op"]
            args = list(map(EvalWriter.eval, ast["args"]))
            if "data" in ast:
                args += ast["data"]

            if op in EvalWriter.operators:
                func = EvalWriter.operators[op]
                return func(args)
            else:
                raise Exception(f"Operador desconhecido: {op}")
        elif "var" in ast:
            return ast["var"]
        else:
            raise Exception("Weird dict on eval")
