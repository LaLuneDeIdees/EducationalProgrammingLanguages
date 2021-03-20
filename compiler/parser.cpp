#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

#define in(x) (int(string(x).find(ss[i])) >=0)
using namespace std;
#define keywords_num 22
string keywords[keywords_num]={
"is",//a
"with",//b
"where",//c
"for",//d
"while",//e
"return",//f
"break",//g
"continue",//h
"if",//i
"elis",//j
"elif",//k
"new",//l
"true",//m
"false",//n
"call",//o
"cpp",//p
"try",//q
"catch",//r
"finally",//s
"syscall",//t
"[=]",//u
"[==]",//v
};
struct tokens{
	string type="";
	string data="";
	tokens* next=nullptr;
};
tokens tok(string type,string data){
	tokens t = tokens();
	t.type=type;
	t.data=data;
	return t;
}
vector<tokens> l1;
vector<void*> tmplist;
void process_word(string word,stringstream* ss){
	for(int i=0;i<keywords_num;i++){
		if(word==keywords[i]){
			l1.push_back(tok((string)"KEYWORD:", word));
			return;
		}
	}
	for(int i=0;i<word.length();i++){
		if(!(word[i]>='0' && word[i]<='9')){
			break;
		}
		if(i==word.length()-1){
			l1.push_back(tok((string)"NUM:", word));
			return;
		}
	}
	l1.push_back(tok((string)"WORD:", word));
}
void parse(string* code){
	string ss = *code;
	stringstream out;
	char ch[1];
	string word;
	int state = 0;
	int line=1;
	for(int i=0;i<ss.length();i++){
		if(ss.substr(i,2)=="/\\"){ //C O M M E N T
			i+=2;
			int vlog=1,startline=line;
			while(vlog!=0){
				if(ss[i]=='\n'){
					line++;
				}
				if(ss.substr(i,2)=="/\\"){
					vlog++;
				}else if(ss.substr(i,2)=="\\/"){
					vlog--;
				}
				i++;
				if(i==ss.length()){
					cout << "\nerror: Comment not closing in line " 
							 << startline << endl;
					exit(1);
				}
			}
			i++;
		}if(ss.substr(i,2)=="\\/"){ //C O M M E N T
			cout << "\nerror: Comment not open in line " 
					 << line << endl;
			exit(1);
		}else if(int(string("\n;").find(ss[i])) >=0){// N E W   L I N E
			if(word!=""){
				process_word(word,&out);
				word="";
			}
			if(ss[i]=='\n'){
				line++;
			}
			l1.push_back(tok((string)"NLN:", ""));
		}else if(ss[i]=='\''){ // S T R I N G   O R   A P O S T R O F
			if(word!=""){
				process_word(word,&out);
				word="";
			}
			int starti = i;
			i++;
			while(ss[i]!='\'' || ss[i-1]=='\\'){
				if(ss[i]=='\n'){
					i=starti;
					break;
				}
				word+=ss[i];
				i++;
			}
			if(i!=starti)
				l1.push_back(tok((string)"STRING:", word));
			else l1.push_back(tok((string)"APOSTROF:", ""));
			word="";
		}else if(ss[i]=='\"'){//S T R I N G   O R   E R R O R
			if(word!=""){
				process_word(word,&out);
				word="";
			}
			i++;
			while(ss[i]!='"' || ss[i-1]=='\\'){
				if(ss[i]=='\n'){
					cout << "\nerror: string not closing in line "
							 << line
							 << "\n";
					exit(1);
					break;
				}
				word+=ss[i];
				i++;
			}
			l1.push_back(tok((string)"STRING:", word));
			word="";
		}else if(ss[i]==' ' || ss[i]=='\t'){ //S P A C E
			if(word!=""){
				process_word(word,&out);
				word="";
			}
		}else if(in(".,+-/*<>=!^&()[]|{}")){
			if(word!=""){
				process_word(word,&out);
				word="";
			}
			string outs="";
			if(ss[i]=='.')outs="DOT:";
			if(ss[i]==',')outs="COMMA:";
			if(ss[i]=='(')outs="OPEN_PRIORITY:";
			if(ss[i]==')')outs="CLOSE_PRIORITY:";
			if(ss[i]=='{')outs="OPEN_CODEBLOCK:";
			if(ss[i]=='}')outs="CLOSE_CODEBLOCK:";
			if(ss.substr(i,2)=="[+"){
				i+=2;
				int vlog=1;
				while(true){
					if(ss[i]=='\n'){
						line++;
					}
					if(ss.substr(i,1)=="["){
						vlog++;
					}else if(ss.substr(i,1)=="]"){
						vlog--;
						if(vlog==0)break;
					}
					word+=ss[i];
					i++;
				}
				l1.push_back(tok((string)"MACROS:", word));
				word="";
				l1.push_back(tok((string)"NLN:", word));
			}else if(ss[i]=='[')outs="OPEN_LIST:";
			else if(ss[i]==']')outs="CLOSE_LIST:";
			if(in("+-/*"))outs="MATH:"+ss.substr(i,1);
			if(in("&^|!<>="))outs="LOGIC:"+ss.substr(i,1);
			if(outs!="")
			l1.push_back(tok(outs.substr(0,outs.find(':')), outs.substr(outs.find(':'))));
		}else{
			word+=ss[i];
		}
	}
	cout << out.str() << endl;
	for(int i=0;i<l1.size();i++){
		cout << l1[i].type << " ";
	}
}

