from email import policy
from email.parser import BytesParser


class EmailParser:

    def parse(self, file_path):

        with open(file_path, "rb") as f:

            msg = BytesParser(
                policy=policy.default
            ).parse(f)

        text = f"""
Subject:
{msg['subject']}

From:
{msg['from']}

To:
{msg['to']}

Date:
{msg['date']}

Body:

{msg.get_body(preferencelist=('plain')).get_content()}
"""

        return text