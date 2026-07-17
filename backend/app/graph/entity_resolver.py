import re


class EntityResolver:

    @staticmethod
    def normalize(value: str) -> str:
        value = value.upper().strip()
        value = re.sub(r"\s+", " ", value)
        return value