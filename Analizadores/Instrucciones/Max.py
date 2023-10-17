class Max:
    def max(self, records, keys, field):
        field = field.replace('"', '')
        
        try:
            index = keys.index(field)
        except ValueError:
            return None
        
        max_value = max(float(record[index]) for record in records)
        return str(max_value)
