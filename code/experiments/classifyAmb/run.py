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

def generate(generator,k,n,total):
    id = "(k: {}, n: {})".format(k,n)

    results = []
    dbDetails = shelve.open("{}/{}_{}_{}".format(data_folder,"regexp",k,n))

    #run tests
    for i in xrange(1,total+1):
        res = {}
        print("{} generate {}... ".format(id,i),end = ""); sys.stdout.flush()

        s = str2regexp(generator.generate(),parser=ParserRPN)
        dbDetails["{}".format(i)] = str(s)

        del res
        print("Done")

    dbDetails.close()
    return

def run(type, k,n,total):
    id = "(k: {}, n: {})".format(k,n)
    ufa = 0
    fnfa = 0
    pnfa = 0
    enfa = 0

    dbRegexp = shelve.open("{}/{}_{}_{}".format(data_folder,"regexp",k,n))
    dbDetails = shelve.open("{}/{}_{}_{}".format(data_folder,type,k,n))

    #run tests
    for i in xrange(1,total+1):
        res = {}
        print("{} {} runing {}... ".format(type,id,i),end = ""); sys.stdout.flush()

        if type == "pd":
            s = str2regexp(dbRegexp["{}".format(i)])
            nfa = s.toNFA()
        else:
            s = str2regexp(dbRegexp["{}".format(i)])
            nfa = s.nfaPosition()

        # print(len(nfa.States))
        # return

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

        dbDetails["{}".format(i)] = res

        if res["ufa"] > res["fnfa"] or res["fnfa"] > res["pnfa"] or res["ufa"] > res["pnfa"]:
            print("Error")
            sys.exit()

        del res
        del nfa
        del s
        print("Done")

    dbDetails.close()
    dbRegexp.close()

    # save results
    dbRes = shelve.open(results_file,writeback=True)
    dbRes["results_{}_{}".format(type,id)] = {"total":total, "ufa":ufa, "fnfa":fnfa, "pnfa":pnfa, "enfa":enfa}
    dbRes.close()

    return



if __name__ == '__main__':
    random.seed(seed)

    # generate(reStringRGenerator(smallAlphabet(2),20,reGrammar['g_rpn']),2,20,10000) #runs ok
    # generate(reStringRGenerator(smallAlphabet(5),20,reGrammar['g_rpn']),5,20,10000) #runs ok
    # generate(reStringRGenerator(smallAlphabet(10),20,reGrammar['g_rpn']),10,20,10000) #runs ok
    # #
    # generate(reStringRGenerator(smallAlphabet(2),35,reGrammar['g_rpn']),2,35,10000) #runs ok
    # generate(reStringRGenerator(smallAlphabet(5),35,reGrammar['g_rpn']),5,35,10000) #runs ok
    # generate(reStringRGenerator(smallAlphabet(10),35,reGrammar['g_rpn']),10,35,10000) #runs ok
    #
    # generate(reStringRGenerator(smallAlphabet(2),50,reGrammar['g_rpn']),2,50,10000) #runs ok
    # generate(reStringRGenerator(smallAlphabet(5),50,reGrammar['g_rpn']),5,50,10000) #runs ok
    # generate(reStringRGenerator(smallAlphabet(10),50,reGrammar['g_rpn']),10,50,10000) #runs ok
    #
    # generate(reStringRGenerator(smallAlphabet(2),75,reGrammar['g_rpn']),2,75,10000) #runs ok
    # generate(reStringRGenerator(smallAlphabet(5),75,reGrammar['g_rpn']),5,75,10000) #runs ok
    # generate(reStringRGenerator(smallAlphabet(10),75,reGrammar['g_rpn']),10,75,10000) #runs ok
    #
    # generate(reStringRGenerator(smallAlphabet(2),100,reGrammar['g_rpn']),2,100,10000) #runs ok
    # generate(reStringRGenerator(smallAlphabet(5),100,reGrammar['g_rpn']),5,100,10000) #runs ok
    # generate(reStringRGenerator(smallAlphabet(10),100,reGrammar['g_rpn']),10,100,10000) #runs ok

    ##########################################################################################
    ##########################################################################################

    # run("pd",2,20,10000) #runs ok
    # run("pd",5,20,10000) #runs ok
    # run("pd",10,20,10000) #runs ok
    #
    # run("pd",2,35,10000) #runs ok
    # run("pd",5,35,10000) #runs ok
    # run("pd",10,35,10000) #runs ok
    #
    # run("pd",2,50,10000) #runs ok
    # run("pd",5,50,10000) #runs ok
    # run("pd",10,50,10000) #runs ok
    #
    # run("pd",2,75,10000) #runs ok
    # run("pd",5,75,10000) #runs ok
    # run("pd",10,75,10000) #runs ok
    #
    # run("pd",2,100,10000) #runs ok
    # run("pd",5,100,10000) #runs ok
    # run("pd",10,100,10000) #runs ok

    ##########################################################################################
    ##########################################################################################

    # run("position",2,20,10000) #runs ok
    # run("position",5,20,10000) #runs ok
    # run("position",10,20,10000) #runs ok
    #
    # run("position",2,35,10000) #runs ok
    # run("position",5,35,10000) #runs ok
    # run("position",10,35,10000) #runs ok
    #
    # run("position",2,50,10000) #runs ok
    # run("position",5,50,10000) #runs ok
    # run("position",10,50,10000) #runs ok
    #
    # run("position",2,75,10000) #runs ok
    # run("position",5,75,10000) #runs ok
    # run("position",10,75,10000) #runs ok
    #
    # run("position",2,100,10000) #runs ok
    # run("position",5,100,10000) #runs ok
    # run("position",10,100,10000) #runs ok

    sys.exit(0)
