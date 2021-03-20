#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 08:04:13 2020

@author: lune
"""
import myFP as parser
import hash
import const
import sys
import functools as f

def isRightAssoc(x):
	if x in '~':
		return True
	return False


def getPriot(x):
	if x in '*/%':
		return 12
	if x in '+-':
		return 11
	if x in '>> <<':
		return 10
	if x in '>= <= > <':
		return 9
	if x in '= !=':
		return 8
	if x in 'and':
		return 7
	if x in 'xor':
		return 6
#	if x in 'not':
#		return 5
	if x in 'or':
		return 4
	if x in '| ~':
		return 1
	return 2


#fix ast use table simbols and sugar table
def fixAst(a,t,ts):

	def clearScobe(a):
		if a == []:
			return []

		if a[0][0] == parser.pP_word:
			thisName = a[0][1][0][1]
			t = hash.get(ts,thisName)
			if t!=None:
				return clearScobe(a[1:])

		return [a[0]] + clearScobe(a[1:])
		pass

	def sliceWhile(l,f):
		if l == []:
			return ([],[])
		if not f(l[0]):
			return ([],l)
		s,l1 = sliceWhile(l[1:],f)
		return ([l[0]]+s,l1)

	def asInfix(x):
		if x[0] != parser.pP_word:
			return None
		thisName = x[1][0][1]

		if thisName in ('+ - / * << >> >= <= != = % and xor not or | ~').split(' '):
			return (getPriot(thisName),isRightAssoc(thisName))

		thisS = hash.get(t,thisName)
		if thisS == None:
			sys.exit('ERROR: undefined symbol:\n' +
				 'symbol: ' + thisName + '\n')

		if thisS[2] & const.S_INFIXL > 0:
			return (getPriot(thisName),False)

		if thisS[2] & const.S_INFIXR > 0:
			return (getPriot(thisName),True)

		return None

	def isInfix(x):
		return asInfix(x) != None

	def createScobes(a):
		if a == []:
			return a
		if not isInfix(a[0]):
			s,l = sliceWhile(a,lambda x:not isInfix(x))
#			print(s,l)
			if len(s) == 1:
				return [a[0]] + createScobes(a[1:])
			return [[parser.pP_newScope,
							[[parser.pP_Expr,s]]
						]] + createScobes(l)
		return [a[0]] + createScobes(a[1:])

	def fix(a):
		if a == []:
			return a

		def foldT(a,x):
			return a[:-2] + [[parser.pP_newScope,
				   [
						[
						   parser.pP_Expr,
						      [x[1]]+a[-2:]]]
				        ]
					]

		def tmp(s,o,d):
			if d == []:
				o1 = f.reduce(foldT,s,o)
				return o1

			x,n = d[0],d[1:]
			asBin = asInfix(x)
			if asBin != None:
#				thisName = x[1][0][1]

#				print(asBin,thisName)
				ff = ((lambda x:x[0]>asBin[0]) if asBin[1]
					 else	(lambda x:x[0]>=asBin[0]))
				ss,ll = sliceWhile(s,ff)
				o1 = f.reduce(foldT,ss,o)
#				print(ss,ll,s)

				return tmp([(asBin[0],x)]+ll,o1,n)

			return tmp(s,o+[x],n)


		return tmp([],[],a)
	return fix(createScobes(clearScobe(a)))