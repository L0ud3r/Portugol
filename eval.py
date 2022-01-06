# eval.py

class LogicEval:

    operators = {
        "ou": lambda args: args[0] or args[1],
        "e": lambda args: args[0] and args[1],
        "nao": lambda a: not a[0],

        "+": lambda args: args[0] + args[1],
        "-": lambda args: args[0] - args[1],
        "*": lambda args: args[0] * args[1],
        "/": lambda args: args[0] / args[1],

        "assign": lambda a: LogicEval._assign(*a),
        "escreva": lambda a: print(*a)

        #FALTA MUITA COISA!
    }

    @staticmethod
    def _assign(var, value):
        LogicEval.symbols[var] = value


    @staticmethod
    def eval(ast):
        if type(ast) in (float, bool, str):
            return ast
        #if type(ast) is dict:
            #return LogicEval._eval_dict(ast)
        #if type(ast) is list:
          #  ans = None
           # for c in ast:
            #    ans = LogicEval._eval_dict(c)
           # return ans
        #raise Exception(f"Eval called with weird type: {type(ast)}")


