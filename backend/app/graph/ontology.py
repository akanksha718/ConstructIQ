import re


class Ontology:

    @staticmethod
    def normalize_equipment(tag):

        tag = tag.upper()

        tag = re.sub(

            r"[^A-Z0-9]",

            "",

            tag,

        )

        return tag