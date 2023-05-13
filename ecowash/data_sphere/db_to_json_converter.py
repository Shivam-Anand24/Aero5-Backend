class DBToJsonConverter:
    @staticmethod
    def convert(table):
        headers = table.columns
        data = []

        for row in table.rows:
            row_data = {header: value for header, value in zip(headers, row)}
            data.append(row_data)

        return {
            'headers': headers,
            'data': data
        }