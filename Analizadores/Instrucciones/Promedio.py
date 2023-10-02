class Promedio:
    def promedio(self, records, keys, field):
        cadena = field.replace('"', '')
        count = 0
        large = len(records)

        for value in keys:
            if value == cadena:
                suma = 0
                i = 0
                while large<i:
                    suma += float(records[i][count])
                    i += 1
                total = float(suma)/float(i)
                return str(round(total, 2))
            count += 1
        return None