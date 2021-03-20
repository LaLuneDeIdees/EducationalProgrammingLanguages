# -*- coding: utf-8 -*-
"""
Редактор Spyder

Это временный скриптовый файл.
"""

import lexer
import parser
import sys
sys.settrace(None)
sys.setrecursionlimit(1024*32)
#8192
file = open("/home/lune/Документы/code/c++/MyProgramLang/ver6/CODE.txt",'r')#codeTest.txt","r")

s = file.read()
#s = '''
#import = \\a,v:g{
#    2+5
#}
#'''

def eraseFirstNln(l):
    if l == []:
        return []
    if l[0][0]==lexer.T_NLN:
        return eraseFirstNln(l[1:])
    else:
        return l

ts1 = eraseFirstNln(list(filter((lambda x:x[0]!=lexer.T_PREPROC),lexer.toTokens(s+'\n'))))


for i in ts1:
    print(i)

p1 = parser.fixTree(parser.Parse(ts1))

fout = open('/tmp/graph.dot','w')

fout.write('''graph tr {
''')
idx = 0
def drawTree(i,l,rodix):
    global idx
    thix = 'n'+str(idx)
    idx+=1
    if type(l) != list:
        fout.write(str(thix) + ' [label="'+str(l)+'"];')
        fout.write(str(rodix)+' -- '+str(thix)+';')
#        print('*'*i,l)
#        print()
    elif l != []:
        if type(l[0]) == int:
#            if len(l) == 1:
#                thix=rodix
#            elif len(l) == 2:
#                drawTree(i+1,l[1],thix)
#                return
#            else:
#            if len(l) == 2:
#                drawTree(i+1,l[1],rodix)
#                return
            fout.write(str(thix)+' [label="'+str(l[0])+'"];')
            fout.write(str(rodix)+' -- '+str(thix)+';')
            l = l[1:]
        else:
            thix = rodix
#            print(thix,';')
#        print(rodix,'-
# type system-',thix,';')
        for k in l:
            drawTree(i+1,k,thix)
drawTree(0,p1[1],0)

fout.write('''}
''')
fout.close()



#TODO
# SYNTAX_ANALIZE:
# cast to ast
# symbols table
# expression check (other in switch, get index from name)

# typedeclared
# type system
# calculate constatnt
# lambda lifting

# open expr to calculus

# acicle graph
# simpler to 3-x addr command