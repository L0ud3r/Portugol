# logic_grammar.py
import ply.yacc as pyacc
from pprint import PrettyPrinter

from logic_lexer import LogicLexer
from logic_eval import LogicEval

#TODO: INICIO E FIM
# Booleanos
# Comparadores (<, >, <=, >=, =)
# and, or, xor
# Se e senao!
# While
# Remover comentários de funções antigas / comentários desnecessários (no fim)
# Remover debug prints
# Documentação


class LogicGrammar:
    precedence = (
        ("left", "+", "-"),
        ("left", "*", "/"),
        ("right", "uminus"),
        ("left", "or", "xor"),   # menor prioridade
        ("left", "and"),
    )

    def p_error(self, p):
        if p:
            raise Exception(f"Parse Error: Unexpected token '{p.type}'")
        else:
            raise Exception("Parse Error: Expecting token")

    def p_code1(self, p):
        """ code : s """
        p[0] = [p[1]]

    def p_code2(self, p):
        """ code : code ';' s  """
        p[0] = p[1] + [p[3]]
    #

    #antigo for
    #def p_ciclo(self, p):
    #    """ ciclo : for var '[' e ellipsis e ']' com_list ';' endfor """
    #    p[0] = {
    #        "op": "for",
    #        "args": [p[2], p[4], p[6]],
    #        "data": [p[8]],
    #    }

    #novo for (para)
    def p_ciclo(self, p):
        """ ciclo : para var de e ate e faca com_list ';' fimpara """
        p[0] = {
            "op": "para",
            "args": [p[2], p[4], p[6]],
            "data": [p[8]],
        }

    #antiga funcao
    #def p_func(self, p):
    #    """ func : fun var '(' args ')' com_list ';' endfun """
    #    p[0] = {
    #        "op": "fun",
    #        "args": [],
    #        "data": [p[2], p[4], p[6]]
    #    }

    #novo fun (funcao)
    def p_func(self, p):
        """ func : funcao var '(' args ')' com_list ';' fimfuncao """
        p[0] = {
            "op": "funcao",
            "args": [],
            "data": [p[2], p[4], p[6]]
        }
    #

    def p_comando1(self, p):
        """ comando : e
                    | ciclo """
        p[0] = p[1]

    def p_comando2(self, p):
        """ comando : var assign e """
        p[0] = {"op": "assign", "args": [p[1], p[3]]}

    # antigo say
    #def p_comando3(self, p):
    #    """ comando : say e_list """
    #    p[0] = {"op": "say", "args": p[2]}


    # novo say (escreva Portugol)
    def p_comando3(self, p):
        """ comando : escreva '(' e_list ')' """
        p[0] = {"op": "escreva", "args": p[3]}


    #antigo read
    #def p_comando4(self,p):
    #    """ comando : read var_list """
    #    p[0] = {"op": "read", "args":  p[2]}

    #novo read (leia Portugol)
    def p_comando4(self, p):
        """ comando : leia '(' var_list ')' """
        p[0] = {"op": "leia", "args":  p[3]}

    def p_comando5(self, p):
        """ comando : vartype ':' var_list """
        p[0] = {"op": "declarar",
                "args": p[3],
                "data": [p[1]]}

    #comando if -> fim de if | else...
    def p_comando6(self, p):
        """ comando : se e entao com_list ';' fimse """
        p[0] = {"op": "se",
                "args": [p[2]],
                "data": [p[4]]}

    #

    def p_s(self, p):
        """ s : func
              | comando
              | fim"""
        p[0] = p[1]

    #

    def p_e_list(self, p):
        """ e_list : e
                   | e_list ',' e """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]
    #

    def p_n1(self, p):
        """ n : nr
              | '-' e  %prec uminus  """
        p[0] = p[1] if len(p) == 2 else {"op": "-", "args": [0.0, p[2]]}

    def p_n2(self, p):
        """ n : e '+' e
              | e '-' e
              | e '*' e
              | e '/' e """
        p[0] = dict(op=p[2], args=[p[1], p[3]])

    #

    def p_b1(self, p):
        """ b : f
              | e or e
              | e and e
              | e xor e """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = dict(op=p[2], args=[p[1], p[3]])

    #

    def p_f1(self, p):
        """ f : true """
        p[0] = True

    def p_f2(self, p):
        """ f : false """
        p[0] = False

    def p_f3(self, p):
        """ f : not f """
        p[0] = dict(op="not", args=[p[2]])

    #

    def p_e1(self, p):
        """ e : var """
        p[0] = {'var': p[1]}

    def p_e2(self, p):
        """ e : '(' e ')' """
        p[0] = p[2]

    def p_e3(self, p):
        """ e : b
              | n
              | string """
        p[0] = p[1]

    def p_e4(self, p):
        """ e : var '(' e_list ')'
              | var '(' ')' """
        p[0] = {"op": "call",
                "args": [],
                "data": [p[1], [] if p[3] == ")" else p[3]]}
                 ###  [ factorial, [4.0, 5.0, 6.0]]
    #

    def p_com_list(self, p):
        """ com_list : comando
                     | com_list ';' comando """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1]
            p[0].append(p[3])

    #

    def p_var_list(self, p):
        """ var_list : var
                     | var_list ',' var """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1]
            p[0].append(p[3])

    #

    def p_args(self, p):
        """ args :
                 | var_list """
        p[0] = p[1] if len(p) == 2 else []

    def __init__(self):
        self.lexer = LogicLexer()
        self.tokens = self.lexer.tokens
        self.yacc = pyacc.yacc(module=self)

    def parse(self, expression):
        ans = self.yacc.parse(lexer=self.lexer.lex, input=expression)
        pp = PrettyPrinter()
        #pp.pprint(ans) #remover, apenas para debug!
        return LogicEval.eval(ans)




