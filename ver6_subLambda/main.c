#include <stdio.h>
#include <memory.h>
#include <stdlib.h>


typedef unsigned short WT;
#define bytes sizeof(WT)
#define bits bytes*8


#define stackSize (1<<bits)
#define heapSize (1<<bits)
#define displaySize (1<<bits-1)
#define funcListSize (1<<bits-1)


#define isApp(n) (n&(1<<bits-1))
#define addrFromApp(n) (n&((1<<bits-1)-1))
#define addrToApp(n) (n|((1<<bits-1)))


#define haltOpCode 0
#define calcOpCode 1


#define USED_FLAG 2
#define SCAN_FLAG 1
#define UNSCAN_FLAG 0


void alloc();
void GC();


void Double();
void I();
void S();


void* funcList[funcListSize]={0,0,I,Double,S};
WT display[displaySize]={0,USED_FLAG};
WT stack[stackSize]={0,0,0x8000,2,2,4};
WT heap[heapSize]={5,0,2,2,4};


WT PC=5,HP=5,DP=2,CL,A,B,C,D,SR=0;

int main(){
    A=DP;
    while (A<displaySize)
    {
        display[A+1]=UNSCAN_FLAG;
        A+=2;
    }
    

    SR|=1;
    while (SR&1)
    {
        switch (stack[PC])
        {
        case haltOpCode:
            if(stack[PC-1]==haltOpCode){
                SR&=~1;
            }else{
                //alloc,copy,run
                printf("calcRet: with %d to %d,%d\n",CL,stack[PC-1],PC);
                PC = stack[PC-1];
                SR&=~1;
            }
            break;
        
        case calcOpCode:
            SR&=~1;
            break;

        default:
            if(isApp(stack[PC])){
                A = display[addrFromApp(stack[PC])];
                B = heap[A]-2;
                A+=2;

                C = A;
                A=B-1;
                safelyAdd();
                A = C;

                while (B!=0)
                {
                    stack[PC] = heap[A];
                    PC++;A++;B--;
                }
                PC--;
                
                // printf("APP %d\n",PC);
                // SR&=~1;
            }else{
                ((void(*)()) funcList[stack[PC]])();
            }
            break;
        }
    }
    printf("end\n");
    return 0;
}
void checkN(){
    B = PC;
    while (A!=0)
    {
        if(stack[B]==haltOpCode)return;
        A--;B--;
    }
}
void safelyAdd(){
    if(PC+A>=stackSize || PC+A<PC){
        perror("memory out fo stack\n");
        printf("memory out fo stack\n");
        exit(1);
    }
}
void I(){
    A = 1;
    PC--;
    checkN();
    if(A){
        CL = A;
    }else{
        // printf("I ");
    }
}

void Double(){
    A = 1;
    PC--;
    checkN();
    if(A){
        CL=A;
    }else
    {
        A=2;
        safelyAdd();
        printf("double ");
        stack[PC+1]=stack[PC];
        stack[PC+2]=stack[PC];
        PC+=2;
    }
    
}
void S(){
    A = 3;
    PC--;
    checkN();
    if(A){
        CL=A;
    }else
    {
        // printf("S ");
        A=2;
        alloc();
        heap[B+1] = stack[PC-1];
        heap[B] = stack[PC-2];

        stack[PC-1]=stack[PC-2];
        stack[PC-2] = addrToApp(C);
        // stack[PC]=stack[PC];
    }
    
}
void alloc(){
    if(HP+A+2<HP || HP+A+2 >= heapSize){
        GC();
    }
    while (display[DP+1]!=UNSCAN_FLAG)
    {
        if(DP+2>=displaySize){
            printf("DPDP");
            GC();
            break;
        }
        DP+=2;
    }
    
    B = HP;
    C = DP;
    HP+=A+2;
    DP+=2;

    display[C] = B;
    display[C+1] = USED_FLAG;

    heap[B] = A+2;
    heap[B+1] = C;

    B+=2;
    // printf("alloc %d %d\n",B,C);
}
void GC(){
    printf("GC %d %d %d\n",PC,HP,DP);
    A = 0;
    while (A<displaySize)
    {
        display[A+1]=UNSCAN_FLAG;
        A+=2;
    }
    B = PC;
    while (B!=0)
    {
        if(isApp(stack[B])){
            display[addrFromApp(stack[B])+1]=SCAN_FLAG;
        }
        B--;
    }
    
    do{
        B = 0;
        A = 0;
        while(A<displaySize){
            if(display[A+1]==SCAN_FLAG){
                C = heap[display[A]];
                D = heap[C]-2;
                C+=2;
                while (D!=0)
                {
                    if(isApp(heap[C])){
                        display[addrFromApp(heap[C])+1]=SCAN_FLAG;
                    }
                    D--;
                    C++;
                }
                

                display[A+1] = USED_FLAG;
                B=1;
            }
            A+=2;
        }
    }while (B!=0);
    
    A = 0;
    B = 0;//last addr to copy object
    DP = 0;
    while (A<displaySize)
    {
        if(display[A+1]==USED_FLAG){
            if(display[A]==B){
                B+=heap[display[A]];
            }
            else{
                D = display[A];
                C = heap[D];
                display[A] = B;
                while (C!=0)
                {
                    heap[B++]=heap[D++];
                    C--;
                }
            }
        }else{
            if(DP==0){
                DP = A;
            }
        }
        A+=2;
    }
    HP = B;
    printf("%d %d\n",HP,DP); 
    while (HP!=0)
    {
        printf("%d ",heap[HP--]);
    }
    
    exit(0);
}
