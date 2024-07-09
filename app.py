import os
import dotenv
import pathway as pw
from pathway.stdlib.ml.index import KNNIndex
from pathway.xpacks.llm.embedders import OpenAIEmbedder
from pathway.xpacks.llm.llms import OpenAIChat, prompt_chat_single_qa

# Load environment variables
dotenv.load_dotenv()

# Define document schema
class DocumentInputSchema(pw.Schema):
    doc: str

# Define query schema
class QueryInputSchema(pw.Schema):
    query: str
    user: str

# Function to run the application
def run(
    api_key: str = os.getenv("OPENAI_API_KEY", ""),
    host: str = os.getenv("PATHWAY_REST_CONNECTOR_HOST", "0.0.0.0"),
    port: int = int(os.getenv("PATHWAY_REST_CONNECTOR_PORT", "8080")),
    embedder_locator: str = "text-embedding-ada-002",
    embedding_dimension: int = 1536,
    model_locator: str = "gpt-3.5-turbo",
    max_tokens: int = 60,
    temperature: float = 0.0,
):
    # Initialize OpenAI Embedder
    embedder = OpenAIEmbedder(
        api_key=api_key,
        model=embedder_locator,
        retry_strategy=pw.udfs.FixedDelayRetryStrategy(),
        cache_strategy=pw.udfs.DefaultCache(),
    )

    # Example: Reading documents from JSON Lines file
    documents = pw.io.jsonlines.read(
        "pathway-docs.json",
        schema=DocumentInputSchema,
        mode="streaming",
        autocommit_duration_ms=50,
    )

    # Example: Embedding documents
    enriched_documents = documents + documents.select(vector=embedder(pw.this.doc))

    # Example: Creating KNN index
    index = KNNIndex(
        enriched_documents.vector, enriched_documents, n_dimensions=embedding_dimension
    )

    # Example: Setting up query handler with REST connector
    query, response_writer = pw.io.http.rest_connector(
        host=host,
        port=port,
        schema=QueryInputSchema,
        autocommit_duration_ms=50,
        delete_completed_queries=True,
    )

    # Example: Embedding queries
    query += query.select(vector=embedder(pw.this.query))

    # Example: Combining query with document context
    query_context = query + index.get_nearest_items(
        query.vector, k=3, collapse_rows=True
    ).select(documents_list=pw.this.doc)

    # Example: Building prompt for template
    @pw.udf
    def build_prompt(documents, query):
        docs_str = "\n".join(documents)
        prompt = f"Given the following documents:\n{docs_str}\n\nAnswer this query:\n{query}"
        return prompt

    # Example: Constructing prompt using template
    prompt = query_context.select(
        prompt=build_prompt(pw.this.documents_list, pw.this.query)
    )

    # Example: Initializing OpenAI Chat model
    model = OpenAIChat(
        api_key=api_key,
        model=model_locator,
        temperature=temperature,
        max_tokens=max_tokens,
        retry_strategy=pw.udfs.FixedDelayRetryStrategy(),
        cache_strategy=pw.udfs.DefaultCache(),
    )

    # Example: Generating response from GPT-3.5 Turbo based on prompt
    responses = prompt.select(
        query_id=pw.this.id, result=model(prompt_chat_single_qa(pw.this.prompt))
    )

    # Example: Writing responses back
    response_writer(responses)

    # Run the Pathway application
    pw.run()

if __name__ == "__main__":
    run()
