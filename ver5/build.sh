#!/usr/bin/bash
cd src
cd lib
for file in ./*.cpp
do
    g++ -std=c++17 -g -O5 -shared -fPIC  "$file" -o "../../bin/${file//\.cpp/\.so}"
done

cd ..
g++ -std=c++17 -g -O5 -ldl ./main.cpp -o ../bin/run

cd ..