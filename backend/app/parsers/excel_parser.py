import pandas as pd


class ExcelParser:

    def parse(self, file_path):

        excel = pd.ExcelFile(file_path)

        output = []

        for sheet in excel.sheet_names:

            df = excel.parse(sheet)

            output.append(
                f"# Sheet: {sheet}\n"
            )

            output.append(
                df.to_markdown(index=False)
            )

        return "\n\n".join(output)