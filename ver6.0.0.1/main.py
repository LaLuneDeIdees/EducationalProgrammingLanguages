import myFL as lexer
import myFP as parser
import drawTree as dt
import functools as f
import sys
import hash


s = open('cmp.txt','r').read()
# print(s)
ss = lexer.getAllTokens(s)
ss = list(filter(lambda x:not x[0] in [
        lexer.tT_skip,
        lexer.tT_preproc,
        lexer.tT_comment
    ],ss))
tree,sss = parser.P_START([],ss)
tree = tree[0]
# print(tree)
# print(sss)
def getAllInfix(s):
    def tmp(a,x):
        if x[0] == parser.pP_Dec:
            if x[1][1][1] != []:
                mode = x[1][1][1][0][1]
                modeTo = mode == 'infixr'
                return a+[(x[1][0][1],modeTo)]
        return a
    return f.reduce(tmp,s,[])

tInfix = getAllInfix(tree[1])
tInfix = hash.create(127,tInfix)

def In(tInfix, s):
    return hash.get(tInfix,s) != None
get = lambda t: lambda s: hash.get(t,s)
isR = get(tInfix)

print(isR('>>>'))
dt.draw(tree)
s