#include <iostream>
#include <regex>
#include <sstream>
#include <vector>

using namespace std;


regex all("(?:\\/\\\\)[\\s\\S]*?(?:\\\\\\/)|\n|#.+?#|\"(?:(?:\\\\\")|[^\"])*?\"|\\b(?:is|true|false|is|else|import|load|name)\\b|\\b[A-Za-z_][A-Za-z0-9_]*\\b|\\b[0-9]+(\\.[0-9]+)?\\b|\\/=|--|\\+\\+|>=|<=|[-+*\\/=<>!|\\^\\.()\\[\\]{}\\\\'&,]");
regex comment("(\\/\\\\)[\\s\\S]*?(\\\\\\/)");
regex newline("\n");
regex compile_cmd("#.+?#");
regex string_r("\"(?:(?:\\\\\")|[^\"])*?\"");
regex keyword("\\b(?:is|true|false|is|else|import|load|name)\\b");
regex label("\\b[A-Za-z_][A-Za-z0-9_]*\\b");
regex number("\\b[0-9]+(\\.[0-9]+)?\\b");
regex characters("\\/=|--|\\+\\+|>=|<=|[-+*\\/=<>!|\\^\\.()\\[\\]{}\\\\'&,]");
cmatch res;

class Type{
    public:
        string type="Type";
        string data="";
        virtual Type* callF(string f,Type* arg)=0;
};
class Var
{
    public:
        string name="";
        Type* data;
        Var(string s,Type* d){
            name = s;
            data = d;
        }
};
class Nothing:Type{
    public:
        Nothing(){type="nothing";}
        Type* callF(string f,Type* arg){
            delete arg;
            cout << "ERORR: nothing"<<endl;
            exit(1);
            return (Type*)new Nothing();
        }
};
class Char: Type{
public:
    Char(){data="0";type="char";}
    Char(string d){data=d;type="char";}
    Type *callF(string f, Type *arg);
};
class Bool:Type{
    public:
        Bool(){data="0";type="bool";}
        Bool(string d){data=d;type="bool";}
        Type* callF(string f,Type* arg){
            bool a,b;
            string out;
            stringstream ss;
            ss<<this->data;
            ss>>a;
            if(arg->type=="bool") {
                ss.clear();
                ss << arg->data;
                ss >> b;
                if (f == "=") {
                    out = ((a==b)? "1":"0");
                    return (Type *) new Bool(out);
                }else if (f == "/=") {
                    out = ((a!=b)? "1":"0");
                    return (Type *) new Bool(out);
                }else if (f == "&") {
                    out = ((a&&b)? "1":"0");
                    return (Type *) new Bool(out);
                }else if (f == "|") {
                    out = ((a||b)? "1":"0");
                    return (Type *) new Bool(out);
                }else if (f == "^") {
                    out = ((a^b)? "1":"0");
                    return (Type *) new Bool(out);
                }
            }
            if (f == "n") {
                out = ((!a)? "1":"0");
                return (Type *) new Bool(out);
            }else if (f == "s") {
//                return (Type *) new String(this->data);
            }
            cout << "ERORR: no supported operation"<<endl;
            exit(1);
            return (Type*)new Nothing();

        }
};
class Num:Type{
    public:
        Num(){
            data="0";
            type = "num";
        }
        Num(string i){
            data=i;
            type = "num";
        }
        Type* callF(string f,Type* arg){
            float a=0,b=0;
            string out;
            stringstream ss;
            ss<<this->data;
            ss>>a;
            ss.clear();
            if(arg->type=="num") {
                ss << arg->data;
                ss >> b;
                if (f == "+") {
                    ss.clear();
                    ss << a + b;
                    ss >> out;
                    return (Type *) new Num(out);
                } else if (f == "-") {
                    ss.clear();
                    ss << a - b;
                    ss >> out;
                    return (Type *) new Num(out);
                } else if (f == "*") {
                    ss.clear();
                    ss << a * b;
                    ss >> out;
                    return (Type *) new Num(out);
                } else if (f == "/") {
                    ss.clear();
                    ss << a / b;
                    ss >> out;
                    return (Type *) new Num(out);
                }else if (f=="="){
                    out = ((a==b)? "1":"0");
                    return (Type*)new Bool(out);
                }else if (f=="/="){
                    out = ((a!=b)? "1":"0");
                    return (Type*)new Bool(out);
                }else if (f==">="){
                    out = ((a>=b)? "1":"0");
                    return (Type*)new Bool(out);
                }else if (f=="<="){
                    out = ((a<=b)? "1":"0");
                    return (Type*)new Bool(out);
                }else if (f==">"){
                    out = ((a>b)? "1":"0");
                    return (Type*)new Bool(out);
                }else if (f=="<"){
                    out = ((a<b)? "1":"0");
                    return (Type*)new Bool(out);
                }
            }
            if(f=="s"){

            }
            cout << "ERORR: no supported operation"<<endl;
            exit(1);
            return (Type*)new Nothing();
        }
};
class List:Type{
    public:
        vector<Type*> list;
        List(){data="";type="list";}
        Type *callF(string f, Type *arg);
};
class String:Type{
    public:
        String(){data="0";type="string";}
        String(string d){data=d;type="string";}
        Type* callF(string f, Type *arg){

        }
};
class Entity:Type{
    public:
        String(){data="0";type="string";}
        String(string d){data=d;type="string";}
        CodeSpace*
        Type* callF(string f, Type *arg){

        }
};

Type* Char::callF(string f,Type* arg){
    stringstream ss;
    string out="";
    if (f == "i") {
        ss << int(this->data[0]);
        ss>>out;
        return (Type *) new Num(out);
    }else if (f == "s") {
//                return (Type *) new String(this->data);
    }
    cout << "ERORR: no supported operation"<<endl;
    exit(1);
    return (Type*)new Nothing();

}

class AST{
public:
    bool isnode = true;
    string name="";
    AST* parent = nullptr;
    void* data;
    vector<AST*> childs;
    AST(){}
    AST(bool b, string n,AST* p,void* d){
        isnode =b;
        name = n;
        parent=p;
        data = d;
    }
};


class CodeSpace{
public:
    vector<Var> Vars;
    string code = "";
    CodeSpace(string c){
        code=c;
    }
    void print(AST* ast){
        if(ast->isnode){
            cout << "NODE:"<<ast->name<<" "<<ast->childs.size()<<endl;
            for(int i=0;i<ast->childs.size();i++){
                print(ast->childs[i]);
            }
        }else{
            cout << ast->name <<" "<< ((Type*)ast->data)->data<<endl;
        }
    }
    Type* run(AST* ast){
        cmatch res;
        if(ast->isnode){
            if(ast->name=="IS"){
                string name = run(ast->childs[0])->data;
                Type* data = run(ast->childs[1]);
                Vars.push_back(Var(name,data));
                return data;
            }else if(ast->name=="node"){
                return run(ast->childs[0]);
            }else if(regex_search(ast->name.c_str(),res,regex("F:"))){
                Type* t1 = run(ast->childs[0]);
                Type* t2 = run(ast->childs[1]);
                cout <<t1->type<<" "<< res.suffix()<<endl;
                return t1->callF(res.suffix(),t2);
            }else if(ast->name=="FF"){
                Type* t1 = run(ast->childs[0]);
                Type* t2 = run(ast->childs[1]);
                return t1->callF(t2->data,(Type*)new Nothing);
            }
        }else{
            if(ast->name=="label"&&ast->parent->name!="FF"){
                for(int i=0;i<Vars.size();i++){
                    if(Vars[i].name==((Type*)ast->data)->data){
                        return Vars[i].data;
                    }
                }
            }
            return (Type*)ast->data;
        }
        return (Type*)new Nothing();
    }
    void run(){
        code+="\n";
        regex_search(code.c_str(), res, all);
        AST* ast = new AST();
        AST* nownode = ast;
        // AST* tmp = new AST(false,"Hello",ast,(void*)new Num());
        // ast->childs.push_back(tmp);

        while (regex_search(code.c_str(), res, all)) {
            string noww=res[0];
            code = res.suffix();

            if(regex_search(noww.c_str(), res, comment)){
            }else if(regex_search(noww.c_str(), res, newline)){
                // print(ast);
                run(ast);
                delete ast;
                ast = new AST();
                nownode = ast;
            }else if(regex_search(noww.c_str(), res, compile_cmd)){
            }else if(regex_search(noww.c_str(), res, string_r)){
                if(noww.length()==3){
                    nownode->childs.push_back(new AST(false,"char",nownode,(void*)new Char(noww.substr(1,1))));
                }
            }else if(regex_search(noww.c_str(), res, keyword)){
                if(noww=="is"){
                    nownode->name = "IS";
                    nownode->childs.push_back(new AST(true,"node",nownode,(void*)new Num() ));
                    nownode=nownode->childs[1];
                }else if(noww=="false"){
                    nownode->childs.push_back(new AST(false,"bool",nownode,(void*)new Bool("0")));
                }else if(noww=="true"){
                    nownode->childs.push_back(new AST(false,"bool",nownode,(void*)new Bool("1")));
                }
            }else if(regex_search(noww.c_str(), res, label)){
                nownode->childs.push_back(new AST(false,"label",nownode,(void*)new Num(res[0]) ));
            }else if(regex_search(noww.c_str(), res, number)){
                nownode->childs.push_back(new AST(false,"num",nownode,(void*)new Num(res[0])));
            }else if(regex_search(noww.c_str(), res, characters)){
                if(noww=="("){
                    nownode->childs.push_back(new AST(true,"node",nownode,(void*)new Num() ));
                    nownode=nownode->childs[nownode->childs.size()-1];
                }else if(noww==")"){
                    nownode = nownode->parent;
                }else if(regex_search(noww.c_str(),res,regex("[+-]"))){
                    AST* tmp = nownode;
                    nownode = new AST(true,"F:"+noww,tmp->parent,(void*)new Num());
                    tmp->parent->childs[tmp->parent->childs.size()-1]=nownode;
                    nownode->childs.push_back(tmp);
                }else if(regex_search(noww.c_str(),res,regex("[*/]"))){
                    if(!regex_search(nownode->name.c_str(),res,regex("[+-]"))) {
                        AST *tmp = nownode;
                        nownode = new AST(true, "F:" + noww, tmp->parent, (void *) new Num());
                        tmp->parent->childs[tmp->parent->childs.size() - 1] = nownode;
                        nownode->childs.push_back(tmp);
                    }else{
                        AST *tmp = nownode->childs[1];
                        nownode->childs[1] = new AST(true, "F:" + noww, nownode, (void *) new Num());
                        nownode = nownode->childs[1];
                        tmp->parent = nownode;
                        nownode->childs.push_back(tmp);
                    }
                }else if(noww=="."){
                    AST *tmp = nownode;
                    nownode = new AST(true, "FF", tmp->parent, (void *) new Num());
                    tmp->parent->childs[tmp->parent->childs.size() - 1] = nownode;
                    nownode->childs.push_back(tmp);
                }else if(regex_search(noww.c_str(),res,regex("=|/=|>|<|>=|<="))){
                    if(!regex_search(nownode->name.c_str(),res,regex("[\\|&\\^]"))) {
                        AST *tmp = nownode;
                        nownode = new AST(true, "F:" + noww, tmp->parent, (void *) new Num());
                        tmp->parent->childs[tmp->parent->childs.size() - 1] = nownode;
                        nownode->childs.push_back(tmp);
                    }else{
                        AST *tmp = nownode->childs[1];
                        nownode->childs[1] = new AST(true, "F:" + noww, nownode, (void *) new Num());
                        nownode = nownode->childs[1];
                        tmp->parent = nownode;
                        nownode->childs.push_back(tmp);
                    }
                }else if(regex_search(noww.c_str(),res,regex("[\\|&\\^]"))){
                    AST *tmp = nownode;
                    nownode = new AST(true, "F:" + noww, tmp->parent, (void *) new Num());
                    tmp->parent->childs[tmp->parent->childs.size() - 1] = nownode;
                    nownode->childs.push_back(tmp);
                }
            }
        }
    }

    void showVars() {
        for(int i=0;i<Vars.size();i++){
            cout << Vars[i].name <<" = "<<Vars[i].data->data<<endl;
        }
    }
};

int main(){
    string code ="a is 6\ni is 0\nb is 5\nc is 3*5+6/3\nfirst_bool is true.n\nfirst_char is \"0\".i\na23 is (a>b).n^b>a";
    CodeSpace n = CodeSpace(code);
    n.run();
    n.showVars();
    cout <<endl;
}
