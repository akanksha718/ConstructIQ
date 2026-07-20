# ConstructIQ AI — Project Notes

ConstructIQ AI is an industrial knowledge platform. It accepts operational documents such as manuals, inspection reports, SOPs, spreadsheets, drawings, emails, and PDFs; turns them into searchable knowledge; and answers questions with citations back to the original documents.

## What the system does

1. An administrator uploads a document in the web application.
2. The backend stores the original file in Supabase Storage and creates a `documents` database row.
3. A background ingestion task downloads the file, extracts its text, creates chunks, and generates embeddings.
4. The ingestion pipeline extracts industrial entities (equipment tags, standards, failure modes, root causes, etc.) and their relationships.
5. Chunks, entities, and graph relationships are saved in PostgreSQL. If Neo4j is configured, they are mirrored there too.
6. When a user asks a question, the API retrieves relevant chunks, reranks them, asks Gemini for a grounded JSON response, and returns only the citations Gemini selected.

## Technology stack

| Technology | Where it is used | What it does |
| --- | --- | --- |
| Next.js 16 + React 19 + TypeScript | `frontend/` | Admin dashboard, upload workflow, asset library, chat interface, and document citations. |
| Tailwind CSS | `frontend/` | Styling for the responsive UI. |
| Clerk | Frontend and backend auth | Handles sign-in/session tokens and admin access checks. |
| FastAPI | `backend/app/main.py` | Python REST API for uploads, chat, documents, statistics, and dashboard data. |
| SQLAlchemy + PostgreSQL | `backend/app/models/` | Stores documents, chunks, entities, equipment, and relationships. |
| pgvector | `document_chunks.embedding` | Stores embeddings and enables semantic similarity search. |
| Google Gemini | `backend/app/ai/` | Produces text embeddings, extracts entities/relationships, reranks evidence, and writes grounded answers. |
| Supabase Storage | `backend/app/services/storage_service.py` | Stores uploaded source files and provides public/signed document access URLs. |
| Neo4j (optional) | `backend/app/graph/` | Mirrors documents, entities, equipment, and relationships for graph traversal and visualization. |
| Redis (optional) | `backend/app/core/redis.py` | Caches chat responses. Cache entries are automatically invalidated when a new document finishes ingestion. |
| Pydantic | API schemas/config | Validates request/response objects and reads environment settings. |

## Backend architecture

### API layer

`backend/app/main.py` creates the FastAPI app, configures CORS, and mounts routes under `/api`.

- `POST /api/upload` uploads one or more files.
- `POST /api/chat/` runs the knowledge copilot.
- `GET /api/documents` lists all uploaded assets for admins.
- `GET /api/documents/{id}/access-url` creates a usable document URL.
- `GET /api/stats` returns live document/graph totals.
- `GET /api/dashboard/recent-uploads` and `/processing-queue` supply live dashboard data.

### Upload and ingestion

`UploadService` stores the original file in Supabase and saves a document record with status `QUEUED`. It then starts `IngestWorker.process_document` in the background.

The worker changes the processing status as it progresses and marks the document as `READY` when successful or `FAILED` if an exception occurs. It always closes the database session and deletes downloaded temporary files.

`IngestionPipeline` performs the core work:

1. Selects a parser with `ParserFactory`.
2. Extracts text from PDFs, images/OCR, spreadsheets, emails, and other supported files.
3. Splits text into contextual chunks using `IndustrialChunker`.
4. Generates a Gemini embedding for each chunk and stores it in pgvector.
5. Extracts structured entities and relationships with Gemini JSON prompts.
6. Builds the PostgreSQL knowledge graph and links equipment to documents.
7. Mirrors the graph into Neo4j when Neo4j variables are configured.
8. Advances the Redis corpus version so previously cached answers are not reused after new knowledge is available.

The ingestion pipeline intentionally degrades safely: if Gemini is unavailable, chunks are still stored and can be found through keyword search.

### Retrieval, reranking, and answers

`HybridRetriever` first retrieves up to 20 candidates from pgvector. If embeddings are unavailable, `VectorSearcher` falls back to keyword matching. It also finds directly mentioned equipment from the knowledge graph.

`GeminiReranker` ranks the candidates before the LLM sees them. It has two protections:

- A local lexical/vector rank is always available as a deterministic fallback.
- Oversized chunks are truncated for the reranker prompt, avoiding a single large source exhausting the model context.

`ChatService` builds numbered context from the reranked chunks. Gemini must respond as JSON:

```json
{
  "answer": "Grounded answer text",
  "sources": [1, 3]
}
```

The backend validates the response, rejects uncited answers, deduplicates citation cards for the same document page, and computes confidence only from the source chunks Gemini selected. The frontend receives only those selected citations.

### Knowledge graph

PostgreSQL is the source of truth:

- `documents` — uploaded files and ingestion status.
- `document_chunks` — searchable text chunks and embeddings.
- `document_entities` — extracted concepts such as `EQUIPMENT`, `STANDARD`, `FAILURE_MODE`, and `ROOT_CAUSE`.
- `graph_relationships` — typed connections between entities.
- `equipment` and `equipment_documents` — equipment records connected to supporting documents.

Neo4j is an optional graph mirror. During ingestion it creates `Document`, `Equipment`, and generic `Entity` nodes plus `MENTIONS` and `RELATED_TO` edges. The API keeps working without Neo4j; it is an enhancement, not a single point of failure.

## Run locally after cloning

### 1. Prerequisites

Install these before starting:

- Python 3.11 or newer
- Node.js 20 or newer with a working npm installation
- PostgreSQL with the `vector` extension enabled
- A Supabase project and Storage bucket
- Clerk application credentials
- Gemini API key

Optional but recommended for production-like behaviour:

- Redis server
- Neo4j server

### 2. Clone and enter the repository

```bash
git clone https://github.com/akanksha718/ConstructIQ.git
cd ConstructIQ-AI
```

### 3. Configure and start the backend

Create a Python virtual environment and install dependencies:

```bash
cd backend
python -m venv .venv
```

Activate it:

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

Install packages and prepare the environment file:

```bash
pip install -r requirements.txt
copy .env.example .env
```

On macOS/Linux, use this instead of `copy`:

```bash
cp .env.example .env
```

Set real values in `backend/.env`:

```dotenv
DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@localhost:5432/constructiq
SUPABASE_URL=https://YOUR_PROJECT.supabase.co
SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVICE_ROLE_KEY
SUPABASE_BUCKET=documents
CLERK_SECRET_KEY=YOUR_CLERK_SECRET_KEY
CLERK_ISSUER=https://YOUR_APP.clerk.accounts.dev
CLERK_JWKS_URL=https://YOUR_APP.clerk.accounts.dev/.well-known/jwks.json
GEMINI_API_KEY=YOUR_GEMINI_KEY
CORS_ORIGINS=["http://localhost:3000"]

# Optional
REDIS_URL=redis://localhost:6379/0
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=YOUR_NEO4J_PASSWORD
```

Create database tables, then start FastAPI:

```bash
python create_tables.py
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Verify it at `http://127.0.0.1:8000/` and open API documentation at `http://127.0.0.1:8000/docs`.

> Note: Redis support is optional. If using it, ensure the Python `redis` package is installed in the backend environment (`pip install redis`) and that `REDIS_URL` points to a running Redis instance.

### 4. Configure and start the frontend

Open a second terminal:

```bash
cd ConstructIQ-AI/frontend
npm install
```

Create `frontend/.env.local`:

```dotenv
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=YOUR_CLERK_PUBLISHABLE_KEY
CLERK_SECRET_KEY=YOUR_CLERK_SECRET_KEY
```

Start the frontend:

```bash
npm run dev
```

Open `http://localhost:3000` in the browser, sign in with a Clerk user configured as an administrator, then upload a document from the Admin area.

## Operational checks

- Document status should move from `QUEUED` through processing stages to `READY`.
- The Dashboard should show uploaded documents and active ingestion jobs.
- The Assets page should list uploaded files and open them using a signed URL.
- A chat answer should show only sources selected by Gemini.
- If the Gemini key is absent, ingestion and keyword retrieval still work, but generated answers and semantic search are limited.

## Important production notes

- Replace `asyncio.create_task` ingestion with a durable job queue (Celery, RQ, Dramatiq, or a cloud queue) before deploying multiple API instances.
- Run PostgreSQL backups and create pgvector indexes once the corpus grows.
- Keep Supabase service-role keys and Gemini keys server-side only.
- Use a private storage bucket with signed URLs for sensitive industrial files.
- Configure HTTPS, restrictive CORS origins, structured logging, monitoring, and rate limits before public deployment.
