import sys
sys.setrecursionlimit(100000)
Const = lambda a: lambda b:a
I = lambda x: x
let = lambda a,b: b(a)
Y = lambda f: (lambda x: x(x))(lambda x:f(lambda v:x(x)(v)))

xor = lambda a,b: (a or b) if not (a and b) else False

# data Maybe a is
#   Just a
#   Nothing
# type Maybe a = (a->r)->r->r

# Just as a -> Maybe a
Just = lambda a: lambda Nothing,Just: Just(a)
# Nothing as Maybe a
Nothing = lambda Nothing,Just:Nothing

bindMaybe = Y(lambda bindMaybe:lambda ll:lambda x:
    Just(x) if len(ll) == 0 else (
        let(ll[0](x),lambda mb:mb(
            Nothing,
            lambda x: bindMaybe(ll[1:])(x)
        ))
    )
)

# data RoseTree a b is
#   Leaf a 
#   Node b [RoseTree a b]
Leaf = lambda a: lambda Leaf, Node: Leaf(a)
Node = lambda b, la: lambda Leaf, Node: Node(b,la)

Pair = lambda a,b: lambda f: f(a,b)
fst = lambda n:n(lambda a,b: a)
snd = lambda n:n(lambda a,b: b)

reverce = Y(lambda reverce:lambda l:
    [] if l == [] else (
        reverce(l[1:]) + [l[0]]
    )
)
fold = Y(lambda fold: lambda f:lambda a:lambda l:
    a if l == [] else fold(f)(f(a,l[0]))(l[1:])
)

# match as a -> [(a,a->b)] -> (a->b) -> b
match = Y(lambda match:lambda x:lambda ll:lambda default:
    default(x) if ll == [] else (
        ll[0][1](x) if ll[0][0] == x else match(x)(ll[1:])(default)
    )
)

split = lambda eqf:Y(lambda split:lambda a:lambda l:[a] if l == [] else (
    [a] + split([])(l[1:]) if eqf(l[0]) else split(a+[l[0]])(l[1:])
))([])


qsort = lambda f:Y(lambda qsort:lambda l:[] if l == [] else (
    qsort(list(filter(f(l[0]),l[1:]))) + [l[0]] +
    qsort(list(filter(lambda a:not f(l[0])(a),l[1:])))
))

#  data ParserState a is 
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


sym = term(" \t\n\r'\\.()",True)
d = term("0987654321",False)
q = term("'",False)
nq = term("'",True)
nb = term("\\",True)
b = term("\\",False)
wordL = term("\n\t\r ().\\'",False)

comment = ser([term("#",False),rep(term("\n",True)),term("\n",False)])
skip = oom(term("\t\r ",False))
nln = term("\n",False)
os = term("(",False)
cs = term(")",False)
abst = b
point = term(".",False)
char = ser([q,par([nb,ser([b,term("nrt\\",False)])]),q])
string = ser([q,oom(par([ser([b,q]),nq])),q])
number = ser([oon(term("+-",False)),oom(d)])
infixFlag = par(list(map(lambda x:
    ser(list(map(lambda x:term(x,False),x)) + [fto(wordL)])
    ,["infix","infixr"])))
isw = ser(list(map(lambda x:term(x,False),"is")) + [fto(wordL)])
word = oom(sym)

comment = noTerm("T_comment",comment)
skip = noTerm("T_skip",skip)
nln = noTerm("T_nln",nln)
os = noTerm("T_os",os)
cs = noTerm("T_cs",cs)
abst = noTerm("T_abst",abst)
point = noTerm("T_point",point)
char = noTerm("T_char",char)
string = noTerm("T_string",string)
number = noTerm("T_number",number)
infixFlag = noTerm("T_infixFlag",infixFlag)
isw = noTerm("T_isw",isw)
word = noTerm("T_word",word)

tokenizer = oom(par([comment,skip,nln,os,cs,abst,point,char,string,number,infixFlag,isw,word]))

p = term("1234567890",False)
p1 = ser([oom(p),p])
p2 = oom(p)
p3 = par([p1,p2])
p4 = ser([p3,fto(term(" ",False))])
p5 = noTerm("Num",p4)

endp = tokenizer

class Tok:
    def __init__(self,n,d):
        self.n=n
        self.d=d
    def __eq__(self,b):
        return self.n == b.n
    def __str__(self):
        return self.n + ':' + str(self.d)
unionRootToList = lambda tree:tree(
    Const(Nothing),
    lambda b,la: Just(list(map(lambda x:x(
        Const(None),
        lambda n,d:Tok(n,''.join(list(map(lambda x:x(I,""),d))))
    ),la)))
)

strConstToCode = Y(lambda f: lambda s:
    ' []' if s == '' else '\''+s[0]+'\':' + f(s[1:])
)
fixThreadWithStrings = Y(lambda f: lambda l:
    [] if l == [] else (
        (toTokens(strConstToCode(l[0].d[1:-1]))(I,I) if l[0].n == 'T_string' else [l[0]]) + f(l[1:])
    )
)
# toTokens as [Char] -> Maybe (List (Tok [Char]))
toTokens = lambda s:bindMaybe([
    parse(tokenizer),
    unionRootToList,
    lambda a:Just(fixThreadWithStrings(a))
])(s)


nln = rep(term([Tok("T_nln",'')],False))
# var = noTerm("P_var",term([
var = term([
    Tok("T_word",''),
    Tok("T_char",''),
    Tok("T_string",''),
    Tok("T_number",'')
],False)#)

abst = lambda expr: noTerm("P_abst",ser([
    term([Tok("T_abst",'')],False),
    noTerm("P_args",oom(term([Tok("T_word",'')],False))),
    term([Tok("T_point",'')],False),
    expr
]))

abstInScobe = lambda expr: noTerm("P_abst",ser([
    term([Tok("T_abst",'')],False),
    noTerm("P_args",oom(
        ser([
            term([Tok("T_word",'')],False),
            nln
        ])
    )),
    term([Tok("T_point",'')],False),
    nln,
    expr
]))

exprInScobe = Y(lambda expr:
    noTerm("P_expr",oom(par([
        ser([
            nln,
            abstInScobe(expr),
            nln
        ]),
        ser([
            nln,
            var,
            nln
        ]),
        ser([
            nln,
            term([Tok("T_os",'')],False),
            nln,
            expr,
            nln,
            term([Tok("T_cs",'')],False),
            nln,
        ])
    ])))
)
expr = Y(lambda expr:
    noTerm("P_expr",oom(par([abst(expr),var,ser([
        term([Tok("T_os",'')],False),
        exprInScobe,
        term([Tok("T_cs",'')],False),
    ])])))
)
options = noTerm("P_options",par([ser([
        term([Tok("T_infixFlag",'')],False),
        term([Tok("T_number",'')],False),
]),empty]))

dec = noTerm("P_dec",ser([
    options,
    term([Tok("T_word",'')],False),
    term([Tok("T_isw",'')],False),
    expr,
    rep(term([Tok("T_nln",'')],False)),
]))
start = ser([
    rep(term([Tok("T_nln",'')],False)),
    rep(dec)
])

# delUnUsedWords as RoseTree (Tok) b -> Maybe (RoseTree (Tok) b)
delUnUsedWords = Y(lambda delUnUsedWords:lambda tr:tr(
    lambda a: Nothing if a.n in ["T_nln","T_isw","T_abst","T_point","T_os","T_cs"] else Just(tr),
    lambda d,la: Just(Node(d,
        list(map(lambda a:a(None,I),
        list(filter(lambda a:a(False,Const(True)),
        list(map(delUnUsedWords,la))
        ))
        ))
    ))
))

getInfixNames = Y(lambda getInfixNames: lambda tr:tr(
    [],
    lambda b,la:fold(lambda a,c:a+getInfixNames(c))([])(la) if b!="P_dec" else (
        let(la[0](I,lambda _,la: ("_",0) if len(la)<2 else (
            la[0](lambda a:a.d,lambda _,__:"ERR"),
            int(la[1](lambda a:a.d,lambda _,__:"ERR"))
            )),lambda opts:
        [(la[1](lambda a:a.d,lambda _,__:"ERR"),opts)] if opts[0] in ["infix","infixr"] else []
        )
    )
))

eqInfixRec = lambda a: lambda b: a[1][1]>b[1][1]

fixWithInfix = lambda eqf,struct,s,b:Y(lambda fix:lambda l:
    l if l == [] else (
        let(split(eqf)(l),lambda l1: 
            fold(lambda a,c:struct(s,a,c))(l1[0])(l1[1:]) if not b else (
                let(reverce(l1),lambda l1:
                    fold(lambda a,c:struct(s,c,a))(l1[0])(l1[1:])
                )
            )
        )
    )
)
fixTreeInfix = lambda s:Y(lambda fix: lambda tr:tr(
    lambda _:tr,
    lambda b,la:Node(b,
        fixWithInfix(
            lambda a:a(lambda n:n.d==s[0],lambda _,__,:False),
            lambda a,b,c:[Node("P_expr",a+[Node('P_expr',b)]+[Node('P_expr',c)])],
            [Leaf(Tok('T_word',s[0]))],
            s[1][0]=='infixr')(list(map(fix,la)))
        )
))

fixAllTree = lambda lofs:Y(lambda fixAllTree:lambda tr:tr(
    Const(tr),
    lambda b,la:Node(b,list(map(fixAllTree,la))) if not b in ['P_expr','P_abst'] else(
        fold(lambda a,c:fixTreeInfix(c)(a))(tr)(lofs)
    )
))

optimisateTreeForExpt = Y(lambda fix:lambda tr:tr(
    Const(tr),
    lambda b,la: Node(b,list(map(fix,la))) if b != 'P_expr' or len(la)!=1 else (
        fix(la[0])
    )
))
parseToST = bindMaybe([
    toTokens,
    lambda a:Just(list(filter(lambda x:not x.n in ["T_skip",'T_comment'],a))),
    # lambda a: Just(Const(a)(print(fold(lambda a,c:a+str(c)+'\n')("")(a)))),
    parse(start),
    delUnUsedWords,
    lambda a: Just(fixAllTree(qsort(eqInfixRec)(getInfixNames(a)))(a)),
    lambda a: Just(optimisateTreeForExpt(a))
])

App = lambda es: lambda app,lam,word,number,character:app(es)
Lam = lambda w,e: lambda app,lam,word,number,character:lam(w,e)
Word = lambda n: lambda app,lam,word,number,character:word(n)
Number = lambda d: lambda app,lam,word,number,character:number(d)
Character = lambda c: lambda app,lam,word,number,character:character(c)

# LExpr = LApp M N | LVar a | Lam x LExpr
LApp = lambda M,N: lambda App,Var,Lam:App(M,N)
LVar = lambda a: lambda App,Var,Lam:Var(a)
Lam = lambda x,M: lambda App,Var,Lam:Lam(x,M)


getChildren = lambda n:n(Const([]),lambda _,la: la)
getName = lambda l: l(lambda t:t.d,lambda _,__:'')
toExprST = Y(lambda f: lambda tr:tr(
    lambda t:match(t.n)([
        ('T_word',lambda w: LVar(t.d)),
        ('T_number',lambda d: Number(int(t.d))),
        ('T_char',lambda c: Character(t.d))
    ])(lambda a:Const(a)(print(a))),
    lambda b,la: match(b)([
        ('P_expr',lambda _: let(list(map(f,la)),lambda la:
            # fold(App)(la[0])(la[1:])
            fold(LApp)(la[0])(la[1:])
            # App(la)
        )),
        ('P_abst',lambda _: let(list(map(getName,getChildren(la[0]))),lambda largs:
            # Lam(largs,f(la[1]))
            fold(lambda a,x:Lam(x,a))(f(la[1]))(list(reversed(largs)))
        ))
    ])(lambda a:Const(a)(print(a)))
))

# toListOfExprs as RoseTree Tok [Char] -> Maybe [([Char],expr)]
toListOfExprs  = lambda tr: (
    tr(
        Const(Nothing),
        lambda b,la:Just(list(map(lambda x:x(
            print,
            lambda b,la: (getName(la[1]),toExprST(la[2]))
        )
        ,la)))
    )
)

err = bindMaybe([
    parseToST,
    # toDot,
    toListOfExprs
])(
'''
n0 is \\z s.z
succ is \\a z s.s a
I is \\x.x
pred is \\a.a n0 I
om is \\x.x x
Y is \\f.om \\x.f (x x)
add is Y \\f a b.a b \\pa. b a \\_.f pa (succ b)

mult1 is Y \\f a b.a b \\pa.add b (f pa b)
mult is \\a b.a n0 \\pa.b n0 \\_.mult1 pa b
fac is Y \\f n.n (succ n0) \\pn.mult n (f pn)
tmp is fac (succ (succ (succ (succ (succ n0)))))

cons is \\a b nil cons.cons a b
nil is \\a b.a
repeat is \\a.Y \\f.cons a (f)
takeN is Y \\f a l.a nil \\pa.l nil \\x xs.cons x (f pa xs)
tail is \\a.a nil \\_ xs.xs
head is \\a.a nil \\x _.x
# main is  head (tail  (takeN (succ(succ (succ n0))) (repeat (succ (succ n0)))) )
main is fac (succ (succ (succ (succ (succ (succ (succ (succ (succ (succ n0))))))))))
# head (tail (cons n0 (cons (succ n0) nil)))

'''
)(
    "Error",
    I#Const("//Ok")
)
# print(err)
# (S (S KS (S (KK) S)) (KK)) = B
# (S (KS) K)

#SKIBC
S = lambda S,K,I,B,C:S()
K = lambda S,K,I,B,C:K()
I = lambda S,K,I,B,C:I()
B = lambda S,K,I,B,C:B()
C = lambda S,K,I,B,C:C()

# S = \f g x.f x (g x)
# I = \x.x
# K = \a b.a
# B = \f g x.f x g
# C = \f g x.f (g x)

# [x] = x
# [M N] = [M] [N]
# [\x.x] = I
# [\x.N] = K N | !f(N)
# [\x.M x] = M | f(x,M)
# [\x.M N] = B [\x.M] N | f(x,M), !f(x,N)
# [\x.M N] = C M [\x.N] | !f(x,M), f(x,N)
# [\x.M N] = S [\x.M] [\x.N] | f(x,M), f(x,N)

# BCI -> I
# BKI -> I
# CxI -> x

# B(CCx)I -> x
# B (C B (C C)) I -> I?

# Expr = App M N | Var a | Comb b
App = lambda M,N: lambda App,Var,Comb:App(M,N)
Var = lambda a: lambda App,Var,Comb:Var(a)
Comb = lambda b: lambda App,Var,Comb:Comb(b)



Y = lambda f:(lambda x:x(x))(lambda x:lambda v:f(x(x))(v))

showCombExpr = Y(lambda f:lambda x:x(
    lambda M,N: '('+f(M)+' '+f(N)+')',
    lambda a: str(a),
    lambda b:b(
        lambda: 'S',
        lambda: 'K',
        lambda: 'I',
        lambda: 'B',
        lambda: 'C'
    )
))
isFree = lambda X:Y(lambda f:lambda t:t(
    lambda M,N: f(M) and f(N),
    lambda a: a != X,
    lambda x,M: (x == X) or f(M)
))

test = Lam('f',LApp(Lam('y',LApp(LVar('y'), LVar('y'))),Lam('x',LApp(LVar('f'), LApp(LVar('x'), LVar('x'))))))

# Lam('x',LApp(LVar('x'), LVar('x')))
# Lam('f',LApp(Lam('x',LApp(LVar('x'), LVar('x'))), Lam('x',LApp(LVar('f'), LApp(LVar('x'), LVar('x'))))))
# Lam('f',
#             Lam('g',
#                         LApp(LVar('g'),LVar('f'))
#             )
#         )
# print(isFree('x')(test))
LamToSKI = Y(lambda f:lambda t:t(
    lambda M,N: App(f(M),f(N)),
    lambda a: Var(a),
    lambda x,M: LApp(LVar(K),f(M)) if isFree(x)(M) else M(
        lambda M,N: (lambda mf,nf:
            f(M) if mf and (N(lambda _,__:False,lambda a: a==x,lambda _,__:False)) else
            LApp(f(M),f(N)) if mf and nf else (
                LApp(LApp(LVar(C),f(M)),f(Lam(x,N))) if mf and (not nf) else (
                    LApp(LApp(LVar(B),f(Lam(x,M))),f(N)) if (not mf) and nf else (
                        LApp(LApp(LVar(S),f(Lam(x,M))),f(Lam(x,N)))
                    )
                )
            )
        )(isFree(x)(M),isFree(x)(N)),
        lambda a: LVar(I) if x == a else LApp(LVar(K),M),
        lambda X,M:f(Lam(x,f(Lam(X,M))))
    )
))
toSKITree = Y(lambda f: lambda t:t(
    lambda M,N: App(f(M),f(N)),
    lambda a: Var(a) if type(a) == str else Comb(a),
    lambda x,M:print(x)
))
# evalSki = Y(lambda eval:lambda t:t(
#     lambda M,N: eval(M)
# ))
mainL = err[-1][1]
mainL = fold(lambda m,n:
    Y(lambda f:lambda t:t(
        lambda M,N:LApp(f(M),f(N)),
        lambda a:n[1] if a == n[0] else t,
        lambda x,M: t if x == n[0] else Lam(x,f(M))
    ))(m)
)(mainL)(list(reversed(err[:-1])))
testSki = toSKITree(LamToSKI(mainL))
print(showCombExpr(testSki))

# 1 - App
# 0001 S
# 0010 K
# 0011 I
# 0100 B
# 0101 C
toLists = Y(lambda f:lambda t:t(
    lambda M,N:f(M)+[f(N)], #(lambda h:[h] if len(h) > 1 else h)(f(N)),
    lambda a:None,
    lambda b:b(
        lambda: ['S'],
        lambda: ['K'],
        lambda: ['I'],
        lambda: ['B'],
        lambda: ['C']
    )
))
def evalS(t):
    while True:
        b,t = ((True,t[0]+t[1:]) if type(t[0]) == list else
        ((False,t) if len(t) < 4 else (True,t[1]+[t[3],t[2]+[t[3]]]+t[4:])) if t[0] == 'S' else
        ((False,t) if len(t) < 3 else (True,t[1]+t[3:]) ) if t[0] == 'K' else
        ((False,t) if len(t) < 2 else (True,t[1]+t[2:]) ) if t[0] == 'I' else
        ((False,t) if len(t) < 4 else (True,t[1]+[t[3],t[2]]+t[4:]) ) if t[0] == 'B' else
        ((False,t) if len(t) < 4 else (True,t[1]+[t[2]+[t[3]]]+t[4:]) ) if t[0] == 'C' else
        (False,t))
        if not b:
            break
    return t

# evalS = Y(lambda f:lambda t:
#         f(t[0]+t[1:]) if type(t[0]) == list else
#         (t if len(t) < 4 else f(t[1]+[t[3],t[2]+[t[3]]]+t[4:])) if t[0] == 'S' else
#         (t if len(t) < 3 else f(t[1]+t[3:]) ) if t[0] == 'K' else
#         (t if len(t) < 2 else f(t[1]+t[2:]) ) if t[0] == 'I' else
#         (t if len(t) < 4 else f(t[1]+[t[3],t[2]]+t[4:]) ) if t[0] == 'B' else
#         (t if len(t) < 4 else f(t[1]+[t[2]+[t[3]]]+t[4:]) ) if t[0] == 'C' else
#         print('ERROR',t)
#     )
# print(toLists(testSki))
T = toLists(testSki)
print(T)
def compil(l):
    if(len(l)==1):
        print('pushNode('+l[0]+');');
    else:
        list(map(compil,list(reversed(l))))
        print('buildApp(',len(l),');',sep='')
compil(T)
# print(evalS(T))
getSize = Y(lambda f:lambda t:t(
    lambda M,N:f(M)+f(N)+1,
    lambda a:-10**5,
    lambda c: 4
))
print(getSize(testSki))
