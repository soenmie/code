#define _CRT_SECURE_NO_WARNINGS
#include<cstdio>
#include<cstring>
#include<cstdlib>
#include<cmath>
#include<cstring>
#include<string>
#include<map>
#include<set>
#include<iostream>
#define MIN(x,y) (x)<(y)?(x):(y)

using namespace std;

const int N=80100;
const int M=1500;
map<string,int> color;
int colnum[N];
int edge[M][M][2];
int ednum[M][M];

int cal(int st,int en)
{
    if(st == en)
        return 0;
    if(edge[st][en][1] == 1)
        return edge[st][en][0];

    map<int,int> minedge;

    edge[st][st][1] = 1;
    for(int i=1; i<=ednum[st][0]; i++)
    {
        int pvt = ednum[st][i];
        minedge[pvt] = edge[st][pvt][0];
    }

    while(!minedge.empty())
    {
        map<int,int>::iterator it;
        int minnum = -1;
        for(it=minedge.begin(); it!=minedge.end(); it++)
        {
            if(minnum<0 || it->second<minedge[minnum])
            {
                minnum = it->first;
            }
        }

        edge[st][minnum][1] = 1;

        for(int i=1; i<=ednum[minnum][0]; i++)
        {
            int pvt = ednum[minnum][i];
            if(edge[st][pvt][0] == -1 || edge[st][pvt][0] > edge[st][minnum][0]+edge[minnum][pvt][0])
            {
                edge[st][pvt][0] = edge[st][minnum][0]+edge[minnum][pvt][0];
                minedge[pvt] = edge[st][pvt][0];
            }
        }
        minedge.erase(minnum);
    }

    for(int i=0; i<M; i++)
    {
        edge[st][i][1] = 1;
    }
    return edge[st][en][0];
}

int main1()
{
    freopen("E-large-practice.in","r",stdin);
    freopen("E-large-practice.out","w",stdout);

    int t;
    scanf("%d",&t);
    for(int cnt=1;cnt<=t;cnt++)
    {
        color.clear();
        memset(colnum,0,sizeof(colnum));
        memset(edge,-1,sizeof(edge));
        memset(ednum,0,sizeof(ednum));

        int n;
        scanf("%d",&n);

        int coln = 0;
        for(int i=1; i<=n; i++)
        {
            char tmp[5];
            scanf("%s",tmp);
            string tmp_s = tmp;

            if(color[tmp_s] == 0)
                color[tmp_s] = ++coln;
            colnum[i] = color[tmp_s];
            //printf("dddd %d %d\n",i,colnum[i]);
        }

        int m;
        scanf("%d",&m);
        for(int i=0;i<m;i++)
        {
            int st,en,ti;
            scanf("%d%d%d",&st,&en,&ti);

            int stc = colnum[st];
            int enc = colnum[en];
            if(stc == enc)
                continue;

            if(edge[stc][enc][0] == -1)
            {
                edge[stc][enc][0] = ti;
                ednum[stc][++ednum[stc][0]] = enc;
            }
            else
            {
                if(edge[stc][enc][0] > ti)
                    edge[stc][enc][0] = ti;
            }
        }
        /*
           printf("\nedge:\n");
           for(int i=1; i<=coln; i++)
           {
           for(int j=1; j<=coln;j++)
           printf("%d ",edge[i][j][0]);
           printf("\n");
           }
           printf("\nedgenum:\n");
           for(int i=1; i<=coln; i++)
           {
           printf("i:",i);
           for(int j=1; j<=ednum[i][0];j++)
           printf("%d ",ednum[i][j]);
           printf("\n");
           }
           */

        printf("Case #%d:\n",cnt);

        int s;
        scanf("%d",&s);

        for(int i=0; i<s; i++)
        {
            int st,en;
            scanf("%d%d",&st,&en);

            int stc = colnum[st];
            int enc = colnum[en];

            //printf("xxx %d %d\n",stc,enc);

            printf("%d\n",cal(stc,enc));
        }
    }
    return 0;
}
