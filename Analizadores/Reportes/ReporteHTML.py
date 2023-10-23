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
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <title>Reporte</title>
                    
                    <style>
                        body {
                            margin: 0;
                            padding: 0;
                            font-family: Arial, sans-serif;
                            background-color: #f2f2f2;
                        }

                        header {
                            background-color: #333;
                            color: #fff;
                            text-align: center;
                            padding: 20px;
                        }

                        h1 {
                            font-size: 24px;
                        }

                        table {
                            width: 80%;
                            margin: 20px auto;
                            background-color: #fff;
                            border-collapse: collapse;
                            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
                        }

                        th, td {
                            text-align: center;
                            padding: 12px;
                            border: 1px solid #ddd;
                        }

                        th {
                            background-color: #333;
                            color: #fff;
                        }

                        tr:nth-child(even) {
                            background-color: #f2f2f2;
                        }
                    </style>
                    </head>
                    <body>
                    <header>
                        <h1>""" + str(title) + """</h1>
                    </header>
                    
                    <table>
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