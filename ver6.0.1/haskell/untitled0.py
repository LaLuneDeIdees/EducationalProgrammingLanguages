#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 07:09:39 2020

@author: lune
"""

a1 = ['I32',['I32','I32']]
a2 = ['I32','a_reserve']

def unifi(a,b):
	print(a,b)
	if type(a) != list and type(b) != list:
		if ord(a[0]) < ord('a') and ord(b[0]) < ord('a'):
			if a == b:
				return True
			else:
				return False
	else:
		if type(a) != list or type(b) != list:
			return True
		else:
			return unifi(a[0],b[0]) and unifi(a[1],b[1])
	return False

print(unifi(a1,a2))