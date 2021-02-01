from FAdo.fa import *
from FAdo.reex import *
from FAdo.fio import *

from ast import literal_eval

import ambiguityTest

def numberWords(nfa, max_size):
    """Computes number accepting words til max_size
       If a word is accepted k times, it will add as if k words are accepted (counts repetitions)
       O(max_size*n^2) where n is number of states
    """
    sz = len(nfa.States)
    img = [0 for i in xrange(0,sz)]
    for i in nfa.Initial: img[i] = 1

    delta = [[0 for j in xrange(0,sz)] for i in xrange(0,sz)]
    for i in nfa.delta:
        for symb in nfa.delta[i]:
            for j in nfa.delta[i][symb]: delta[i][j] += 1

    counter = [0 for i in xrange(0,max_size)]
    total = 0
    for k in xrange(0, max_size):
        aux = [0 for i in xrange(0,sz)]
        for i in xrange(0,sz):
            for state in xrange(0,sz):
                aux[state] += img[i]*delta[i][state]

        img = list(aux)

        for i in nfa.Final: counter[k] += img[i]
        total+=counter[k]

    return total,counter

def isSubsetOf(nfa, other):
    """test if nfa is subset of other, gives valid result if both are ufa"""
    sz = len(other.States)
    conj = ambiguityTest.myProduct(nfa,other)
    for x in [(a, b) for a in nfa.Final for b in other.Final]:
        if str(x) in conj.States:
            conj.addFinal(x[0]*sz+x[1])
    conj.trim()
    # conj.display()

    szconj = len(conj.States)

    return numberWords(conj,szconj) == numberWords(nfa,szconj)

def degreeOfWord(nfa, word, img=None):
    """Computes the number of accepting paths of word in nfa
       O(len(word)*n^2) where n is number of states
    """
    sz = len(nfa.States)
    if img == None:
        img = [0 for i in xrange(0,sz)]
        for i in nfa.Initial: img[i] = 1

    for letter in word:
        aux = [0 for i in xrange(0,sz)]
        for i in nfa.delta:
            if letter not in nfa.delta[i]: continue
            for state in nfa.delta[i][letter]:
                 aux[state] += img[i]

        img = list(aux)
        # print letter, img

    counter = 0
    for i in nfa.Final:
        counter += img[i]
    return counter,img

def dfsWords(nfa, node, word, vis, words, test):
    # print nfa.States[node],vis[node], word, test

    if node in nfa.Final and test: words.add(word)
    if vis[node]==2: return #maybe this should go first

    if vis[node]==1: vis[node]=2
    if vis[node]==0: vis[node]=1

    if node in nfa.delta:
        for symb in nfa.delta[node]:
            for child in nfa.delta[node][symb]:
                (x,y) = literal_eval(nfa.States[child])
                if x==y: dfsWords(nfa, child, word+symb, vis, words, test)
                else   : dfsWords(nfa, child, word+symb, vis, words, True)

    if vis[node]==1: vis[node]=0
    if vis[node]==2: vis[node]=1
    return


def degreeOfNFA(nfax):
    """[WIP]"""
    """Computes the finite degree of nfa, if not finite returns -1"""
    nfa = nfax.dup()
    nfa.trim()

    if not ambiguityTest.isPNFA(nfa): return -1 #is enfa
    if not ambiguityTest.isFNFA(nfa): return -1 #is pnfa
    if ambiguityTest.isUFA(nfa): return 1                     #is ufa

    sz = len(nfa.States)
    nfa.addState()
    nfa.addState()
    for s in nfa.Initial: nfa.addTransition(sz,'#',s)
    for s in nfa.Final: nfa.addTransition(s,'$',sz+1)
    nfa.Initial = {sz}
    nfa.Final = {sz+1}
    sz+=2

    conj = ambiguityTest.myProduct(nfa,nfa)
    ambiguityTest.addFinals(conj, nfa, nfa)
    conj.trim()

    print "start words"
    #get ambiguous words
    words = set()
    for node in conj.Initial:
        vis = [0 for i in conj.States]
        (x,y) = literal_eval(conj.States[node])
        if x==y: dfsWords(conj, node, "", vis, words, False)
        else   : dfsWords(conj, node, "", vis, words, True)

    words = list(words)
    words.sort()

    print "finish words: " + str(len(words))

    maxAmb = 0
    stack = []
    i = 0
    for word in words:
        print "{} {}".format(i,word)
        img = None
        wordx = word
        while len(stack)>0:
            (pref, imgx) = stack.pop()
            if word.startswith(pref):
                img = imgx
                wordx = word[len(pref):]
                break
        degree,img = degreeOfWord(nfa, wordx, img)
        stack.append((word,img))

        # print word, degree
        if degree > maxAmb: maxAmb = degree

    return maxAmb
