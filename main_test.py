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

intent = "project_details"
query = "Give me the details of Hourly Bucket projects which were signed off in 2022."
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
    return [val["table_name"] for val in examples]


tables = table_selector(target_table_list, query=query, lambda_mult=0.1, k=5)
print(f'tables============={tables}')
temp_table_list = get_related_tables(list(set(tables)), original_table_list=target_table_list)
print(f'temp_table_list==================={temp_table_list}')


# final_table_list = table_selector(temp_table_list, k=4, lambda_mult=1, search_type="similarity")
# print(f'final_table_list=================={final_table_list}')

# LuceneSearch
# def create_collection(table_list):
#     documents = list()
#
#     for i in range(0, len(table_list)):
#         document = dict()
#         document["id"] = f'doc{i + 1}'
#         document["contents"] = \
#             [table["table_description"] for table in table_names if table['table_name'] == table_list[i]][0]
#         documents.append(document)
#
#     print(f'documents========={documents}')
#
#     directory = "collection_json_array"
#     if not os.path.exists(directory):
#         os.mkdir(directory)
#
#     json_object = json.dumps(documents, indent=4)
#
#     with open(f"{directory}/documents.json", "w") as outfile:
#         outfile.write(json_object)
#
#
# create_collection(temp_table_list)


# def create_index():
#     input_directory_path = 'collection_json_array'
#     index_path = 'indexes/collection_json_array'
#     cmd = f'python -m pyserini.index.lucene \
#   --collection JsonCollection \
#   --input {input_directory_path} \
#   --index {index_path} \
#   --generator DefaultLuceneDocumentGenerator'
#     subprocess.check_output(cmd, shell=True)
#
#
# create_index()


# def search(query: str):
#     searcher = LuceneSearcher("indexes/collection_json_array")
#     # searcher.set_bm25(k1=0.5, b=0.9)
#     hits = searcher.search(query)
#     for i in range(len(hits)):
#         # print(hits[i].docid)
#         print(f'{i + 1:2} {hits[i].docid:4} {hits[i].score:.5f}')


# search(query)

# rank_bm25
# def search(table_list, query):
#     corpus = ["".join(example['table_description']) for example in table_names if example['table_name'] in
#               table_list]
#     print(corpus)
#     tokenized_corpus = [doc.split(" ") for doc in corpus]
#     bm25 = BM25(tokenized_corpus)
#     tokenized_query = query.split(" ")
#     doc_scores = bm25.get_top_n(tokenized_query, corpus, n=4)
#     print(doc_scores)
#
#
# search(temp_table_list, query)

def rerank(table_list: list, query: str):
    # if len(table_list) < 6:
    #     output = table_list
    #     return output
    output = list()
    ranker = Ranker(model_id="ms-marco-MiniLM-L-12-v2")
    tokenizer = Tokenizer(model_id="ms-marco-MiniLM-L-12-v2")
    reranker = ReRankPipeline(ranker=ranker, tokenizer=tokenizer)

    documents = list()
    for i in range(0, len(table_list)):
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


final_table_list = rerank(temp_table_list, query)
print(f'final_table_list==============={final_table_list}')
# rerank(temp_table_list, query)

# temp_table_list = rerank(target_table_list, query)
# print(f'temp_table_list==================={temp_table_list}')
# final_table_list = get_related_tables(list(set(temp_table_list)), original_table_list=target_table_list)
# print(f'final_table_list==============={final_table_list}')
