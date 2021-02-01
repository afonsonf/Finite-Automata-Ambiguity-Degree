import shelve
import os

import cPickle as pickle

from FAdo.fa import *
from FAdo.reex import *
from FAdo.fio import *

import ambiguityTest
import degreeOfAmbiguity

results_file = "data/results"
data_folder = "data"

def printDetails_aux(file):
    """auxiliar function for printDetails"""

    nFNFA = 0
    ndegree = 0
    lstdegree = []
    lstdegree_sz = 0
    nstate = 0
    lststate = []
    lststate_sz = 0

    db = shelve.open("{}/{}".format(data_folder,file))
    print "PD results for {}: {}".format(file,len(db))
    # xx = 0
    for key in db:
        # print xx
        # xx +=1
        if db[key]["ufa"] > db[key]["fnfa"] or db[key]["fnfa"] > db[key]["pnfa"] or db[key]["ufa"] > db[key]["pnfa"]:
            print "Error"
            sys.exit()

        if db[key]["fnfa"] and not db[key]["ufa"]:
            r = db[key]["nfa"]
            nfa = r.toNFA()

            nFNFA += 1

            sz = len(nfa.States)
            nstate += sz
            while sz>=lststate_sz:
                lststate.append(0)
                lststate_sz += 1
            lststate[sz]+=1

            degree = degreeOfAmbiguity.degreeOfNFA(nfa)
            ndegree += degree
            while degree>=lstdegree_sz:
                lstdegree.append(0)
                lstdegree_sz += 1
            lstdegree[degree]+=1

    print "number FNFA: {}".format(nFNFA)
    print "average number states: {}".format(nstate/nFNFA)
    print "average degree: {}".format(ndegree/nFNFA)

    print "Degrees"
    for i in xrange(0,lstdegree_sz):
        if lstdegree[i] == 0: continue
        print i,lstdegree[i]

    print "Sizes"
    for i in xrange(0,lststate_sz):
        if lststate[i] == 0: continue
        print i,lststate[i]

    db.close()
    return

def printDetails():
    """print details of result for type
    """

    for file in os.listdir(data_folder):
        if file.startswith("pd"):
            printDetails_aux(file)
            # break
    return

if __name__ == '__main__':
    printDetails()
