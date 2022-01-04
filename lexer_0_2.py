# lexer.py
# Documento que contém a parte léxica do projeto

import ply.lex as lex

# Dados feitos da classe a partir do exercício aula:    2021.12.17 - PL
class PortugolLexer:

    # Por fazer tokens específicas
    estruturas = ("enquanto", "logico", "caracter", "inteiro", "real", "para", "se")

    # Copiado do exemplo stor, ver porquê
    t_ignore = " \t\n"

    # Função inicializadora do objeto
    def __init__(self):
        self.lex = lex.lex(module=self)

    # Função com expressão regular capaz de ler comentários
    def t_comentario(self, t):
        r"\#.*"
        pass

    def t_atribuir(self, t):
        r"<-"
        return t

    def t_identificador(self, t):
        r"([A-Z]|[a-z])(([a-z]|[0-9])+)?"
        return t

    def t_declaracao(self, t):
        r"inteiro|caracter|real|logico"
        return t

    def t_valor_string(self, t):
        r'"[^"]*"'
        return t

    def t_valor_num(self, t):
        r"[0-9]+(\.[0-9]+)?"
        return t

    # Função para controlo de erros
    def t_error(self, t):
        raise Exception(f"Unexpected token: {t.value[:10]}")

    def token(self):
        return self.lex.token()
