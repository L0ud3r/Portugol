# symbol_table.py

class SymbolTable:
    def __init__(self):
        self._data = {} #dicionário de simbolos



    # re_set permite que self._data[key] armazene mais que um valor (variáveis temporárias)
    def re_set(self, key, value): #TODO testar várias utilizações do re_set para verificar se está mesmo a funcionar como deve
        if key in self._data:
            self._data[key][-1].append(value)
        else:
            self[key][-1] = value  # reutiliza setitem
            # ou
             # self._data[key] = value

    # __getitem__ retorna um item caso exista no dicionário self._data -> var = dictionary[key]
    def __getitem__(self, item):
        if item in self._data:
            return self._data[item][-1]
        else:
            raise Exception(f"{item} não existe na tabela de símbolos")


    # __setitem__ possibilita atribuir um valor -> dict[key] = value
    def __setitem__(self, key, value):
        if key in self._data:
            self._data[key][-1] = value #key ja existe ou seja array ja existe, adiciona no ultimo
        else:
            self._data[key] = [value] # key não existe ou seja array não existe, criar

    # __delitem__ possibilita apagar tudo o que esteja "dentro" de uma key
    # caso apenas exista um valor, é apagada a key e os seus valores
    # caso existam vários valores, á apagado o último da lista
    def __delitem__(self, key):
        if key in self._data: #se key existir em data
            if len(self._data[key]) == 1:           #só existe um valor
                del self._data[key]                 #apaga key e o que está dentro dela
            else:                                   #há mais que um valor
                self._data[key].pop()               #remove ultimo valor da lista
        else:
            raise Exception(f"{key} not found.")


    # __contains__ permite verificar se um item está em self._data
    def __contains__(self, item):
        return item in self._data



