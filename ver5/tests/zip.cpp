#include <iostream>
#include <fstream>
#include <memory>
#include <zlib.h>

using namespace std;
//a b -> c
//f(c) -> a b
//c1 c2 ->
int main(){
    ifstream input("test.bin");
    ofstream output("test_zip.bin");

    char n[1];
    string file="";
    while (!input.eof())
    {
        input.read(n,1);
        file+=n[0];
    }

    // cout << sum<<endl;

    // if(1){
    //     uLongf compresSize1= compresSize*10;
    //     void* zipBuff1 = malloc(compresSize1);
    //     uncompress((Bytef*)zipBuff1,&compresSize1,(const Bytef*)zipBuff,compresSize);
    //     output.write((char*)zipBuff1,compresSize1);
    // }
    uLongf osize;
    void* out=malloc(file.size());
    compress((Bytef*)out,&osize,(Bytef*)file.c_str(),file.size());
    output.write((char*)out,osize);
    
    return 0;
}