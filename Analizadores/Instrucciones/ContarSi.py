class ContarSi:
    def contarSi(self, records, keys, field, value):
        cadena = field.replace('"', '')
        count = 0
        large = len(records)
        for value in keys:
            if str(value) == str(cadena):
                suma = 0
                i = 0
                while large>i:
                    if records[i][count] == str(value).replace('"', ''):
                        suma += 1
                    i += 1
                return str(suma)
            count += 1
        return None