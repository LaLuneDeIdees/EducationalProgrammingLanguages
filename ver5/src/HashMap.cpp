#ifndef HASH_MAP_LDI
#define HASH_MAP_LDI

#include <vector>
#include <memory>
#include <cmath>

using namespace std;
extern uint32_t pushes;

uint32_t hashC(string str){
	uint32_t out=0;
	for(int i=0;i<str.size();i++){
        uint8_t d = str[i];
        for(int k=0;k<8;k++){
            uint8_t b = (out&1) ^ ((d>>k) & 1);
            out = (out>>1) | (b<<31);
            out = out ^ (b<<(31-2));
            out = out ^ (b<<(24-2));
            out = out ^ (b<<(22-2));
            out = out ^ (b<<(16-2));
            out = out ^ (b<<(14-2));
            out = out ^ (b<<(8-2));
            out = out ^ (b<<(7-2));
            out = out ^ (b<<(5-2));
            out = out ^ (b<<(3-2));
        }
        //32 31 24 22 16 14 8 7 5 3 1 0
		// out+=(int(str[i])-64)*(i+1);
	}
	return out;
}

template<typename DataT>
struct hashData
{
    string key;
    DataT data;
    uint32_t hashCode;
    uint32_t idx1;
    bool isUse=true;
};


template<typename DataT>
class HashMap
{
public:
    /* data */
    uint32_t banksize = BANKSIZE;//in last use 1024*1024;
    vector<hashData<DataT>> datas;
    vector<uint32_t> idxs[BANKSIZE];
    vector<uint32_t> frees;
    bool fail = false;
// public:
    HashMap(){
        // idxs = (vector<uint32_t>*)malloc(sizeof(vector<uint32_t>)*banksize);
        // for(int i=0;i<banksize;i++){
        //     vector<uint32_t> n;
        //     idxs[i] = n;
        // }
    }
    ~HashMap(){
        // realloc(idxs,banksize);
    }
    void put(string key,DataT data){
        put(key,data,hashC(key));
    }
    void put(string key,DataT data,uint32_t hashCode){
        hashData<DataT> n;
        n.key = key;
        n.data = data;
        n.hashCode = hashCode;
        n.idx1 = hashCode%banksize;
        if(frees.size()>0){
            idxs[hashCode%banksize].push_back(frees.back());
            datas[frees.back()] = n;
            frees.pop_back();
        }else{
            idxs[hashCode%banksize].push_back(datas.size());
            datas.push_back(n);
        }
    }
    DataT get(string key){
        return get(key,hashC(key));
    }
    DataT get(string key, uint32_t hashCode){
        fail=false;
        for(auto i:idxs[hashCode%banksize]){
            if(datas[i].isUse==true && datas[i].hashCode==hashCode
                #ifdef CHECK_KEYS
                    && datas[i].key==key
                #endif
                ){
                return datas[i].data;
            }
        }
        fail=true;
        return DataT();
    }

    DataT getLast(string key){
        return getLast(key,hashC(key));
    }
    DataT getLast(string key, uint32_t hashCode){
        fail=false;
        for(int i=idxs[hashCode%banksize].size()-1;i>=0;i--){
            if(datas[idxs[hashCode%banksize][i]].isUse==true && datas[idxs[hashCode%banksize][i]].hashCode==hashCode
                #ifdef CHECK_KEYS
                    && datas[idxs[hashCode%banksize][i]].key==key
                #endif
                ){
                return datas[idxs[hashCode%banksize][i]].data;
            }
        }
        fail=true;
        return DataT();
    }
    void pop(){
        idxs[datas.back().idx1].pop_back();//[datas.back().idx2]=0;
        datas.pop_back();
    }
    void erase(string key){
        erase(key,hashC(key));
    }
    void erase(string key,uint32_t hashCode){

        for(int i=0;i<idxs[hashCode%banksize].size();i++){
            if(datas[idxs[hashCode%banksize][i]].isUse==true && datas[idxs[hashCode%banksize][i]].hashCode==hashCode
                #ifdef CHECK_KEYS
                    && datas[idxs[hashCode%banksize][i]].key==key
                #endif
                ){
                datas[idxs[hashCode%banksize][i]] = hashData<DataT>();
                datas[idxs[hashCode%banksize][i]].isUse=false;

                frees.push_back(idxs[hashCode%banksize][i]);

                idxs[hashCode%banksize].erase(idxs[hashCode%banksize].begin()+i);
                return;
            }
        }
    }
};

#endif