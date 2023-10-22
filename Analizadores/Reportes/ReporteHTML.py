import os

class reportHtml:
    def __init__(self):
        pass

    def reportHTML(self, title, records, keys):
        title = title.strip('"')
        html = """<!DOCTYPE html>
                    <html lang="en">
                    <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <title>Reporte</title>

                    <!-- Bootstrap CSS -->
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

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
                    
                    </head>
                    <body>
                    <h1>""" + str(title) + """</h1>

                    <table class="table table-hover table-dark">
                    <thead>
                    <tr>"""
        for record in records:
            html += '<th>' + str(record) + '</th>'
        html += """ </tr>
                    </thead>
                    <tbody>
                    """
        for row in keys:
            html += """<tr>"""
            for column in row:
                html += """<td>""" + str(column) + """</td>"""
            html += """</tr>"""
        html += """ </tbody>
                    </table>
                    </body>
                    </html>"""
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, "exportarReporte.html")
        with open(file_path, "w+", encoding="utf-8") as archivo:
            archivo.write(html)
        abs_file_path = os.path.abspath(file_path)
        return f"\n>>> Se generó el reporte HTML: {abs_file_path}"