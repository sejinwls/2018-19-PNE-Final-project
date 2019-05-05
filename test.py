import http.client
import json

def get_gene(chromo, start, end):
    HOSTNAME = "rest.ensembl.org"
    ENDPOINT = "/overlap/region/human/"
    ENDPOINT = ENDPOINT + chromo + ":" + start + "-" + end + "?feature=gene"
    METHOD = "GET"
    headers = {"Content-Type": "application/json"}

    conn = http.client.HTTPSConnection(HOSTNAME)

    conn.request(METHOD, ENDPOINT, None, headers)

    r1 = conn.getresponse()

    print()
    print("Response received: ", end='')
    print(r1.status, r1.reason)


    seq = (r1.read().decode("utf-8"))
    conn.close()
    info = json.loads(seq)
    genes = ""
    for infor in info:
        gene = infor['gene_id']
        genes += gene + ", "
    return genes

seq = get_gene("7", "140424943", "140624564")
print(seq)
