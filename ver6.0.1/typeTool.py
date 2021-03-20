#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 08:33:53 2020

@author: lune
"""
import myFL as lexer
import myFP as parser
import functools as f
import hash
import sys
import const


def unifi(a,b,at = None,bt = None):
	def unifi(a,b,at,bt):
		if type(a) != list and type(b)!=list:
			if ord(a[0]) < ord('a') and ord(b[0]) < ord('a'):
				if a == b:
					return (at,bt,True)
				else:
					return (at,bt,False)
			else:
				if ord(a[0]) >= ord('a'):
					nnn = hash.get(at,a)
					if nnn == None:
						return (hash.create(256,hash.toList(at)+[(a,b)]),bt,True)
					else:
						if type(nnn) != list:
							if ord(nnn[0]) >= ord('a'):
								return (at,bt,True)
						return unifi(nnn,b,at,bt)
				else:
					nnn = hash.get(bt,b)
					if nnn == None:
						return (at,hash.create(256,hash.toList(bt)+[(b,a)]),True)
					else:
						if type(nnn) != list:
							if ord(nnn[0]) >= ord('a'):
								return (at,bt,True)
						return unifi(a,nnn,at,bt)
		elif type(a) != list:
			if ord(a[0]) >= ord('a'):
				nnn = hash.get(at,a)
				if nnn == None:
					return (hash.create(256,hash.toList(at)+[(a,b)]),bt,True)
				else:
					if type(nnn) != list:
						if ord(nnn[0]) >= ord('a'):
							return (at,bt,True)
					return unifi(nnn,b,at,bt)
			return (at,bt,False)
		elif type(b) != list:
			if ord(b[0]) >= ord('a'):
				nnn = hash.get(bt,b)
				if nnn == None:
					return (at,hash.create(256,hash.toList(bt)+[(b,a)]),True)
				else:
					if type(nnn) != list:
						if ord(nnn[0]) >= ord('a'):
							return (at,bt,True)
					return unifi(a,nnn,at,bt)
			return (at,bt,False)
		else:
			at1,bt1,b1 = unifi(a[0],b[0],at,bt)
			at2,bt2,b2 = unifi(a[1],b[1],at1,bt1)
			return (at2,bt2,b1 and b2)
		return (at,bt,False)
	if at == None:
#		at,bt,b = unifi(a,b,hash.create(256,[]),hash.create(256,[]))
		return unifi(a,b,hash.create(256,[]),hash.create(256,[]))
	else:
#		at,bt,b = unifi(a,b,at,bt)
		return unifi(a,b,at,bt)
#	return b
	pass

#def unifi(a,b):
#	if type(a) != list and type(b) != list:
#		if ord(a[0]) < ord('a') and ord(b[0]) < ord('a'):
#			if a == b:
#				return True
#			else:
#				return False
#		else:
#			return True
#	else:
#		if type(a) != list or type(b) != list:
#			return True
#		else:
#			return unifi(a[0],b[0]) and unifi(a[1],b[1])
#	return False


def castTreeToTypeSig(a):
	if type(a) == list:
		if len(a[1]) == 1:
			return castTreeToTypeSig(a[1][0])
		return f.reduce(lambda a,x:a+[castTreeToTypeSig(x)],a[1],[])
	else:
		return a[1]

def strToType(s):
	lll = lexer.getAllTokens(s)
	lll = list(filter(lambda x:not x[0] in [lexer.tT_comment,lexer.tT_skip,lexer.tT_preproc], lll))
	tree1,l1 = parser.P_tip([],lll)
	tree1 = castTreeToTypeSig(tree1[0])
	return tree1

def toApplyT(a):
	return [a,'s_reserve']

def toString(a):
#	print(a)
	if type(a) == list:
		if type(a[0]) == list:
			return '(' + toString(a[0]) + ')' + '->' + toString(a[1])
		else:
			return toString(a[0]) + '->' + toString(a[1])
	else:
		return ' ' + a + ' '

def checkRedefined(t,msg):
	if t == []:
		return
	listOfAll = f.reduce(lambda a,x:a+hash.toList(x),t,[])
	tOfAll = hash.create(1024,listOfAll);
	def checkForName(x):
		res = hash.getAll(tOfAll,x[0])
#		print(res)
		if len(res) > 1:
			sys.exit(msg +
			'name: ' + x[0] + '\n' +
			'declared in lines: ' +
			f.reduce(lambda a,x: a + (str(x[1]) if x[1]>=0 else 'Generic') +', ', res,"") +'\n')
		return
	list(map(checkForName,listOfAll))

def checkType(t,ts,line):
	if ts == []:
		return
	listOfAll = f.reduce(lambda a,x: a + hash.toList(x),ts,[])
	tOfAll = hash.create(1024,listOfAll)
	def check(x):
		if type(x) == list:
			return check(x[0]) and check(x[1])
		if ord(x[0]) >= ord('a') and ord(x[0]) <= ord('z'):
			return True
#		print(x)
		res = hash.getAll(tOfAll,x)
#		print(len(res))
		if len(res) == 0:
			sys.exit('ERROR: missing type declaration\n'+
				'Undeclared type: ' + x +'\n' +
				'in line: ' + str(line))
		return True


	def checkNameUses(x):
#		print('In check: ',x)
		if type(x) == list:
			if type(x[0]) != list:
				if ord(x[0][0]) >= ord('A') and ord(x[0][0]) <= ord('X'):
					isThisC = hash.get(tOfAll,x[0])
#					print(x,isThisC[0])
					if type(isThisC[0]) != list:
#						pass
						return checkNameUses(x[0]) and checkNameUses(x[1])
					else:
#						_,_,b = unifi(x, isThisC[0])
#						if b == False:
#							sys.exit('ERROR: wrong parameters for type\n' +
#									 'in line: ' + str(line) + '\n' +
#									 'for type: ' + x[0] + '\n' +
#									 'declared in line: ' + str(isThisC[1]) + '\n' +
#									 'with pattern: ' + str(isThisC[0]) + '\n' +
#									 '            | ' + toString(isThisC[0]) + '\n' +
#									 'in full type: ' + str(t) + '\n' +
#									 '            | ' + toString(t) + '\n' +
#									 'in local pattern: ' + str(x) + '\n' +
#									 '                | ' + toString(x) + '\n' )
#							return False
#							print('Error:',toString(x),x,isThisC[1])
						return checkNameUses(x[1])
				else:
					return checkNameUses(x[1])
			else:
				return checkNameUses(x[0]) and checkNameUses(x[1])
		else:
#			print(x)
			if ord(x[0]) >= ord('A') and ord(x[0]) <= ord('X'):
				isThisC = hash.get(tOfAll,x)
				if isThisC != None:
#					print(isThisC)
					if type(isThisC[0]) != list:
						return True
					else:
						sys.exit('ERROR: missing parameters for type\n' +
								 'in line: ' + str(line) + '\n' +
								 'for type: ' + x + '\n' +
								 'declared in line: ' + str(isThisC[1]) + '\n' +
								 'with pattern: ' + str(isThisC[0]) + '\n' +
								 '            | ' + toString(isThisC[0]) + '\n' +
								 'in full type: ' + str(t) + '\n' +
								 '            | ' + toString(t) + '\n' )
#						print('Error:',x,isThisC[1],isThisC[0])
						return False
				else:
					sys.exit('ERROR: undefined type:' + str(x) +'\n' +
							  'in line: ' + str(line) + '\n')
					return False
			else:
				return True

	if check(t) == True:
		if checkNameUses(t):
			return True
		else:
			return False
	else:
		return False

def loadFlag(x):
#						print(x)
	if x[0] == lexer.tT_binary:
		if x[1] == 'infixl':
			return const.S_INFIXL
		if x[1] == 'infixr':
			return const.S_INFIXR
	elif x[0] == lexer.tT_evalT:
		import inspect
		sys.exit('FIXME: tT_evalT not suported in compiler\n'+
		'about in source file \'typeTool.py\' in line: ' + str(inspect.currentframe().f_lineno ))
	return 0

#def loadTypeFromOptionList(x):
def loadTypeFromOptionList(l):
	if l == []:
		return None
	if l[0][0] == parser.pP_tip:
		thisType = castTreeToTypeSig(l[0])
		return thisType
#			print(thisType)
	return loadTypeFromOptionList(l[1:])
#	return tmp(x)

def getTypesFromScope(a):
	if a == []:
		return ([],[])
	a1 = a[0]
	if a1[0] == parser.pP_TypeDeclare:
		TypeName = a1[1][0][1]
		if not TypeName[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
			sys.exit('ERROR: Type Name must begin with a capital letter\n' +
			'in line: ' + str(a1[1][0][2]) +'\n' +
			'in type name: ' + TypeName + '\n')
#		print(TypeName)

		TypeStr = TypeName + ' '
		if a1[1][1][1] != []:
			TypeStr += ' '.join(list(map(lambda x:x[1],a1[1][1][1])))
		TypeThis = strToType(TypeStr)

		Constructors = a1[1][2][1]
#		print(a1[1][2][1])
		ConstructorsReg = None
		if len(Constructors) == 1:
#			print('Thos simple type')
			# print(Constructors)
			constructorThis = strToType(
					 toString(
							 castTreeToTypeSig(Constructors[0][1][0])
							 ) +
					 ' -> ' +
					 toString(
							 TypeThis
							 )
					 )
			ConstructorsReg = [(TypeName,(constructorThis,
										   a1[1][0][2],const.S_TYPE_CONSTRUCTOR))]
#			print(ConstructorsReg)
		else:
#			print('This adt type')
			def getTypeConstructor(a,x):
				if len(x[1]) == 1:
					return a + [(x[1][0][1],(TypeThis,x[1][0][2],const.S_TYPE_CONSTRUCTOR))]
				else:
#					print(x)
#					print('Compex constructor')
					flags = f.reduce((
							lambda a,x:a + loadFlag(x)
							),x[1][0][1],const.S_TYPE_CONSTRUCTOR)

					lineThis = x[1][1][2]
					nameThis = x[1][1][1]
					constructorThis = strToType(
							 toString(
									 castTreeToTypeSig(x[1][2])
									 ) +
							 ' -> ' +
							 toString(
									 TypeThis
									 )
							 )
#					print(flags,lineThis,nameThis,constructorThis)
					return a + [(nameThis,(constructorThis,lineThis,flags))]
				return a
			ConstructorsReg = f.reduce(getTypeConstructor,Constructors,[])
		at1,at2 = getTypesFromScope(a[1:])
		return ([(TypeName,(TypeThis,a1[1][0][2]))] + at1,ConstructorsReg + at2)
	return getTypesFromScope(a[1:])
#a = strToType('(a -> b) -> L a -> L b')
#a1 = toApplyT(strToType('U32 -> U32'))
#a2 = toApplyT(strToType('L U32'))
#at,bt,b = unifi(a,a1)
#print(b)
#at,bt,b = unifi(a[1],a2,at,hash.create(256,[]))
#print(b)
#print(a)
#print(strToType(toString(a)))
#checkType()