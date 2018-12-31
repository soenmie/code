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
#define SIZE 111
int N;
int dx[4]={1,0,-1,0};
int dy[4]={0,-1,0,1};
char s[SIZE][SIZE],an[SIZE*SIZE];
char ss[6]="SWNE";
void nxt(int& x){
    x=(x+1)&3;
}
void last(int& x){
    x=(x+3)&3;
}
int main(){
    freopen("D-large-practice.in","r",stdin);
    freopen("D-large-practice.out","w",stdout);
    CASET{
        RI(N);
        REPP(i,1,N+1)RS(s[i]+1);
        REP(i,N+2)s[0][i]=s[i][0]=s[N+1][i]=s[i][N+1]='#';
        DRII(sx,sy);
        DRII(ex,ey);
        int now=0,dir=0;
        while(1){
            int nx=sx+dx[dir];
            int ny=sy+dy[dir];
            if(s[nx][ny]=='#')break;
            nxt(dir);
        }
        nxt(dir);
        while((sx!=ex||sy!=ey)&&now<10010){
            int tt=0;
            last(dir);
            while(tt<8){
                tt++;
                int nx=sx+dx[dir];
                int ny=sy+dy[dir];
                if(s[nx][ny]!='#')break;
                nxt(dir);
            }
            if(tt==8){
                now=0;
                break;
            }
            an[now++]=ss[dir];
            sx+=dx[dir];
            sy+=dy[dir];
        }
        printf("Case #%d: ",case_n++);
        if(!now||now>10000)puts("Edison ran out of energy.");
        else{
            printf("%d\n",now);
            an[now]=0;
            puts(an);
        }
    }
    return 0;
}
