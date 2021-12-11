import contextlib
import pysolr
import csv


def query_from_file(my_file):
    # initialize the parameters
    host = "localhost"
    port = "8983"
    core = "Process_BM25"
    qt = "select"
    op = ""
    sort = "score desc"
    rows = "7"
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

            # Extraction of the 5 first docs (top 5)
            top_docs = []
            for i in range(5):
                top_docs.append(documents[i])



            # Add the rank key to the docs and print line in trec_eval format
            # for document in documents:
            #     document.update({'rank': documents.index(document) + 1})
            #     # redirect output to a file
            #     with open('output.txt', 'a') as external_file:
            #         with contextlib.redirect_stdout(external_file):
            #             print(line[0], "\tQ0", document['docno'][0], "\t", document['rank'], "\t",
            #                   "{:.6f}".format(document['score']), "\tSTANDARD")
            #     external_file.close()


query_from_file("duplicate.csv")
