import contextlib
import nltk
import pandas as pd
from gensim.parsing.preprocessing import remove_stopwords as stopwords
import pysolr
import csv
from sklearn.feature_extraction.text import TfidfVectorizer


# initialize the parameters
host = "localhost"
port = "8983"
core = "Process_BM25"
qt = "select"
op = ""
sort = "score desc"
rows = "30"
query_field = "text"
expanded_query_field = "docno, score"
df = "text"

# construct the url
url = 'http://' + host + ':' + port + '/solr/' + core

# construct the query
solr_client = pysolr.Solr(url, search_handler="/" + qt, timeout=5)

# Extract the relevant words by calculating their weight using tf*idf
def weighting(top_texts):
    relevant_words = []
    # Remove the stop words
    filtered_sentences = []
    for sentence in top_texts:
        filtered_sentences.append(stopwords(sentence))

    # Ponderation of each term in the set
    tfidf = TfidfVectorizer(use_idf=True)
    tf_idf = tfidf.fit_transform(filtered_sentences)
    data_frame = pd.DataFrame(tf_idf[0].T.todense(), index=tfidf.get_feature_names_out(), columns=["score"])\
        .sort_values(by='score', ascending=False)\
        .head(25)
    print(data_frame)

# Run the expanded query
def expanded_query(num_q,query,relevant_words):
    print()
# Add the rank key to the docs and print line in trec_eval format
# for document in documents:
#     document.update({'rank': documents.index(document) + 1})
#     # redirect output to a file
#     with open('output.txt', 'a') as external_file:
#         with contextlib.redirect_stdout(external_file):
#             print(line[0], "\tQ0", document['docno'][0], "\t", document['rank'], "\t",
#                   "{:.6f}".format(document['score']), "\tSTANDARD")
#     external_file.close()

# Run the queries from a csv file
def query(my_file):
    with open(my_file, "r") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader, None)
        for line in reader:
            q = line[1]
            query_response = solr_client.search(q, **{
                'q.op': op,
                'sort': sort,
                'rows': rows,
                'fl': query_field,
                'df': df,
            })

            # Number of docs found for the query
            print(query_response.hits, "documents found for the query number", line[0])

            # Get the docs of the response
            documents = query_response.docs

            # extract all the 30 texts and convert to lower case
            top_texts = []
            for doc in documents:
                for text in doc['text']:
                    text = text.replace('\n', ' ')
                    top_texts.append(str(text).lower())

            # Find relevant word in the top texts
            words = weighting(top_texts)

            # Run the expanded query with relevant words
            # expanded_query(line[0],line[1],words)


query("duplicate.csv")
