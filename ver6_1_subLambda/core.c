// valgrind --tool=callgrind --dump-instr=yes --simulate-cache=yes
// --collect-jumps=yes
#include <malloc.h>
#include <memory.h>
#include <stdio.h>
#include <stdlib.h>

#define stackSize 1024 * 1024 * 128  // in bytes
#define oneGenSize 1024 * 1024 * 128 // in bytes

#define ID_THUNK 1
#define ID_DATA 2
#define ID_INDIRECT 3
#define ID_FUNCTION 4

#define OP_STOP 0
#define OP_EVAL 1
#define OP_RETURN 2

struct ConsPull {
  struct ConsPull *next;
  int size;
  int pullSize;
  int nodeType;
  void **data;
};

struct ConsPull *pulls[256];
#define startPull 0
#define maxPull (startPull + sizeof(pulls) / sizeof(pulls[0]) - 1)

struct Gen {
  char *nowP;
  char *start;
  char *end;
  struct Gen *next;
};
void **stack;
struct Gen mempull;
void **PC;
void **startPos;
void **localEnd;
void **LC;

void *alloc(int size);
void dealloc(void *p);
void GC();
struct ConsPull* copy(struct ConsPull *p);
struct ConsPull* newThunk(struct ConsPull** list,int size);
struct ConsPull* newInt(long long a);
struct ConsPull* newFunction(void* a);

#define checks(argNum, postSize)                                               \
  if (PC - argNum <= localEnd) {                                               \
    LC = PC;                                                                   \
    PC = localEnd;                                                             \
  } else if ((char *)(PC + postSize - argNum - 1) >=                           \
             (char *)stack + stackSize) {                                      \
    printf("ERROR:stack memory out\n");                                        \
    exit(-1);                                                                  \
  } else

void f_6576616c() { // eval
  checks(2, 2) {
    dealloc(*PC);
    *PC = OP_EVAL;
  }
}
void f_616464496e74() { // addInt
  checks(2, 1) {
    struct ConsPull *p1 = *(PC - 1);
    struct ConsPull *p2 = *(PC - 2);
    p2->data = (long long)p1->data + (long long)p2->data;
    dealloc(p1);
    dealloc(*PC);
    PC -= 2;
  }
}
void f_737562496e74() { // subInt
  checks(2, 1) {
    struct ConsPull *p1 = *(PC - 1);
    struct ConsPull *p2 = *(PC - 2);
    long long a = (long long)p1->data - (long long)p2->data;
    p2->data = (a < 0) ? 0 : a;
    dealloc(p1);
    dealloc(*PC);
    PC -= 2;
  }
}
void f_69735a65726f() { // isZero
  checks(3, 1) {
    struct ConsPull *p1 = *(PC - 1);
    long long a = (long long)p1->data;
    *(PC - 3) = (a == 0) ? *(PC - 2) : *(PC - 3);
    dealloc((a != 0) ? *(PC - 2) : *(PC - 3));
    dealloc(*PC);
    dealloc(*(PC - 1));
    PC -= 3;
  }
}
void f_7072696e74496e74() { // printInt
  checks(1, 1) {
    // printf("printInt\n");
    struct ConsPull *p1 = *(PC - 1);
    long long a = (long long)p1->data;
    printf("%llu\n", a);
    dealloc(*PC);
    // dealloc(*(PC-1));
    PC -= 1;
  }
}

void Double() {
  checks(1, 2) {
    // printf("Double\n");
    dealloc(*PC);
    *PC = copy(*(PC - 1));
    // PC-=1;
  }
}
void Y() {
  checks(1, 2) {
    // printf("Y ");
    // dealloc(*PC);
    struct ConsPull *c1 = alloc(2);
    c1->nodeType = ID_THUNK;
    void **d1 = c1->data;

    d1[1] = *PC;
    d1[0] = copy(*(PC - 1));

    *PC = *(PC - 1);
    *(PC - 1) = c1;
  }
}
void I() {
  checks(1, 1) {
    // printf("I ");
    dealloc(*PC);
    PC -= 1;
  }
}
#include "test_LC.c"

int main() {
  for (int i = 0; i < sizeof(pulls) / sizeof(pulls[0]); i++) {
    pulls[i] = NULL;
  }
  printf("START: startPull:%d; maxpull:%d\n", startPull, maxPull);

  mempull.nowP = malloc(oneGenSize);
  mempull.start = mempull.nowP;
  mempull.end = mempull.start + oneGenSize;

  stack = (void **)malloc(stackSize);
  PC = stack;
  localEnd = PC;

  // init code
  *(PC++) = 0;
  struct ConsPull *p1 = alloc(0);
  p1->nodeType = ID_FUNCTION;
  p1->data = f_6d61696e;
  *(PC) = p1;

  // loop
  while (1) {
    // for (void **i = stack; i <= PC; i++) {
    //   printf("%llu ", *i);
    // }
    // printf("\n");

    if (*PC <= OP_RETURN) {
      if (*PC == OP_STOP) {
        printf("END\n");
        break;
      } else if (*PC == OP_EVAL) {
        checks(2, 2) {
          // printf("EVAL ");
          *(PC + 1) = *(PC - 1);
          *(PC - 1) = localEnd;
          *(PC) = OP_RETURN;
          localEnd = PC;
          PC += 1;
        }
      } else if (*PC == OP_RETURN) {
        int size = (unsigned long long)(LC - localEnd);
        // printf("RETURN(%d)\n",size);
        // break;
        if (size == 1) {
          PC--;
          localEnd = *(PC);
          *(PC) = *(PC - 1);
          *(PC - 1) = *(PC + 2);
        } else {
          struct ConsPull *p1 = alloc(size);
          p1->nodeType = ID_THUNK;
          memcpy(p1->data, PC+1, size * sizeof(void **));
          PC--;
          localEnd = *(PC);
          *(PC) = *(PC - 1);
          *(PC - 1) = p1;
        }
      }
    } else {
      struct ConsPull *p1 = *PC;
      switch (p1->nodeType) {
      case ID_FUNCTION:
        ((void (*)())(p1->data))();
        break;
      case ID_THUNK:
        // printf("THUNK(%d)\n",p1->pullSize);
        memcpy(PC, p1->data, p1->pullSize * sizeof(void **));
        PC += p1->pullSize - 1;
        p1->nodeType = ID_DATA;
        dealloc(p1);
        break;
      case ID_DATA:
        LC = PC;
        PC = localEnd;
        // printf("DATA(%d)\n",LC-localEnd);
        break;
      default:
        printf("ERROR:invalod nodeType(%d)\n", p1->nodeType);
        *PC = 0;
        break;
      }
    }
  }

  return 0;
}
struct ConsPull* newThunk(struct ConsPull** list,int size){
    struct ConsPull* out = alloc(size);
    out->nodeType = ID_THUNK;
    for(int i =0;i<size;i++){
        out->data[i] = list[i];
    }
    return out;
}

struct ConsPull* newInt(long long a){
    struct ConsPull* out = alloc(0);
    out->nodeType = ID_DATA;
    out->data = a;
    return out;
}
struct ConsPull* newFunction(void* a){
    struct ConsPull* out = alloc(0);
    out->nodeType = ID_FUNCTION;
    out->data = a;
    return out;
}
void *alloc(int size) {
  void *out;
  size -= startPull;

  if (pulls[size] != NULL) {
    out = (void *)pulls[size];
    pulls[size] = pulls[size]->next;
  } else {
    int allAlloc =
        sizeof(struct ConsPull) + sizeof(void **) * (size + startPull);
    if (mempull.nowP + allAlloc >= mempull.end) {
      printf("ERROR:memory out\n");
      exit(-1);
    }
    out = (void *)mempull.nowP;
    mempull.nowP = mempull.nowP + allAlloc;
    ((struct ConsPull *)out)->size = allAlloc;
    ((struct ConsPull *)out)->pullSize = size + startPull;
    ((struct ConsPull *)out)->next = NULL;
    ((struct ConsPull *)out)->data =
        (void **)((char *)out + sizeof(struct ConsPull));
  }

  // printf("ALLOC(%d,%llu)\n",size+startPull,out);
  return out;
}
void dealloc(void *p) {
  struct ConsPull *c = p;
  int size = c->pullSize;
  c->next = pulls[size];
  pulls[size] = c;
  if (c->nodeType == ID_THUNK) {
    for (void **i = c->data; (char *)i < (char *)c + c->size; i++) {
      dealloc(*i);
    }
  }
}
struct ConsPull *copy(struct ConsPull *p) {
  struct ConsPull *new = alloc(p->pullSize);
  new->nodeType = p->nodeType;
  // printf("NTCOPY(%d)\n",new->nodeType);
  if (p->nodeType == ID_THUNK) {
    void **i1 = new->data;
    void **i = p->data;
    while (i < p->data + p->pullSize) {
      *(i1++) = copy(*(i++));
    }
  } else {
    new->data = p->data;
  }
  return new;
}