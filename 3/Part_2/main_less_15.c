#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define K 12
int main(void){
    FILE *f=fopen("input.txt","r");if(!f){perror("Error");return 1;}
    char l[256];unsigned long long total=0;
    while(fgets(l,sizeof(l),f)){l[strcspn(l,"\r\n")]=0;int len=strlen(l),ri=0;char r[K+1];
        for(int i=0;i<len;i++){if(l[i]<'0'||l[i]>'9')continue;
            while(ri>0&&r[ri-1]<l[i]&&(len-i-1+ri)>=K)ri--;
            if(ri<K)r[ri++]=l[i];}
        r[ri]='\0';total+=strtoull(r,NULL,10);}
    fclose(f);printf("%llu\n",total);return 0;
}
