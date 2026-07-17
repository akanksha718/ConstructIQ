"""Optional Neo4j client.

Neo4j is a nice-to-have mirror of the Postgres knowledge graph. It is entirely
optional: if the driver isn't installed or ``NEO4J_URI`` isn't configured,
``Neo4jClient.enabled()`` is ``False`` and callers skip graph mirroring.
"""

from __future__ import annotations

import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class Neo4jClient:

    def __init__(self) -> None:
        self.driver = None
        if not settings.NEO4J_URI:
            return
        try:
            from neo4j import GraphDatabase

            self.driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
            )
        except Exception:  # pragma: no cover - optional dependency
            logger.exception("Failed to init Neo4j driver; skipping.")
            self.driver = None

    def enabled(self) -> bool:
        return self.driver is not None

    def execute(self, query: str, **params) -> None:
        if self.driver is None:
            return
        try:
            with self.driver.session() as session:
                session.run(query, params)
        except Exception:  # pragma: no cover - network
            logger.exception("Neo4j query failed.")

    def close(self) -> None:
        if self.driver is not None:
            self.driver.close()
