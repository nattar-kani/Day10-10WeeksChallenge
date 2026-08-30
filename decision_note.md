# Database Decision Note — LLM Chat Application

## SQL

Use SQL when the application requires structured relational data,
strong consistency, constraints, transactions, complex joins, and
analytical queries.

Examples:
- Users
- Billing
- Feedback
- Usage analytics
- Transactional data

## MongoDB

Use MongoDB when data is naturally document-oriented, nested, or
expected to evolve frequently.

Examples:
- Conversation documents
- Message metadata
- Flexible application metadata
- JSON-like API data

MongoDB can reduce the need to split naturally nested data across
multiple relational tables.

## Vector Database

Use a vector database when the application needs semantic similarity
search over embeddings.

Examples:
- RAG document retrieval
- Semantic search
- Similarity search
- Finding relevant chunks for an LLM

## They can work together

SQL, MongoDB, and a vector database solve different problems.

A production LLM application may use:

SQL/MongoDB
    → application and transactional data

Vector DB
    → embedding storage and semantic retrieval

LLM
    → generation using the retrieved context

## Decision

For the core transactional layer, SQL is a strong choice when the
data has well-defined relationships and requires consistency.

MongoDB is a strong choice when conversation data is naturally
document-oriented and the schema needs flexibility.

A vector database should be added when semantic retrieval or RAG
is required.

The choice should therefore be driven by the access pattern and
data requirements rather than choosing one database for everything.