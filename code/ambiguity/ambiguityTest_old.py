from FAdo.fa import *
from FAdo.reex import *
from FAdo.fio import *

def dfsNFA(nfa, i, f, lstTrans, nfa_aux, vis):
    """add transitions that take state i to state j in nfa to nfa_aux"""
    if vis[i]:
        if i==f:
            for (x,symb,y) in lstTrans:
                nfa_aux.addTransition(x,symb,y)
        return

    vis[i] = 1
    dfsNFA(nfa,i,f,lstTrans, nfa_aux, vis)

    if i not in nfa.delta:
        vis[i] = 0
        return

    for symb in nfa.delta[i]:
        for y in nfa.delta[i][symb]:
            lstTrans.append((i,symb,y))
            dfsNFA(nfa,y,f,lstTrans, nfa_aux, vis)
            lstTrans.pop()

    vis[i] = 0
    return

def isFNFA2(nfa):
    """checks if ambiguity of nfa is finite,  nfa has to be epsilon free"""
    vis = []
    canGoToFinal = []
    mem_nfa = []
    mem_prod = []

    nfa = nfa.trim()

    sz = len(nfa.States)

    nfapp = None
    nfaqq = None
    nfapq = None

    for i in xrange(0,sz):
        vis.append(0)
        canGoToFinal.append(0)

    for p in xrange(0,sz):
        nfax = NFA()

        #add (p,w,p) w in E*
        for i in range(0,sz): canGoToFinal[i] = 0
        dfsNFA(nfa,p,p,[],nfax, vis, canGoToFinal)
        nfax.addInitial(p)
        nfax.addFinal(p)

        for i in range(0,sz):
            nfax.addState()

        mem_nfa.append(nfax)

    for i in xrange(0,sz):
        mem_prod.append([])
        for j in xrange(0,sz): mem_prod[i].append(None)

    for p in xrange(0,sz):
        for q in xrange(0,sz):
            if p<q:
                nfa_aux = mem_nfa[p].__and__(mem_nfa[q])
                if nfa_aux.witness() is not None:
                    mem_prod[p][q] = nfa_aux
                    mem_prod[q][p] = nfa_aux

            if p == q or mem_prod[p][q] is None:
                continue

            del nfapq
            nfapq = NFA()

            #add (p,w,q) w in E*
            for i in range(0,sz): canGoToFinal[i] = 0
            dfsNFA(nfa,p,q,[],nfapq, vis, canGoToFinal)
            nfapq.addInitial(p)
            nfapq.addFinal(q)

            for i in range(0,sz):
                nfapq.addState()

            nfa_aux = mem_prod[p][q].__and__(nfapq)

            if nfa_aux.witness() is not None:
                return False

            del nfa_aux
    return True

def isFNFA(nfa):
    """checks if ambiguity of nfa is finite,  nfa has to be epsilon free"""
    vis = []

    nfa = nfa.trim()

    nfapp = NFA()
    nfapq = NFA()
    nfaqq = NFA()

    sz = len(nfa.States)

    for i in xrange(0,sz):
        vis.append(0)

    for p in xrange(0,sz):

        nfapp.__init__()

        #add (p,w,p) w in E*
        dfsNFA(nfa,p,p,[],nfapp, vis)
        nfapp.addInitial(p)
        nfapp.addFinal(p)

        for i in range(0,sz):
            nfapp.addState()

        for q in xrange(0,sz):
            if p == q:
                continue

            nfapq.__init__()
            nfaqq.__init__()

            #add (p,w,q) w in E*
            dfsNFA(nfa,p,q,[],nfapq, vis)
            nfapq.addInitial(p)
            nfapq.addFinal(q)

            #add (q,w,q) w in E*
            dfsNFA(nfa,q,q,[],nfaqq, vis)
            nfaqq.addInitial(q)
            nfaqq.addFinal(q)

            for i in range(0,sz):
                nfapq.addState()
                nfaqq.addState()

            nfa_aux = (nfapp.__and__(nfapq.__and__(nfaqq)))

            if nfa_aux.witness() != None:
                return False
    return True

def isUFA(nfa):
    """checks if nfa is unambiguous"""
    nfa = nfa.trim()

    conj = nfa.product(nfa)

    for x in [(nfa.States[a], nfa.States[b]) for a in nfa.Final for b in nfa.Final]:
            if x in conj.States:
                conj.addFinal(conj.stateIndex(x))

    useful = conj.usefulStates()

    for i in useful:
        (x,y) = conj.States[i]
        if x != y:
            return False

    return True

def isPNFA(nfa):
    """checks if nfa is a pnfa (nfa with infinite polynimial ambiguity)"""
    nfa = nfa.trim()
    nfa_aux = NFA()

    sz = len(nfa.States)

    vis = []
    for i in xrange(0,sz): vis.append(0)

    for state in xrange(0,sz):
        nfa_aux.__init__()
        nfa_aux.addInitial(state)
        nfa_aux.addFinal(state)

        for i in xrange(0,sz): nfa_aux.addState()

        dfsNFA(nfa,state,state,[],nfa_aux, vis)
        if not isUFA(nfa_aux):
            return False

    return True

"""
ufas = 0

gen = reStringRGenerator(smallAlphabet(10),50,reGrammar['g_rpn'])
for i in range(0,1000):
    s = gen.generate()
    print s
    r = str2regexp(s,parser=ParserRPN)
    m = r.toNFA()
    m = FIFA.nfaToFIFA(m)
    teste = 0
    if isFNFA_slow(m):
        ufas += 1
        teste = 1
    print "Done " + str(i) + "... " + str(teste) + " " + str(len(m.States))

print "ufas: " + str(ufas)
"""
