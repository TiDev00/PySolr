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
    rows = "1000"
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
            results = solr.search(q, **{
                'q.op': op,
                'sort': sort,
                'rows': rows,
                'fl': fl,
                'df': df,
            })

            # Number of docs found
            print(results.hits, "documents found")

            # iterate over results
            for result in results:
                print(line[0], "\tQ0", result['docno'][0], "{:.5f}".format(result['score']), "\tSTANDARD")

query_from_file("long_q.csv")