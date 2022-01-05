# logic_grammar.py
import ply.yacc as yacc
from lexer import PortugolLexer
# fazer import ao eval


# Ideias tiradas de Aulas 2021.11.22 - D, 2021.11.24 - D e 2021.12.17-PL
class PortugolGrammar:

    # adicionar precedentes?

    def __init__(self):
        self.lexer = PortugolLexer()
        self.tokens = self.lexer.tokens
        # self.yacc = pyacc.yacc(module=self)

    def parse(self, expression):
        ans = self.yacc.parse(lexer=self.lexer.lex, input=expression)
        # return LogicEval.eval(ans)

    # Fazer recursividades descendentes

    def p_error(self, p):
        if p:
            raise Exception(f"Parse Error: Token inesperada: {p.type[:10]}")
        else:
            raise Exception("Parse Erro: Expecting token")

    def p_PORTUGOL(self, p):
        """ PORTUGOL : Inicio INICIO """
        p[0] = p[1] + p[2]

    def p_INICIO(self, p):
        """ INICIO : DECLARACAO | Fim """
        p[0] = p[1]

    def p_DECLARACAO(self, p):
        """ DECLARACAO : tipoVariavel ':' DECLARACAO2 ';' CODE """
        p[0] = p[1] + p[3] + p[5]

    def p_DECLARACAO2v1(self, p):
        """ DECLARACAO2 : nomeVariavel """
        p[0] = p[1]

    def p_DECLARACAO2v2(self, p):
        """ DECLARACAO2 : nomeVariavel ',' DECLARACAO2 """
        p[0] = p[1] + p[3]

    def p_CODE(self, p):
        """ CODE : CODE2
                 | Fim"""
        p[0] = p[1]

    def p_CODE2(self, p):
        """ CODE2 : ATRIBUICAO
                  | CONDICAO
                  | CICLO
                  | IO """
        p[0] = p[1]

    def p_ATRIBUICAO(self, p):
        """ ATRIBUICAO : nomeVariavel assign VALUE ';' CODE """
        p[0] = dict(op = "assign", args = [p[1], p[3], p[4]])


    def p_VALUE(self, p):
        """ VALUE : EXP
                  | STR
                  | BOOL """
        p[0] = p[1]

    def p_EXP(self, p):
        """ EXP : valorNumero """
        p[0] = p[1]

    def p_EXP2(self, p):
        """EXP : VALUE '+' VALUE
               | VALUE '-' VALUE
               | VALUE '/' VALUE
               | VALUE '*' VALUE
               | VALUE '<' VALUE
               | VALUE '>' VALUE
               | VALUE menorIgual VALUE
               | VALUE maiorIgual VALUE
               | VALUE dif VALUE
               | VALUE '=' VALUE"""
        p[0] = dict(op=p[2], args=[p[1], p[3]])

    def p_STR(self, p):
        """ STR : valorString """
        p[0] = p[1]

    def p_BOOL(self, p):
        """ BOOL : TNF
                 | VALUE e VALUE
                 | VALUE ou VALUE """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = dict(op = p[2], args = [p[1] ,p[3]])

    def p_TNF(self, p):
        """ TNF : True
                | False """
        p[0] = p[1]

    def p_TNF2(self, p):
        """ TNF : nao TNF """
        p[0] = dict(op = "nao", args = [p[2]])

    def p_CONDICAO(self, p):
        """ CONDICAO : se VALUE CODE CODICAO2 """
        p[0] = dict(op = "se", args = [p[2], p[3], [4]])

    def p_CODICAO2(self, p):
        """ CODICAO2 : fim_se CODE """
        p[0] = p[1] + p[2]

    def p_CONDICAO2v1(self, p):
        """ CONDICAO2 : SENAO"""
        p[0] = p[1]

    def p_SENAO(self, p):
        """ senao CODE fim_se CODE """
        ...

    def p_CICLO(self, p):
        """ CICLO : FOR | WHILE """
        ...

    def p_FOR(self, p):
        """ para ATRIBUICAO ate valorNumero faca CODE2 fim_para """
        ...

    def p_WHILE(self, p):
        """ enquanto ... entao CODE fim_enquanto """
        ...






















