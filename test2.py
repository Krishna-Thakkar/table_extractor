from langchain_community.embeddings import HuggingFaceEmbeddings
from swiftrank import Ranker, Tokenizer, ReRankPipeline

from get_specific_table_list import intent_table_selector
from get_referenced_tables import get_related_tables
from table_list import table_names

intent = "asset_details"
query = "Who has the Realme-C3?"
target_table_list = []
for table_intent_pair in intent_table_selector:
    if table_intent_pair['intent'] == intent:
        target_table_list = table_intent_pair['table_names']
        print(f'target_table_list==============={target_table_list}')
embeddings = HuggingFaceEmbeddings(model_name="WhereIsAI/UAE-Large-V1")
print(len(table_names))


def rerank(table_list: list, query: str, k: int):
    ranker = Ranker(model_id="ms-marco-MiniLM-L-12-v2")
    tokenizer = Tokenizer(model_id="ms-marco-MiniLM-L-12-v2")
    reranker = ReRankPipeline(ranker=ranker, tokenizer=tokenizer)

    documents = list()
    for i in range(len(table_list)):
        document = dict()
        document["id"] = i
        document["contents"] = \
            [" ".join(table.values()) for table in table_names if table['table_name'] == table_list[i]][0]
        documents.append(document)
    # print(documents)
    output = list()
    for mapping in reranker.invoke(
            query=query, contexts=documents, key=lambda x: x['contents']
    ):
        # print(mapping)
        index = int(mapping['context']['id'])
        output.append(table_list[index])
    return output[:k]


tables = rerank(table_list=target_table_list, query=query, k=3)
print(f'tables============================{tables}')
temp_table_list = get_related_tables(list_of_tables=list(set(tables)), original_table_list=target_table_list)
print(f'temp_table_list==================={temp_table_list}')
final_table_list = rerank(table_list=target_table_list, query=query, k=5)
print(f'final_table_list=================={final_table_list}')
