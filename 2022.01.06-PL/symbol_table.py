class SymbolTable:
    def __init__(self):
        self._data = {} #dicionário de simbolos



    # permitir que self._data[key] armazene mais que um valor (variáveis temporárias)
    def re_set(self, key, value):
        if key in self._data:
            self._data[key][-1].append(value)
        else:
            self[key][-1] = value  # reutiliza setitem
            # ou
             # self._data[key] = value

    #y = table["x"]
    def __getitem__(self, item):
        if item in self._data:
            return self._data[item][-1]
        else:
            raise Exception(f"{item} não existe na tabela de símbolos")


    #table["x"] = 10
    def __setitem__(self, key, value):
        if key in self._data:
            self._data[key][-1] = value # key ja existe ou seja array ja existe, adiciona no ultimo
        else:
            self._data[key] = [value] # key não existe ou seja array não existe, criar

    # del table["y"]
    def __delitem__(self, key):
        if key in self._data: #se key existir em data
            if len(self._data[key]) == 1: #só existe um valor
                del self._data[key]
            else: #há mais que um valor
                self._data[key].pop() #remove ultimo valor da lista
                #ou
                #self._data[key].pop(-1)
        else:
            raise Exception(f"{key} not found.")


    # confirmar se item está em data
    def __contains__(self, item):
        return item in self._data



