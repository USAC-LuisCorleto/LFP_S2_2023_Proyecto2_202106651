class Promedio:
    def promedio(self, records, keys, field):
        cadena = field.replace('"', '')
        count = 0
        large = len(records)

        if cadena not in keys:
            return "0"
        for value in keys:
            if value == cadena:
                suma = 0
                i = 0
                while large > i:
                    try:
                        suma += float(records[i][count])
                        i += 1
                    except ValueError:
                        return "No se puede promediar un string."
                if i > 0:
                    total = float(suma) / float(i)
                    return str(round(total, 2))
                else:
                    return "No es posible la división por 0"
            count += 1
        return "0"