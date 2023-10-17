import os

class reportMistakes():
    def __init__(self):
        pass

    def reportMistakes(self, mistakesTable):
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
                    <h1 style="text-align: center;">Reporte de Errores</h1>
                    &nbsp;                    

                    <table class="table table-hover table-dark">
                    <thead>
                    <tr style="height: 18px;">
                    <th><strong>Error</strong></th>
                    </tr>
                    </thead>
                    <tbody>
                    """

        for error in mistakesTable:
            
            html += """<tr style="height: 18px;">
                    <td>""" + str(error).replace("<", "&#60;").replace(">", "&#62;") +"""</span></td>
                    </tr>"""
        html += """ 
                </tbody>
                </table>
                <p>&nbsp;</p>
        """
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, "Errores.html")
        with open(file_path, "w+", encoding="utf-8") as archivo:
            archivo.write(html)
        abs_file_path = os.path.abspath(file_path)
        return f"\n>>> Se generó el reporte HTML: {abs_file_path}"