
####################################################
/\This is comment!!!\/
a is 'Hello world'
b is 5
c is 2.187
d is a+b*c/3*-1+ ++c++ + 3
a is a-- -b
a is a + a++
a is a++ + a
b is b + 1
b++
b is b+a
== != <= >= | & ^ !

max with a, b is {
	if a<b is{
		return b
	}elis{
		return a
	}
}
	/\
and this
	\/
e is max 5, (max 4,6)
f1 is max 5, . << max ., 2

g is f1 4

hello with name is{
	nextMsg is '';
	hi is {
		if name == '' is{
			return
		}
		return 'Hello '
	}
	name is hi + name + nextMsg + '\n'
	return name
}

/\
	I like ascii art!!
	 (')) ^v^  _           (`)_
	(__)_) ,--j j-------, (__)_)
		    /_.-.___.-.__/ \
		  ,8| [_],-.[_] | oOo
	,,,oO8|_o8_|_|_8o_|&888o,,,hjw
\/

h is hello 'dad'
j is hello.hi
obj1 is new hello
obj.nextMsg is '. Wellcome!!!'
obj 'New Day'

thr is [=]hello 'dad'
thr.obj.hi
[=]thr.obj.hi
[==]thr.obj.hi
thr.close

k is true

if k is {

}elif !k is{

}elis{

}

while k is [=]{

}

for with i is 0 while i<0 call i++ is{}
for while !k is{}
for with i is 0 while i<1 call {i++;k=!k} is {}

f2 with a is{
	if a<=0 is{
		return
	}elis{
		a--
		f2' a
	}
}

[+/macro/{(hello 'world')}]

if a is{
	macro
}
newhello is new hello 'world'
newhello

[+inc{style.1.example.3.ldi}]

[+cpp{hello}{void,void,none}{
	#include <iostream>
	using namespace std;
	void hello(){
		cout << "Hi!" << endl;
	}
}]

cpp.hello

[+cpp{add}{int,int,int,num}{
	void add(int a, int b){
		return a+b;
	}
}]

a is 5
b is 9
c is cpp.add a, b

syscall 0, a


mylist is [1,2,3,4]
add5 is add 5, .
mylist is add5 mylist

f3 is {
	a is 5
	b is 7
}

obj is func2
obj.a is 6

obj is new func2
obj.a is 7

nnn is mylist
nnn.0 is 98

nnn is new mylist
nnn."HI" is "HELLO"

abc is mylist."HI"
try{
	abc is add5 abc
}catch with e is{
	abc is 6
}finally is{

}

f4 with a,b where ., 7 is{
	return a+b
}

