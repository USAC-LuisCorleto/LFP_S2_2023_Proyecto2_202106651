class Max:
    def max(self, records, keys, field):
        cadena = field.replace('"', '')
        count = 0
        max = 0
        large = len(records)

        for value in keys:
            if value == cadena:
                i = 0
                while large>i:
                    if float(records[i][count]) > max:
                        max = float(records[i][count])
                    i += 1
                return str(max)
            count += 1
        return None