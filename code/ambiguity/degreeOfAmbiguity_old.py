def degreeOfNFA_aux(node, graph, vis, memo, sz):
    if memo[node]!=-1:
        # print node,memo[node]
        return memo[node]

    counter = [0 for i in vis]

    vis[node] = True
    for (child,_) in graph[node]:
        if child!=node and not vis[child]:
            v = degreeOfNFA_aux(child, graph, vis, memo, sz)
            (x,y) = (child/sz,child%sz)
            id = 0
            if x<y: id=x*sz+y
            else:   id=y*sz+x
            # print node,child,v,counter[child]
            counter[id]+=v
    vis[node] = False

    res = max(counter)
    memo[node] = res

    return res

def degreeOfNFA(nfax):
    """Computes the finite degree of nfa, if not finite returns -1"""
    nfa = nfax.dup()
    nfa.trim()

    if not ambiguityTest.isPNFA(nfa): return -1 #is enfa
    if not ambiguityTest.isFNFA(nfa): return -1 #is pnfa
    if ambiguityTest.isUFA(nfa): return 1       #is ufa

    sz = len(nfa.States)
    nfa.addState()
    nfa.addState()
    for s in nfa.Initial: nfa.addTransition(sz,'#',s)
    for s in nfa.Final: nfa.addTransition(s,'$',sz+1)
    nfa.Initial = {sz}
    nfa.Final = {sz+1}
    sz+=2

    # nfa.display()

    conj = ambiguityTest.myProduct(nfa,nfa)
    ambiguityTest.addFinals(conj, nfa, nfa)
    conj.trim()

    # conj.display(strict = True)

    graph = [[] for i in xrange(sz*sz)]
    for s1 in conj.delta:
        (x,y) = literal_eval(conj.States[s1])
        v1 = x*sz+y

        # aux = set()
        for symb in conj.delta[s1]:
            for s2 in conj.delta[s1][symb]:
                # aux.add(s2)
                (x,y) = literal_eval(conj.States[s2])
                v2 = x*sz+y
                graph[v2].append((v1,symb))

        # for s in aux:
        #     (x,y) = literal_eval(conj.States[s])
        #     v2 = x*sz+y
        #     graph[v2].append(v1)

    memo = [-1 for i in xrange(0,sz*sz)]
    vis = [False for i in xrange(0,sz*sz)]

    for s in conj.Initial:
        # print conj.States[s]
        (x,y) = literal_eval(conj.States[s])
        memo[x*sz+y] = 1

    for f in conj.Final: break
    (x,y) = literal_eval(conj.States[f])
    # print "sz",sz
    return degreeOfNFA_aux(x*sz+y, graph, vis, memo, sz)
