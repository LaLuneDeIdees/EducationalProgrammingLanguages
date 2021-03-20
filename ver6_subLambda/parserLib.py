from util import Const,I,let,Y,xor,Just,Nothing,Leaf,Node

# data ParserState a is 
#   Fail 
#   Accept [[Char]] (RoseTree a [Char]) [a]

Fail = lambda Fail,Accept: Fail
Accept = lambda alreadyVisited, alreadyProcessing, dataForParsing: lambda Fail,Accept: Accept(alreadyVisited,alreadyProcessing,dataForParsing)


# parse as Parser a -> [a] -> Maybe (RoseTree a [Char])
parse = lambda p:lambda la:p(Accept([],Node("__ROOT__",[]),la))(
    Nothing,
    lambda _,d,__:Just(d)
)

# type parser a is ParserState a -> ParserState a

# empty as parser a
empty = I

# term as [a] -> Bool -> parser a
term = lambda ll, f: lambda ps: ps(
    I,
    lambda v,p,d: (Fail if not xor(d[0] in ll,f) else (
        p(
            Const(Fail),
            lambda a,ls: Accept([],Node(a,ls+[Leaf(d[0])]),d[1:])
        )
    )) if len(d)>0 else Fail
)

# noTerm as [Char] -> parser a -> parser a
noTerm = lambda n,pp:lambda ps: ps(
    ps,
    # lambda v,p,d: Fail if n in v else (
    lambda v,p,d: Fail if len(list(filter(lambda x:x==n,v))) > 1 else (
        let(pp(Accept(v+[n],Node(n,[]),d)),lambda ps1: ps1(
            ps1,
            lambda v,p1,d1: Accept(v,
            p(p,lambda b,la:Node(b,la+[p1]))
            ,d1)
        ))
    )
)

# rep as parser a -> parser a
rep = lambda p:Y(lambda rep:lambda ps: ps(
    ps,
    lambda _,_1,_2: let(p(ps),lambda ps1: ps1(
        ps,
        lambda _,__,___:rep(ps1)
    ))
))

# serial
# ser as [parser a] -> parser a
ser = Y(lambda ser:lambda lp:lambda ps: Fail if len(lp) == 0 else ps(
    ps,
    lambda _,_1,_2: lp[0](ps) if len(lp) == 1 else (
        let(lp[0](ps),
        lambda ps1: ps1(ps1,lambda _,_1,_2: ser(lp[1:])(ps1))
        )
    ) 
))

# paraler
# par as [parser a] -> parser a
par = Y(lambda par:lambda lp:lambda ps:Fail if len(lp)==0 else ps(
    ps,
    lambda _,_1,_2: lp[0](ps) if len(lp) == 1 else (
        let(lp[0](ps),lambda ps1:ps1(
            par(lp[1:])(ps),
            lambda _,_1,_2:ps1
        ))
    )
))

# one or more
# oom as parser a -> parser a
oom = lambda p: ser([p,rep(p)])

# one or none
# oon as parser a -> parser
oon = lambda p:lambda ps: ps(
    ps,
    lambda _,_1,_2: let(p(ps),lambda ps1:ps1(
        ps,
        lambda _,_1,_2: ps1
    ))
)

# is follow
# fto as parser a -> parser a
fto = lambda p: lambda ps: ps(
    ps,
    lambda _,_1,_2: p(ps)(Fail,lambda _,_1,_2:ps)
)

# is not follow
# nof as parser a -> parser a
nof  = lambda p: lambda ps: ps(
    ps,
    lambda _,_1,_2: p(ps)(ps,lambda _,_1,_2:Fail)
)

def printTree(d):
    d(
        lambda a:print("+",a),
        lambda b,la: Const(print(b))(list(map(printTree,la)))
    )

