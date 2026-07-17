from langchain_text_splitters import RecursiveCharacterTextSplitter


class IndustrialChunker:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=1200,

            chunk_overlap=250,

            separators=[

                "\n# ",

                "\n## ",

                "\n### ",

                "\n",

                ". ",

                " ",

            ],
        )

    def create_chunks(self, markdown: str):

        chunks = self.splitter.create_documents(

            [markdown]

        )

        return chunks