#include<stdio.h>
#include<stdlib.h>

int main()
{
    char *vname = "HOME";
    char *value;
    char *newvalue;

    value = getenv(vname);

    if(value != 0 )
    {
        printf("the value of the environment variable %s  is %s\n",vname,value);
    }
    else{
        printf("error reading the value");
    }

    if(setenv("HELLO","SPANIDEA\n",1)!=0)
    {
        printf("error");
    }
    newvalue = getenv("HELLO");
    printf("the value is changed to %s",newvalue);
    
}