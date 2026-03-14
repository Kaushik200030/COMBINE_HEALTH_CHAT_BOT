# UnitedHealthcare Policy Chatbot

A production-ready RAG (Retrieval-Augmented Generation) chatbot for querying UnitedHealthcare commercial medical and drug policies. This system helps doctors, clinic staff, and hospital staff quickly find coverage criteria, documentation requirements, applicable procedure codes, and policy guidance from official UHC sources.

## 🆓 100% Free - No API Keys Required!

This chatbot uses **completely free, open-source components**:
- ✅ **sentence-transformers** for embeddings (local, free)
- ✅ **Ollama** or **Hugging Face** for LLM (local, free)
- ✅ **FAISS** for vector database (open-source, free)
- ✅ **Streamlit** for UI (free)
- ✅ **No OpenAI or paid APIs needed!**

See [FREE_SETUP.md](FREE_SETUP.md) for detailed setup instructions.

## 🚀 Deployment

**Ready to deploy?** See [QUICK_DEPLOY.md](QUICK_DEPLOY.md) for the fastest deployment guide!

### Deployment Options

- **Streamlit Cloud** (Easiest) - [Guide](DEPLOY_STREAMLIT_CLOUD.md)
- **Railway** (Best Performance) - [Guide](DEPLOY_RAILWAY.md)  
- **Render** (Good Free Tier) - [Guide](DEPLOY_RENDER.md)
- **Complete Guide** - [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

**Note:** For cloud deployment, use Hugging Face instead of Ollama (Ollama doesn't work on cloud platforms).

## 📋 Table of Contents

- [Features](#features)
- [Step-by-Step Usage Guide](#step-by-step-usage-guide)
- [Setup Instructions](#setup-instructions)
- [Architecture](#architecture)
  - [High-Level Design (HLD)](#high-level-design-hld)
  - [Low-Level Design (LLD)](#low-level-design-lld)
- [Data Flow](#data-flow)
- [Edge Cases Handled](#edge-cases-handled)
- [Extensibility](#extensibility)
- [Limitations](#limitations)
- [API Documentation](#api-documentation)

## ✨ Features

- **Hybrid Search RAG System**: Combines semantic (vector) and keyword (BM25) search for better retrieval
- **Source Citations**: Every answer includes references to specific policy documents
- **Confidence Scoring**: Indicates answer reliability based on similarity scores
- **Provider Abstraction**: Easy to extend to other insurance providers
- **Edge Case Handling**: Gracefully handles ambiguous queries, missing information, and outdated policies
- **Modern UI**: Clean Streamlit interface with chat history and source links

## 📖 Step-by-Step Usage Guide

### Using the Web Interface

1. **Start the Application**
   ```bash
   # Start the API server
   python main.py
   
   # In another terminal, start the Streamlit UI
   python run_streamlit.py
   ```

2. **Access the Chatbot**
   - Open your browser and navigate to `http://localhost:8501`
   - The Streamlit interface will load

3. **Ask a Question**
   - Type your question in the chat input at the bottom
   - Example questions:
     - "What does the spinal pain ablation policy say?"
     - "What procedures are covered for uterine fibroids?"
     - "What documentation is required for spinal pain ablation?"
     - "Which CPT codes are mentioned in the policy?"
     - "Is prior authorization required?"

4. **Review the Answer**
   - The chatbot will display:
     - A direct answer based on policy documents
     - Confidence level (High/Medium/Low)
     - Source citations with policy names and URLs
     - Important disclaimers

5. **Explore Sources**
   - Click on the "Sources" expander to see:
     - Policy title
     - Section name
     - Effective date
     - Direct link to the source document

6. **Use Example Questions**
   - Click on example questions in the sidebar to quickly test the system

### Using the API Directly

```bash
# Query the API
curl -X POST "http://localhost:8000/api/chat/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What does the spinal pain ablation policy say?"}'
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.11 or higher
- **No API keys required!** Uses 100% free, open-source models
- Internet connection (for initial data ingestion and model downloads)

### Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd COMBINE_HEALTH_CHAT_BOT
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Free LLM (Choose One)**

   **Option A: Ollama (Recommended - Easiest)**
   ```bash
   # Install Ollama from https://ollama.ai
   # Then download a model:
   ollama pull llama3.2
   
   # Start Ollama (runs in background)
   ollama serve
   ```

   **Option B: Hugging Face (Completely Local)**
   ```bash
   # Models will download automatically on first use
   # No additional setup needed!
   ```

5. **Configure Environment (Optional)**
   ```bash
   # Create .env file if you want to customize settings
   # See .env.example for options
   # Defaults work out of the box!
   ```

**📖 For detailed free setup instructions, see [FREE_SETUP.md](FREE_SETUP.md)**

5. **Ingest Policy Data**
   ```bash
   # Option 1: Scrape and ingest policies (takes time)
   python scripts/ingest_data.py --limit 10  # Start with 10 policies for testing
   
   # Option 2: Load existing processed data
   python scripts/ingest_data.py --load-existing
   ```

6. **Start the Application**
   ```bash
   # Terminal 1: Start API server
   python main.py
   
   # Terminal 2: Start Streamlit UI
   python run_streamlit.py
   ```

### Docker Deployment

```bash
# Build the image
docker build -t insurance-chatbot .

# Run the container
docker run -p 8000:8000 -p 8501:8501 \
   # No API keys needed - uses free local models!
  insurance-chatbot
```

## 🏗️ Architecture

### High-Level Design (HLD)

The system follows a 4-layer RAG architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Layer                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Streamlit Chat UI                            │   │
│  │  - User interface                                    │   │
│  │  - Chat history                                      │   │
│  │  - Source citations                                  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Retrieval + Reasoning Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Retriever  │→ │   Embedder   │→ │ Answer Service│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                   │              │
│         └──────────────────┴───────────────────┘              │
│                            │                                  │
│                            ▼                                  │
│                   ┌──────────────┐                            │
│                   │  Vector DB   │                            │
│                   │   (FAISS)    │                            │
│                   └──────────────┘                            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Processing Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Scraper    │→ │   Parser     │→ │   Chunker    │     │
│  │  (UHC Site)  │  │ (PDF/HTML)   │  │  (Text Split)│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Ingestion Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Provider   │  │   Document   │  │   Metadata   │     │
│  │   Loader     │  │   Downloader  │  │  Extractor   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

**Layer Responsibilities:**

1. **Data Ingestion Layer**: Crawls UHC policy pages, downloads documents, extracts metadata
2. **Processing Layer**: Parses PDFs/HTML, chunks documents, generates embeddings
3. **Retrieval + Reasoning Layer**: Vector search, context retrieval, LLM-based answer generation
4. **Frontend Layer**: User interface, chat interaction, source display

### Low-Level Design (LLD)

#### Project Structure

```
insurance-chatbot/
│
├── app/
│   ├── api/                    # FastAPI endpoints
│   │   ├── __init__.py
│   │   ├── chat.py            # Chat query endpoint
│   │   ├── ingest.py          # Data ingestion endpoint
│   │   └── health.py          # Health check
│   │
│   ├── core/                   # Core configuration
│   │   ├── __init__.py
│   │   ├── config.py          # Settings management
│   │   ├── logger.py          # Logging setup
│   │   └── prompts.py         # LLM prompts
│   │
│   ├── ingestion/              # Data ingestion
│   │   ├── __init__.py
│   │   ├── base_provider.py   # Provider abstraction
│   │   ├── uhc_provider.py    # UHC implementation
│   │   ├── scraper.py         # Main scraper
│   │   ├── pdf_parser.py      # PDF parsing
│   │   ├── html_parser.py    # HTML parsing
│   │   └── chunker.py         # Text chunking
│   │
│   ├── retrieval/              # Retrieval system
│   │   ├── __init__.py
│   │   ├── embedder.py        # Embedding generation
│   │   ├── vectordb.py        # FAISS vector DB
│   │   ├── keyword_search.py  # BM25 keyword search
│   │   └── retriever.py       # Hybrid retrieval logic
│   │
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── policy_service.py  # Main service
│   │   └── answer_service.py  # Answer generation
│   │
│   └── ui/                     # Frontend
│       ├── __init__.py
│       └── streamlit_app.py   # Streamlit UI
│
├── data/                       # Data storage
│   ├── raw/                    # Raw documents
│   ├── processed/              # Processed chunks
│   └── index/                  # Vector DB files
│
├── scripts/
│   └── ingest_data.py          # Data ingestion script
│
├── main.py                     # FastAPI entry point
├── run_streamlit.py            # Streamlit entry point
├── requirements.txt            # Dependencies
├── Dockerfile                  # Docker config
└── README.md                   # This file
```

#### Key Components

**1. Provider Abstraction (`base_provider.py`)**
- Abstract base class for insurance providers
- Enables easy extension to other providers (Aetna, Cigna, etc.)
- Methods: `fetch_index()`, `fetch_document()`, `parse_document()`, `extract_metadata()`

**2. Vector Database (`vectordb.py`)**
- FAISS-based vector store
- Stores embeddings with metadata
- Supports similarity search with threshold filtering
- Persistent storage on disk

**3. Retrieval System (`retriever.py`)**
- **Hybrid Search**: Combines semantic (vector) and keyword (BM25) search
- Weighted combination of semantic and keyword scores (configurable alpha)
- Metadata filtering support
- Top-K retrieval with combined scoring

**4. Keyword Search (`keyword_search.py`)**
- BM25 algorithm for keyword-based retrieval
- Tokenization and term frequency analysis
- Complements semantic search for better recall

**4. Answer Generation (`answer_service.py`)**
- LLM-based answer synthesis
- Context-aware responses
- Source citation extraction
- Confidence scoring

**5. Chunking Strategy (`chunker.py`)**
- Sentence-aware chunking
- Configurable chunk size and overlap
- Section-aware chunking for structured documents

#### Data Flow

```
1. User Query
   │
   ▼
2. Hybrid Search:
   ├─ Semantic: Query Embedding (sentence-transformers) → Vector Search (FAISS)
   └─ Keyword: BM25 Search (Term Matching)
   │
   ▼
3. Combine Results (Weighted Score)
   │
   ▼
4. Retrieve Top-K Chunks
   │
   ▼
5. Format Context for LLM
   │
   ▼
6. Generate Answer (GPT-4o-mini)
   │
   ▼
7. Extract Sources & Citations
   │
   ▼
8. Return Response to User
```

#### Ingestion Flow

```
1. Scrape UHC Policy Index
   │
   ▼
2. Download Policy Documents (PDF/HTML)
   │
   ▼
3. Parse Documents (Extract Text + Structure)
   │
   ▼
4. Chunk Documents (Sentence-aware)
   │
   ▼
5. Generate Embeddings (sentence-transformers - free, local)
   │
   ▼
6. Store in Vector DB (FAISS)
   │
   ▼
7. Save Metadata (JSON)
```

## 🔄 Data Flow

### Query Processing Flow

1. **User Input**: User submits a question via Streamlit UI or API
2. **Query Embedding**: Question is converted to embedding vector using sentence-transformers (free, local)
3. **Vector Search**: FAISS searches for similar document chunks
4. **Context Retrieval**: Top-K most relevant chunks are retrieved
5. **Answer Generation**: Free LLM (Ollama or Hugging Face) synthesizes answer from retrieved context
6. **Source Extraction**: Policy sources and metadata are extracted
7. **Response Formatting**: Answer, sources, and disclaimers are formatted
8. **User Display**: Response is shown with citations and confidence score

### Data Ingestion Flow

1. **Index Scraping**: UHC policy index page is scraped for policy listings
2. **Document Download**: Policy documents (PDFs/HTML) are downloaded
3. **Parsing**: Documents are parsed to extract text and structure
4. **Metadata Extraction**: Policy metadata (dates, codes, categories) is extracted
5. **Chunking**: Documents are split into smaller chunks with overlap
6. **Embedding**: Chunks are converted to embeddings using sentence-transformers (free, local)
7. **Storage**: Embeddings and metadata are stored in FAISS vector database

## 🛡️ Edge Cases Handled

### 1. Question Not Found
- **Scenario**: User asks about a procedure not in the policy database
- **Handling**: Bot returns a clear message indicating no relevant policy was found
- **Response**: Suggests checking exact procedure name or consulting UHC portal directly

### 2. Ambiguous Service Names
- **Scenario**: Query matches multiple different policies
- **Handling**: Bot identifies ambiguity and lists relevant policy candidates
- **Response**: Asks user to refine query with specific codes or conditions

### 3. Prior Authorization Confusion
- **Scenario**: User asks about prior authorization requirements
- **Handling**: Bot clearly states that prior auth requirements are maintained separately
- **Response**: Directs user to separate prior-authorization resources

### 4. Old vs Current Policy
- **Scenario**: Multiple policy versions exist for the same procedure
- **Handling**: System prioritizes most recent effective date
- **Response**: Shows effective date in source citations

### 5. Clinical Advice Prevention
- **Scenario**: User asks for medical advice
- **Handling**: Bot includes disclaimers that policies are informational only
- **Response**: States that treating physicians remain responsible for care decisions

### 6. Coverage Determination
- **Scenario**: User asks "Is this definitely covered?"
- **Handling**: Bot explains coverage depends on member-specific benefit plans
- **Response**: Includes disclaimer about benefit plan documents overriding policy

### 7. Low Confidence Answers
- **Scenario**: Retrieved chunks have low similarity scores
- **Handling**: Bot indicates low confidence and suggests verification
- **Response**: Shows confidence level and recommends checking sources

## 🔧 Extensibility

The system is designed for easy extension to other insurance providers:

### Adding a New Provider

1. **Create Provider Class**
   ```python
   from app.ingestion.base_provider import BaseProviderLoader
   
   class AetnaProviderLoader(BaseProviderLoader):
       def __init__(self):
           super().__init__(
               provider_name="Aetna",
               base_url="https://www.aetna.com"
           )
       
       def fetch_index(self):
           # Implement Aetna-specific scraping
           pass
       
       # Implement other abstract methods
   ```

2. **Update Configuration**
   ```python
   # In config.py, add provider settings
   aetna_base_url = "https://www.aetna.com"
   ```

3. **Use in Scraper**
   ```python
   scraper = Scraper(provider_loader=AetnaProviderLoader())
   ```

### Provider Metadata Schema

Each provider's documents are stored with consistent metadata:
- `provider_name`: Insurance provider name
- `policy_title`: Policy document title
- `policy_type`: Commercial, Medicare, etc.
- `effective_date`: Policy effective date
- `published_date`: Publication date
- `procedure_codes`: CPT/HCPCS codes
- `source_url`: Original document URL
- `section_name`: Document section

This schema enables:
- Multi-provider queries
- Provider-specific filtering
- Unified retrieval across providers

## ⚠️ Limitations

1. **Data Dependency**: System depends on publicly available UHC policy documents. If documents are removed or changed, the system needs re-ingestion.

2. **Not Medical Advice**: The chatbot provides policy information only. It does not provide medical advice, and coverage decisions depend on member-specific benefit plans.

3. **Prior Authorization**: Prior authorization requirements are maintained separately by UHC and may not be fully captured in policy documents.

4. **Coverage Variability**: Actual coverage depends on:
   - Member-specific benefit plan documents
   - State regulations
   - Plan type (commercial, Medicare, etc.)
   - Individual plan provisions

5. **Real-time Updates**: Policy updates may not be immediately reflected. Regular re-ingestion is recommended.

6. **LLM Performance**: Free local models (Ollama/Hugging Face) may be slower than paid APIs, but work completely offline with no costs.

7. **Scraping Limitations**: Web scraping may break if UHC changes their website structure. Regular monitoring is needed.

8. **Model Size**: Hugging Face models require significant disk space (2-7GB). Ollama models are more efficient.

## 📡 API Documentation

### Chat Endpoint

**POST** `/api/chat/query`

Query the policy database.

**Request Body:**
```json
{
  "question": "What does the spinal pain ablation policy say?",
  "filters": {
    "provider_name": "UnitedHealthcare",
    "procedure_code": "64625"
  }
}
```

**Response:**
```json
{
  "answer": "According to UHC policy...",
  "sources": [
    {
      "policy_title": "Ablative Treatment for Spinal Pain",
      "source_url": "https://...",
      "effective_date": "02/01/2026",
      "section_name": "Coverage",
      "procedure_codes": ["64625", "64628"]
    }
  ],
  "confidence": "high",
  "disclaimer": "Note: This information..."
}
```

### Ingestion Endpoint

**POST** `/api/ingest/start`

Start policy ingestion process.

**Request Body:**
```json
{
  "limit": 10,
  "provider": "UHC"
}
```

### Health Check

**GET** `/api/health`

Returns system health and vector database statistics.

## 📝 License

This project is created for the CombineHealth technical assignment.

## 👤 Author

[Your Name]

---

**Note**: This chatbot is designed to assist healthcare providers in understanding UHC policies. It should not be used as a substitute for consulting official UHC resources or member-specific benefit documents.
