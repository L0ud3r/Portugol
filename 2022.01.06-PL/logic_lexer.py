# logic_lexer.py
import ply.lex as plex


class LogicLexer:
    keywords = ("true", "false", "not", "and", "or", "xor", "para", "de", "ate", "faca", "fimpara", "escreva", "leia", "fun", "endfun")
    tokens = keywords + ("var", "assign", "nr", "string")
    literals = "()+-/*;[],"
    t_ignore = " \t\n"

    def t_comment(self, t):
        r"""\#.*"""
        pass

    #def t_ellipsis(self, t):
    #    r"""\.{3}"""
    #    return t

    def t_string(self, t):
        r'"[^"]*"'
        t.value = t.value[1:-1]
        return t

    def t_nr(self, t):
        r"""[0-9]+(\.[0-9]+)?"""
        t.value = float(t.value)
        return t

    def t_assign(self, t):
        r"""<-"""
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







