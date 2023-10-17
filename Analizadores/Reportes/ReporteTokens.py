import os

class reportTokens:
    def __init__(self):
        pass

    def reportTokens(self, tokensTable):
        html =  """<!doctype html>
                    <html lang="en">
                    <head>
                    <!-- Required meta tags -->
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

                    <!-- Bootstrap CSS -->
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
                    <style>
                        body {
                            margin: 20px;
                            background-color: #2E2E2E; 
                        }

                        h1 {
                            text-align: center;
                            margin-bottom: 20px;
                            color: #FFFFFF;
                        }

                        table {
                            height: 108px;
                            width: 60%;
                            border-collapse: collapse;
                            margin-left: auto;
                            margin-right: auto;
                        }

                        th, td {
                            height: 18px;
                            text-align: center;
                            padding: 8px;
                        }
                    </style>
                    <title>Reportes</title>
                    </head>
                    <body>
                
                    &nbsp;
                    <h1 style="text-align: center;">Reporte de Tokens</h1>
                    &nbsp;                 

                    <table class="table table-hover table-dark">
                    <thead>
                    <tr style="height: 18px;">
                    <th><strong>Token</strong></th>
                    <th><strong>Tipo</strong></th>
                    <th><strong>Linea</strong></th>
                    <th><strong>Columna</strong></th>
                    </tr>
                    </thead>
                    <tbody>
                    """
        for token in tokensTable:
            html += """<tr style="height: 18px;">
                    <td>""" + str(token.lexeme) +"""</span></td>
                    <td>""" + str(token.type) +"""</td>
                    <td>""" + str(token.row) +"""</td>
                    <td>""" + str(token.column) +"""</td>
                    </tr>"""
        html += """ 
                </tbody>
                </table>
                <p>&nbsp;</p>
        """
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, "Reporte Tokens.html")
        with open(file_path, "w+", encoding="utf-8") as archivo:
            archivo.write(html)
        abs_file_path = os.path.abspath(file_path)
        return f"\n>>> Se generó el reporte HTML: {abs_file_path}"