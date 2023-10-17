class Suma:
    def sumar(self, records, keys, field):
        field = field.replace('"', '')

        try:
            index = keys.index(field)
        except ValueError:
            return None

        suma = 0
        for record in records:
            try:
                suma += float(record[index])
            except (ValueError, TypeError):
                return "No se pueden sumar valores no numéricos."

        return str(round(suma, 2))

