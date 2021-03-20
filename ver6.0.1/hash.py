#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 15:45:02 2020

@author: lune
"""

def hash(str):
	if str=='':
		return 0
	def hash1(a,b,str):
		if len(str) == 1:
			a1 = a+ord(str[0])
			b1 = b + a1
			return a1%65536 + b1%65536*65536

		a1 = a+ord(str[0])
		b1 = b + a1
		return hash1(a1,b1,str[1:])
	return hash1(1,0,str)

def sort(f,l):
	if len(l)<=1:
		return l
	l1 = list(filter(lambda x:f(l[0],x),l[1:]))
	l2 = list(filter(lambda x:not f(l[0],x),l[1:]))
	return sort(f,l1)+[l[0]]+sort(f,l2)
	pass

def create(s,l):
	l1 = list(map(lambda x:(hash(x[0])%s,x),l))
	l1 = sort(lambda a,b:a[0]>b[0],l1)
	def ll(l,i):
		if i==s:
			return []
		def getSerialize(l,i):
			if i == s:
				return (l,[])

			if len(l)!=0:
				if l[0][0]==i:
					i1,n = getSerialize(l[1:],i)
					return (i1,[l[0]] + n)
			return (l,[])
		i1,n=getSerialize(l,i)
		return [n] + ll(i1,i+1)
	return (s,ll(l1,0))

def get(t,k):
	s,ll = t
	h = hash(k)%s
	l = ll[h]
#	print(l[0])
	def findWith(l,s):
		if l == []:
			return None
		if l[0][1][0] == s:
			return l[0][1][1]
		else:
			return findWith(l[1:],s)
	return findWith(l,k)
def getAll(t,k):
	s,ll = t
	h = hash(k)%s
	l = ll[h]
#	print(l[0])
	def findWith(l,s):
		if l == []:
			return []
		if l[0][1][0] == s:
			return [l[0][1][1]]+findWith(l[1:],s)
		else:
			return findWith(l[1:],s)
	return findWith(l,k)

def toList(t):
	_,ll = t
	def l1(l):
		if l == []:
			return []
		else:
			return l[0] + l1(l[1:])
	l2 = list(map(lambda x:x[1],l1(ll)))
	return l2
