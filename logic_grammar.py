# logic_grammar.py

import ply.yacc as pyacc
from pprint import PrettyPrinter

from logic_lexer import LogicLexer
from logic_eval_interpreter import LogicEvalInterpreter
from logic_eval_writer import LogicEvalWriter


# Classe referente à gramática utilizada na interpretação do pseudocódigo em Portugol
class LogicGrammar:

    # Lista de precedências com as operações por ordem de prioridade
    precedence = (

        ("left", "or", "xor"),  # menor prioridade
        ("left", "and"),

        ("left", "<", ">"),

        ("left", "+", "-"),
        ("left", "*", "/"),
        ("right", "uminus")

    )

    # Método com mensagens de controlo de erros inesperados
    def p_error(self, p):
        if p:
            raise Exception(f"Parse Error: Unexpected token '{p.type}'")
        else:
            raise Exception("Parse Error: Expecting token")

    # Método com a regra inicial da gramática implementada, sendo que pode haver funções declaradas acima do "main" (no caso do Portugol, é o início)
    def p_portugol(self, p):
        """portugol : func_list ';' inicio code"""
        p[0] = [p[1]] + [p[3]] + [p[4]]

    # Método com outra via da regra inicial da gramática implementada, sem funções previamente declaradas
    def p_portugol2(self, p):
        """portugol : inicio code"""
        p[0] =  [p[1]] + [p[2]]

    # Método com a regra de ler funções ou múltiplas funções
    def p_func_list(self, p):
        """func_list : func
                    | func_list ';' func"""
        # Dependendo do tamanho do p, irá interpretar de forma diferente
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1]
            p[0].append(p[3])

    # Método com a regra de leitura de declaração e implementação função
    def p_func(self, p):
        """ func : funcao var '(' args ')' com_list ';' fimfuncao """
        p[0] = {
            "op": "funcao",
            "args": [],
            "data": [p[2], p[4], p[6]]
        }

    # Método com a regra de leitura de código, sendo que esta regra assume apenas 1 estrutura de código
    def p_code1(self, p):
        """ code : s """
        p[0] = [p[1]]

    # Método com a regra de leitura de código, sendo que esta regra assume múltiplas estrutura de código
    def p_code2(self, p):
        """ code : code ';' s  """
        p[0] = p[1] + [p[3]]

    # Método com a regra de definição de fim do "main" ou continuação de código
    def p_s(self, p):
        """ s : comando
              | fim"""
        p[0] = p[1]

    # Método com a regra de leitura do ciclo for() em Portugol
    def p_ciclo(self, p):
        """ ciclo : para var de e ate e faca com_list ';' fimpara """
        p[0] = {
            "op": "para",
            "args": [p[2], p[4], p[6]],
            "data": [p[8]],
        }

    # Método com a regra de leitura do ciclo while() em Portugol
    def p_ciclo2(self,p):
        """ciclo : enquanto n faca com_list ';' fimenquanto"""
        p[0] = {
            "op": "enquanto",
            "args": [],
            "data": [p[2], p[4]]
        }

    # Método com a regra de leitura de comandos, sendo estes atribuição de valores a variaveis ou criação de ciclos
    def p_comando1(self, p):
        """ comando : e
                    | ciclo """
        p[0] = p[1]

    # Método com a regra de leitura de declaração de variáveis
    def p_comando2(self, p):
        """ comando : var assign e """
        p[0] = {"op": "assign", "args": [p[1], p[3]]}

    # Método com a regra de leitura do print() em Portugol
    def p_comando3(self, p):
        """ comando : escreva '(' e_list ')' """
        p[0] = {"op": "escreva", "args": p[3]}

    # Método com a regra de leitura do input() em Portugol
    def p_comando4(self, p):
        """ comando : leia '(' var_list ')' """
        p[0] = {"op": "leia", "args":  p[3]}

    # Método com a regra de leitura de declaração de múltiplas variáveis
    def p_comando5(self, p):
        """ comando : vartype ':' var_list """
        p[0] = {"op": "declarar",
                "args": p[3],
                "data": [p[1]]}

    # Método com a regra de leitura do if() -> else() em Portugol
    def p_comando6(self, p):
        """comando : se e entao com_list ';' senao com_list ';' fimse"""
        p[0] = {"op": "se",
                "args": [p[2]],
                "data": [p[4], p[7]]}

    # Método com a regra de leitura do if() em Portugol
    def p_comando7(self, p):
        """comando : se e entao com_list ';' fimse"""
        p[0] = {"op": "se",
                "args": [p[2]],
                "data": [p[4]]}

    # Método com a regra de definição de múltiplos comandos (ciclos e declarações) ou apenas 1 comando
    def p_com_list(self, p):
        """ com_list : comando
                     | com_list ';' comando """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1]
            p[0].append(p[3])

    # Método com a regra de leitura de valores ou operações, ou conjuntos destes
    def p_e_list(self, p):
        """ e_list : e
                   | e_list ',' e """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    #  Método com regra de leitura de variável como um valor
    def p_e1(self, p):
        """ e : var """
        p[0] = {'var': p[1]}

    #  Método com regra de leitura de valores, strings ou operações dentro de parêntesis
    def p_e2(self, p):
        """ e : '(' e ')' """
        p[0] = p[2]

    #  Método com regra de leitura de valores como bool, número (ou operações) ou strings
    def p_e3(self, p):
        """ e : b
              | n
              | string"""
        p[0] = p[1]

    #  Método com regra de leitura de chamar uma função (com ou  sem parâmetros)
    def p_e4(self, p):
        """ e : var '(' e_list ')'
              | var '(' ')' """
        p[0] = {"op": "call",
                "args": [],
                "data": [p[1], [] if p[3] == ")" else p[3]]}

    #  Método com regra de leitura de um número sendo positivo ou negativo
    def p_n1(self, p):
        """ n : nr
              | '-' e  %prec uminus  """
        p[0] = p[1] if len(p) == 2 else {"op": "-", "args": [0.0, p[2]]}

    #  Método com regra de leitura de um número ou operação entre parêntesis
    def p_n2(self, p):
        """ n : '(' n ')' """
        p[0] = p[2]

    # Método com regra de leitura de uma operação matemática
    def p_n3(self, p):
        """ n : e '+' e
              | e '-' e
              | e '*' e
              | e '/' e """
        p[0] = dict(op=p[2], args=[p[1], p[3]])

    # Método com regra de leitura de uma operação "comparadora"
    def p_n4(self, p):
        """n : e '<' e
              | e leq e
              | e '>' e
              | e geq e
              | e '=' e
              | e dif e"""
        p[0] = dict(op=p[2], args=[p[1], p[3]])

    # Método com regra de leitura de um booleano ou expressão lógica booleana
    def p_b1(self, p):
        """ b : f
              | e or e
              | e and e
              | e xor e """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = dict(op=p[2], args=[p[1], p[3]])

    # Método com regra de leitura de um boolean true
    def p_f1(self, p):
        """ f : true """
        p[0] = True

    # Método com regra de leitura de um boolean false
    def p_f2(self, p):
        """ f : false """
        p[0] = False

    # Método com regra de leitura de um boolean not <boolean>
    def p_f3(self, p):
        """ f : not f """
        p[0] = dict(op="not", args=[p[2]])

    # Método com regra de leitura de uma variável ou várias
    def p_var_list(self, p):
        """ var_list : var
                     | var_list ',' var """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1]
            p[0].append(p[3])

    # Método com regra de leitura de args para serem utilizados numa função
    def p_args(self, p):
        """ args :
                 | var_list """
        p[0] = p[1] if len(p) == 2 else []

    # Método inicializador da classe com os seus atributos declarados
    def __init__(self):
        self.lexer = LogicLexer()
        self.tokens = self.lexer.tokens
        self.yacc = pyacc.yacc(module=self)

    # Método de execução do Parse do texto no documento alvo (Exercução do funcionamento do Grammar)
    def parse(self, expression, output):
        ans = self.yacc.parse(lexer=self.lexer.lex, input=expression)
        pp = PrettyPrinter()
        pp.pprint(ans) #remover, apenas para debug!
        if output == "interpreter":
            return LogicEvalInterpreter.eval(ans)
        elif output == "writer":
            return LogicEvalWriter.eval(ans)


