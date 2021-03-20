// valgrind --tool=callgrind --dump-instr=yes --simulate-cache=yes
// --collect-jumps=yes
#include <malloc.h>
#include <memory.h>
#include <stdio.h>
#include <stdlib.h>

#define heapSize (1024 * 1024 * 16)
#define stackSize (1024 * 1024 * 16)

#define ID_APP 1
#define ID_DATA 2
#define ID_S 3
#define ID_K 4
#define ID_I 5
#define ID_B 6
#define ID_C 7

#define FLAG_UNSCAN 1
#define FLAG_SCAN 2
#define FLAG_USED 3

struct node {
  char ID;
  char size;
  char flag;
  struct node *data;
};
struct nodeRec {
  struct node *data;
  struct node *root;
};

struct nodeRec *Stack, *sp;
void **heap1, **heap2;
void **hp1, **hp2;

#define data(node, i) *((&node->data) + i)
#define checkFroAlloc(i)                                                       \
  if (hp1 + i >= (void *)heap1 + heapSize)                                     \
    GC();
#define alloc(n)                                                               \
  hp1;                                                                         \
  ((struct node *)hp1)->size = n;                                              \
  ((struct node *)hp1)->flag = FLAG_UNSCAN;                                    \
  hp1 += 1 + n;

#define pushNode(node)                                                         \
  sp += 1;                                                                     \
  ((struct nodeRec *)sp)->data = node;                                         \
  ((struct nodeRec *)sp)->root = NULL;

struct node *nodeForApp;
#define buildApp(n)                                                            \
  nodeForApp = alloc(n);                                                       \
  nodeForApp->ID = ID_APP;                                                     \
  for (char i = n - 1; i >= 0; i--) {                                          \
    data(nodeForApp, i) = *((void **)sp);                                      \
    sp -= 1;                                                                   \
  }                                                                            \
  pushNode(nodeForApp);

struct node *S, *K, *I, *B, *C;
struct node *recGC(struct node *a) {
  if (a->flag != FLAG_UNSCAN) {
    return data(a, 0);
  }
  memcpy(hp2, a, sizeof(void *) * (1 + a->size));
  a->flag = FLAG_SCAN;
  data(a, 0) = hp2;
  a = hp2;
  hp2 += 1 + a->size;
  if (a->ID == ID_APP)
    for (size_t i = 0; i < a->size; i++) {
      data(a, i) = recGC(data(a, i));
    }
  return a;
}
long long ccc = 0;
void GC() {
  printf("GC %d\n", ccc++);
  for (struct nodeRec *i = Stack; i <= sp; i++) {
    if (i->root != NULL)
      i->root = recGC(i->root);

    i->data = recGC(i->data);
  }

  void *tmp = heap1;
  heap1 = heap2;
  heap2 = tmp;

  hp1 = hp2;
  hp2 = heap2;
}
void eval() {
  if (sp->data->ID != ID_APP) {
    return;
  }
  long long H = 1;
  struct node *a;
  while (1) {
    while (sp->data->ID == ID_APP) {
      a = sp->data;
      sp->root = a;
      for (char i = 0; i < a->size; i++) {
        sp->data = data(a, i);
        if (i != 0) {
          sp->root = NULL;
        }
        sp += 1;
        H += 1;
      }
      H -= 1;
      sp -= 1;
    }
    // printf("H:%d\n",H);
    char di = 0;

    switch (sp->data->ID) {
    case ID_DATA:
      goto def;
      break;
    case ID_I:
      if (H > 1) {
        di = 1;
        // printf("i\n");
        H -= 1;
        sp -= 1;
      } else {
        goto def;
      }
      break;
    case ID_K:
      if (H > 2) {
        di = 1;
        // printf("k\n");
        H -= 2;
        *(sp - 2) = *(sp - 1);
        sp -= 2;
      } else {
        goto def;
      }
      break;
    case ID_S:
      if (H > 3) {
        di = 3;
        // printf("s \n");
        H -= 1;
        sp -= 1;
        pushNode((sp - 2 - 1)->data);
        pushNode((sp - 2 - 1)->data);
        checkFroAlloc(2 + 1+2+1);
        buildApp(2);
        sp -= 1;
        (sp - 1)->data = (sp - 2)->data;
        (sp - 2)->data = (sp + 1)->data;
      } else {
        goto def;
      }
      break;
    case ID_B:
      if (H > 3) {
        // printf("b \n");
        di = 2;
        H -= 1;
        sp -= 1;
        (sp + 1)->data = (sp - 1)->data;
        (sp - 1)->data = (sp - 2)->data;
        (sp - 2)->data = (sp + 1)->data;
      } else {
        goto def;
      }
      break;
    case ID_C:
      if (H > 3) {
        // printf("c \n");
        di = 2;
        H -= 2;
        sp -= 1;
        pushNode((sp - 2 - 1)->data);
        pushNode((sp - 2 - 1)->data);
        checkFroAlloc(2 + 1+2+1);
        buildApp(2);
        sp -= 2;
        (sp)->data = (sp + 1)->data;
        (sp - 1)->data = (sp + 2)->data;
      } else {
        goto def;
      }
      break;
    default:
      goto def;
      break;
    }
    a = (sp-di+1)->root;
    if (a != NULL) {
      // if(a->ID!=ID_APP)
      // printf("%d\n",a->size);
      if(di == 1){
        a->size = 1;
        data(a, 0) = sp->data;
      }else{
        // checkFroAlloc(di + 1);
        buildApp(di);
        a->size = 1;
        data(a, 0) = sp->data;
        // sp->data = a;
      }
      // sp-=1;
    }
    // printf("H:%d\n",H);
    // printf("%d\n",hp1-heap1);
  }
def:
  sp -= H - 1;
  a = sp->root;
  if (a != NULL) {
    buildApp(H);
    a->size = 1;
    data(a, 0) = sp->data;
    sp->data = a;
  } else if (H > 1)
    buildApp(H);
}
void test() {
  pushNode(K);
  pushNode(I);
  pushNode(B);
  buildApp(2);
  pushNode(K);
  pushNode(C);
  buildApp(4);
  pushNode(I);
  pushNode(B);
  buildApp(2);
  pushNode(K);
  pushNode(C);
  buildApp(4);
  pushNode(I);
  pushNode(B);
  buildApp(2);
  pushNode(K);
  pushNode(C);
  buildApp(4);
  pushNode(I);
  pushNode(B);
  buildApp(2);
  pushNode(K);
  pushNode(C);
  buildApp(4);
  pushNode(I);
  pushNode(B);
  buildApp(2);
  pushNode(K);
  pushNode(C);
  buildApp(4);
  pushNode(I);
  pushNode(B);
  buildApp(2);
  pushNode(K);
  pushNode(C);
  buildApp(4);
  pushNode(I);
  pushNode(B);
  buildApp(2);
  pushNode(K);
  pushNode(C);
  buildApp(4);
  pushNode(I);
  pushNode(B);
  buildApp(2);
  pushNode(K);
  pushNode(C);
  buildApp(4);
  pushNode(I);
  pushNode(B);
  buildApp(2);
  pushNode(K);
  pushNode(C);
  buildApp(4);
  pushNode(I);
  pushNode(B);
  buildApp(2);
  pushNode(K);
  pushNode(C);
  buildApp(4);
  pushNode(B);
  pushNode(I);
  pushNode(B);
  buildApp(2);
  pushNode(K);
  pushNode(C);
  buildApp(3);
  pushNode(B);
  pushNode(C);
  pushNode(C);
  buildApp(3);
  pushNode(B);
  buildApp(3);
  pushNode(K);
  pushNode(C);
  buildApp(2);
  pushNode(C);
  buildApp(2);
  pushNode(C);
  buildApp(3);
  pushNode(I);
  pushNode(B);
  buildApp(2);
  pushNode(C);
  pushNode(C);
  buildApp(2);
  pushNode(C);
  buildApp(3);
  pushNode(S);
  pushNode(C);
  buildApp(3);
  pushNode(B);
  buildApp(2);
  pushNode(C);
  buildApp(3);
  pushNode(S);
  pushNode(S);
  buildApp(2);
  pushNode(C);
  buildApp(3);
  pushNode(I);
  pushNode(I);
  pushNode(S);
  buildApp(3);
  pushNode(C);
  pushNode(B);
  buildApp(3);
  pushNode(I);
  pushNode(I);
  pushNode(S);
  buildApp(3);
  pushNode(C);
  buildApp(4);
  pushNode(C);
  pushNode(C);
  buildApp(3);
  pushNode(S);
  buildApp(2);
  pushNode(C);
  buildApp(3);
  pushNode(S);
  pushNode(B);
  buildApp(2);
  pushNode(C);
  buildApp(3);
  pushNode(I);
  pushNode(I);
  pushNode(S);
  buildApp(3);
  pushNode(C);
  pushNode(B);
  buildApp(3);
  pushNode(I);
  pushNode(I);
  pushNode(S);
  buildApp(3);
  pushNode(C);
  buildApp(4);
  pushNode(B);
  buildApp(2);
  pushNode(K);
  pushNode(C);
  buildApp(2);
  pushNode(C);
  buildApp(3);
  pushNode(K);
  pushNode(I);
  pushNode(B);
  buildApp(3);
  pushNode(C);
  pushNode(C);
  buildApp(3);
  pushNode(S);
  buildApp(3);
  pushNode(K);
  pushNode(I);
  pushNode(B);
  buildApp(3);
  pushNode(C);
  pushNode(C);
  buildApp(3);
  pushNode(B);
  buildApp(3);
  pushNode(C);
  pushNode(C);
  buildApp(3);
  pushNode(B);
  buildApp(2);
  pushNode(K);
  pushNode(I);
  pushNode(B);
  buildApp(2);
  pushNode(K);
  pushNode(C);
  buildApp(4);
  pushNode(I);
  pushNode(B);
  buildApp(3);
  pushNode(S);
  buildApp(2);
  pushNode(C);
  buildApp(3);
  pushNode(I);
  pushNode(I);
  pushNode(S);
  buildApp(3);
  pushNode(C);
  pushNode(B);
  buildApp(3);
  pushNode(I);
  pushNode(I);
  pushNode(S);
  buildApp(3);
  pushNode(C);
  buildApp(5);
}
int main() {
  Stack = malloc(stackSize);
  heap1 = malloc(heapSize);
  heap2 = malloc(heapSize);
  sp = Stack - 1;
  hp1 = heap1;
  hp2 = heap2;

  S = alloc(1);
  K = alloc(1);
  I = alloc(1);
  B = alloc(1);
  C = alloc(1);
  S->ID = ID_S;
  K->ID = ID_K;
  I->ID = ID_I;
  B->ID = ID_B;
  C->ID = ID_C;
  pushNode(S);
  pushNode(K);
  pushNode(I);
  pushNode(B);
  pushNode(C);

  // checkFroAlloc(3 + 4 + 2);

  test();
  // pushNode(I);
  // pushNode(I);
  // pushNode(S);
  // buildApp(3);
  // pushNode(I);
  // pushNode(I);
  // pushNode(S);
  // buildApp(4);
  eval();
  printf("%d\n", hp1 - heap1);
  GC();
  printf("%d\n", hp1 - heap1);

  // for (long long k = 0; k < 1000000; k++) {
  //   checkFroAlloc(1000 * 2);
  //   for (int i = 0; i < 1000; i++) {
  //     struct node *a = alloc(1);
  //     a->ID = ID_DATA;
  //     data(a, 0) = i;
  //   }
  // }
  printf("END\n");
  return 0;
}
