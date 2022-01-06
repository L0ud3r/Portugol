# grammar.py
import ply.yacc as pyacc
from lexer import PortugolLexer
from eval import LogicEval
# fazer import ao eval


# Ideias tiradas de Aulas 2021.11.22 - D, 2021.11.24 - D e 2021.12.17-PL
class PortugolGrammar:

    # adicionar precedentes?

    precedence = (
        ("left", "+", "-"), #menos prioridade
        ("left", "*", "/"),
        ("left", "ou"),
        ("left", "e"), #mais prioridade
    )

    def __init__(self):
        self.lexer = PortugolLexer()
        self.tokens = self.lexer.tokens
        self.yacc = pyacc.yacc(module=self)

    def parse(self, expression):
        ans = self.yacc.parse(lexer=self.lexer.lex, input=expression)
        return LogicEval.eval(ans)

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
        """ INICIO : DECLARACAO
                    | Fim """
        p[0] = p[1]

    def p_DECLARACAO(self, p):
        """ DECLARACAO : TIPOVARIAVEL ':' DECLARACAO2 ';' CODE """
        p[0] = p[1] + p[3] + p[5]

    def p_TIPOVARIAVEL(self, p):
        """TIPOVARIAVEL : inteiro
                        | real
                        | logico
                        | caracter"""
        p[0] = p[1]

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
                  | BOOL
                  | nomeVariavel"""
        p[0] = p[1]

    def p_EXP(self, p):
        """ EXP : valorNumero """
        p[0] = p[1]

    def p_EXP2(self, p): # testar se é possivel fazer por exemplo "3 + 4 + 4"
        """EXP : VALUE '+' VALUE
               | VALUE '-' VALUE
               | VALUE '/' VALUE
               | VALUE '*' VALUE
               | VALUE '<' VALUE
               | VALUE '>' VALUE
               | VALUE menorIgual VALUE
               | VALUE maiorIgual VALUE
               | VALUE diferente VALUE
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
        """ TNF : verdadeiro
                | falso """
        p[0] = p[1]

    def p_TNF2(self, p):
        """ TNF : nao TNF """
        p[0] = dict(op = "nao", args = [p[2]])

    def p_CONDICAO(self, p):
        """ CONDICAO : se VALUE CODE2 CONDICAO2 """
        p[0] = dict(op = "se", args = [p[2], p[3], [4]])

    def p_CODICAO2v1(self, p):
        """ CONDICAO2 : fim_se CODE """
        p[0] = p[1] + p[2]

    def p_CONDICAO2v2(self, p):
        """ CONDICAO2 : SENAO"""
        p[0] = p[1]

    def p_SENAO(self, p):
        """ SENAO : senao CODE2 fim_se CODE """
        p[0] = dict(op = "senao", args = [p[2], p[4]])

    def p_CICLO(self, p):
        """ CICLO : FOR
                    | WHILE """
        p[0] = p[1]

    def p_FOR(self, p):
        """ FOR : para ATRIBUICAO de VALUE ate VALUE passo valorNumero faca CODE2 fim_para CODE""" #aqui podem entrar bools em VALUE!
        p[0] = dict(op="para", args = [p[2], p[4], p[6], p[8]])

    def p_WHILE(self, p):
        """ WHILE : enquanto VALUE entao CODE2 fim_enquanto CODE"""
        p[0] = dict(op="enquanto", args = [p[2], p[4], p[6]])

    def p_IO(self, p):
        """ IO : LEIA """
    #            | ESCREVA"""
        p[0] = p[1]

    def p_LEIA(self,p): #HANDLE THIS!
        """LEIA : leia '(' nomeVariavel ')' ';' CODE"""
        p[0] = dict(op="leia", args=[p[3], p[6]])

    #def p_ESCREVA(self, p):
        #"""ESCREVA: escreva '('nomeVariavel')'';' CODE""" FIX!!
        #p[0]
        ...
