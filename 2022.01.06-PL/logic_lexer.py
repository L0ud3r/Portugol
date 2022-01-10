# logic_lexer.py
import ply.lex as plex


class LogicLexer:
    #TODO organizar
    keywords = ("inicio", "true", "false", "not", "and", "or", "xor", "leq", "geq", "dif", "para", "de", "ate", "faca", "fimpara", "enquanto", "fimenquanto", "se", "senao", "entao", "fimse", "escreva", "leia", "funcao", "fimfuncao", "fim")
    tokens = keywords + ("var", "vartype", "assign", "nr", "string")
    literals = "()+-<>!=/*;[],:"
    t_ignore = " \t\n"

    def t_comment(self, t):
        r"""\#.*"""
        pass

    def t_string(self, t):
        r'"[^"]*"'
        t.value = t.value[1:-1]
        return t

    def t_nr(self, t):
        r"""[0-9]+(\.[0-9]+)?"""
        t.value = float(t.value)
        return t

    def t_vartype(self, t):
        r"""inteiro
            |caracter
            |logico
            |real"""
        return t

    def t_assign(self, t):
        r"""<-"""
        return t

    def t_leq(self,t ):
        r""""<="""
        return t

    def t_geq(self, t):
        r""">="""
        return t

    def t_dif(self, t):
        r"""!="""
        return t

    def t_keywords(self, t):
        r"""[a-z]+"""
        t.type = t.value if t.value in self.keywords else "var"
        return t

    def t_error(self, t):
        raise Exception(f"Unexpected token {t.value[:10]}")

    def __init__(self):
        self.lex = plex.lex(module=self)

    def token(self):
        return self.lex.token()







