# my_utils.py

# "Utilitários" - funções que são úteis para a execução do nosso código residem neste documento
# são repetidas diversas vezes e, por isso, são definidas aqui e chamadas onde for necessário.


#Função slurp serve para abrir um ficheiro e ler os seus conteúdos
#Retorna os conteúdos lidos
def slurp(filename):
    with open(filename, "rt") as fh:
        contents = fh.read()
    return contents