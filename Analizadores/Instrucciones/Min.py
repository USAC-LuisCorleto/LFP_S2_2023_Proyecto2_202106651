class Min:
    def min(self, records, keys, field):
        field = field.replace('"', '')

        try:
            index = keys.index(field)
        except ValueError:
            return None

        min_value = min(float(record[index]) for record in records)
        return str(min_value)
