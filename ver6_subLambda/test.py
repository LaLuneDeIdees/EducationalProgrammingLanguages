import sys
sys.setrecursionlimit(10000)

from util import (I,bindMaybe,Nothing,
                  Just,Const,fold,Y,let,
                  Leaf,Node,qsort,split,reverce,
                  match,find)

from lexer import toTokens,Tok

from showTree import toDot,toDotExpr,endWrite
from parser import parseToST

# data expr is
#   App [expr]
#   Lam [[Char]] expr
#   Word [Char]
#   Number Num
#   Character Char
App = lambda es: lambda app,lam,word,number,character:app(es)
Lam = lambda w,e: lambda app,lam,word,number,character:lam(w,e)
Word = lambda n: lambda app,lam,word,number,character:word(n)
Number = lambda d: lambda app,lam,word,number,character:number(d)
Character = lambda c: lambda app,lam,word,number,character:character(c)

getChildren = lambda n:n(Const([]),lambda _,la: la)
getName = lambda l: l(lambda t:t.d,lambda _,__:'')
toExprST = Y(lambda f: lambda tr:tr(
    lambda t:match(t.n)([
        ('T_word',lambda w: Word(t.d)),
        ('T_number',lambda d: Number(int(t.d))),
        ('T_char',lambda c: Character(t.d))
    ])(lambda a:Const(a)(print(a))),
    lambda b,la: match(b)([
        ('P_expr',lambda _: let(list(map(f,la)),lambda la:
            # fold(App)(la[0])(la[1:])
            App(la)
        )),
        ('P_abst',lambda _: let(list(map(getName,getChildren(la[0]))),lambda largs:
            Lam(largs,f(la[1]))
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
# disFreeExpr as [([Char],expr)] -> expr -> expr
disFreeExpr = Y(lambda f: lambda pd:lambda e:
    e(
        lambda al:let(fold(lambda a,c:
            let(f(pd)(c),lambda rs:
                (a[0]+[rs[0]],
                a[1]+list(filter(lambda x:not x in a[1],rs[1])))
            )
        )(([],[]))(al),lambda rs:
            (App(rs[0]),rs[1])
        ),
        lambda wl,el:let(f(pd+wl)(el),lambda unfree:
                let(list(filter(lambda a:not a in wl,unfree[1])),lambda un1:
                    (App([Lam(un1+wl,unfree[0])] + list(map(Word,un1))),un1)
                    if len(un1) > 0 else (Lam(wl,unfree[0]),[])
                )
        ),
        lambda w:(e,[w]) if w in pd else (e,[]),
        lambda n:(e,[]),
        lambda c:(e,[])
    )
)([])
# lambdaDisFree as [([Char],expr)] -> Maybe [([Char],expr)]
lambdaDisFree = lambda ls: Y(lambda f:lambda l:
    [] if l == [] else (
        [(l[0][0],
        disFreeExpr(l[0][1])[0] )] + 
        f(l[1:])
    )
)(ls)

# codeName as [Char] -> [Char]
codeName = lambda a:'f_'+''.join(list(map(lambda a:hex(ord(a)+0x100)[3:],a)))

seed = 0
def getSeed():
    global seed
    seed+=1
    return seed
# compileExpr as expr -> ([Char],[Char])
costForAlloc = Y(lambda f: lambda e:e(
    lambda es: fold(lambda a,x: a+f(x))(len(es)+2)(es),
    lambda ws,e:0,
    Const(0),
    Const(0),
    Const(0)
))

compileExpr = Y(lambda f:lambda ps:lambda e:e(
    lambda es:let(fold(lambda a,x:
                let(f(ps)(x),lambda proc:
                    (a[0]+proc[0],a[1]+proc[1]+'*(DPtr+'+str(a[2])+') = res;\n',a[2]-1)
                ))(('',
               'if(1){\n'+
                    'struct ConsPull* p1 = alloc('+str(len(es))+');\n' +
                    'p1->nodeType = ID_THUNK;\n'+
                    'void** DPtr = p1->data;\n'
                    ,len(es)-1
                    ))(es),lambda fs:(fs[0],fs[1] + 
                    'res = p1;\n'+
                    '}\n')),
    lambda ws,e: let('f_tmp_'+str(getSeed()),lambda thin:
            let(f(ws)(e),lambda proc:
            (proc[0] + '\nvoid '+thin+'(){\n'+
                'struct ConsPull* res;\n'+
                'checks('+str(len(ws))+',1){\n' + 
                proc[1]+
                '\n'.join(['dealloc(*(PC-'+str(i)+'));' for i in range(len(ws)+1)]) +
                '\nPC-=' + str(len(ws)) +';\n'+
                '*PC=res;\n'
                '}\n}\n','res = alloc(0);\n'+
                         'res->nodeType = ID_FUNCTION;\n'+
                         'res->data = '+thin+';\n')
            )),
    lambda w:('','res = newFunction('+codeName(w)+');\n') if not w in ps else (
        '',
        'res = copy(*(PC-'+str(find(lambda x:x==w)(ps)(I,I)+1)+'));\n'
    ),
    lambda n:('','res = newInt('+str(n)+');\n'),
    lambda c:('','res = newInt('+str(ord(c[1]))+');\n')
))([])

# compileWithName as ([Char], expr) -> [Char]
compileWithName = lambda p:let(compileExpr(p[1]),lambda c:
    c[0] + '\n' +
    'void '+codeName(p[0])+'(){\n' +
        'struct ConsPull* res;\n'+
        c[1]+'\n'+
        'dealloc(*PC);'+
        '*PC = res;\n'
    '}\n'
)
# compileExpr = Y(lambda f:lambda ps:lambda e:e(
#     lambda es:let(fold(lambda a,x:
#                 let(f(ps)(x),lambda proc:
#                     (a[0]+proc[0],a[1]+proc[1]+'*(DPtr+'+str(a[2])+') = res;\n',a[2]-1)
#                 ))(('',
#                'if(1){\n'+
#                     'void** DPtr = alloc('+str(len(es))+');\n'
#                     ,len(es)-1
#                     ))(es),lambda fs:(fs[0],fs[1] + 
#                     'res = DPtr;\n'+
#                     '}\n')),
#     lambda ws,e: let('f_tmp_'+str(getSeed()),lambda thin:
#             let(f(ws)(e),lambda proc:
#             (proc[0] + '\nvoid '+thin+'(){\n'+
#                 'void** res;\n'+
#                 'checkArgs('+str(len(ws))+'){\n'+
#                 let(costForAlloc(e),lambda cost:
#                     '' if cost == 0 else 'checkHeap('+str(cost)+');\n') + 
#                 proc[1]+
#                 'PC-=' + str(len(ws)) +';\n'+
#                 '*PC=res;\n'
#                 '}\n}\n','res = '+thin+';\n')
#             )),
#     lambda w:('','res = '+codeName(w)+';\n') if not w in ps else (
#         '',
#         'res = *(PC-'+str(find(lambda x:x==w)(ps)(I,I)+1)+');\n'
#     ),
#     lambda n:('','res = '+hex((1<<63)|n)+';\n'),
#     lambda c:('','res = '+hex((1<<63)|ord(c[1]))+';\n')
# ))([])

# # compileWithName as ([Char], expr) -> [Char]
# compileWithName = lambda p:let(compileExpr(p[1]),lambda c:
#     c[0] + '\n' +
#     'void '+codeName(p[0])+'(){\n' +
#         'void** res;\n'+
#         c[1]+'\n'+
#         '*PC = res;\n'
#     '}\n'
# )

err = bindMaybe([
    parseToST,
    # toDot,
    toListOfExprs,
    lambda a: Just(lambdaDisFree(a)),
    lambda a: Just(Const(a)(print( ''.join(list(map(lambda x:'void '+codeName(x[0])+'();\n',a)))+
        '\n\n\n'+
        ''.join(list(map(lambda x:compileWithName(x),a)))))),
    lambda a:Just(list(map(lambda c:toDotExpr(codeName(c[0]),c[1]),a))),
    endWrite
])(
'''
# [] is \\a b.a
# infixr 1 : is \\x y a b.b x y
# tmpStr is 'Hello, world!'
# I is \\x.x
# n0 is \\s x.x
# succ is \\n s x.n s
# pred is \\n.n n0 I
# ww is \\x.x x
# infix 0 |> is \\a b.b a
# infixr 0 <| is \\a b.a b
# Y is \\f.ww \\x.f <| x x
# add is Y(\\add a b.b
    # a
    # \\pb.a b \\_.add (succ a) pb
# )
add is \\a b.eval a \\a.eval b \\b.addInt a b
infix 2 + is add
sub is \\a b.eval a \\a.eval b \\b.subInt a b
infix 2 - is sub
isZ is \\a.eval a \\a.isZero a

# sumN is \\n.n + n + n + n

# fib is \\n.eval n \\n. isZ (subInt n 2) 1 (fib (subInt n 1) + fib (subInt n 2))
# fib is \\n.eval n \\n. isZ ((\\n.subInt n 2) n) 1 ((\\n.fib ((\\n.subInt n 1) n) + fib ((\\n.subInt n 2) n)) n )
Y is (\\f.f (Y f))

# fib is \\n.isZ (n - 2) 1 (fib (n - 1) + fib (n - 2))

main is eval ((Y \\f n.isZ n 0 (f (n - 1) + n)) 10) printInt

'''
# fib 30
# real    0m1,191s
# user    0m1,020s
# sys     0m0,169s
# optimize to with GC
# real    0m0,827s
# user    0m0,709s
# sys     0m0,117s
# optimize to with code //memory use over 128M/256M
# real    0m0,508s
# user    0m0,400s
# sys     0m0,107s
# new GC,new functions //memory use 1.7M
# real    0m0,288s
# user    0m0,284s
# sys     0m0,004s
# nextStage: memoized & best compiled
# |now 300 lines for prev test of generated C code


)(
    "Error",
    Const("//Ok")
)

print(err)
