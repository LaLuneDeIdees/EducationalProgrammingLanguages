//g++ -ldl run.cpp -o run && ./run
// std:{./stdio}clib
// {hello}std.print
// r:{start: {r}std.print {2+4*(6-7)/4} std.calc end: {start|end} lclr r } std.function r
#include <iostream>
#include <dlfcn.h>
#include <deque>
#include <fstream> //while i write interpriter
using namespace std;

struct Symbol{
    string name="";
    int index=0;
};

deque<Symbol> symbols;

struct Library{
    string name="\0";
    string fullFilePath="\0";
    void* library=nullptr;
};
deque<Library> libraries;

deque<string> stack;

//special characters: ' . { } : "
// . if object is Clib, call sym func
// ' push spesial symbol to stack
// " rebind value from stack, if it's special symbol, stop, replaces already loaded, meta deforming code
// {} constant
// : declared symbol

//special world: llib clib
string buf="";
deque<string> inputBufferS;

void loadLib(){
    string filename = stack.back().substr(0,stack.back().find("\1"));

    Library l;
    int cursor = filename.find_last_of("/");

    l.name=filename;
    if(cursor>=0)
        l.name = filename.substr(cursor+1);

    for(auto i:libraries)if(i.name==l.name){
            stack.pop_back();
            stack.push_back(i.name+"\1clib");
            return;
        }

    l.library = dlopen((filename+".so").c_str(),RTLD_LAZY);

    if(l.library==nullptr){
        cout << "error load c library"<<endl;
        return;
    };

    libraries.push_back(l);
    stack.pop_back();
    stack.push_back(l.name+"\1clib");
}
void loadLLib(){
    string fname = stack.back().substr(0,stack.back().find("\1"));
    stack.pop_back();
    ifstream inputf(fname+".ldi");
    if(!inputf.is_open()){
        cout<<"ERROR load library\n";
        return;
    }
    string code="";
    while (!inputf.eof())
    {
        string line;
        getline(inputf,line);
        code+=line+'\n';
    }
    inputBufferS.push_back(code);
}
void callFuncFromLib(string lib,string func){
    Library l;
    for(auto i:libraries)if(i.name==lib)l=i;
    if(l.library==nullptr)return;
    void (*f)(deque<string>&);
    f = (void (*)(deque<string>&))dlsym(l.library,func.c_str());
    if(f!=nullptr){
        f(stack);
        // stack.pop_back();
        // if(out!="\1NOTHING")stack.push_back(out);
    }
}

string dataFromSym(string name){

    deque<Symbol>::iterator from = symbols.end();
    deque<Symbol>::iterator to = symbols.begin();
    for(;from>=to;from--){
        if((*from).name==name){
            return stack[(*from).index];
        }
    }
    return stack[Symbol().index];
}
Symbol symFromName(string name){
    for(int i=symbols.size()-1;i>=0;i--){
        if(symbols[i].name==name){
            return symbols[i];
        }
    }
    return Symbol();
}
void clcr(){
    string distance = stack.back();
    distance = distance.substr(0,distance.find("\1"));
    stack.pop_back();
    string from = distance.substr(0,distance.find('|'));
    string to = distance.substr(distance.find('|')+1);
    Symbol fromS = symFromName(from);
    Symbol toS = symFromName(to);
    int fromI = fromS.index;
    int toI = toS.index;

    stack.erase(stack.begin()+fromI,stack.begin()+toI);

    for(int i=symbols.size();i>=0;i--){
        // cout << symbols[i].name<<endl;
        if(symbols[i].name==fromS.name){
            while(symbols[i].name!=toS.name){
                symbols.erase(symbols.begin()+i);
            }
            symbols.erase(symbols.begin()+i);
            break;
        }
    }
}

void checkString(string word){
    if(word=="")return;
    if(word[word.size()-1]==':'){
        Symbol s;
        s.name = word.substr(0,word.size()-1);
        s.index = (int)stack.size();
        symbols.push_back(s);
    }else if(word == "clib"){
        loadLib();
    }else if(word == "llib"){
        loadLLib();
    }else if(word == "lclr"){
        clcr();
    }else if(word == "\""){
        symbols.back().index--;
    }else if(word == "'"){
        inputBufferS.push_back(stack.back().substr(0,stack.back().find("\1")));
        stack.pop_back();
    }else{
        int cursor;
        if((cursor=word.find("."))>=0){
            string data = dataFromSym(word.substr(0,cursor));
            if(data.substr(data.find('\1')+1)=="clib"){
                callFuncFromLib(data.substr(0,data.find('\1')),word.substr(cursor+1));
            }
        }else{
            stack.push_back(dataFromSym(word));
        }
    }
}
void run(){
    char tmp[1];
    
    int lastsize = inputBufferS.size();
    while(inputBufferS.size()>0)
    {
        if(inputBufferS.back().size()==0){
            inputBufferS.pop_back();
            continue;
        }
        if(abs(int(lastsize-inputBufferS.size())>100)){
            for(int i=0;i<inputBufferS.size();i++)if(inputBufferS[i]=="")inputBufferS.erase(inputBufferS.begin()+ i--);
            lastsize = inputBufferS.size();
        }
        tmp[0] = inputBufferS.back()[0];
        inputBufferS.back().erase(inputBufferS.back().begin(),inputBufferS.back().begin()+1);

        if(tmp[0]=='{'){
            checkString(buf);
            buf="";
            int level = 1;
            char last = ' ';
            while(true){
                if(inputBufferS.back().size()==0){
                    inputBufferS.pop_back();
                    continue;
                }
                tmp[0] = inputBufferS.back()[0];
                inputBufferS.back().erase(inputBufferS.back().begin(),inputBufferS.back().begin()+1);

                if(last=='\\'){
                    buf.erase(buf.end()-1,buf.end());
                }else if(tmp[0]=='{'){level++;}
                else if(tmp[0]=='}'){
                    level--;
                    if(level==0){
                        stack.push_back(buf+"\1default");
                        buf="";
                        break;
                    }
                }
                
                last=tmp[0];
                buf+=tmp[0];

            }
        }else if(tmp[0]==' ' || tmp[0]=='\t' || tmp[0]=='\n'){
            checkString(buf);
            buf="";
        }else if(tmp[0]=='"' ||
                 tmp[0]=='\''){
            checkString(buf);
            buf="";
            checkString(tmp);
        }else if(tmp[0]==':'){
            checkString(buf+tmp[0]);
            buf="";
        }else if(tmp[0]=='|'){
            while(tmp[0]!='\n'){
                tmp[0] = inputBufferS.back()[0];
                inputBufferS.back().erase(inputBufferS.back().begin(),inputBufferS.back().begin()+1);
            }
        }else{
            buf+=tmp[0];
        }
    }
    checkString(buf);
    buf="";
}

int main(int argc,char** arga){
    if(argc<2){
        while(true){
            string line;
            getline(cin,line);
            inputBufferS.push_front(line);
            run();
        }
    }else{
        ifstream input(arga[1]);
        if(!input.is_open()){
            cout << "error open file\n";
            return -1;
        }
        while (!input.eof())
        {
            string line;
            getline(input,line);
            inputBufferS.push_front(line+'\n');
        }
        run();
    }
//    for(auto i:symbols)cout << i.name << " " << i.index << endl;

    for(auto i:libraries)
        dlclose(i.library);
    return 0;
}
