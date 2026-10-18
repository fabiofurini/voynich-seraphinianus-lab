#include <bits/stdc++.h>
using namespace std;
int key4(const array<int,4>&a,const vector<int>&m){int v=0;for(int x:a)v=v*27+(x==26?26:m[x]);return v;}
int main(int argc,char**argv){
 if(argc<6)return 2;
 ifstream lmfile(argv[1]);vector<double>lm(27*27*27*27);for(auto &x:lm)lmfile>>x;
 ifstream in(argv[2]);string text;getline(in,text);int n;in>>n;
 vector<array<int,4>>grams(n);vector<int>count(n);vector<vector<int>>ix(26);
 for(int j=0;j<n;j++){for(int k=0;k<4;k++)in>>grams[j][k];in>>count[j];set<int>seen;for(int x:grams[j])if(x<26)seen.insert(x);for(int x:seen)ix[x].push_back(j);}
 vector<double>cf(26),pf(26);for(int i=0;i<n;i++)for(int x:grams[i])if(x<26)cf[x]+=count[i];
 ifstream freq(argv[3]);for(auto &x:pf)freq>>x;
 vector<int>a(26),b(26);iota(a.begin(),a.end(),0);iota(b.begin(),b.end(),0);
 sort(a.begin(),a.end(),[&](int i,int j){return cf[i]>cf[j];});sort(b.begin(),b.end(),[&](int i,int j){return pf[i]>pf[j];});
 vector<int>initial(26);for(int i=0;i<26;i++)initial[a[i]]=b[i];
 mt19937 rng(20261017);uniform_real_distribution<double>unif(0,1);double best=-1e300;vector<int>bestmap;
 int restarts=stoi(argv[4]),steps=stoi(argv[5]);
 vector<vector<vector<int>>>affected(26,vector<vector<int>>(26));
 for(int i=0;i<26;i++)for(int j=i+1;j<26;j++)set_union(ix[i].begin(),ix[i].end(),ix[j].begin(),ix[j].end(),back_inserter(affected[i][j]));
 for(int restart=0;restart<restarts;restart++){
  vector<int>m=initial;if(restart)for(int i=0;i<12+restart;i++)swap(m[rng()%26],m[rng()%26]);
  vector<double>vals(n);double score=0;for(int i=0;i<n;i++){vals[i]=lm[key4(grams[i],m)]*count[i];score+=vals[i];}
  for(int st=0;st<steps;st++){
   int i=rng()%26,j=rng()%26;if(i==j)continue;if(i>j)swap(i,j);auto &ids=affected[i][j];
   swap(m[i],m[j]);double delta=0;for(int id:ids)delta+=lm[key4(grams[id],m)]*count[id]-vals[id];
   double temp=60*pow(.001,(double)st/steps);
   if(delta>=0 || unif(rng)<exp(delta/temp)){score+=delta;for(int id:ids)vals[id]=lm[key4(grams[id],m)]*count[id];}
   else swap(m[i],m[j]);
   if(score>best){best=score;bestmap=m;}
  }
 }
 cout<<setprecision(12)<<best<<"\n";for(int x:bestmap)cout<<char('a'+x);cout<<"\n";
 for(char x:text)cout<<(x==' '? ' ':char('a'+bestmap[x-'a']));cout<<"\n";
}
