from __future__ import print_function

import sys
import shelve

import cPickle as pickle

from FAdo.fa import *
from FAdo.reex import *
from FAdo.fio import *
from FAdo.cfg import reGrammar
from randomGen import *

from fifa import *

import ambiguityTest

seed = 314159
results_file = "data/results"
data_folder = "data"

def run(generator, type, k,n,total):
    id = "(k: {}, n: {})".format(k,n)
    ufa = 0
    fnfa = 0
    pnfa = 0
    enfa = 0

    results = []
    dbDetails = shelve.open("{}/{}_{}_{}".format(data_folder,type,k,n))

    #run tests
    for i in xrange(1,total+1):
        res = {}
        print("{} {} runing {}... ".format(type,id,i),end = ""); sys.stdout.flush()

        if type == "fifa":
            nfa = generator.next()
            # res["nfa"] = nfa.uniqueRepr() #gives error
            # res["nfa"] = pickle.dumps(nfa)
        else:
            s = str2regexp(generator.generate(),parser=ParserRPN)
            res["nfa"] = s
            nfa = s.toNFA()

        dbDetails["{}".format(i)] = res
        dbDetails.sync()

        isufa = ambiguityTest.isUFA(nfa)
        print("UFA... ",end=""); sys.stdout.flush()
        isfnfa = ambiguityTest.isFNFA(nfa)
        print("FNFA... ",end=""); sys.stdout.flush()
        ispnfa = ambiguityTest.isPNFA(nfa)
        print("PNFA... ",end=""); sys.stdout.flush()

        if not ispnfa: enfa+=1
        elif not isfnfa: pnfa+=1
        elif not isufa: fnfa+=1
        else: ufa+=1

        res["ufa"] = isufa
        res["fnfa"] = isfnfa
        res["pnfa"] = ispnfa

        results.append(res)
        dbDetails["{}".format(i)] = res
        # dbDetails.sync()

        if res["ufa"] > res["fnfa"] or res["fnfa"] > res["pnfa"] or res["ufa"] > res["pnfa"]:
            print("Error")
            sys.exit()

        del res
        print("Done")

    # dbDetails["details"] = results
    dbDetails.close()

    #save results
    dbRes = shelve.open(results_file)
    tmp = {}
    if dbRes.has_key("results_{}".format(type)): tmp = dbRes["results_{}".format(type)]
    tmp[id] = {"total":total, "ufa":ufa, "fnfa":fnfa, "pnfa":pnfa, "enfa":enfa}
    dbRes["results_{}".format(type)] = tmp
    dbRes.close()

    return



if __name__ == '__main__':
    random.seed(seed)

    # run(FIFArnd(5,2),"fifa",2,5,10000) #runs ok
    # run(FIFArnd(5,5),"fifa",5,5,10000) #runs ok
    # run(FIFArnd(5,10),"fifa",10,5,10000) #memory blow up next

    # run(FIFArnd(10,2),"fifa",2,10,10000) #runs ok
    # run(FIFArnd(10,5),"fifa",5,10,10000) #runs ok
    # run(FIFArnd(10,10),"fifa",10,10,10000) #[not tested] previous run out of mem

    # run(FIFArnd(20,2),"fifa",2,20,10000) #runs ok
    # run(FIFArnd(20,5),"fifa",5,20,10000) #memory blow up computing next
    # run(FIFArnd(20,10),"fifa",10,20,10000) #[not tested] previous run out of mem

    # run(FIFArnd(50,2),"fifa",2,50,10000) #memory blow up in size of delta in fnfaTest
    # run(FIFArnd(50,5),"fifa",5,50,10000) #[not tested] previous run out of mem
    # run(FIFArnd(50,10),"fifa",10,50,10000) #[not tested] previous run out of mem

    # run(FIFArnd(100,2),"fifa",2,100,10000) #[not tested] previous run out of mem
    # run(FIFArnd(100,5),"fifa",5,100,10000) #[not tested] previous run out of mem
    # run(FIFArnd(100,10),"fifa",10,100,10000) #[not tested] previous run out of mem
