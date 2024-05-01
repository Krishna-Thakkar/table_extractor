from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.example_selectors import MaxMarginalRelevanceExampleSelector, SemanticSimilarityExampleSelector
import os
import json
from pyserini.search.lucene import LuceneSearcher
from rank_bm25 import BM25
from swiftrank import Ranker, Tokenizer, ReRankPipeline
import subprocess

from get_specific_table_list import intent_table_selector
from get_referenced_tables import get_related_tables
from table_list import table_names

intent = "team_details"
query = "Who all are fully free today?"
target_table_list = []
for table_intent_pair in intent_table_selector:
    if table_intent_pair['intent'] == intent:
        target_table_list = table_intent_pair['table_names']
        print(f'target_table_list==============={target_table_list}')
embeddings = HuggingFaceEmbeddings(model_name="WhereIsAI/UAE-Large-V1")
print(len(table_names))


def table_selector(table_list, query: str, k: int = 3, lambda_mult: float = 1, fetch_k: int = 5,
                   search_type: str = "mmr"):
    # print(f'table_list======={table_list}')
    to_vectorize = ["".join(example['table_description']) for example in table_names if example['table_name'] in
                    table_list]
    # print(f'to_vectorize======{to_vectorize}')
    metadata = [example for example in table_names if example['table_name'] in table_list]
    # print(f'metadata========{metadata}')

    vectorstore = Chroma.from_texts(
        to_vectorize, embeddings,
        metadatas=metadata
    )
    if search_type.lower() == "mmr":
        example_selector = MaxMarginalRelevanceExampleSelector(
            vectorstore=vectorstore,
            k=k,
            fetch_k=fetch_k,
            lambda_mult=lambda_mult
        )
    else:
        example_selector = SemanticSimilarityExampleSelector(
            vectorstore=vectorstore,
            k=k,
        )
    examples = example_selector.select_examples(
        input_variables={"query": f"{query}"})
    vectorstore.delete_collection()
    return [val['table_name'] for val in examples]


tables = table_selector(target_table_list, query=query, lambda_mult=0.1, k=3)
print(f'tables============={tables}')
temp_table_list = get_related_tables(list(set(tables)), original_table_list=target_table_list)
print(f'temp_table_list==================={temp_table_list}')


def rerank(table_list: list, query: str):
    output = list()
    ranker = Ranker(model_id="ms-marco-MiniLM-L-12-v2")
    tokenizer = Tokenizer(model_id="ms-marco-MiniLM-L-12-v2")
    reranker = ReRankPipeline(ranker=ranker, tokenizer=tokenizer)

    docs_name = list()
    docs_desc = list()
    docs_tkw = list()
    docs_rkw = list()

    for i in range(0, len(table_list)):
        for table in table_names:
            if table['table_name'] == table_list[i]:
                for key, val in table.items():
                    doc_name = dict()
                    doc_desc = dict()
                    doc_tkw = dict()
                    doc_rkw = dict()
                    doc_name["id"] = doc_desc["id"] = doc_tkw["id"] = doc_rkw["id"] = i
                    document["contents"] = \
                        [" ".join(table.values()) for table in table_names if table['table_name'] == table_list[i]][0]
                    documents.append(document)
        document = dict()
        document["id"] = i
        document["contents"] = \
            [" ".join(table.values()) for table in table_names if table['table_name'] == table_list[i]][0]
        documents.append(document)
    # print(documents)
    for mapping in reranker.invoke(
            query=query, contexts=documents, key=lambda x: x['contents']
    ):
        # print(mapping)
        index = int(mapping['context']['id'])
        output.append(table_list[index])
    return output[:5]