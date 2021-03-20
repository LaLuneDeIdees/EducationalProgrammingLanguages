//g++ -shared -fPIC  stdio.cpp -o stdio.so
#include <iostream>
#include <cmath>
#include <deque>

using namespace std;

extern "C" void print(deque<string>& stack){
    cout << string(stack.back()).substr(0,string(stack.back()).find("\1")) << endl;
    stack.pop_back();
}
extern "C" void function(deque<string>& stack){
    string out = stack.back().substr(0,stack.back().find("\1"))+"\1function";
    stack.pop_back();
    stack.push_back(out);
}
extern "C" void replace(deque<string>& stack){
    string data = stack.back();stack.pop_back();
    data = data.substr(0,data.find("\1"));
    string to = stack.back();stack.pop_back();
    to = to.substr(0,to.find("\1"));
    string from = stack.back();stack.pop_back();
    from = from.substr(0,from.find("\1"));
    int cursor = data.find(from,0);
    while(cursor!=-1){
        data = data.replace(cursor,from.size(),to);
        cursor = data.find(from,cursor+to.size());
    }
    stack.push_back(data+"\1default");
    // TODO: replace from string in while loop with find and replace cmd
    // cout << string(str).substr(0,string(str).find("\1")) << endl;
    // return string(str).substr(0,string(str).find("\1"))+"\1function";
}
extern "C" void If(deque<string>& stack){
    string elseF = stack.back();stack.pop_back();
    string ifF = stack.back();stack.pop_back();
    string condition = stack.back();stack.pop_back();
    if(condition[0]=='0')stack.push_back(elseF);
    else stack.push_back(ifF);

    // cout << string(str).substr(0,string(str).find("\1")) << endl;
    // return string(str).substr(0,string(str).find("\1"))+"\1function";
}
extern "C" void minus(deque<string>& stack){
    double b = stod(stack.back().substr(0,stack.back().find("\1")));
    stack.pop_back();
    double a = stod(stack.back().substr(0,stack.back().find("\1")));
    stack.pop_back();
    stack.push_back(to_string(a-b)+"\1default");
}
extern "C" void plus(deque<string>& stack){
    double b = stod(stack.back().substr(0,stack.back().find("\1")));
    stack.pop_back();
    double a = stod(stack.back().substr(0,stack.back().find("\1")));
    stack.pop_back();
    stack.push_back(to_string(a+b)+"\1default");
}

extern "C" void mult(deque<string>& stack){
    double b = stod(stack.back().substr(0,stack.back().find("\1")));
    stack.pop_back();
    double a = stod(stack.back().substr(0,stack.back().find("\1")));
    stack.pop_back();
    stack.push_back(to_string(a*b)+"\1default");
}
extern "C" void del(deque<string>& stack){
    stack.pop_back();
}
extern "C" void concat(deque<string>& stack){
    string b = (stack.back().substr(0,stack.back().find("\1")));
    stack.pop_back();
    string a = (stack.back().substr(0,stack.back().find("\1")));
    stack.pop_back();
    stack.push_back((a+b)+"\1default");
}
extern "C" void getChar(deque<string>& stack){
    int n = stoi(stack.back().substr(0,stack.back().find("\1")));
    stack.pop_back();
    string s = (stack.back().substr(0,stack.back().find("\1")));
    stack.pop_back();
    stack.push_back(s[n]+"\1default");
}
extern "C" void charCode(deque<string>& stack){
    string ch= (stack.back().substr(0,stack.back().find("\1")));
    stack.pop_back();
    stack.push_back(to_string(ch[0])+"\1default");
}
extern "C" void calc(deque<string>& stack){
    string sss = stack.back();
    stack.pop_back();

    if(sss.substr(sss.find("\1")+1)!="default")stack.push_back("0\1default");

    string code = sss.substr(0,sss.find("\1"));
    deque<string> stek;
    deque<string> out_stek;
    out_stek.push_back("0");
    string buffer="";

    for(auto i:code){
        string is = string(1,i);
        if(string("1234567890.").find(is)!=-1){
            buffer+=is;
        }else if(string("+-*/^").find(is)!=-1){
            if(buffer!="")out_stek.push_back(buffer);buffer="";
            while (stek.size()>0)
            {
                if(string("+-").find(is)!=-1 && string("+-*/^").find(stek.back())!=-1){
                    out_stek.push_back(stek.back());
                    stek.pop_back();
                }else if(string("*/").find(is)!=-1 && string("*/^").find(stek.back())!=-1){
                    out_stek.push_back(stek.back());
                    stek.pop_back();
                }else if(string("^").find(is)!=-10 && string("^").find(stek.back())!=-1){
                    out_stek.push_back(stek.back());
                    stek.pop_back();
                }else break;
            }
            stek.push_back(is);
        }else if(is=="("){
            if(buffer!="")out_stek.push_back(buffer);buffer="";
            stek.push_back(is);
        }else if(is==")"){
            if(buffer!="")out_stek.push_back(buffer);buffer="";
            while (stek.back()!="(")
            {
                out_stek.push_back(stek.back());
                stek.pop_back();
            }
            stek.pop_back();
        }else{
            if(buffer!="")out_stek.push_back(buffer);buffer="";
        }
    }
    if(buffer!="")out_stek.push_back(buffer);buffer="";
    while (stek.size()>0)
    {
        out_stek.push_back(stek.back());
        stek.pop_back();
    }
    for(int i=0;i<out_stek.size();i++){

        if(string("+-*/^").find(out_stek[i])!=-1){
            double arg1 = stod(out_stek[i-2]);
            double arg2 = stod(out_stek[i-1]);
            if(out_stek[i]=="+")out_stek[i-2] = to_string(arg1 + arg2);
            if(out_stek[i]=="-")out_stek[i-2] = to_string(arg1 - arg2);
            if(out_stek[i]=="*")out_stek[i-2] = to_string(arg1 * arg2);
            if(out_stek[i]=="/")out_stek[i-2] = to_string(arg1 / arg2);
            if(out_stek[i]=="^")out_stek[i-2] = to_string(pow(arg1,arg2));

            out_stek.erase(out_stek.begin()+i-1);
            out_stek.erase(out_stek.begin()+i-1);
            i-=2;
        }
    }
    stack.push_back(out_stek.back()+"\1default");
}

int main(){
}