#ifndef JIT_LDI
#define JIT_LDI

#include <iostream>
// #include <sys/mman.h>
// #include <cstring>
// #include "RunTime.cpp"

using namespace std;
//g++ -ffunction-sections -c ./src/Jit.cpp -o ./test.o
//objdump -d test.o
//objcopy -O binary -j .text.JIT test.o test.bin
void JIT(){
    // unsigned char code[]={0x48,0x89,0xf8};


    // void* f = mmap(0,sizeof(code),PROT_EXEC|PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS,-1,0);
    // memcpy(f,code,sizeof(code));

    // int (*func)(int,int) = (int(*)(int,int))f;
    // cout << func(1,2)<<endl;

    // munmap(f,sizeof(code));

    // int a=5,b=6;
    // return a+b;
    // Data d;
    // d.data="HEI!";
    // Stack.push_back(Data());
    // Stack.pop_back();
}

#endif