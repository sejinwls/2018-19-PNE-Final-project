import http.server
import socketserver
import termcolor
import http.client
import json
from seq import Seq
# Define the Server's port
PORT = 8000

# Funtion that gets the list of available species
def get_list():
    HOSTNAME = "rest.ensembl.org"
    ENDPOINT = "/info/species"
    METHOD = "GET"
    headers = { "Content-Type" : "text/plain"}
    conn = http.client.HTTPSConnection(HOSTNAME)


    conn.request(METHOD, ENDPOINT, None, headers)

    r1 = conn.getresponse()

    print()
    print("Response received: ", end='')
    print(r1.status, r1.reason)
    specie_list = r1.read().decode("utf-8")
    conn.close()
    specie_list = specie_list.split(" name:")
    list_species = []
    for info in specie_list[1:]:
        info = info.split("\n")
        # Add to the list only the name of the species
        specie = info[0][1:]
        specie = specie.replace("_", " ")
        list_species.append(specie)
    return list_species

# Function that gets information about the karyotype of a species
def get_karyotype(name):
    HOSTNAME = "rest.ensembl.org"
    ENDPOINT = "/info/assembly/"
    ENDPOINT = ENDPOINT + name
    METHOD = "GET"
    headers = {"Content-Type": "text/plain"}
    conn = http.client.HTTPSConnection(HOSTNAME)

    conn.request(METHOD, ENDPOINT, None, headers)

    r1 = conn.getresponse()

    print()
    print("Response received: ", end='')
    print(r1.status, r1.reason)
    info = r1.read().decode("utf-8")
    conn.close()
    return info


# Function that gets the id of a gene
def get_id(gene):
    HOSTNAME = "rest.ensembl.org"
    ENDPOINT = "xrefs/symbol/homo_sapiens/"
    ENDPOINT = ENDPOINT + gene
    METHOD = "GET"
    headers = {"Content-Type": "application/json"}

    conn = http.client.HTTPSConnection(HOSTNAME)

    conn.request(METHOD, ENDPOINT, None, headers)

    r1 = conn.getresponse()

    print()
    print("Response received: ", end='')
    print(r1.status, r1.reason)


    infor = (r1.read().decode("utf-8"))
    conn.close()
    if "id" in infor:
        info = json.loads(infor)
        id = info[0]['id']
    else:
        id = "no"
    return id
# Function that gets the sequence of a gene
def get_seq(gene):
    HOSTNAME = "rest.ensembl.org"
    ENDPOINT = "/sequence/id/"
    ENDPOINT = ENDPOINT + gene
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
    return seq


# Function that gets the start, the end and the id of a gene
def get_startendid(gene):
    HOSTNAME = "rest.ensembl.org"
    ENDPOINT = "/overlap/id/"
    ENDPOINT = ENDPOINT + gene
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
    start = info[0]['start']
    end = info[0]['end']
    id = info[0]['id']
    return start, end, id



def get_chromo(gene):
    HOSTNAME = "rest.ensembl.org"
    ENDPOINT = "/overlap/id/"
    ENDPOINT = ENDPOINT + gene + "?feature=gene"
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
    chromo = info[0]['seq_region_name']
    return chromo

def get_genes(chromo, start, end):
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


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        if self.requestline.startswith("GET / ") or self.requestline.startswith("GET /mainpage.html"):
            f = open("mainpage.html", 'r')
            contents = f.read()
        elif self.requestline.startswith("GET /listSpecies.html"):
            f = open('listSpecies.html', 'r')
            contents = f.read()
        elif self.requestline.startswith("GET /listSpecies?limit"):
            # if the user hasn't introduced a limit
            if self.requestline.startswith("GET /listSpecies?limit= "):
                f = open('listSpeciesresponse.html', 'r')
                contents = f.read()
                species = ""
                self.requestline = self.requestline.split("=")
                for name in get_list():
                    species = species + name + "," + " "
                contents = contents.replace("&", species)
            else:
                self.requestline = self.requestline.split("=")
                limit = self.requestline[1].split(" ")[0]
                if limit.isdigit():
                    f = open('listSpeciesresponse.html', 'r')
                    contents = f.read()
                    species = ""
                    slist = get_list()
                    for name in slist[:int(limit)]:
                        species = species + name + "," + " "
                    contents = contents.replace("&", species)
                else:
                    f = open('error.html', 'r')
                    contents = f.read()
        elif self.requestline.startswith("GET /karyotype.html"):
            f = open('karyotype.html', 'r')
            contents = f.read()
        elif self.requestline.startswith("GET /karyotype?specie="):
            self.requestline = self.requestline.split("=")
            # if the user hans't introduced the name if the species
            if self.requestline[1][0] == " ":
                f = open('errornoinput.html', 'r')
                contents = f.read()
                contents = contents.replace("#", "specie")
            # if the user has introduced an input
            else:
                specie = self.requestline[1].split(" ")[0]
                # is the name of the species is formed by two words
                if "+" in specie:
                    specie = specie.replace("+", "_")
                info = get_karyotype(specie)
                # Restore the original specie name
                if "_" in specie:
                    specie = specie.replace("_", " ")
                # Check that the specie introduced is in the database
                # If it isn't in the database we get an error message without the word karyotype in it
                if "karyotype" in info:
                    info = info.split("karyotype")[1]
                    info = info.split("top_level_region")[0][1:]
                    if not info == " []\n\n":
                        f = open('karyotyperesponse.html', 'r')
                        contents = f.read()
                        contents = contents.replace("#", specie)
                        contents = contents.replace("&", info)
                    # If there is no information about the karyotype of that species
                    else:
                        f = open('errornotavailable.html', 'r')
                        contents = f.read()
                        contents = contents.replace("#", "karyotype")
                # If the species introduced is not in the database
                else:
                    f = open('errornotavailable.html', 'r')
                    contents = f.read()
                    contents = contents.replace("#", 'specie')
        elif self.requestline.startswith("GET /chromosomeLenght.html"):
            f = open("chromosomeLenght.html", 'r')
            contents = f.read()
        elif self.requestline.startswith("GET /chromosomeLenght?"):
            specie = self.requestline.split("=")[1].split("&")[0]
            chromo = self.requestline.split("=")[2].split(" ")[0]
            # Check that the user has introduced a species
            if not(specie == ""):
                info = get_karyotype(specie)
                # Check that the specie introduced is in the database
                if "karyotype" in info:
                    # If the user has introduced a chromosome name
                    if not(chromo == ""):

                        info1 = info.split("karyotype")[1]
                        chromosomes = info1.split("-")[1:]
                        # Create a list with all the chromosomes
                        chromos = []
                        for chromosome in chromosomes:
                            chromosome = chromosome.replace("\n", "")
                            chromosome = chromosome.replace(" ", "")
                            chromos.append(chromosome)
                        # if the chromosome introduced is in the chromosome list
                        if chromo in chromos:
                            chromoinfolist = info.split("top_level_region")[1]
                            chromoinfolist = chromoinfolist.split("length")
                            chromolenght = chromoinfolist[(chromos.index(chromo))+1]
                            chromolenght = chromolenght.split(" ")[1]
                            f = open('chromosomeLenghtresponse.html', 'r')
                            contents = f.read()
                            contents = contents.replace("#", chromo).replace("&", specie).replace("@", chromolenght)
                        # if the chromosome introduced is not in the chromosome list
                        else:
                            f = open("errornotavailable.html", 'r')
                            contents = f.read()
                            contents = contents.replace("#", 'chromosome')
                    # if the user hasn't introduced a chromosome
                    else:
                        f = open('errornoinput.html', 'r')
                        contents = f.read()
                        contents = contents.replace("#", 'chromosome')
                # if the species introduced is not available
                else:
                    f = open('errornotavailable.html', 'r')
                    contents = f.read()
                    contents = contents.replace("#", "species")
            # if the user hasn't introduced a species
            else:
                f = open('errornoinput.html', 'r')
                contents = f.read()
                contents = contents.replace("#", 'species')
        elif self.requestline.startswith("GET /geneSeq.html"):
            f = open("geneSeq.html", 'r')
            contents = f.read()
        elif self.requestline.startswith("GET /geneSeq?"):
            gene = self.requestline.split("=")[1].split(" ")[0]
            geneid = get_id(gene)
            # If the gene has no id, it is not in the database
            if geneid == "no":
                f = open("errornotavailable.html", 'r')
                contents = f.read()
                contents = contents.replace("#", 'gene')
            else:
                sequence = get_seq(geneid)
                seq = json.loads(sequence)
                seq = seq['seq']
                # We place /n every 120 bases so it fits int he screen
                new_seq = []
                for i in range(0, len(seq), 120):
                    fragment = seq[i:i+120]
                    new_seq.append(fragment)
                def_seq = ""
                for frag in new_seq:
                    def_seq = def_seq + frag + "\n"
                f = open("geneSeqresponse.html", 'r')
                contents = f.read()
                contents = contents.replace("#", gene)
                contents = contents.replace("@", def_seq)
        elif self.requestline.startswith("GET /geneInfo.html"):
            f = open('geneInfo.html', 'r')
            contents = f.read()
        elif self.requestline.startswith("GET /geneInfo?"):
            gene = self.requestline.split("=")[1].split(" ")[0]
            geneid = get_id(gene)
            # if the gene is not in the database
            if geneid == "no":
                f = open('errornotavailable.html', 'r')
                contents = f.read()
                contents = contents.replace("#", 'gene')
            else:
                gene1 = geneid + "?feature=gene"
                # get the start, the end and the id of the gene
                start1, end1, id1 = get_startendid(gene1)
                f = open('geneInforesponse.html', 'r')
                contents = f.read()
                contents = contents.replace("#", gene).replace("@", str(start1))
                contents = contents.replace("$", str(end1)).replace("%", id1)
                # get the length of the gene
                sequence = get_seq(geneid)
                length = len(sequence)
                contents = contents.replace("*", str(length))
                # get the chromosome it belongs to
                chromosome = get_chromo(geneid)
                contents = contents.replace("?", chromosome)
        elif self.requestline.startswith("GET /geneCal.html"):
            f = open("geneCal.html", 'r')
            contents = f.read()
        elif self.requestline.startswith("GET /geneCal?"):
            gene = self.requestline.split("=")[1].split(" ")[0]
            geneid = get_id(gene)
            # if the gene introduced is not in the database
            if geneid == "no":
                f = open("errornotvaialable.html", 'r')
                contents = f.read()
                contents = contents.replace("#", 'gene')
            else:
                sequence = Seq(get_seq(geneid))
                f = open("geneCalresponse.html", 'r')
                contents = f.read()
                contents = contents.replace("@", str(sequence.len()))
                contents = contents.replace("$", str(sequence.perc("A")))
                contents = contents.replace("&", str(sequence.perc("C")))
                contents = contents.replace("*", str(sequence.perc("G")))
                contents = contents.replace("%", str(sequence.perc("T")))
        elif self.requestline.startswith("GET /geneList.html"):
            f = open('geneList.html', 'r')
            contents = f.read()
        elif self.requestline.startswith("GET /geneList?"):
            chromo = self.requestline.split("?")[1].split("&")[0].split("=")[1]
            start = self.requestline.split("?")[1].split("&")[1].split("=")[1]
            end = self.requestline.split("?")[1].split("&")[2].split("=")[1].split(" ")[0]
            # We make sure the user has introduced an input
            if chromo == "" or start == "" or end == "":
                f = open("errornoinput.html", 'r')
                contents = f.read()
                contents = contents.replace("#", 'chromosome, start and end')
            else:
                genes = get_genes(chromo, start, end)
                f = open('geneListresponse.html', 'r')
                contents = f.read()
                contents = contents.replace("#", chromo).replace("@", start)
                contents = contents.replace("%", end).replace("&", genes)
        else:
            f = open('error.html', 'r')
            contents = f.read()

        # Generating the response message
        self.send_response(200)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(contents)))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(contents))

        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()

print("")
print("Server Stopped")
