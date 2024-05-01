from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.example_selectors import MaxMarginalRelevanceExampleSelector, SemanticSimilarityExampleSelector
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from get_specific_table_list import intent_table_selector
from get_referenced_tables import get_related_tables
from table_list import table_names
from sentence_transformers import SentenceTransformer
from pyserini.search.lucene import LuceneSearcher


intent = 'team_details'
target_table_list = []
for table_intent_pair in intent_table_selector:
    if table_intent_pair['intent'] == intent:
        target_table_list = table_intent_pair['table_names']
        print(f'target_table_list==============={target_table_list}')
# embeddings = HuggingFaceEmbeddings(model_name="WhereIsAI/UAE-Large-V1")
embedding_model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
print(len(table_names))

def table_selector(table_list):
    to_vectorize = ["".join(example.values()) for example in table_names if example['table_name'] in
                    table_list]
    # print(f'to_vectorize======{to_vectorize}')
    metadata = [example for example in table_names if example['table_name'] in table_list]
    # print(f'metadata========{metadata}')

    query = 'Give me python devs who are available.'
    for doc in to_vectorize:
        print(doc)
        count_vectorizer = CountVectorizer(stop_words="english")
        # count_vectorizer = CountVectorizer()
        sparse_matrix = count_vectorizer.fit_transform([doc, query])
        doc_term_matrix = sparse_matrix.toarray()
        cosine_similarity_matrix = cosine_similarity(doc_term_matrix)
        print(cosine_similarity_matrix)
        df = pd.DataFrame(
            cosine_similarity_matrix,
            # columns=count_vectorizer.get_feature_names_out(),
            index=[1, 2]
        )
        print(df)
    return None

tables = table_selector(target_table_list)
# tables = ['employee_skill', 'tech_stack', 'daily_allocation', 'project_basic']
print(f'tables============={tables}')
# temp_table_list = get_related_tables(list(set(tables)), original_table_list=target_table_list)
# print(f'temp_table_list==================={temp_table_list}')
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
