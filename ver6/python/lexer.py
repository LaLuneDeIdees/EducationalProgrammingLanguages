#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 09:24:17 2020

@author: lune
"""

#    # -> while not \n -> ret
#    ' ' or \t -> nothing
#    [a-zA-Z_`] -> while [a-zA-Z`_0-9] -> ret
#
#    0 -> x -> while [0-9A-Fa-f] -> ret
#         b -> while [01] -> ret
#         . ->                \\/
#         [eE] ->                             \\/
#         while [0-9] -> . -> while [0-9] -> [eE] -> [+-] -> while[0-9] -> ret
#            ^           _ -> ret                 ->     -> ^
#    [1-9]-> ^
#
#    ' -> while[^'\\] -> \\ -> any -> toFirstWhile
#                    -> ' -> ret
#    - -> > ->ret
#      -> ret
#    > -> = -> ret
#      -> ret
#    < -> = -> ret
#      -> ret
#    ! -> = -> ret
#    (|)|{|}|+|-|>|<|=|/|*|%|&|:|,|.|\n|\\|\\|\n -> ret
#
#    preprocessor:
#        #.*\n
#    language:
#        skip = ' '|\t
#        lable = [a-zA-Z`_][a-zA-Z`_0-9]*
#        num = 0b[10]+|0x[0-9A-Fa-f]+|[0-9]+(?:\\.[0-9]+)?(?:[Ee][+-]?[0-9]+)?
#        string = '(\\'|[^'])*'
#
#        sym
#        //one simbols oper
#            = (|)|{|}|+|-|>|<|=|/|*|%|&|:|,|.|\n|\\|\\|
#        //two sym
#            = ->|>=|<=|!=
#
#        //cast from sym
#        operator = ->|\\+|-|>=|<=|<|>|=|\\!=|\\/|\\*|%
#        leftS = (
#        rightS = )
#        leftB = {
#        rightB = }
#        typeCast = :
#        sem = ,
#        getProp = \\.
#        NLN = \n
#        lambda = \\
#
#        //cast from lable
#        operator += xor|and|or|not
#        if = if
#        then = then
#        else = else
#        do = do
#        bool = true|false
#        typeDeclared = type
#        switch = switch

T_NONE = 0
T_NLN = 1
T_PREPROC = 2
T_ONEOPR = 3
T_WORD = 4
T_LITERAL = 5
T_NUM = 6

T_K_BOOL = 70   #true|false
T_K_DO = 71
T_K_SWITCH = 72
T_K_IF = 73
T_K_THEN = 74
T_K_ELSE = 75
T_K_SIZEOF = 76
T_K_TYPE = 77
T_K_OTHER = 78
T_K_ASM = 79
T_K_SET = 80
T_K_AND_XOR = 81
T_K_OR = 82
T_K_NOT = 83

T_OPEN_S = 8    #(
T_CLOSE_S = 9   #)
T_OPEN_C = 10   #{
T_CLOSE_C = 11  #}
T_OPEN_I = 12   #[
T_CLOSE_I = 13  #]
T_GET_PROP = 14 #.
T_TYPE_CAST = 15#:
T_SEM = 16      #,
T_LAMBDA = 17   #\
T_CONV = 18     #|
T_RIHT_A = 19   #->
T_MULT = 20     #*
T_DIV = 21      #/
T_PLUS = 22     #+
T_MINUS = 23    #-
T_DIV_CEL = 24  #%
T_EQ_OP = 25    #>= <= != < >
T_EQ = 26       #=
T_ADDR = 27     #&
T_SHIFT = 29    #<< >>
T_NOT_EQ = 30   #!=




class State:
    n = None #nextState
    a = '' #acm
    t = [] #tokens
    l = 1
    def __init__(self,nextS=None,acm='',tokens=None,line = 1):
        self.l = line
        self.n = nextS
        self.a = acm
        if tokens == None:
            self.t=[]
        else:
            self.t = tokens
def preproc(s,c):
    if c in '\n':
        return State(parse,'',s.t+[(T_PREPROC,s.a,s.l)],s.l+1)
    else:
        return State(preproc,s.a+c,s.t,s.l)
def comment1(s,c):
    if c in '\n':
        return State(parse,'',s.t+[(T_NLN,'',s.l)],s.l+1)
    else:
        return State(comment1,'',s.t,s.l)
def comment(s,c):
    if c in '/':
        return State(comment1,'',s.t,s.l)
    else:
        return parse(State(parse,'',s.t+[(T_ONEOPR,'/',s.l)],s.l),c)
def word(s,c):
    if c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_`0123456789':
        return State(word,s.a+c,s.t,s.l)
    else:
        return parse(State(parse,'',s.t+[(T_WORD,s.a,s.l)],s.l),c)
def literal1(s,c):
    return State(literal,s.a+c,s.t,s.l)
def literal(s,c):
    if c in '\\':
        return State(literal1,s.a+c,s.t,s.l)
    elif c in '\'':
        return State(parse,'',s.t+[(T_LITERAL,s.a,s.l)],s.l)
    else:
        return State(literal,s.a+c,s.t,s.l)

def bini(s, c):
    if c in '01':
        return State(bini,s.a+c,s.t,s.l)
    else:
        return parse(State(parse, '', s.t+[(T_NUM, s.a,s.l)],s.l), c)


def hexi(s, c):
    if c in '1234567890ABCDEFabcdef':
        return State(hexi, s.a+c, s.t,s.l)
    else:
        return parse(State(parse, '', s.t+[(T_NUM,s.a,s.l)],s.l), c)


def expon(s, c):
    return State(dec,s.a+c,s.t,s.l)
def bin_dec_hex(s,c):
    if c in 'b':
        return State(bini,'0b',s.t,s.l)
    elif c in 'x':
        return State(hexi,'0x',s.t,s.l)
    elif c in '0123456789':
        return State(dec,s.a+c,s.t,s.l)
    elif c in '.':
        return State(dec,s.a+c,s.t,s.l)
    elif c in 'eE':
        return State(expon,s.a+c,s.t,s.l)
    else:
        return parse(State(parse,'',s.t+[(T_NUM,c,s.l)],s.l),c)
def dec(s,c):
    if c in '0123456789':
        return State(dec,s.a+c,s.t,s.l)
    elif c in '.':
        return State(dec,s.a+c,s.t,s.l)
    elif c in 'eE':
        return State(expon,s.a+c,s.t,s.l)
    else:
        return parse(State(parse,'',s.t+[(T_NUM,s.a,s.l)],s.l),c)
def leftA(s,c):
    if c in '>':
        return State(parse,'',s.t+[(T_ONEOPR,'->',s.l)],s.l)
    else:
        return parse(State(parse,'',s.t +[(T_ONEOPR,s.a,s.l)],s.l),c)

def mlnoe(s,c): #more/less or eq /not er
    if c in '=':
        return State(parse,'',s.t+[(T_ONEOPR,s.a+c,s.l)],s.l)
    elif c == '>' and s.a=='>':
        return State(parse,'',s.t+[(T_ONEOPR,s.a+c,s.l)],s.l)
    elif c == '<' and s.a=='<':
        return State(parse,'',s.t+[(T_ONEOPR,s.a+c,s.l)],s.l)
    else:
        return parse(State(parse,'',s.t +[(T_ONEOPR,s.a,s.l)],s.l),c)

def parse(s,c):
    if c in ' \t':
        return State(parse,s.a,s.t,s.l)
    elif c in '\n':
        return State(parse,s.a,s.t+[(T_NLN,'',s.l)],s.l+1)
    elif c in '#':
        return State(preproc,'',s.t,s.l)
    elif c in '/':
        return State(comment,'',s.t,s.l)
    elif c in '0':
        return State(bin_dec_hex,c,s.t,s.l)
    elif c in '0123456789':
        return State(dec,c,s.t,s.l)
    elif c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_`':
        return State(word,c,s.t,s.l)
    elif c in '\'':
        return State(literal,'',s.t,s.l)
    elif c in '[](){}+=/*%&:,.|\\':
        return State(parse,'',s.t+[(T_ONEOPR,c,s.l)],s.l)
    elif c in '-':
        return State(leftA,c,s.t,s.l)
    elif c in '><!':
        return State(mlnoe,c,s.t,s.l)
    else:
        return State(parse,s.a+c,s.t,s.l)
def toTokens(s):
    st = State(parse)
    def loop(st,s):
        if s=='':
            return st
        else:
            return loop(st.n(st,s[0]),s[1:])
    def fixTokens(t1,t2):
        if t1==[]:
            return t2
        else:
            if t1[0][0] == T_ONEOPR:
                if t1[0][1] == '(':
                    return fixTokens(t1[1:],t2+[(T_OPEN_S,t1[0][1],t1[0][2])])
                if t1[0][1] == ')':
                    return fixTokens(t1[1:],t2+[(T_CLOSE_S,t1[0][1],t1[0][2])])
                if t1[0][1] == '{':
                    return fixTokens(t1[1:],t2+[(T_OPEN_C,t1[0][1],t1[0][2])])
                if t1[0][1] == '}':
                    return fixTokens(t1[1:],t2+[(T_CLOSE_C,t1[0][1],t1[0][2])])
                if t1[0][1] == '[':
                    return fixTokens(t1[1:],t2+[(T_OPEN_I,t1[0][1],t1[0][2])])
                if t1[0][1] == ']':
                    return fixTokens(t1[1:],t2+[(T_CLOSE_I,t1[0][1],t1[0][2])])

                if t1[0][1] == '.':
                    return fixTokens(t1[1:],t2+[(T_GET_PROP,t1[0][1],t1[0][2])])
                if t1[0][1] == ':':
                    return fixTokens(t1[1:],t2+[(T_TYPE_CAST,t1[0][1],t1[0][2])])
                if t1[0][1] == ',':
                    return fixTokens(t1[1:],t2+[(T_SEM,t1[0][1],t1[0][2])])
                if t1[0][1] == '\\':
                    return fixTokens(t1[1:],t2+[(T_LAMBDA,t1[0][1],t1[0][2])])
                if t1[0][1] == '|':
                    return fixTokens(t1[1:],t2+[(T_CONV,t1[0][1],t1[0][2])])
                if t1[0][1] == '->':

                    return fixTokens(t1[1:],t2+[(T_RIHT_A,t1[0][1],t1[0][2])])
                if t1[0][1] == '*':
                    return fixTokens(t1[1:],t2+[(T_MULT,t1[0][1],t1[0][2])])
                if t1[0][1] == '/':
                    return fixTokens(t1[1:],t2+[(T_DIV,t1[0][1],t1[0][2])])
                if t1[0][1] == '+':
                    return fixTokens(t1[1:],t2+[(T_PLUS,t1[0][1],t1[0][2])])
                if t1[0][1] == '-':
                    return fixTokens(t1[1:],t2+[(T_MINUS,t1[0][1],t1[0][2])])
                if t1[0][1] == '%':
                    return fixTokens(t1[1:],t2+[(T_DIV_CEL,t1[0][1],t1[0][2])])
                if t1[0][1] == '=':
                    return fixTokens(t1[1:],t2+[(T_EQ,t1[0][1],t1[0][2])])
                if t1[0][1] == '&':
                    return fixTokens(t1[1:],t2+[(T_ADDR,t1[0][1],t1[0][2])])
                if t1[0][1] in '>= <= > <':
                    return fixTokens(t1[1:],t2+[(T_EQ_OP,t1[0][1],t1[0][2])])
                if t1[0][1] in '!=':
                    return fixTokens(t1[1:],t2+[(T_NOT_EQ,t1[0][1],t1[0][2])])
                if t1[0][1] in '>> <<':
                    return fixTokens(t1[1:],t2+[(T_SHIFT,t1[0][1],t1[0][2])])
            elif t1[0][0] == T_WORD:
                if t1[0][1] == 'xor' or t1[0][1]=='and':
                    return fixTokens(t1[1:],t2+[(T_K_AND_XOR,t1[0][1],t1[0][2])])
                if t1[0][1] == 'not':
                    return fixTokens(t1[1:],t2+[(T_K_NOT,t1[0][1],t1[0][2])])
                if t1[0][1] == 'or':
                    return fixTokens(t1[1:],t2+[(T_K_OR,t1[0][1],t1[0][2])])
                if t1[0][1] == 'set':
                    return fixTokens(t1[1:],t2+[(T_K_SET,t1[0][1],t1[0][2])])
                if t1[0][1] == '_asm':
                    return fixTokens(t1[1:],t2+[(T_K_ASM,t1[0][1],t1[0][2])])
                if t1[0][1] == 'other':
                    return fixTokens(t1[1:],t2+[(T_K_OTHER,t1[0][1],t1[0][2])])
                if t1[0][1] == 'type':
                    return fixTokens(t1[1:],t2+[(T_K_TYPE,t1[0][1],t1[0][2])])
                if t1[0][1] == 'sizeof':
                    return fixTokens(t1[1:],t2+[(T_K_SIZEOF,t1[0][1],t1[0][2])])
                if t1[0][1] == 'else':
                    return fixTokens(t1[1:],t2+[(T_K_ELSE,t1[0][1],t1[0][2])])
                if t1[0][1] == 'then':
                    return fixTokens(t1[1:],t2+[(T_K_THEN,t1[0][1],t1[0][2])])
                if t1[0][1] == 'if':
                    return fixTokens(t1[1:],t2+[(T_K_IF,t1[0][1],t1[0][2])])
                if t1[0][1] == 'switch':
                    return fixTokens(t1[1:],t2+[(T_K_SWITCH,t1[0][1],t1[0][2])])
                if t1[0][1] == 'do':
                    return fixTokens(t1[1:],t2+[(T_K_DO,t1[0][1],t1[0][2])])
                if t1[0][1] == 'true' or t1[0][1] == 'false':
                    return fixTokens(t1[1:],t2+[(T_K_BOOL,t1[0][1],t1[0][2])])

            return fixTokens(t1[1:],t2+[t1[0]])
    return fixTokens(loop(st,s).t,[])