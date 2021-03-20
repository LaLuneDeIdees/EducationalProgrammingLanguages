#include <stdio.h>
#include <memory.h>
#include "rom.c"
// #define LOG2
#define LOG
#define ramsize (1<<(6+10))
#define alloc(a,n) if(SP+n+1>=PC)SP=SSP; a=SP;SP+=n+1;//printf("SP:%d: ",SP)

#define opC_I 0x8001
#define opC_K 0x8002
#define opC_S 0x8003
#define opC_C 0x8004 //a (b c)
#define opC_B 0x8005 //a c b  
#define opC_IO 0x8006
#define opC_CALC 0x8007
#define opC_CONT 0x8008
#define opC_HULT 0x8000

extern unsigned short pr[];

unsigned short PC,SP,SSP;
unsigned short mem[ramsize];

// void malloc(n){

// }

int main(){
	memset(mem,00,sizeof(mem));
	SP = 0;
	PC = 0;
	unsigned short a,b;
	char f = 1;

	b = pr[SP];
	while (1)
	{
		a = b;
		b = pr[SP+1];

		if(a==opC_HULT && b ==opC_HULT){
			if(f==1){
				PC = SP;
			}
			mem[SP]=pr[SP];SP++;
			mem[SP]=pr[SP];SP++;
			break;
		}
		if((a==opC_HULT) && f==1){
			PC = SP;
			f=0;
		}
		mem[SP]=pr[SP];
		SP++;
	}
	a = ramsize-1;
	while (1)
	{
		mem[a]=mem[PC];
		if(PC==0){
			break;
		}
		PC--;a--;
	}
	PC = a;

	SSP = SP;
	
	f = 1;

	unsigned long counter = 0;
	while (f)
	{
		#ifdef LOG1
			printf("%d %d %d\n",mem[PC],PC,SP);
		#endif
		#ifdef LOG2
			printf("%d\n",counter++);
		#endif
		switch(mem[PC]){
			case opC_HULT:
				f=0;
				break;
			case opC_I:
				if(mem[PC+1]==opC_HULT){f=0;break;}
				PC++;	
				#ifdef LOG
					printf("I ");
				#endif
				break;
			case opC_K:
				if(mem[PC+1]==opC_HULT){f=0;break;}
				if(mem[PC+2]==opC_HULT){f=0;break;}
				mem[PC+2]=mem[PC+1];
				PC+=2;	
				#ifdef LOG
					printf("K ");
				#endif
				break;
			case opC_S:
				if(mem[PC+1]==opC_HULT){f=0;break;}
				if(mem[PC+2]==opC_HULT){f=0;break;}
				if(mem[PC+3]==opC_HULT){f=0;break;}
				if(mem[PC+2]==opC_I){
					mem[PC+2]=mem[PC+3];
				}else
				{
					alloc(a,2);
					mem[a] = mem[PC+2];
					mem[a+1] = mem[PC+3];
					mem[a+2] = opC_HULT;
					
					mem[PC+2] = mem[PC+3];
					mem[PC+3]=a;
				}
				PC++;
				#ifdef LOG
					printf("S ");
				#endif
				break;
			case opC_C:
				if(mem[PC+1]==opC_HULT){f=0;break;}
				if(mem[PC+2]==opC_HULT){f=0;break;}
				if(mem[PC+3]==opC_HULT){f=0;break;}
				if(mem[PC+2]!=opC_I){
					alloc(a,2);
					mem[a]=mem[PC+2];
					mem[a+1]=mem[PC+3];
					mem[a+2]=opC_HULT;

					mem[PC+2] = mem[PC+1];
					mem[PC+3] = a;
				}else
				{
					mem[PC+2] = mem[PC+1];
				}
				PC+=2;
				#ifdef LOG
					printf("C ");
				#endif
				break;
			case opC_B:
				if(mem[PC+1]==opC_HULT){f=0;break;}
				if(mem[PC+2]==opC_HULT){f=0;break;}
				if(mem[PC+3]==opC_HULT){f=0;break;}
				a = mem[PC+3];
				mem[PC+3] = mem[PC+2];
				mem[PC+2] = a;
				PC++;	
				#ifdef LOG
					printf("B ");
				#endif
				break;
			default:
				a = mem[PC];
				b = mem[PC];
				while (mem[a]!=opC_HULT){a++;};
				a--;
				while (1)
				{
					mem[PC] = mem[a];
					if(a-b==0)break;
					a--;PC--;
				}
				
				#ifdef LOG1
					printf("copy from %d to %d\n",b,PC);
				#endif
			break;
		}
	}
	
	
	
	printf("\n\tend\n");
	return 0;
}