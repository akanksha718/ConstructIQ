from dataclasses import dataclass


@dataclass
class Chunk:

    text: str

    page: int

    heading: str

    section: str

    metadata: dict