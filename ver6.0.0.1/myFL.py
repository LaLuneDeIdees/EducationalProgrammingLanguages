
import functools as f

def empty(i,s):
    return [i]
def sim(c,isIn=0):
    def parse(i,s):
        if i >= len(s):
            return []
        if isIn == 0:
            if s[i] in c:
                return [i+1]
            return []
        else:
            if s[i] in c:
                return []
            return [i+1]
    return parse
def app(a,b):
    def parser(i,s):
        t1 = map((lambda x:b(x,s)),a(i,s))
        t2 = f.reduce((lambda x,y:x+y),t1,[])
        return t2
    return parser

def par(a,b):
    def parser(i,s):
        t1 = a(i,s)
        t2 = b(i,s)
        return max(t1,t2)
    return parser

def rep(a):
    def parser(i,s):
        t1 = a(i,s)
        if t1 != [] and t1[0] > i:
            return parser(t1[0],s)
        return [i]
    return parser
def serial(s):
    if s == []:
        return empty
    elif len(s)==1:
        return s[0]
    else:
        return app(s[0],serial(s[1:]))

def mor(s):
    if s == []:
        return empty
    elif len(s)==1:
        return s[0]
    else:
        return par(s[0],mor(s[1:]))

def word(s):
    if s == '':
        return empty
    if len(s) == 1:
        return sim(s)
    return app(sim(s[0]),word(s[1:]))

tT_NONE = 0
forWord = serial([sim('1234567890\\ \t\n;(){}[]',1),])
forWordWithNum = serial([mor([sim('1234567890'),forWord,]),])
T_word = serial([forWord,rep(forWordWithNum,),])
d = serial([sim('0987654321'),])
nums = serial([d,rep(d,),])
float1 = serial([sim('.'),nums,])
float = serial([mor([float1,empty,]),])
expon1 = serial([sim('eE'),mor([sim('+-'),empty,]),nums,])
expon = serial([mor([expon1,empty,]),])
dec = serial([nums,float,expon,])
bin = serial([sim('0'),sim('b'),sim('01'),rep(sim('01'),),])
af = serial([sim('0987654321abcdefABCDEF'),])
hex = serial([sim('0'),sim('x'),af,rep(af,),])
T_number = serial([mor([dec,hex,bin,]),])
literal1 = serial([sim('\\'),sim('\''),])
literal2 = serial([mor([sim('\'',1),literal1,empty,]),])
T_literal = serial([sim('\''),rep(literal2,),sim('\''),])
T_skip = serial([sim(' \t'),rep(sim(' \t'),),])
T_nln = serial([sim('\n'),rep(sim('\n'),),])
T_slash = serial([sim(';'),])
T_comment = serial([sim('/'),sim('/'),rep(sim('\n',1),),])
T_preproc = serial([sim('#'),rep(sim('\n',1),),])
T_OPEN_S = serial([sim('('),])
T_CLOSE_S = serial([sim(')'),])
T_OPEN_C = serial([sim('{'),])
T_CLOSE_C = serial([sim('}'),])
T_OPEN_I = serial([sim('['),])
T_CLOSE_I = serial([sim(']'),])
T_GET_ADDR = serial([sim('&'),])
T_RIGHT_ARROW = serial([sim('-'),sim('>'),])
T_LAMBDA = serial([sim('\\'),])
T_SEM = serial([sim(','),])
T_is = serial([word('is'),])
T_type = serial([word('type'),])
T_import = serial([word('import'),])
T_binary = serial([mor([word('infixl'),word('infixr'),]),])
tT_word = 1
tT_number = 2
tT_literal = 3
tT_skip = 4
tT_nln = 5
tT_slash = 6
tT_comment = 7
tT_preproc = 8
tT_OPEN_S = 9
tT_CLOSE_S = 10
tT_OPEN_C = 11
tT_CLOSE_C = 12
tT_OPEN_I = 13
tT_CLOSE_I = 14
tT_GET_ADDR = 15
tT_RIGHT_ARROW = 16
tT_LAMBDA = 17
tT_SEM = 18
tT_is = 19
tT_type = 20
tT_import = 21
tT_binary = 22
lexerList = [
T_word,T_number,T_literal,T_skip,T_nln,T_slash,T_comment,T_preproc,T_OPEN_S,T_CLOSE_S,T_OPEN_C,T_CLOSE_C,T_OPEN_I,T_CLOSE_I,T_GET_ADDR,T_RIGHT_ARROW,T_LAMBDA,T_SEM,T_is,T_type,T_import,T_binary,]
tokenIdList = [
tT_word,tT_number,tT_literal,tT_skip,tT_nln,tT_slash,tT_comment,tT_preproc,tT_OPEN_S,tT_CLOSE_S,tT_OPEN_C,tT_CLOSE_C,tT_OPEN_I,tT_CLOSE_I,tT_GET_ADDR,tT_RIGHT_ARROW,tT_LAMBDA,tT_SEM,tT_is,tT_type,tT_import,tT_binary,]

def lexem(i,s):
    a = list(map(lambda x:x(i,s),lexerList))
#    print(a)
    def getmax(s,n):
        if n == 0:
            return s
        elif a[n-1] == []:
            return getmax(s,n-1)
        else:
#            return (tokenIdList[n-1],a[n-1][0])
            if s[1] < a[n-1][0]:
#                print(s,(tokenIdList[n-1],a[n-1][0]))
                return getmax((tokenIdList[n-1],a[n-1][0]),n-1)
            return getmax(s,n-1)
    a,b = getmax((tT_NONE,0),len(tokenIdList))
    if b == 0:
        return ((tT_NONE,''),0)

    return ((a,s[i:b]),b)

def getAllTokens(s,i=0,l=1):
    a,b = lexem(i,s)
    a1 = (a[0],a[1],l)
    if a[0] == tT_NONE:
        return [a1]
    if '\n' in a[1]:
        return [a1]+getAllTokens(s,b,l+1)
    return [a1]+getAllTokens(s,b,l)
      