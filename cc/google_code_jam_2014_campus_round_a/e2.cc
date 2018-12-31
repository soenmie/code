#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#include<string>
#include<math.h>
#include<stdlib.h>
#include<set>
#include<bitset>
#include<map>
#include<vector>
#include<string.h>
#include<algorithm>
#include<iostream>
#include<queue>
#define SZ(X) ((int)(X).size())
#define ALL(X) (X).begin(), (X).end()
#define REP(I, N) for (int I = 0; I < (N); ++I)
#define REPP(I, A, B) for (int I = (A); I < (B); ++I)
#define REPC(I, C) for (int I = 0; !(C); ++I)
#define RI(X) scanf("%d", &(X))
#define RII(X, Y) scanf("%d%d", &(X), &(Y))
#define RIII(X, Y, Z) scanf("%d%d%d", &(X), &(Y), &(Z))
#define DRI(X) int (X); scanf("%d", &X)
#define DRII(X, Y) int X, Y; scanf("%d%d", &X, &Y)
#define DRIII(X, Y, Z) int X, Y, Z; scanf("%d%d%d", &X, &Y, &Z)
#define RS(X) scanf("%s", (X))
#define CASET int ___T, case_n = 1; scanf("%d ", &___T); while (___T-- > 0)
#define MP make_pair
#define PB push_back
#define MS0(X) memset((X), 0, sizeof((X)))
#define MS1(X) memset((X), -1, sizeof((X)))
#define LEN(X) strlen(X)
#define F first
#define S second
using namespace std;
#define SIZE 88888
int get_digit(char c){
    if(c>='a'&&c<='z')return c-'a';
    return c-'0'+26;
}
int get_num(char s[]){
    return get_digit(s[0])*36+get_digit(s[1]);
}
int id[SIZE],an[1300][1300];
vector<pair<int,int> >e[1300];
struct data{
    int x,v;
    data(int _x=0,int _v=0):x(_x),v(_v){}
    bool operator<(const data& b)const{return v>b.v;}
};
bool fresh(int&x,int v){
    if(x==-1||x>v){
        x=v;
        return true;
    }
    return false;
}
void go(int st,int res[]){
    priority_queue<data>H;
    res[st]=0;
    H.push(data(st,0));
    while(!H.empty()){
        data now=H.top();
        H.pop();
        int x=now.x;
        if(res[x]<now.v)continue;
        REP(i,SZ(e[x])){
            int y=e[x][i].F;
            if(fresh(res[y],res[x]+e[x][i].S)){
                H.push(data(y,res[y]));
            }
        }
    }
}
void main1(){
    freopen("E-large-practice.in","r",stdin);
    freopen("E-large-practice.out","w",stdout);
    CASET{
        MS1(an);
        DRI(N);
        REPP(i,1,N+1){
            char s[4];
            scanf("%s",s);
            id[i]=get_num(s);
        }
        DRI(M);
        REP(i,1300)e[i].clear();
        while(M--){
            DRIII(x,y,v);
            e[id[x]].PB(MP(id[y],v));
        }
        REP(i,1296){
            go(i,an[i]);
        }
        printf("Case #%d:\n",case_n++);
        DRI(cc);
        while(cc--){
            DRII(x,y);
            int* xxx;
            xxx = an[1107];
            printf("%d\n",an[id[x]][id[y]]);
        }
    }
}
