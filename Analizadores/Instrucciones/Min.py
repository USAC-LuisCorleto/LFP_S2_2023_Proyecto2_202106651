class Min:
    def min(self, records, keys, field):
        cadena = field.replace('"', '')
        count = 0
        min = float('inf')
        large = len(records)

        for value in keys:
            if value == cadena:
                i = 0
                while large>i:
                    if float(records[i][count]) < min:
                        min = float(records[i][count])
                    i += 1
                return str(min)
            count += 1
        return None