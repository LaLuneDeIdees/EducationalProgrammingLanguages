#include "../RunTime.cpp"

using namespace std;

extern "C" void print(vector<Data>& Stack){
    cout << Stack.back().data<<endl;
    Stack.pop_back();
}
extern "C" void plus(vector<Data>& Stack){
    double a = stod(Stack.back().data);Stack.pop_back();
    double b = stod(Stack.back().data);Stack.pop_back();
    Data n;
    n.data = to_string(a+b);
    n.hashCode = hashC(n.data);
    Stack.push_back(n);
}
extern "C" void minus(vector<Data>& Stack){
    double a = stod(Stack.back().data);Stack.pop_back();
    double b = stod(Stack.back().data);Stack.pop_back();
    Data n;
    n.data = to_string(b-a);
    n.hashCode = hashC(n.data);
    Stack.push_back(n);
}
extern "C" void charCode(vector<Data>& Stack){
    Data data = Stack.back();Stack.pop_back();
    data.data = to_string(int(data.data[0]));
    Stack.push_back(data);
}
extern "C" void If(vector<Data>& Stack){
    Data IfFalse = Stack.back();Stack.pop_back();
    Data IfTrue = Stack.back();Stack.pop_back();
    Data IfCondition = Stack.back();Stack.pop_back();
    if(IfCondition.data[0]=='0'){
        Stack.push_back(IfFalse);
    }else
    {
        Stack.push_back(IfTrue);
    }
    
}
int main(){
	return 0;
}
