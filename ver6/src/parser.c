#include <stdio.h>
#include <string.h>
#include <memory.h>
#include <malloc.h>

#define NONE 0
#define ANY 2
#define TOKEN_NLN 1

#define BUFSIZE 4

char buffer[BUFSIZE*2];
int startToken = 0;
int endToken = BUFSIZE*2-1;

char nextChar(FILE* from){
    endToken++;
    if( endToken == BUFSIZE){
        int count = fread(&buffer[BUFSIZE],sizeof(char),BUFSIZE,from);
        if(count < BUFSIZE){
            memset(&buffer[BUFSIZE+count-1],EOF,BUFSIZE-count);
        }
    }else if( endToken == BUFSIZE*2){
        endToken = 0;
        int count = fread(buffer,sizeof(char),BUFSIZE,from);
        if(count < BUFSIZE){
            memset(&buffer[count-1],EOF,BUFSIZE-count);
        }
    }
    return buffer[endToken];
}
int tokenParse(FILE* from){
    int tok = NONE;
    char* str;
    while (1)
    {
        char next = nextChar(from);
        if(next == EOF){endToken--;break;}
        if(next == ' ' || next == '\t'){
            if((endToken-startToken)%(BUFSIZE*2)>1){
                // break;
            }else{
                startToken = endToken;
            }
        }else{

        }
    }
    if(endToken!=startToken){
        if(endToken>startToken){
            printf("%d %d\n",startToken,endToken);
            // str = malloc((endToken-startToken) * sizeof(char)+1);
            // memcpy(str,&buffer[startToken],(endToken-startToken) * sizeof(char));
        }else{
            printf("\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n");
        }
        printf("%s\n",str);
        tok = ANY;
        startToken=endToken;
    }
    return tok;
}