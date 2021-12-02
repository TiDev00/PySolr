import contextlib
import pysolr
import csv

def query_from_file(myFile):
    # initialize the parameters
    host = "localhost"
    port = "8983"
    core = "test"
    qt = "select"
    op = ""
    sort = "score desc"
    rows = "3"
    fl = "docno,score"
    df = "text"

    # construct the url
    url = 'http://' + host + ':' + port + '/solr/' + core

    # construct the query
    solr = pysolr.Solr(url, search_handler="/" + qt, timeout=5)

    with open(myFile, "r") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader, None)
        for line in reader:
            q = line[1]
            response = solr.search(q, **{
                'q.op': op,
                'sort': sort,
                'rows': rows,
                'fl': fl,
                'df': df,
            })

            # Number of docs found
            print(response.hits, "documents found")

            # Get the docs of the response
            documents = response.docs

            # Add the rank key to the docs and print line in trec_eval format
            for document in documents:
                document.update({'rank': documents.index(document)+1})
                # redirect output to a file
                with open('output.txt', 'a') as external_file:
                    with contextlib.redirect_stdout(external_file):
                        print(line[0], "\tQ0", document['docno'][0], "\t", document['rank'], "\t",
                              "{:.4f}".format(document['score']), "\tSTANDARD")
                external_file.close()

query_from_file("long_q.csv")