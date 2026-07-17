from app.retrieval.query_analyzer import QueryAnalyzer
from app.retrieval.vector_search import VectorSearcher
from app.retrieval.graph_search import GraphSearcher
from app.retrieval.metadata_search import MetadataSearcher
from app.retrieval.reranker import ResultReranker
from app.retrieval.context_builder import ContextBuilder
from app.retrieval.citation_service import CitationService


class HybridRetriever:

    def __init__(self, db):

        self.db = db

    def retrieve(

        self,

        question: str,

    ):

        analysis = QueryAnalyzer.analyze(

            question

        )

        graph = GraphSearcher(

            self.db

        ).search(

            analysis.equipment

        )

        vectors = VectorSearcher.search(

            question

        )

        metadata = MetadataSearcher(

            self.db

        ).search(

            analysis

        )

        ranked = ResultReranker.rerank(

            graph,

            vectors,

            metadata,

        )

        context = ContextBuilder.build(

            ranked

        )

        citations = CitationService.build(

            ranked

        )

        return {

            "context": context,

            "citations": citations,

        }