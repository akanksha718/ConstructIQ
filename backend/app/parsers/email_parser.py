"""Email (.eml) parsing using the standard library."""

from __future__ import annotations

import logging
from email import policy
from email.parser import BytesParser

logger = logging.getLogger(__name__)


class EmailParser:

    def parse(self, file_path: str) -> str:
        try:
            with open(file_path, "rb") as fh:
                msg = BytesParser(policy=policy.default).parse(fh)
        except Exception:
            logger.exception("Failed to parse email %s", file_path)
            return ""

        body = ""
        try:
            part = msg.get_body(preferencelist=("plain", "html"))
            if part is not None:
                body = part.get_content()
        except Exception:
            body = ""

        return (
            f"Subject: {msg['subject'] or ''}\n"
            f"From: {msg['from'] or ''}\n"
            f"To: {msg['to'] or ''}\n"
            f"Date: {msg['date'] or ''}\n\n"
            f"{body}"
        ).strip()
