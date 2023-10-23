class Promedio:
    def promedio(self, records, keys, field):
        cadena = field.replace('"', '')
        count = keys.index(cadena) if cadena in keys else -1

        if count == -1:
            return "0"

        suma = 0
        i = 0
        for record in records:
            try:
                suma += float(record[count])
                i += 1
            except ValueError:
                return "No se puede promediar un string."

        if i == 0:
            return "No es posible la división por 0"

        total = suma / i
        return str(round(total, 2))
