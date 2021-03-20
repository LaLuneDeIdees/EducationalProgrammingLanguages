def fold(f,l,a):
    if l == []:
        return a
    return fold(f,l[1:],f(a,l[0]))
def foldt(f,l):
    if l == []:
        return l
    return fold(f,l[1:],l[0])
def foldr(f,l,a):
    if l == []:
        return a
    return f(l[0],foldr(f,l[1:],a))
def foldrt(f,l):
    if l == []:
        return l
    return foldr(f,l[:-1],l[-1])

def xor(a,b):
    return not ((a and b) or (not a or b))
def leter(l,i=False):
    def parse(d,p):
        if len(p)==0:
            return (None,p)
        if xor(p[0] in l,i):
            return (d + [p[0]],p[1:])
        return (None,p)
    return parse
def empty(d,p):
    return (d,p)
def ser(a,b):
    def parse(d,p):
        d1,p1 = a(d,p)
        if d1 == None:
            return (None,p1)
        return b(d1,p1)
    return parse
def serial(l):
    return foldrt(ser,l)
def par(a,b):
    def parse(d,p):
        d1,p1 = a(d,p)
        if d1 != None:
            return (d1,p1)
        d2, p2 = b(d,p)
        if d2 != None:
            return (d2,p2)
        return (None,p1)
    return parse
def paraler(l):
    return foldrt(par,l)
def rep(a):
    def parse(d,p):
        d1,p1 = a(d,p)
        if d1 == None:
            return (d,p)
        return parse(d1,p1)
    return parse
def word(s):
    return serial(list(map(leter,s)))
class Tok:
    def __init__(self,n,d):
        self.n=n
        self.d=d
    def __eq__(self,other):
        return self.n==other.n
    def __str__(self):
        return str(self.n) + ' -> [' + ', '.join(list(map(str,self.d))) + ']'
        #str(self.d)
def term(a,n):
    def parse(d,p):
        d1,p1 = a([],p)
        if d1 == None:
            return (None,p1)
        return (d+[Tok(n,d1)],p1)
    return parse
def notSave(a):
    def parse(d,p):
        d1,p1 = a(d,p)
        if d1 != None:
            return (d,p1)
        return (None,p1)
    return parse

import sys
sys.setrecursionlimit(10000)

#lexer
lam = term(leter('\\'),'lambda')
bbb = leter('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890`')
to = term(word('->'),'to')
word = term(ser(bbb,rep(bbb)),'word')
point = term(leter('.'),'point')
skip = term(leter(' \t\n'),'skip')
os = term(leter('('),'os')
cs = term(leter(')'),'cs')

toTokens = rep(paraler([lam,to,word,point,skip,os,cs]))
#parser
tlWord = leter([Tok('word','')])
wordList = term(serial([tlWord,rep(tlWord)]),'wordList')
def atom(d,p):
    return paraler([tlWord,serial([
        notSave(leter([Tok('os','')])),
        expr,
        notSave(leter([Tok('cs','')])),
    ]),
    lam])(d,p)
expr = term(serial([atom,rep(atom)]),'expr')
lam = term(serial([
    notSave(leter([Tok('lambda','')])),
    wordList,
    notSave(leter([Tok('point','')])),
    expr
]),'Lambda')
##############

def fixScopes(t):
    if type(t)!=Tok:
        return t
    if t.n == 'expr':
        if len(t.d) == 1:
            return fixScopes(t.d[0])
    return Tok(t.n,list(map(fixScopes,t.d)))


class F:
    def __init__(self,a,c):
        self.a=a
        self.c=c
    def __str__(self):
        return 'F('+str(self.a)+', '+str(self.c)+')'

class A:
    def __init__(self,a,c):
        self.a=a
        self.c=c
    def __str__(self):
        return 'A('+str(self.a)+', '+str(self.c)+')'

def fixToTree(t):
    if type(t) != Tok:
        return t
    if t.n == 'Lambda':
        a = foldr(lambda a,x:F(''.join(a.d),x),t.d[0].d,fixToTree(t.d[1]))
        return a
    if t.n == 'expr':
        a = foldt(lambda a,x:A(fixToTree(a),fixToTree(x)),t.d)
        return a
    if t.n == 'word':
        return ''.join(t.d)
    return t


def isFree(n,t):
    if type(t)==F or type(t)==A:
        return isFree(n,t.a) or isFree(n,t.c)
    return n==t
def toSKI_AP(t):
    if type(t) == F:
        t.c = toSKI_AP(t.c)
        if t.a == t.c:
            return 'I'
        if type(t.c) != A:
            return A('K',toSKI_AP(t.c))
        else:
            a1 = isFree(t.a,t.c.a)
            b1 = isFree(t.a,t.c.c)
            if a1 and b1:
                return A(A('S',toSKI_AP(F(t.a,t.c.a))),
                           toSKI_AP(F(t.a,t.c.c)))
            if a1:
                return A(A('B',toSKI_AP(F(t.a,t.c.a))),
                           t.c.c)
            if b1:
                return A(A('C',t.c.a),
                           toSKI_AP(F(t.a,t.c.c)))
            return A('K',t.c)
        pass
    if type(t) == A:
        return A(toSKI_AP(t.a),toSKI_AP(t.c))
        # pass
    return t

def AtoList(t):
    if type(t) == A:
        if type(t.c) != A:
            return AtoList(t.a) + [t.c]
        return AtoList(t.a)+[AtoList(t.c)]
        # return t
    return [t]


pc = open('main.lam','r').read()
pc = pc.split('\n')
pc = list(filter(lambda x: x!='' and x[0]!='#',pc))
pc = list(map(lambda x:x.split('='),pc))
pc = list(map(lambda x:(x[0].split(),x[1]),pc))
def foldToLambda(a,x):
    head,tail = a
    head += '(\\'+x[0][0]+'.'
    tail = ')(' +x[1]+')' + tail
    print(x)
    return (head,tail)
pc = fold(foldToLambda,pc,('',''))
pc = pc[0] + 'main'+pc[1]

s=pc
print(s)

l,p = toTokens([],s)
l = list(filter(lambda x:x!=Tok('skip',''),l))

pp,p = expr([],l)
# print('Parser')
# print(pp,fold(lambda a,x:a+str(x)+'\n',p,''))
pp = fixScopes(pp[0])
# print(pp)
pp = fixToTree(pp)
print(pp)
pp = toSKI_AP(pp)
print(pp)
pp = AtoList(pp)
print(pp)

# pp = compile(pp,0)
# pp = pp[2]
# for l in range(16,len(pp),16):
#     list(map(lambda x: print(x,end=','),pp[l-16:l]))
#     print()
# print(pp)

print()
def compile1(t,a=0):
    if type(t) != list:
        if t == 'I':
            return (0x8001,[])
        if t == 'K':
            return (0x8002,[])
        if t == 'S':
            return (0x8003,[])
        if t == 'C':
            return (0x8004,[])
        if t == 'B':
            return (0x8005,[])
        print("EEEE:",t)
        sys.exit(1)
        return (0xFFFF,[])
    # print(t)
    size = len(t)
    memout = [0x8000]*(size+1)
    for i in range(size):
        c,mm = compile1(t[i],a+len(memout))
        size += len(mm)
        memout[i]=c
        memout+=mm
    return (a,memout)

binC = compile1(pp)[1] + [0x8000]
ff = open("rom.c",'r').read();
outt = ff.split("__EDIT_LABEL__")[0]+"__EDIT_LABEL__\n"
outt += 'unsigned short pr[] = {\n\t'
outt += fold(lambda a,x:(a[0]+hex(x)+', '+('\n\t' if a[1]%16==0 else ''),a[1]+1),binC,("",1))[0]
outt += '\n};'
print(outt)
fff = open("rom.c",'w')
fff.write(outt)
fff.close()