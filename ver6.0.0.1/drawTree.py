idx = 0
def draw(tree):
    global idx
    idx = 0
    
    fout = open('ats.dot','w')
    fout.write('''
    graph ast{
    ''')

    

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
