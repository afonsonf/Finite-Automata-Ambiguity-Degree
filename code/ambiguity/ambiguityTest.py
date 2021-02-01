from FAdo.fa import *
from FAdo.reex import *
from FAdo.fio import *

from ast import literal_eval

def addFinals(conj, nfa1, nfa2):
    sz = len(nfa2.States)
    for x in [(a, b) for a in nfa1.Final for b in nfa2.Final]:
        if str(x) in conj.States:
            conj.addFinal(x[0]*sz+x[1])

def myProduct(nfa1, nfa2):
    nfa = NFA()

    sz1 = len(nfa1.States)
    sz2 = len(nfa2.States)

    #state (i,j) is in index i*sz2+j
    for i in xrange(0,sz1):
        for j in xrange(0,sz2): nfa.addState(str((i,j)))

    for i in nfa1.Initial:
        for j in nfa2.Initial: nfa.addInitial(i*sz2+j)


    for s1 in nfa1.delta:
        for symb in nfa1.delta[s1]:
            for s2 in nfa2.delta:
                if symb not in nfa2.delta[s2]: continue
                states = [i*sz2+j for i in nfa1.delta[s1][symb] for j in nfa2.delta[s2][symb]]
                for state in states: nfa.addTransition(s1*sz2+s2,symb,state)
    return nfa

def stronglyConnectedComponents(nfa):
    def dfs(graph, node, vis, list):
        stack = [node]
        while len(stack) > 0:
            n = stack.pop()
            if vis[n] == 2: continue
            if vis[n] == 1:
                list.append(n)
                vis[n] = 2
                continue

            vis[n] = 1
            stack.append(n)
            for child in graph[n]:
                if not vis[child]: stack.append(child)

    sz = len(nfa.States)
    graph  = [set() for i in xrange(0,sz)]
    graphT = [set() for i in xrange(0,sz)]

    for i in nfa.delta:
        for symb in nfa.delta[i]:
            for j in nfa.delta[i][symb]:
                graph[i].add(j)
                graphT[j].add(i)

    stack = []
    vis = [0 for i in xrange(0,sz)]
    for node in xrange(sz-1,-1,-1):
        if not vis[node]: dfs(graph, node, vis, stack)

    strongComp = []
    vis = [0 for i in xrange(sz-1,-1,-1)]
    while len(stack) > 0:
        node = stack.pop()
        if vis[node]: continue

        comp = []
        dfs(graphT, node, vis, comp)
        strongComp.append(comp)

    return strongComp

def isPNFA(nfax):
    nfa = nfax.dup()
    nfa.trim()

    conj = myProduct(nfa,nfa)
    addFinals(conj, nfa, nfa)

    conj.trim()
    comp = stronglyConnectedComponents(conj)
    for l in comp:
        for s1 in l:
            for s2 in l:
                if s1==s2: continue
                (p1,p2) = literal_eval(conj.States[s1])
                (q1,q2) = literal_eval(conj.States[s2])
                if p1==p2 and q1!=q2:
                    # print conj.States[s1], conj.States[s2]
                    return False
    return True

def isFNFA(nfa):
    sz = len(nfa.States)

    conj = myProduct(nfa,nfa)
    addFinals(conj, nfa, nfa)

    conj2 = myProduct(conj,nfa)
    addFinals(conj2, conj, nfa)

    for p in xrange(0,sz):
        for q in xrange(0,sz):
            if p==q: continue
            a = (p*sz+p,q)
            b = (p*sz+q,q)
            conj2.addTransition(a[0]*sz+a[1],'#',b[0]*sz+b[1])

    conj2.trim()

    comp = stronglyConnectedComponents(conj2)
    for l in comp:
        tcard = False
        tother = False
        for i in l:
            if i not in conj2.delta: continue
            for symb in conj2.delta[i]:
                for t in conj2.delta[i][symb]:
                    if t in l:
                        if symb=='#': tcard = True
                        else: tother = True
                        if tcard and tother: return False

    return True

def isUFA(nfax):
    """checks if nfa is unambiguous"""
    nfa = nfax.dup()

    nfa = nfa.trim()

    conj = myProduct(nfa,nfa)
    addFinals(conj, nfa, nfa)

    useful = conj.usefulStates()
    for i in useful:
        (x,y) = literal_eval(conj.States[i])
        if x != y:
            return False

    return True
