# logic_lexer.py
import ply.lex as plex


# Classe referente ao lexer e às linguagens utilizadas para ler o ficheiro em pseudocódigo Portugol
class LogicLexer:

    # Tokens por divisões

    start_end = ("inicio", "fim")
    bools = ("true", "false")
    comparators_logic = ("not", "and", "or", "xor")
    comparators_numbers = ("leq", "geq", "dif")
    cycles = ("para", "de", "ate", "faca","fimpara", "enquanto", "fimenquanto")
    conditionals = ("se", "senao", "entao", "fimse")
    io = ("escreva", "leia")
    functions = ("funcao", "fimfuncao")

    keywords = start_end + bools + comparators_logic + comparators_numbers + cycles + conditionals + io + functions

    tokens = keywords + ("var", "vartype", "assign", "nr", "string")
    literals = "()+-<>!=/*;[],:"
    t_ignore = " \t\n"

    # Método com expressão regular do comentário
    def t_comment(self, t):
        r"""\#.*"""
        pass

    # Método com expressão regular capaz de ler um valor de string
    def t_string(self, t):
        r'"[^"]*"'
        t.value = t.value[1:-1]
        return t

    # Método com expressão regular capaz de ler um valor de número inteiro ou real
    def t_nr(self, t):
        r"""[0-9]+(\.[0-9]+)?"""
        t.value = float(t.value)
        return t

    # Método com expressão regular capaz de ler os diferentes tipos de variáveis
    def t_vartype(self, t):
        r"""inteiro
            |caracter
            |logico
            |real"""
        return t

    # Método com expressão regular capaz de ler o sinal de atruibuição de valores a variaveis em Portugol
    def t_assign(self, t):
        r"""<-"""
        return t

    # Método com expressão regular capaz de ler o simbolo de lower or equal (leq) (menor ou igual)
    def t_leq(self, t):
        r""""<="""
        return t

    # Método com expressão regular capaz de ler o simbolo de greater or equal (geq) (maior ou igual)
    def t_geq(self, t):
        r""">="""
        return t

    # Método com expressão regular capaz de ler o simbolo de diferente (dif)
    # (o símbolo de igual lógico ficou designado como '=', não sendo necessária uma expressão regular para o mesmo)
    def t_dif(self, t):
        r"""!="""
        return t

    # Método com expressão regular capaz de ler todos os tipos de keywords presentes no lexer
    def t_keywords(self, t):
        r"""[a-z]+"""
        # No caso da palavra não estar nas keywords, então assume-se como o nome de uma variável
        t.type = t.value if t.value in self.keywords else "var"
        return t

    # Método de controlo de erros no lexer
    def t_error(self, t):
        raise Exception(f"Unexpected token {t.value[:10]}")

    # Método inicializador da classe com o seu atributo lex inicializado
    def __init__(self):
        self.lex = plex.lex(module=self)

    # Método de execução do lexer no documento
    def token(self):
        return self.lex.token()







