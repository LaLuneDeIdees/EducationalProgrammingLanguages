long fib(long i){
    if(i<=2)return 1;
    return fib(i-1)+fib(i-2);
}
int main(){
    printf("%d\n",fib(40));
    return 0;
}