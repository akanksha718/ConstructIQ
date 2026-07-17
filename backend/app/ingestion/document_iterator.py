from docling_core.types.doc import DoclingDocument


class DocumentIterator:

    @staticmethod
    def iterate(document: DoclingDocument):

        chunks = []

        for item in document.iterate_items():

            chunks.append(item)

        return chunks