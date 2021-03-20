#ifndef SOURCE_TO_BYTE_CODE_LDI
#define SOURCE_TO_BYTE_CODE_LDI

#include <iostream>
#include <sstream>
#include "HashMap.cpp"
using namespace std;

#define CODE_END_SECTION                1   // +
#define CODE_EVAL                       12  // +
#define CODE_DECREMENT_LABEL            2   // +
#define CODE_REGISTER_LABEL             3   // +
#define CODE_REGISTER_DATA              4   // +
#define CODE_CLIB                       5   // +
#define CODE_LLIB                       6   // +
#define CODE_LCLR                       7   // +
#define CODE_MONAD                      8   // +
#define CODE_CALL_CLIB                  10  // +
#define CODE_DATA_FROM_LABEL_TO_STACK   11  // +

// #define CODE_ARGUMENTS_DECLARATE        13 //? -
// #define CODE_MEMORAZE                   14 //? -

struct ByteCode
{
    uint32_t size;
    string bytes;
};

HashMap<ByteCode> ByteCodesFromData;	   	//key is function data, data is string of bytecode

void writeAsByte(uint32_t data,stringstream* ss){
    ss->write((const char*)&data,4);
}
void processWord(string* word,stringstream* ss){
    if((*word).size()<=0)return;
    if((*word).find('.')!=-1){
        *ss<<(char)CODE_CALL_CLIB;

        *ss<<word->substr(0,(*word).find('.'));
        *ss<<(char)CODE_END_SECTION;

        writeAsByte(hashC(word->substr(0,(*word).find('.'))),ss);
        *ss<<(char)CODE_END_SECTION;

        *ss<<word->substr((*word).find('.')+1);
        *ss<<(char)CODE_END_SECTION;
        
        writeAsByte(hashC(word->substr((*word).find('.')+1)),ss);
        *ss<<(char)CODE_END_SECTION;

    }else if(*word =="clib"){
        *ss<<(char)CODE_CLIB;
    }else if(*word =="llib"){
        *ss<<(char)CODE_LLIB;
    }else if(*word =="lclr"){
        *ss<<(char)CODE_LCLR;
    }else if(*word =="monad"){
        *ss<<(char)CODE_MONAD;
    // }else if(*word =="args"){
    //     *ss<<(char)CODE_ARGUMENTS_DECLARATE;
    }else{
        *ss<<(char)CODE_DATA_FROM_LABEL_TO_STACK;
        *ss<<*word;
        *ss<<(char)CODE_END_SECTION;

        writeAsByte(hashC(*word),ss);
        *ss<<(char)CODE_END_SECTION;
    }
    *word="";
}
ByteCode SourceToByteCode(string code,uint32_t hashCode){
    ByteCode already = ByteCodesFromData.getLast(code,hashCode);
    if(!ByteCodesFromData.fail){
        return already;
    }

    ByteCode out;
    stringstream ss;

    string buffer = "";
    for(int i =0;i<code.size();i++){
        if(string("\n\t\r '\"{}:#").find(code[i])!=-1){
            if(code[i]==':'){
                ss << (char)CODE_REGISTER_LABEL;
                ss<<buffer;
                ss<<(char)CODE_END_SECTION;

                writeAsByte(hashC(buffer),&ss);
                ss<<(char)CODE_END_SECTION;

            }else if(code[i]=='\''){
                processWord(&buffer,&ss);
                ss << (char)CODE_EVAL;
            }else if(code[i]=='"'){
                processWord(&buffer,&ss);
                ss << (char)CODE_DECREMENT_LABEL;
            }else if(code[i]=='#'){
                while(code[i]!='\n')i++;
            }else if(code[i]=='{'){
                processWord(&buffer,&ss);

                int level = 1;

                while(level!=0){
                    i++;
                    if(code[i]=='{')level++;
                    if(code[i]=='}')level--;
                    buffer+=code[i];
                }

                buffer.erase(buffer.end()-1);


                ss<<(char)CODE_REGISTER_DATA;
                ss<<buffer;
                ss<<(char)CODE_END_SECTION;

                writeAsByte(hashC(buffer),&ss);
                ss<<(char)CODE_END_SECTION;
            }else{
                processWord(&buffer,&ss);
            }
            buffer="";
        }else
        {
            buffer+=code[i];
        }
    }processWord(&buffer,&ss);

    string dataout = ss.str();
    out.size = dataout.size();
    out.bytes = dataout;

    ByteCodesFromData.put(code,out,hashCode);
    return out;
}

ByteCode SourceToByteCode(string code){
    return SourceToByteCode(code,hashC(code));
}

#endif