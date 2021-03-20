#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 09:24:17 2020

@author: lune
"""

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

P_ANY = 99
P_START = 100
P_LINE = 101
P_TYPE_DEC = 102
P_ARGS = 103
P_ARGS1 = 104
P_ARG = 105
P_TYPECAST = 106
P_TYPE_CONSTRUCTOR = 107
P_TYPE_CONSTRUCTOR1 = 108
P_ARGS_TO = 109
P_Z = 110
P_NLN = 111
P_ARG_TO = 112
P_ARGS_TO1 = 113

P_CONST = 117
P_A = 118
P_TYPE_DEC_PROP2 = 119

P_DEC = 120
P_PROP = 121
P_PROP1 = 122
P_EXPR = 149#123
P_EXPR1 = 124
P_EXPR2 = 123#124

P_LAMBDA = 125
P_LAMBDALINES = 126

P_DOEXPR = 127
P_DOEXPR1 = 128
P_DOLINES = 129

P_SWITCH_EXPR = 130
P_SWITCH_LINES = 131

P_IF = 132

P_CONV = 133

P_A1 = 134
P_A2 = 135
P_A3 = 136
P_A4 = 137
P_A5 = 138
P_A6 = 139
P_A7 = 140
P_A8 = 141
P_A9 = 142
P_A10 = 143
P_A11 = 144
P_A12 = 145
P_A13 = 146
P_A14 = 147
P_A15 = 148
P_A16 = 149
P_A17 = 150

P_SET = 151
P_ASM = 152
P_I = 153
P_SIZEOF = 154


ParseTable = [
    [(T_K_TYPE,[P_LINE,P_START]),
     (T_WORD,[P_LINE,P_START]),
     (P_ANY,[])], #P_START
    [(T_K_TYPE,[P_TYPE_DEC]),
     (T_WORD,[P_DEC])], #P_LINE
    [(P_ANY,[T_K_TYPE,T_WORD,T_OPEN_S,P_ARGS,T_CLOSE_S,T_OPEN_C,P_NLN,P_START,T_CLOSE_C,P_NLN])],#P_TYPE_DEC

    [(T_WORD,[P_ARG,P_ARGS1]),(P_ANY,[])],#P_ARGS
    [(T_SEM,[T_SEM,P_ARG, P_ARGS1]),(P_ANY,[])],#P_ARGS1
    [(P_ANY,[T_WORD,P_TYPECAST])],#P_ARG
    [(T_TYPE_CAST,[P_TYPE_CONSTRUCTOR]),(P_ANY,[])],#P_TYPECAST
    [(T_TYPE_CAST,[T_TYPE_CAST,T_WORD,P_TYPE_CONSTRUCTOR1,P_Z])],#P_TYPE_CONSTRUCTOR
    [(T_OPEN_S,[T_OPEN_S,P_ARGS_TO,T_CLOSE_S]),(P_ANY,[])],#P_TYPE_CONSTRUCTOR1
    [(P_ANY,[P_ARG_TO,P_ARGS_TO1])],#P_ARGS_TO
    [(T_MULT,[T_MULT,P_Z]),(P_ANY,[])],#P_Z
    [(T_NLN,[T_NLN,P_NLN]),(P_ANY,[])],#P_NLN
    [(P_ANY,[P_EXPR])],#P_ARG_TO
    [(T_NLN,[T_NLN,T_SEM,P_NLN,P_ARG_TO,P_ARGS_TO1]),
     (T_SEM,[T_SEM,P_NLN,P_ARG_TO,P_ARGS_TO1]),
     (P_ANY,[])],#P_ARGS_TO1

    [],[],[],

    [(T_NUM,[T_NUM]),
     (T_LITERAL,[T_LITERAL]),
     (T_K_BOOL,[T_K_BOOL]),
     (T_OPEN_C,[T_OPEN_C,P_NLN,P_ARGS_TO,P_NLN,T_CLOSE_C])],#P_CONST
    [(T_ADDR,[T_ADDR,P_A]),(P_ANY,[])],#P_A
    [],

    [(T_WORD,[P_PROP,T_EQ,P_EXPR,P_NLN])],#P_DEC
    [(T_WORD,[T_WORD,P_PROP1])],#P_PROP
    [(T_GET_PROP,[T_GET_PROP,T_WORD,P_PROP1]),(P_ANY,[])],#P_PROP1
    [(T_NUM,[P_EXPR1,P_EXPR2]),
     (T_K_BOOL,[P_EXPR1,P_EXPR2]),
     (T_LITERAL,[P_EXPR1,P_EXPR2]),
     (T_ADDR,[P_EXPR1,P_EXPR2]),
     (T_WORD,[P_EXPR1,P_EXPR2]),
     (T_OPEN_C,[P_EXPR1,P_EXPR2]),
     (T_LAMBDA,[P_LAMBDA,P_EXPR2]),
     (T_K_DO,[P_DOEXPR,P_EXPR2]),
     (T_OPEN_S,[P_EXPR1,P_EXPR2]),
     (T_K_SWITCH,[P_SWITCH_EXPR,P_EXPR2]),
     (T_K_OTHER,[T_K_OTHER,P_EXPR2]),
     (T_K_IF,[P_IF,P_EXPR2]),
     (T_TYPE_CAST,[P_TYPE_CONSTRUCTOR,P_EXPR2]),
     (T_K_SET,[P_SET,P_EXPR2]),
     (T_K_ASM,[P_ASM,P_EXPR2]),
     (T_OPEN_I,[P_I,P_EXPR2]),
     (T_K_SIZEOF,[P_SIZEOF,P_EXPR2]),

     (P_ANY,[])],#P_EXPR
    [(T_NUM,[P_CONST,P_TYPECAST]),
     (T_K_BOOL,[P_CONST,P_TYPECAST]),
     (T_LITERAL,[P_CONST,P_TYPECAST]),
     (T_ADDR,[P_A,T_WORD,P_Z,P_TYPECAST]),
     (T_WORD,[P_PROP,P_Z,P_TYPECAST]),
     (T_OPEN_C,[P_CONST,P_TYPECAST]),
     (T_OPEN_S,[T_OPEN_S,P_NLN,P_EXPR,P_NLN,T_CLOSE_S]),
     ],#P_EXPR1

     [(P_ANY,[T_LAMBDA,P_ARGS,T_OPEN_C,P_NLN,P_EXPR,P_NLN,P_LAMBDALINES,T_CLOSE_C])],#P_LAMBDA
     [(T_WORD,[P_DEC,P_LAMBDALINES]),(P_ANY,[])],#P_LAMBDALINES

     [(P_ANY,[T_K_DO,P_DOEXPR1])],#P_DOEXPR
     [(T_CONV,[P_DOLINES]),(P_ANY,[])],#P_DOEXPR1
     [(T_CONV,[T_CONV,P_EXPR,P_NLN,P_DOLINES]),(P_ANY,[])],#P_DOLINES

    [(P_ANY,[T_K_SWITCH,P_NLN,P_SWITCH_LINES])],#P_SWITCH_EXPR
    [(T_CONV,[T_CONV,P_EXPR,T_RIHT_A,P_EXPR,P_NLN,P_SWITCH_LINES]),
     (P_ANY,[])],#P_SWITCH_LINES

    [(P_ANY,[T_K_IF,P_EXPR,P_NLN,T_K_THEN,P_NLN,P_EXPR,P_NLN,T_K_ELSE,P_NLN,P_EXPR])],#P_IF

    [(T_CONV,[T_CONV]),(P_ANY,[])],#P_CONV


    [(P_ANY,[P_EXPR2,P_A2])],#P_A1
    [(T_MULT,[T_MULT,P_NLN,P_EXPR2,P_A2]),
     (T_DIV,[T_DIV,P_NLN,P_EXPR2,P_A2]),
     (T_DIV_CEL,[T_DIV_CEL,P_NLN,P_EXPR2,P_A2]),
     (P_ANY,[])],

    [(P_ANY,[P_A1,P_A4])],#P_A3
    [(T_PLUS,[T_PLUS,P_NLN,P_A1,P_A4]),
     (T_MINUS,[T_MINUS,P_NLN,P_A1,P_A4]),
     (P_ANY,[])],

    [(P_ANY,[P_A3,P_A6])],#P_A5
    [(T_SHIFT,[T_SHIFT,P_NLN,P_A3,P_A6]),
     (P_ANY,[])],

    [(P_ANY,[P_A5,P_A8])],#P_A7
    [(T_EQ,[T_EQ,P_A5,P_A8]),
     (T_NOT_EQ,[T_NOT_EQ,P_NLN,P_A5,P_A8]),
     (P_ANY,[])],

    [(P_ANY,[P_A7,P_A10])],#P_A9
    [(T_EQ_OP,[T_EQ_OP,P_NLN,P_A7,P_A10]),
     (P_ANY,[])],

    [(T_K_NOT,[T_K_NOT,P_A9,P_A11]),#P_A11
     (P_ANY,[P_A9])],

    [(P_ANY,[P_A11,P_A13])],#P_A12
    [(T_K_AND_XOR,[T_K_AND_XOR,P_NLN,P_A11,P_A13]),
     (P_ANY,[])],

    [(P_ANY,[P_A12,P_A15])],#P_A14
    [(T_K_OR,[T_K_OR,P_NLN,P_A12,P_A15]),
     (P_ANY,[])],

    [(P_ANY,[P_A14,P_A17])],#P_A16
    [(T_CONV,[T_CONV,P_NLN,P_A14,P_A17]),
     (P_ANY,[])],

    [(T_K_SET,[T_K_SET]),
     (P_ANY,[])], #P_SET

    [(T_K_ASM,[T_K_ASM]),
     (P_ANY,[])], #P_ASM

    [(T_OPEN_I,[T_OPEN_I,P_NLN,P_EXPR,P_NLN,T_CLOSE_I,P_I]),
     (P_ANY,[])],#P_I

    [(T_K_SIZEOF,[T_K_SIZEOF,T_OPEN_S,P_TYPE_CONSTRUCTOR,T_CLOSE_S]),
     (P_ANY,[])], #P_SIZEOF
]


import functools as f
def Parse(t):
    def ParseLoop(p,i):
#        print(p)
        def elseFl():
            fl2 = list(filter((lambda x:x[0]==t[i][0]),ParseTable[p-100]))
            return fl2[0] if fl2 != [] else ParseTable[p-100][-1]
        fl1 = ParseTable[p-100][-1] if i>= len(t) else elseFl()
#        print(fl1)
        def tmp(y,tl):
            if tl < 99:
                print(t[y[0]])
                if tl == t[y[0]][0]:
                    return (y[0]+1,y[1] + [t[y[0]]])
                else:
                    import sys
                    sys.exit(0)
            else:
                a = ParseLoop(tl,y[0])
                return (a[0],y[1]+[a[1]])
        i1 = f.reduce(tmp,fl1[1],(i,[]))
        return (i1[0],[p]+i1[1])
    return ParseLoop(P_START,0)


def fixTree(n):
    def tmp(a,x):
        if x ==[]:
            return a
#        if x == P_NLN:
#            return a
#        if type(x) == int:
#            return a
        if type(x) == list:
            if x[0] == P_NLN:
                return a
            if len(x)==1:
                return a
#            if len(x) == 2:
#                return a + [fixTree(x[1])]
            t = fixTree(x)
            if len(t) == 2 and type(t[1])!=tuple:
                return a + [t[1]]
            return a + [t]
        else:
            return a + [x]
    ts = f.reduce(tmp,n,[])
    return ts
