#include <fstream>

using namespace std;

int main(){
    ofstream f("/dev/stdout");
    f <<"HEllo world"<<endl;
    return 0;
}