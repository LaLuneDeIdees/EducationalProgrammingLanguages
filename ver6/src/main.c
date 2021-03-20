#include <stdio.h>
#include <string.h>
#include "parser.c"
//
//
//
int main(char argc, char** arga){
    FILE* file;
    if(argc == 2){
        file = fopen(arga[1],"r");
        if(file != NULL){
            int token = -1;
            while (token!=0)
            {
                token = tokenParse(file);
                printf("%d ",token);
            }
        }else{
            printf("can't open file %s\n",arga[1]);
        }
    }
    return 0;
}