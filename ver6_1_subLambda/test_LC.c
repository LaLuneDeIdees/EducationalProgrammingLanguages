void f_616464();
void f_2b();
void f_737562();
void f_2d();
void f_69735a();
void f_59();
void f_6d61696e();




void f_tmp_3(){
struct ConsPull* res;
checks(2,1){
if(1){
struct ConsPull* p1 = alloc(3);
p1->nodeType = ID_THUNK;
void** DPtr = p1->data;
res = newFunction(f_616464496e74);
*(DPtr+2) = res;
res = copy(*(PC-1));
*(DPtr+1) = res;
res = copy(*(PC-2));
*(DPtr+0) = res;
res = p1;
}
dealloc(*(PC-0));
dealloc(*(PC-1));
dealloc(*(PC-2));
PC-=2;
*PC=res;
}
}

void f_tmp_2(){
struct ConsPull* res;
checks(2,1){
if(1){
struct ConsPull* p1 = alloc(3);
p1->nodeType = ID_THUNK;
void** DPtr = p1->data;
res = newFunction(f_6576616c);
*(DPtr+2) = res;
res = copy(*(PC-1));
*(DPtr+1) = res;
if(1){
struct ConsPull* p1 = alloc(2);
p1->nodeType = ID_THUNK;
void** DPtr = p1->data;
res = alloc(0);
res->nodeType = ID_FUNCTION;
res->data = f_tmp_3;
*(DPtr+1) = res;
res = copy(*(PC-2));
*(DPtr+0) = res;
res = p1;
}
*(DPtr+0) = res;
res = p1;
}
dealloc(*(PC-0));
dealloc(*(PC-1));
dealloc(*(PC-2));
PC-=2;
*PC=res;
}
}

void f_tmp_1(){
struct ConsPull* res;
checks(2,1){
if(1){
struct ConsPull* p1 = alloc(3);
p1->nodeType = ID_THUNK;
void** DPtr = p1->data;
res = newFunction(f_6576616c);
*(DPtr+2) = res;
res = copy(*(PC-1));
*(DPtr+1) = res;
if(1){
struct ConsPull* p1 = alloc(2);
p1->nodeType = ID_THUNK;
void** DPtr = p1->data;
res = alloc(0);
res->nodeType = ID_FUNCTION;
res->data = f_tmp_2;
*(DPtr+1) = res;
res = copy(*(PC-2));
*(DPtr+0) = res;
res = p1;
}
*(DPtr+0) = res;
res = p1;
}
dealloc(*(PC-0));
dealloc(*(PC-1));
dealloc(*(PC-2));
PC-=2;
*PC=res;
}
}

void f_616464(){
struct ConsPull* res;
res = alloc(0);
res->nodeType = ID_FUNCTION;
res->data = f_tmp_1;

dealloc(*PC);*PC = res;
}

void f_2b(){
struct ConsPull* res;
res = newFunction(f_616464);

dealloc(*PC);*PC = res;
}

void f_tmp_6(){
struct ConsPull* res;
checks(2,1){
if(1){
struct ConsPull* p1 = alloc(3);
p1->nodeType = ID_THUNK;
void** DPtr = p1->data;
res = newFunction(f_737562496e74);
*(DPtr+2) = res;
res = copy(*(PC-1));
*(DPtr+1) = res;
res = copy(*(PC-2));
*(DPtr+0) = res;
res = p1;
}
dealloc(*(PC-0));
dealloc(*(PC-1));
dealloc(*(PC-2));
PC-=2;
*PC=res;
}
}

void f_tmp_5(){
struct ConsPull* res;
checks(2,1){
if(1){
struct ConsPull* p1 = alloc(3);
p1->nodeType = ID_THUNK;
void** DPtr = p1->data;
res = newFunction(f_6576616c);
*(DPtr+2) = res;
res = copy(*(PC-1));
*(DPtr+1) = res;
if(1){
struct ConsPull* p1 = alloc(2);
p1->nodeType = ID_THUNK;
void** DPtr = p1->data;
res = alloc(0);
res->nodeType = ID_FUNCTION;
res->data = f_tmp_6;
*(DPtr+1) = res;
res = copy(*(PC-2));
*(DPtr+0) = res;
res = p1;
}
*(DPtr+0) = res;
res = p1;
}
dealloc(*(PC-0));
dealloc(*(PC-1));
dealloc(*(PC-2));
PC-=2;
*PC=res;
}
}

void f_tmp_4(){
struct ConsPull* res;
checks(2,1){
if(1){
struct ConsPull* p1 = alloc(3);
p1->nodeType = ID_THUNK;
void** DPtr = p1->data;
res = newFunction(f_6576616c);
*(DPtr+2) = res;
res = copy(*(PC-1));
*(DPtr+1) = res;
if(1){
struct ConsPull* p1 = alloc(2);
p1->nodeType = ID_THUNK;
void** DPtr = p1->data;
res = alloc(0);
res->nodeType = ID_FUNCTION;
res->data = f_tmp_5;
*(DPtr+1) = res;
res = copy(*(PC-2));
*(DPtr+0) = res;
res = p1;
}
*(DPtr+0) = res;
res = p1;
}
dealloc(*(PC-0));
dealloc(*(PC-1));
dealloc(*(PC-2));
PC-=2;
*PC=res;
}
}

void f_737562(){
struct ConsPull* res;
res = alloc(0);
res->nodeType = ID_FUNCTION;
res->data = f_tmp_4;

dealloc(*PC);*PC = res;
}

void f_2d(){
struct ConsPull* res;
res = newFunction(f_737562);

dealloc(*PC);*PC = res;
}

void f_tmp_8(){
struct ConsPull* res;
checks(1,1){
if(1){
struct ConsPull* p1 = alloc(2);
p1->nodeType = ID_THUNK;
void** DPtr = p1->data;
res = newFunction(f_69735a65726f);
*(DPtr+1) = res;
res = copy(*(PC-1));
*(DPtr+0) = res;
res = p1;
}
dealloc(*(PC-0));
dealloc(*(PC-1));
PC-=1;
*PC=res;
}
}

void f_tmp_7(){
struct ConsPull* res;
checks(1,1){
if(1){
struct ConsPull* p1 = alloc(3);
p1->nodeType = ID_THUNK;
void** DPtr = p1->data;
res = newFunction(f_6576616c);
*(DPtr+2) = res;
res = copy(*(PC-1));
*(DPtr+1) = res;
res = alloc(0);
res->nodeType = ID_FUNCTION;
res->data = f_tmp_8;
*(DPtr+0) = res;
res = p1;
}
dealloc(*(PC-0));
dealloc(*(PC-1));
PC-=1;
*PC=res;
}
}

void f_69735a(){
struct ConsPull* res;
res = alloc(0);
res->nodeType = ID_FUNCTION;
res->data = f_tmp_7;

dealloc(*PC);*PC = res;
}

void f_tmp_9(){
struct ConsPull* res;
checks(1,1){
if(1){
struct ConsPull* p1 = alloc(2);
p1->nodeType = ID_THUNK;
void** DPtr = p1->data;
res = copy(*(PC-1));
*(DPtr+1) = res;
if(1){
struct ConsPull* p1 = alloc(2);
p1->nodeType = ID_THUNK;
void** DPtr = p1->data;
res = newFunction(f_59);
*(DPtr+1) = res;
res = copy(*(PC-1));
*(DPtr+0) = res;
res = p1;
}
*(DPtr+0) = res;
res = p1;
}
dealloc(*(PC-0));
dealloc(*(PC-1));
PC-=1;
*PC=res;
}
}

void f_59(){
struct ConsPull* res;
res = alloc(0);
res->nodeType = ID_FUNCTION;
res->data = f_tmp_9;

dealloc(*PC);*PC = res;
}

void f_tmp_10(){
struct ConsPull* res;
checks(2,1){
if(1){
struct ConsPull* p1 = alloc(4);
p1->nodeType = ID_THUNK;
void** DPtr = p1->data;
res = newFunction(f_69735a);
*(DPtr+3) = res;
res = copy(*(PC-2));
*(DPtr+2) = res;
res = newInt(0);
*(DPtr+1) = res;
if(1){
struct ConsPull* p1 = alloc(3);
p1->nodeType = ID_THUNK;
void** DPtr = p1->data;
res = newFunction(f_2b);
*(DPtr+2) = res;
if(1){
struct ConsPull* p1 = alloc(2);
p1->nodeType = ID_THUNK;
void** DPtr = p1->data;
res = copy(*(PC-1));
*(DPtr+1) = res;
if(1){
struct ConsPull* p1 = alloc(3);
p1->nodeType = ID_THUNK;
void** DPtr = p1->data;
res = newFunction(f_2d);
*(DPtr+2) = res;
res = copy(*(PC-2));
*(DPtr+1) = res;
res = newInt(1);
*(DPtr+0) = res;
res = p1;
}
*(DPtr+0) = res;
res = p1;
}
*(DPtr+1) = res;
res = copy(*(PC-2));
*(DPtr+0) = res;
res = p1;
}
*(DPtr+0) = res;
res = p1;
}
dealloc(*(PC-0));
dealloc(*(PC-1));
dealloc(*(PC-2));
PC-=2;
*PC=res;
}
}

void f_6d61696e(){
struct ConsPull* res;
if(1){
struct ConsPull* p1 = alloc(3);
p1->nodeType = ID_THUNK;
void** DPtr = p1->data;
res = newFunction(f_6576616c);
*(DPtr+2) = res;
if(1){
struct ConsPull* p1 = alloc(2);
p1->nodeType = ID_THUNK;
void** DPtr = p1->data;
if(1){
struct ConsPull* p1 = alloc(2);
p1->nodeType = ID_THUNK;
void** DPtr = p1->data;
res = newFunction(f_59);
*(DPtr+1) = res;
res = alloc(0);
res->nodeType = ID_FUNCTION;
res->data = f_tmp_10;
*(DPtr+0) = res;
res = p1;
}
*(DPtr+1) = res;
res = newInt(10);
*(DPtr+0) = res;
res = p1;
}
*(DPtr+1) = res;
res = newFunction(f_7072696e74496e74);
*(DPtr+0) = res;
res = p1;
}

dealloc(*PC);*PC = res;
}

//Ok
