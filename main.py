from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.example_selectors import MaxMarginalRelevanceExampleSelector, SemanticSimilarityExampleSelector

from get_specific_table_list import intent_table_selector
from get_referenced_tables import get_related_tables
from table_list import table_names

intent = 'project_details'
target_table_list = []
for table_intent_pair in intent_table_selector:
    if table_intent_pair['intent'] == intent:
        target_table_list = table_intent_pair['table_names']
        print(f'target_table_list==============={target_table_list}')
embeddings = HuggingFaceEmbeddings(model_name="WhereIsAI/UAE-Large-V1")
print(len(table_names))


def table_selector(table_list, k: int = 3, lambda_mult: float = 1, fetch_k: int = 5, search_type: str = "mmr"):
    # print(f'table_list======={table_list}')
    to_vectorize = [" ".join(example['table_description']) for example in table_names if example['table_name'] in
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
        input_variables={"query": "Which project has the least hours remaining in hourly buckets today?"})
    vectorstore.delete_collection()
    return [val['table_name'] for val in examples]


tables = table_selector(target_table_list, lambda_mult=0.1, k=3)
print(f'tables============={tables}')
temp_table_list = get_related_tables(list(set(tables)), original_table_list=target_table_list)
print(f'temp_table_list==================={temp_table_list}')
# final_table_list = table_selector(temp_table_list, k=4, lambda_mult=1, search_type="similarity")
# print(f'final_table_list=================={final_table_list}')
# example_prompt = PromptTemplate(
#     input_variables=[
#         "table_name",
#         "table_description",
#         "keywords_describing_table",
#         "relevant_keywords",
#     ],
#     template="\nTable Name: {table_name}\nTable Description: {table_description}\nKeywords Describing Table: {"
#              "keywords_describing_table}\nRelevant Keywords: {"
#              "relevant_keywords}",
# )
