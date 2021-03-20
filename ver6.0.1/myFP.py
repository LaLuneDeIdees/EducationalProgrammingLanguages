

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
			lines,
			N_NONE,
		]),
	])(d,p)
	return (d1,p1)
P_START = notTerm(1,P_START)
def lines(d,p):
	d1,p1 = mor([
		serial([
			line,
			N_nln,
			lines,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
def line(d,p):
	d1,p1 = mor([
		serial([
			P_Declare,
		]),
		serial([
			P_TypeDeclare,
		]),
		serial([
			P_sugar,
		]),
	])(d,p)
	return (d1,p1)
def _wordList(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_word),
			_wordList,
		]),
		serial([
			term(lexer.tT_word),
		]),
	])(d,p)
	return (d1,p1)
def P_sugar(d,p):
	d1,p1 = mor([
		serial([
			N_sugar,
			_wordList,
			NN_nln,
		]),
	])(d,p)
	return (d1,p1)
P_sugar = notTerm(2,P_sugar)
def P_TypeNotAdtDec(d,p):
	d1,p1 = mor([
		serial([
			N_type,
			term(lexer.tT_word),
			N_is,
			N_nln,
			P_TNAD_decT_lines,
		]),
	])(d,p)
	return (d1,p1)
P_TypeNotAdtDec = notTerm(3,P_TypeNotAdtDec)
def P_TNAD_decT_lines(d,p):
	d1,p1 = mor([
		serial([
			_TNAD_decT_lines,
		]),
	])(d,p)
	return (d1,p1)
P_TNAD_decT_lines = notTerm(4,P_TNAD_decT_lines)
def _TNAD_decT_lines(d,p):
	d1,p1 = mor([
		serial([
			_TNAD_decT,
			NN_nln,
			_TNAD_decT_lines,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
def _TNAD_decT(d,p):
	d1,p1 = mor([
		serial([
			P_typeSig,
		]),
	])(d,p)
	return (d1,p1)
def P_TypeDeclare(d,p):
	d1,p1 = mor([
		serial([
			N_type,
			term(lexer.tT_word),
			P_TD_arg,
			N_is,
			N_nln,
			_TD_decTline,
		]),
	])(d,p)
	return (d1,p1)
P_TypeDeclare = notTerm(5,P_TypeDeclare)
def _TD_decTline(d,p):
	d1,p1 = mor([
		serial([
			P_decT_lines,
		]),
	])(d,p)
	return (d1,p1)
def P_TD_arg(d,p):
	d1,p1 = mor([
		serial([
			N_with,
			_TD_arg_list,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
P_TD_arg = notTerm(6,P_TD_arg)
def _TD_arg_list(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_word),
			_TD_arg_list,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
def P_decT_lines(d,p):
	d1,p1 = mor([
		serial([
			_decT_lines,
		]),
	])(d,p)
	return (d1,p1)
P_decT_lines = notTerm(7,P_decT_lines)
def _decT_lines(d,p):
	d1,p1 = mor([
		serial([
			_decT,
			NN_nln,
			_decT_lines,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
def _decT(d,p):
	d1,p1 = mor([
		serial([
			P_DecType,
		]),
		serial([
			P_tipSig,
		]),
	])(d,p)
	return (d1,p1)
def P_DecType(d,p):
	d1,p1 = mor([
		serial([
			P_decOptions,
			term(lexer.tT_word),
			N_AR,
			P_tipSig,
		]),
		serial([
			term(lexer.tT_word),
		]),
	])(d,p)
	return (d1,p1)
P_DecType = notTerm(8,P_DecType)
def P_decOptions(d,p):
	d1,p1 = mor([
		serial([
			_decOptions,
		]),
	])(d,p)
	return (d1,p1)
P_decOptions = notTerm(9,P_decOptions)
def _decOptions(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_evalT),
			_decOptions,
		]),
		serial([
			term(lexer.tT_binary),
			_decOptions,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
def P_Declare(d,p):
	d1,p1 = mor([
		serial([
			_decName,
			N_is,
			N_nln,
			P_DEC_options,
			_decExprList,
		]),
	])(d,p)
	return (d1,p1)
P_Declare = notTerm(10,P_Declare)
def _decName(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_word),
		]),
	])(d,p)
	return (d1,p1)
def _decExprList(d,p):
	d1,p1 = mor([
		serial([
			P_Expr,
			NN_nln,
			_decExprList,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
def dec_oneOption(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_binary),
		]),
		serial([
			term(lexer.tT_evalT),
		]),
		serial([
			term(lexer.tT_inline),
		]),
		serial([
			P_tip,
		]),
	])(d,p)
	return (d1,p1)
def replace(d,p):
	d1,p1 = mor([
		serial([
			P_tip,
			to,
			P_type,
		]),
	])(d,p)
	return (d1,p1)
def _DEC_options(d,p):
	d1,p1 = mor([
		serial([
			dec_oneOption,
			NN_nln,
			_DEC_options,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
def P_DEC_options(d,p):
	d1,p1 = mor([
		serial([
			_DEC_options,
		]),
	])(d,p)
	return (d1,p1)
P_DEC_options = notTerm(11,P_DEC_options)
def P_tip(d,p):
	d1,p1 = mor([
		serial([
			_ser,
			N_AR,
			P_tip,
		]),
		serial([
			_ser,
		]),
	])(d,p)
	return (d1,p1)
P_tip = notTerm(12,P_tip)
def _ser(d,p):
	d1,p1 = mor([
		serial([
			P_ser,
		]),
		serial([
			N_os,
			_ser,
			N_cs,
		]),
		serial([
			N_os,
			P_tip,
			N_cs,
		]),
		serial([
			term(lexer.tT_word),
		]),
	])(d,p)
	return (d1,p1)
def P_ser(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_word),
			_ser,
		]),
	])(d,p)
	return (d1,p1)
P_ser = notTerm(13,P_ser)
def P_tipSig(d,p):
	d1,p1 = mor([
		serial([
			_varSig,
			_tailSig,
		]),
		serial([
			_varSig,
		]),
	])(d,p)
	return (d1,p1)
P_tipSig = notTerm(14,P_tipSig)
def _tailSig(d,p):
	d1,p1 = mor([
		serial([
			P_tailSig,
		]),
		serial([
			_varSig,
		]),
	])(d,p)
	return (d1,p1)
def P_tailSig(d,p):
	d1,p1 = mor([
		serial([
			_varSig,
			_tailSig,
		]),
	])(d,p)
	return (d1,p1)
P_tailSig = notTerm(15,P_tailSig)
def _varSig(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_word),
		]),
		serial([
			N_os,
			P_tipSig,
			N_cs,
		]),
	])(d,p)
	return (d1,p1)
def _P_tipSig(d,p):
	d1,p1 = mor([
		serial([
			_serSig,
		]),
	])(d,p)
	return (d1,p1)
def _serSig(d,p):
	d1,p1 = mor([
		serial([
			P_serSig,
		]),
		serial([
			N_os,
			_serSig,
			N_cs,
		]),
		serial([
			term(lexer.tT_word),
		]),
	])(d,p)
	return (d1,p1)
def P_serSig(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_word),
			_serSig,
		]),
	])(d,p)
	return (d1,p1)
P_serSig = notTerm(16,P_serSig)
def P_type(d,p):
	d1,p1 = mor([
		serial([
			P_typeSig,
			N_AR,
			_type_serialize,
		]),
		serial([
			P__type_serialize1,
			N_AR,
			_type_serialize,
		]),
	])(d,p)
	return (d1,p1)
P_type = notTerm(17,P_type)
def _type_serialize(d,p):
	d1,p1 = mor([
		serial([
			P_typeSig,
			N_AR,
			_type_serialize,
		]),
		serial([
			P_typeSig,
		]),
		serial([
			P__type_serialize1,
			N_AR,
			_type_serialize,
			#,
		]),
	])(d,p)
	return (d1,p1)
def P__type_serialize1(d,p):
	d1,p1 = mor([
		serial([
			N_os,
			_type_serialize,
			N_cs,
		]),
	])(d,p)
	return (d1,p1)
P__type_serialize1 = notTerm(18,P__type_serialize1)
def P_wordWithPtr(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_word),
		]),
	])(d,p)
	return (d1,p1)
P_wordWithPtr = notTerm(19,P_wordWithPtr)
def _typeSig(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_word),
			_typeSig,
		]),
		serial([
			P__typeSig,
			_typeSig,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
def P__typeSig(d,p):
	d1,p1 = mor([
		serial([
			N_os,
			_typeSig,
			N_cs,
		]),
	])(d,p)
	return (d1,p1)
P__typeSig = notTerm(20,P__typeSig)
def P_typeSig(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_word),
			_typeSig,
		]),
		serial([
			P__typeSig,
			_typeSig,
		]),
		serial([
			P_DO,
		]),
	])(d,p)
	return (d1,p1)
P_typeSig = notTerm(21,P_typeSig)
def P_Expr(d,p):
	d1,p1 = mor([
		serial([
			_Expr_list,
			_typeCast,
		]),
	])(d,p)
	return (d1,p1)
P_Expr = notTerm(22,P_Expr)
def _typeCast(d,p):
	d1,p1 = mor([
		serial([
			N_as,
			P_tipSig,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
def _Expr_list(d,p):
	d1,p1 = mor([
		serial([
			_Expr,
			_Expr_list,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
def _Expr(d,p):
	d1,p1 = mor([
		serial([
			P_constant,
		]),
		serial([
			P_Lambda,
		]),
		serial([
			P_word,
		]),
		serial([
			P_IDX,
		]),
		serial([
			P_newScope,
		]),
	])(d,p)
	return (d1,p1)
def P_newScope(d,p):
	d1,p1 = mor([
		serial([
			N_os,
			N_nln,
			P_Expr,
			N_nln,
			_nSS,
			N_nln,
			N_cs,
		]),
	])(d,p)
	return (d1,p1)
P_newScope = notTerm(23,P_newScope)
def _nSS(d,p):
	d1,p1 = mor([
		serial([
			lines,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
def P_Lambda(d,p):
	d1,p1 = mor([
		serial([
			N_Lambda,
			P_Lam_typeSig,
			N_AR,
			P_Expr,
		]),
	])(d,p)
	return (d1,p1)
P_Lambda = notTerm(24,P_Lambda)
def _lwordWithPtr(d,p):
	d1,p1 = mor([
		serial([
			P_wordWithPtr,
		]),
		serial([
			P_constant,
		]),
	])(d,p)
	return (d1,p1)
def _LtypeSig(d,p):
	d1,p1 = mor([
		serial([
			_lwordWithPtr,
			_LtypeSig,
		]),
		serial([
			P__LtypeSig,
			_LtypeSig,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
def P__LtypeSig(d,p):
	d1,p1 = mor([
		serial([
			N_os,
			_LtypeSig,
			N_cs,
		]),
	])(d,p)
	return (d1,p1)
P__LtypeSig = notTerm(25,P__LtypeSig)
def P_Lam_typeSig(d,p):
	d1,p1 = mor([
		serial([
			_lwordWithPtr,
			_LtypeSig,
		]),
		serial([
			P__LtypeSig,
			_LtypeSig,
		]),
	])(d,p)
	return (d1,p1)
P_Lam_typeSig = notTerm(26,P_Lam_typeSig)
def P_word(d,p):
	d1,p1 = mor([
		serial([
			_getAddr,
			term(lexer.tT_word),
		]),
	])(d,p)
	return (d1,p1)
P_word = notTerm(27,P_word)
def _getAddr(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_GET_ADDR),
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
def P_IDX(d,p):
	d1,p1 = mor([
		serial([
			N_oi,
			P_Expr,
			N_ci,
		]),
	])(d,p)
	return (d1,p1)
P_IDX = notTerm(28,P_IDX)
def P_DO(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_DO),
		]),
	])(d,p)
	return (d1,p1)
P_DO = notTerm(29,P_DO)
def P_constant(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_number),
		]),
		serial([
			term(lexer.tT_BOOL),
		]),
		serial([
			term(lexer.tT_literal),
		]),
		serial([
			N_oc,
			_arraList,
			N_cc,
		]),
	])(d,p)
	return (d1,p1)
P_constant = notTerm(30,P_constant)
def _arraList(d,p):
	d1,p1 = mor([
		serial([
			_arraList1,
		]),
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
def _arraList1(d,p):
	d1,p1 = mor([
		serial([
			P_Expr,
			N_sem,
			_arraList1,
		]),
		serial([
			P_Expr,
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
N_Lambda = notSaveTerm(31,N_Lambda)
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
N_nln = notSaveTerm(31,N_nln)
def NN_nln(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_nln),
			N_nln,
		]),
	])(d,p)
	return (d1,p1)
NN_nln = notSaveTerm(31,NN_nln)
def N_is(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_is),
		]),
	])(d,p)
	return (d1,p1)
N_is = notSaveTerm(31,N_is)
def N_type(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_type),
		]),
	])(d,p)
	return (d1,p1)
N_type = notSaveTerm(31,N_type)
def N_AR(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_RIGHT_ARROW),
		]),
	])(d,p)
	return (d1,p1)
N_AR = notSaveTerm(31,N_AR)
def N_os(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_OPEN_S),
		]),
	])(d,p)
	return (d1,p1)
N_os = notSaveTerm(31,N_os)
def N_cs(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_CLOSE_S),
		]),
	])(d,p)
	return (d1,p1)
N_cs = notSaveTerm(31,N_cs)
def N_oc(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_OPEN_C),
		]),
	])(d,p)
	return (d1,p1)
N_oc = notSaveTerm(31,N_oc)
def N_cc(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_CLOSE_C),
		]),
	])(d,p)
	return (d1,p1)
N_cc = notSaveTerm(31,N_cc)
def N_oi(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_OPEN_I),
		]),
	])(d,p)
	return (d1,p1)
N_oi = notSaveTerm(31,N_oi)
def N_ci(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_CLOSE_I),
		]),
	])(d,p)
	return (d1,p1)
N_ci = notSaveTerm(31,N_ci)
def N_sem(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_SEM),
		]),
	])(d,p)
	return (d1,p1)
N_sem = notSaveTerm(31,N_sem)
def N_NONE(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_NONE),
		]),
	])(d,p)
	return (d1,p1)
N_NONE = notSaveTerm(31,N_NONE)
def N_with(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_with),
		]),
	])(d,p)
	return (d1,p1)
N_with = notSaveTerm(31,N_with)
def N_sugar(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_sugar),
		]),
	])(d,p)
	return (d1,p1)
N_sugar = notSaveTerm(31,N_sugar)
def N_adt(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_adt),
		]),
	])(d,p)
	return (d1,p1)
N_adt = notSaveTerm(31,N_adt)
def P_empty(d,p):
	d1,p1 = mor([
		serial([
			empty,
		]),
	])(d,p)
	return (d1,p1)
P_empty = notTerm(31,P_empty)
def N_as(d,p):
	d1,p1 = mor([
		serial([
			term(lexer.tT_as),
		]),
	])(d,p)
	return (d1,p1)
N_as = notSaveTerm(32,N_as)
sys.setrecursionlimit(2**10*2**16)

pP_START = 1
pP_sugar = 2
pP_TypeNotAdtDec = 3
pP_TNAD_decT_lines = 4
pP_TypeDeclare = 5
pP_TD_arg = 6
pP_decT_lines = 7
pP_DecType = 8
pP_decOptions = 9
pP_Declare = 10
pP_DEC_options = 11
pP_tip = 12
pP_ser = 13
pP_tipSig = 14
pP_tailSig = 15
pP_serSig = 16
pP_type = 17
pP__type_serialize1 = 18
pP_wordWithPtr = 19
pP__typeSig = 20
pP_typeSig = 21
pP_Expr = 22
pP_newScope = 23
pP_Lambda = 24
pP__LtypeSig = 25
pP_Lam_typeSig = 26
pP_word = 27
pP_IDX = 28
pP_DO = 29
pP_constant = 30
pP_empty = 31
