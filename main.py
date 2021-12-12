import contextlib

import nltk
import pandas as pd
from gensim.parsing.preprocessing import remove_stopwords as stopwords
import pysolr
import csv

from sklearn.feature_extraction.text import TfidfVectorizer


def query_from_file(my_file):
    # initialize the parameters
    host = "localhost"
    port = "8983"
    core = "Process_BM25"
    qt = "select"
    op = ""
    sort = "score desc"
    rows = "50"
    query_field = "docno,text"
    query_expansion_field = "docno,score"
    df = "text"

    # construct the url
    url = 'http://' + host + ':' + port + '/solr/' + core

    # construct the query
    solr_client = pysolr.Solr(url, search_handler="/" + qt, timeout=5)

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
            # print(query_response.hits, "documents found for the query number", line[0])

            # Get the docs of the response
            documents = query_response.docs

            # Extract the 20 first docs (top 20)
            top_docs = []
            for index in range(30):
                top_docs.append(documents[index])

            # Create a dataset for each text
            for top_doc in top_docs:
                dataset = []

            # Replace every \n in text and convert all text to Lower Case
                for text in top_doc['text']:
                    text = text.replace('\n', ' ')
                    dataset.append(text.lower())

            # Tokenize the sentences
                    tokens = nltk.sent_tokenize(dataset[0])

            # Remove stop words
                    filtered_sentences = []
                    for sentence in tokens:
                        filtered_sentences.append(stopwords(sentence))

            # Ponderation of each term in a document
                    TFIDF = TfidfVectorizer(use_idf=True)
                    tf_idf = TFIDF.fit_transform(filtered_sentences)
                    print(tf_idf)
                    # df = pd.DataFrame(tf_idf[0].T.todense(), index=TFIDF.get_feature_names_out(), columns=["TF-IDF"])
                    # df = df.sort_values('TF-IDF', ascending=False)
                    # print(df.head(25))



            # Add the rank key to the docs and print line in trec_eval format
            # for document in documents:
            #     document.update({'rank': documents.index(document) + 1})
            #     # redirect output to a file
            #     with open('output.txt', 'a') as external_file:
            #         with contextlib.redirect_stdout(external_file):
            #             print(line[0], "\tQ0", document['docno'][0], "\t", document['rank'], "\t",
            #                   "{:.6f}".format(document['score']), "\tSTANDARD")
            #     external_file.close()


query_from_file("mini_duplicate.csv")
