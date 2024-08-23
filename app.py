import os
import dotenv
import pathway as pw
from pathway.stdlib.ml.index import KNNIndex
from pathway.xpacks.llm.embedders import OpenAIEmbedder
from pathway.xpacks.llm.llms import OpenAIChat, prompt_chat_single_qa

dotenv.load_dotenv()

class DocumentInputSchema(pw.Schema):
    doc: str


class QueryInputSchema(pw.Schema):
    query: str
    user: str


def run(
    api_key: str = os.getenv("OPENAI_API_KEY", ""),
    host: str = os.getenv("PATHWAY_REST_CONNECTOR_HOST", "0.0.0.0"),
    port: int = int(os.getenv("PATHWAY_REST_CONNECTOR_PORT", "8080")),
    embedder_locator: str = "text-embedding-ada-002",
    embedding_dimension: int = 1536,
    model_locator: str = "gpt-3.5-turbo",
    max_tokens: int = 500,
    temperature: float = 0.0,
):
  
    embedder = OpenAIEmbedder(
        api_key=api_key,
        model=embedder_locator,
        retry_strategy=pw.udfs.FixedDelayRetryStrategy(),
        cache_strategy=pw.udfs.DefaultCache(),
    )

   
    documents = pw.io.jsonlines.read(
        "pathway-docs.json",
        schema=DocumentInputSchema,
        mode="streaming",
        autocommit_duration_ms=50,
    )


    enriched_documents = documents + documents.select(vector=embedder(pw.this.doc))

    index = KNNIndex(
        enriched_documents.vector, enriched_documents, n_dimensions=embedding_dimension
    )

  
    query, response_writer = pw.io.http.rest_connector(
        host=host,
        port=port,
        schema=QueryInputSchema,
        autocommit_duration_ms=50,
        delete_completed_queries=True,
    )


    query += query.select(vector=embedder(pw.this.query))


    query_context = query + index.get_nearest_items(
        query.vector, k=3, collapse_rows=True
    ).select(documents_list=pw.this.doc)


    @pw.udf
    def build_prompt(documents, query):
        docs_str = "\n".join(documents)
        prompt = f"Given the following documents:\n{docs_str}\n\nAnswer this query:\n{query}"
        return prompt


    prompt = query_context.select(
        prompt=build_prompt(pw.this.documents_list, pw.this.query)
    )

 
    model = OpenAIChat(
        api_key=api_key,
        model=model_locator,
        temperature=temperature,
        max_tokens=max_tokens,
        retry_strategy=pw.udfs.FixedDelayRetryStrategy(),
        cache_strategy=pw.udfs.DefaultCache(),
    )


    responses = prompt.select(
        query_id=pw.this.id, result=model(prompt_chat_single_qa(pw.this.prompt))
    )


    response_writer(responses)


    pw.run()

if __name__ == "__main__":
    run()
