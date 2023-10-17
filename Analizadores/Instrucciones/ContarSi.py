class ContarSi:
    def contarSi(self, records, keys, field, value):
        field = field.replace('"', '')
        
        try:
            index = keys.index(field)
        except ValueError:
            return None
        
        count = sum(1 for record in records if str(record[index]) == str(value).replace('"', ''))
        return str(count)
