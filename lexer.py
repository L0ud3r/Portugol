# lexer.py
# Documento que contém a parte léxica do projeto

import ply.lex as lex


# Dados feitos da classe a partir do exercício aula:    2021.12.17 - PL
class PortugolLexer:

    # keys por dividir
    keywords = ("Inicio", "Fim", "se", "para", "de", "passo", "enquanto", "fim_se", "fim_para", "fim_enquanto",
                "escreva", "leia")
    tipoVariavel = ( "inteiro", "real", "logico", "caracter")
    # tokens a parte de keywords tendo em conta os acentos + operacoes com mais de 1 caracter de simbolo
    tokens = ("entao" ,"senao", "ate", "faca", "nao", "dif", "maiorIgual", "menorIgual", "nomeVariavel",
              "assign", "valorString", "valorNumero") + keywords + tipoVariavel
    literals = "()+/-*<>;,[]="

    # Copiado do exemplo stor, ver porquê
    t_ignore = " \t\n"

    # Função inicializadora do objeto
    def __init__(self):
        self.lex = lex.lex(module=self)

    def t_entao(self, t):
        r"""então"""
        return t

    def t_senao(self, t):
        r"""senão"""
        return t

    def t_ate(self, t):
        r"""até"""
        return t

    def t_faca(self, t):
        r"""faça"""
        return t

    def t_nao(self, t):
        r"""não"""
        return t

    def t_dif(self, t):
        r"""!="""
        return t

    def t_maiorIgual(self, t):
        r""">="""
        return t

    def t_menorIgual(self, t):
        r"""<="""
        return t

    def t_assign(self, t):
        r"""<-"""
        return t

    def t_valorString(self, t):
        r'''"[^"]+"'''
        # Retirar as aspas da string lida
        t.value = t.value[1:-1]
        return t

    def t_valorNumero(self, t):
        r"""\-?[0-9]+(\.[0-9]+)?"""
        t.value = float(t.value)
        return t

    def t_keywords(self, t):
        # POR TESTAR
        r"""[^\s]+"""

        if t.value in self.keywords:
            t.type = t.value
        else:
            t.type = "nomeVariavel"

        return t

    # Função para controlo de erros
    def t_error(self, t):
        raise Exception(f"Unexpected token: {t.value[:10]}")

    def token(self):
        return self.lex.token()
