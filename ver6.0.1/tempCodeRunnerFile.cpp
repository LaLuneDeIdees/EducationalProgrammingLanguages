#include <vector>
using namespace std;
vector<void*> S;
int main(){
    goto end;
// main is ST | (
//     ret (add 1 2)
//    ) >=> ( \ a -> printf '%d\n' (a : Nil)
//    ) >>> exit

// | is
//     infixl
//     a -> (a -> b) -> a -> b
//     \ a b -> b a

// ~ is
//     infixr
//     (a -> b) -> a -> a -> b
//     \ a b -> a b


// >>> is
//     infixl
//     (State -> IO a) -> (State -> IO b) -> State -> IO b
//     \ a b x -> (
//         b ~ (\ (IO a s) -> s) ~ (a x)
//     )


// >=> is
//     infixl
//     (State -> IO a) -> (a -> s -> IO b) -> State -> IO b
//     \ a b x -> (
//         (\ (IO a s) -> b a s) a x
//     )


// + is
//   infixl
//   I32 -> I32 -> I32


// add is 
//     \ a b -> a + b


// ret is
//     a -> x -> IO a
//     \ a s -> IO a s


// exit is
//     State -> IO a

// printf is
//     Ptr U8 -> I32 -> State -> IO c

    end:
    return 0;
}