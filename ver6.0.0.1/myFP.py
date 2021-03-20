

import sys
import myFL as lexer

def empty(d,p):
    return (d,p)

def term(t):
    def parser(d,p):
        if p[0][0] == t:
            return (d+[p[0]],p[1:])
        return (None,[(t,'',0)]+p[1:])
    return parser


def notTerm(c,pp):
	def parser(d,p):
		d1,p1 = pp([],p)
		if d1 == None:
			return (None,p1)
		return (d+[[c,d1]],p1)
	return parser

def notSaveTerm(c,pp):
    def parser(d,p):
        d1,p1 = pp([],p)
        if d1 == None:
            return (None,p1)
        return (d,p1)
    return parser

def app(a,b):
    def parser(d,p):
        d1,p1 = a([],p)
        if d1 == None:
            return (None,p1)
        d2,p2 = b(d1,p1)
        if d2 == None:
            return (None,p2)
        return (d+d2,p2)
    return parser

def par(a,b):
    def parser(d,p):
        d1,p1 = a([],p)
        if d1 != None:
            return (d+d1,p1)
        d2,p2 = b([],p)
        if d2 != None:
            return (d+d2,p2)
        return (None,p1)
    return parser

def mor(l):
    if l == []:
        return empty
    elif len(l) == 1:
        return l[0]
    return par(l[0],mor(l[1:]))

def serial(l):
    if l == []:
        return empty
    elif len(l) == 1:
        return l[0]
    return app(l[0],serial(l[1:]))

def P_START(d,p):
	d1,p1 = mor([
		serial([
			N_nln,
			lLines,
			N_nln,
			N_NONE,
		]),
	])(d,p)
	return (d1,p1)
P_START = notTerm(1,P_START)
def lLines(d,p):
	d1,p1 = mor([
		serial([
			lLine,
			lLines,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
def lLine(d,p):
	d1,p1 = mor([
		serial([
			P_typeDec,
		]),
		serial([
			P_adtDec,
		]),
		serial([
			P_Dec,
		]),
	])(d,p)
	return (d1,p1)
def P_typeDec(d,p):
	d1,p1 = mor([
		serial([
			N_type,
			term(lexer.tT_word),
			N_is,
			term(lexer.tT_word),
			lWordList,
			NN_nln,
		]),
	])(d,p)
	return (d1,p1)
P_typeDec = notTerm(2,P_typeDec)
def lWordList(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_word),
			lWordList,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
def P_adtDec(d,p):
	d1,p1 = mor([
		serial([
			N_type,
			term(lexer.tT_word),
			N_is,
			NN_nln,
			P_adtLine,
			adtDecLines,
		]),
	])(d,p)
	return (d1,p1)
P_adtDec = notTerm(3,P_adtDec)
def adtDecLines(d,p):
	d1,p1 = mor([
		serial([
			P_adtLine,
			adtDecLines,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
def P_adtLine(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_word),
			_adtLine,
			NN_nln,
		]),
	])(d,p)
	return (d1,p1)
P_adtLine = notTerm(4,P_adtLine)
def _adtLine(d,p):
	d1,p1 = mor([
		serial([
			N_AR,
			term(lexer.tT_word),
			lWordList,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
def P_Dec(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_word),
			N_is,
			N_nln,
			P_optionDec,
			N_nln,
			_P_decLines,
			N_nln,
		]),
	])(d,p)
	return (d1,p1)
P_Dec = notTerm(5,P_Dec)
def P_optionDec(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_binary),
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
P_optionDec = notTerm(6,P_optionDec)
def _P_decLines(d,p):
	d1,p1 = mor([
		serial([
			P_expr,
			NN_nln,
			_decLines,
		]),
	])(d,p)
	return (d1,p1)
def _decLines(d,p):
	d1,p1 = mor([
		serial([
			P_expr,
			NN_nln,
			_decLines,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
def P_expr(d,p):
	d1,p1 = mor([
		serial([
			_exprs,
		]),
	])(d,p)
	return (d1,p1)
P_expr = notTerm(7,P_expr)
def _exprs(d,p):
	d1,p1 = mor([
		serial([
			_expr,
			N_sl,
			_exprs,
		]),
		serial([
			_expr,
		]),
	])(d,p)
	return (d1,p1)
def _expr(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_word),
		]),
		serial([
			P_constant,
		]),
		serial([
			P_lambda,
		]),
		serial([
			N_os,
			N_nln,
			P_expr,
			N_nln,
			N_cs,
		]),
	])(d,p)
	return (d1,p1)
def P_constant(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_number),
		]),
		serial([
			term(lexer.tT_literal),
		]),
	])(d,p)
	return (d1,p1)
P_constant = notTerm(8,P_constant)
def P_lambda(d,p):
	d1,p1 = mor([
		serial([
			N_Lambda,
			P_args,
			N_AR,
			P_expr,
		]),
	])(d,p)
	return (d1,p1)
P_lambda = notTerm(9,P_lambda)
def P_args(d,p):
	d1,p1 = mor([
		serial([
			arg,
			_args,
		]),
	])(d,p)
	return (d1,p1)
P_args = notTerm(10,P_args)
def _args(d,p):
	d1,p1 = mor([
		serial([
			arg,
			_args,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
def arg(d,p):
	d1,p1 = mor([
		serial([
			_arg,
		]),
		serial([
			N_os,
			arg,
			_args,
			N_cs,
		]),
	])(d,p)
	return (d1,p1)
def _arg(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_word),
		]),
		serial([
			P_constant,
		]),
	])(d,p)
	return (d1,p1)
def N_Lambda(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_LAMBDA),
		]),
	])(d,p)
	return (d1,p1)
N_Lambda = notSaveTerm(11,N_Lambda)
def N_nln(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_nln),
			N_nln,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
N_nln = notSaveTerm(11,N_nln)
def NN_nln(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_nln),
			N_nln,
		]),
	])(d,p)
	return (d1,p1)
NN_nln = notSaveTerm(11,NN_nln)
def N_is(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_is),
		]),
	])(d,p)
	return (d1,p1)
N_is = notSaveTerm(11,N_is)
def N_type(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_type),
		]),
	])(d,p)
	return (d1,p1)
N_type = notSaveTerm(11,N_type)
def N_AR(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_RIGHT_ARROW),
		]),
	])(d,p)
	return (d1,p1)
N_AR = notSaveTerm(11,N_AR)
def N_os(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_OPEN_S),
		]),
	])(d,p)
	return (d1,p1)
N_os = notSaveTerm(11,N_os)
def N_cs(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_CLOSE_S),
		]),
	])(d,p)
	return (d1,p1)
N_cs = notSaveTerm(11,N_cs)
def N_oc(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_OPEN_C),
		]),
	])(d,p)
	return (d1,p1)
N_oc = notSaveTerm(11,N_oc)
def N_cc(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_CLOSE_C),
		]),
	])(d,p)
	return (d1,p1)
N_cc = notSaveTerm(11,N_cc)
def N_oi(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_OPEN_I),
		]),
	])(d,p)
	return (d1,p1)
N_oi = notSaveTerm(11,N_oi)
def N_ci(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_CLOSE_I),
		]),
	])(d,p)
	return (d1,p1)
N_ci = notSaveTerm(11,N_ci)
def N_sem(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_SEM),
		]),
	])(d,p)
	return (d1,p1)
N_sem = notSaveTerm(11,N_sem)
def N_NONE(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_NONE),
		]),
	])(d,p)
	return (d1,p1)
N_NONE = notSaveTerm(11,N_NONE)
def N_sl(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_slash),
			N_nln,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
N_sl = notSaveTerm(11,N_sl)
sys.setrecursionlimit(2**10*2**16)

pP_START = 1
pP_typeDec = 2
pP_adtDec = 3
pP_adtLine = 4
pP_Dec = 5
pP_optionDec = 6
pP_expr = 7
pP_constant = 8
pP_lambda = 9
pP_args = 10
