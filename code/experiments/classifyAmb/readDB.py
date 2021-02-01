import shelve
import os

import cPickle as pickle

from FAdo.fa import *
from FAdo.reex import *
from FAdo.fio import *

import ambiguityTest

results_file = "data/results"
data_folder = "data"

def addResult():
    k = 5
    n = 75
    file = "position_{}_{}".format(k,n)
    db = shelve.open("{}/{}".format(data_folder,file))

    ufa = 0
    fnfa = 0
    pnfa = 0
    enfa = 0

    keys = []
    for key in db:
        keys.append(key)

    total = 10000

    keys.sort()
    for key in keys:
        if not db[key]["pnfa"]: enfa+=1
        elif not db[key]["fnfa"]: pnfa+=1
        elif not db[key]["ufa"]: fnfa+=1
        else: ufa+=1

        if db[key]["ufa"] > db[key]["fnfa"] or db[key]["fnfa"] > db[key]["pnfa"] or db[key]["ufa"] > db[key]["pnfa"]:
            print "Error"
            sys.exit()

    db.close()

    type = "position"
    id = "(k: {}, n: {})".format(k,n)

    dbRes = shelve.open(results_file,writeback=True)
    dbRes["results_{}_{}".format(type,id)] = {"total":total, "ufa":ufa, "fnfa":fnfa, "pnfa":pnfa, "enfa":enfa}
    dbRes.close()
    return

def printResults(type):
    """print resume of result for type
       type = {'fifa','pd'}
    """

    file = "results_{}".format(type)
    db = shelve.open(results_file)

    ids = []
    for id in db:
        if not id.startswith(file): continue
        ids.append(id)

    ids.sort()
    for id in ids:
        total = db[id]["total"]
        counter = 0
        print "results for {}: {}".format(id,total)

        print "...ufa : {} {}%".format(db[id]["ufa"], db[id]["ufa"]*100.0/total)
        print "...fnfa: {} {}%".format(db[id]["fnfa"], db[id]["fnfa"]*100.0/total)
        print "...pnfa: {} {}%".format(db[id]["pnfa"], db[id]["pnfa"]*100.0/total)
        print "...enfa: {} {}%".format(db[id]["enfa"], db[id]["enfa"]*100.0/total)

    db.close()
    return

def printDetails_aux(type, file):
    """auxiliar function for printDetails"""

    db = shelve.open("{}/{}".format(data_folder,file))
    # print db
    print "{} results for {}: {}".format(type,file,len(db))

    keys = []
    for key in db:
        keys.append(key)

    keys.sort()
    for key in keys:
        print key,"...ufa : {}".format(db[key]["ufa"]),"...fnfa: {}".format(db[key]["fnfa"]),"...pnfa: {}".format(db[key]["pnfa"])
        # print "...ufa : {}".format(db[key]["ufa"])
        # print "...fnfa: {}".format(db[key]["fnfa"])
        # print "...pnfa: {}".format(db[key]["pnfa"])
        # print ""

        if db[key]["ufa"] > db[key]["fnfa"] or db[key]["fnfa"] > db[key]["pnfa"] or db[key]["ufa"] > db[key]["pnfa"]:
            print "Error"
            sys.exit()

    db.close()
    return

def printDetails(type):
    """print details of result for type
       type = {'fifa','pd'}
    """

    for file in os.listdir(data_folder):
        if file.startswith(type):
            printDetails_aux(type, file)
    return

if __name__ == '__main__':
    # printDetails('pd')
    # printDetails('position')
    #
    # printResults('pd')
    printResults('position')

    # addResult()
