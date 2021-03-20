# -*- coding: utf-8 -*-
import sys
import functools as f
import myFL as lexer
import myFP as parser
import hash
import typeTool as Type
import const
import fixAst



def getShugarFromeScope(a):
	if a == []:
		return []
	a1 = a[0]
	if a1[0] == parser.pP_sugar:
#		print(a1[1])
		return f.reduce(lambda a,x:a+[(x[1],x[2],const.S_SUGAR)],a1[1],[]) + getShugarFromeScope(a[1:])
	return getShugarFromeScope(a[1:])


def checkOnUseSugar(x,t):
	listOfAll = f.reduce(lambda a,x:a + hash.toList(x),t,[])
	tOfAll = hash.create(1024,listOfAll)
	res = hash.get(tOfAll,x[0])
	if res == None:
		return True
	sys.exit('ERROR: name conflict:  syntax sugar and type constructor\n' +
			'name: ' + x[0] + '\n' +
			'syntax sugar declared in line: ' + str(x[1]) + '\n' +
			'type constructor declared in line: ' + str(res[1]) + '\n')
	return False

def getTables(s):
	tSugar = hash.create(128,getShugarFromeScope(s))
	tTypes2 = Type.getTypesFromScope(tree[1])

	tTypes = hash.create(256,tTypes2[0])
	tTypeConstructor = hash.create(256,tTypes2[1])
	return (tSugar,tTypes,tTypeConstructor)

def checkTables(ts,tt,ttc):
	Type.checkRedefined(ttc,
			   'ERROR: type constructor names must not match\n')

	Type.checkRedefined(tt,
				   'ERROR: type names must not match\n')

	ttc1 = f.reduce(lambda a,x:a + hash.toList(x),ttc,[])
	list(map(lambda x:Type.checkType(x[1][0],tt,x[1][1]),ttc1))
	list(map(lambda x:checkOnUseSugar(x,ttc),hash.toList(ts)))
	return True


########################################################
#get type for DECLARE and check types

########################################################
# get type for EXPR and check types

########################################################
# get type for SCOPE and check types
#s -> scobe
#ts -> sugar table
#tt -> typeTable
#ttc -> typeConstructor table
def compileStage1(s,ts,tt,ttc):
	return []
########################################################
# get  list of names

def listNameFromScope(t):
	if t == []:
		return []
	if t[0][0] == parser.pP_Declare:
#		print(t[0][1][0][1])
		return [(t[0][1][0][1],None)] + listNameFromScope(t[1:])
	return listNameFromScope(t[1:])

########################################################
# get  list of names with options

def listNameFromScopeWithOptions(t):
	if t == []:
		return []
	if t[0][0] == parser.pP_Declare:
		flags = f.reduce(lambda a,x:a + Type.loadFlag(x),t[0][1][1][1],const.S_FUNC_EXPR)
		thisType = Type.loadTypeFromOptionList(t[0][1][1][1])
		return [(t[0][1][0][1],(thisType,t[0][1][0][2],flags))] + listNameFromScopeWithOptions(t[1:])
	return listNameFromScopeWithOptions(t[1:])


########################################################
s = open('concept.txt','r').read()

s = '''
sugar if else
sugar then

* is
	infixl
	I32 -> I32 -> I32

- is
	infixl
	I32 -> I32 -> I32

- is
	infixl
	I16 -> I16 -> I16

mYtrue is \\x y -> x

tmp is if mYtrue then 1 else 0

main is fac 100

y is \\f -> f (y f)
y` is \\f -> (\\x -> f (x x)) (\\x -> f(x x))


fac is
    (
        y fac
        fac is
            \\_ 1 -> 1
            \\fac x -> x * (fac (x - 1))
    )

type A is U8

type List with a is
    Nil
    infixr : -> a (List a)

: is
	infixr
	a -> List a -> List a

type Char is U8

type B is (List Char)


type C with a is (a (C a))



tmpa is 123 as A

<> is
    //strict
    infixl
    List A -> U32 -> A
    \\ (List x _) 0 -> x
    \\ (List _ xs) i -> xs <> (i - 1)

succ is
	\ a -> a + 1

forTest is
	if succ 1 + 4 * (- 4) - 1 and 1 << 3 : 123 : Nil <> succ 12
'''

s = lexer.getAllTokens(s)
s = list(filter(lambda x:not x[0] in [lexer.tT_comment,lexer.tT_skip,lexer.tT_preproc], s))

tree,l = parser.P_START([],s)
if tree == None:
	msg = ' '.join(list(map(lambda x:x[1],l[1:10])))
	sys.exit('ERROR: syntax about '+str(l[1][2])+' line\n' +
	  'it is possinle near this text: '+msg+'\n' +
	  'I want to token ' + str(l[0])+'\n')
tree = tree[0]

##############
tDefTypes = hash.create(128,
	[('Ptr',(['Ptr','a'],-1))] +
	list(map(lambda x:(x,(x,-1)),'I8,I16,I32,U8,U16,U32,F8,F16,F32,F64'.split(',')))
	)
tDefConstructor = hash.create(128,
	  [('Ptr',(Type.strToType('a -> Ptr a'),-1))]
  )

tSugar,tTypes,tTypeConstructor = getTables(tree[1])
checkTables(tSugar,[tTypes,tDefTypes],[tTypeConstructor,tDefConstructor])\

#########################################################
tmpL = (listNameFromScopeWithOptions(tree[1]) +
	hash.toList(tTypeConstructor) +
	hash.toList(tDefConstructor)
	)
tFromThis = hash.create(256,tmpL)
tree = fixAst.fixAst(tree[1][-1][1][2][1],tFromThis,tSugar)
print(tree)

#########################################################

# invalid check types
# unifi with types template
# redefined check
# other for full type include system?

#check for use sugar word -


# TODO
#first register all symbols for check definded and binary
#compile anything declare
#if I need the symbols and can't type create for expression
#

#evolution for compile functions
# compile if already compiler depency
# if I can't compile anything
# error

#in expr first type for all lines
#if i need depency
#wait
#else
#check all types

#if special polimorphism find needed type
#if can't find then error
#else CREATE reference
#TODO: How create reference? with line + name?

#in lambda check valid pattern matching
#and get Type from expr
#TYPE: arg -> arg -> exprType

#TODO: get type with constant





# then add to stack for loading
# process needed symbol or other
# process this

#####################################################
#import typeTool as Type
#a = Type.strToType('(a -> b) -> L a -> L b')
#b = Type.strToType('I32 -> I32')
#print(a,b)
#tmp = Type.strToType('Ast a (List a)')
#print(tmp)
#print(Type.unifi(a,[b,'reserve']))
#####################################################


fout = open('ats.dot','w')
fout.write('''
graph ast{
''')

idx = 0
def drawTree(l,rodix):
    global idx
    thix = idx+1
    idx += 1
    if type(l) == list:
        if len(l) == 2 and type(l[0]) == int:
            fout.write('n'+str(thix)+'[label="'+str(l[0])+'"];\n')
            fout.write('n'+str(rodix) + ' -- ' +'n'+str(thix)+';\n' )
            l = l[1]
        else:
	        fout.write('n'+str(rodix) + ' -- ' +'n'+str(thix)+';\n' )
        for k in l:
            drawTree(k,thix)
    else:
        fout.write('n'+str(thix)+'[label="'+str(l)+'"];\n')
        fout.write('n'+str(rodix) + ' -- ' +'n'+str(thix)+';\n' )

drawTree(tree,0)


fout.write('''
}
''')

fout.close();
