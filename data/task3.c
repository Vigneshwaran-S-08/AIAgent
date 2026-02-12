#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<sys/wait.h>
#include<pthread.h>


int main()
{
    pid_t pid;
    int i;
    char *commands[][3] = { {"ls","-1",NULL},{"pwd",NULL,NULL},{"date",NULL,NULL} };  
    
    int n_commands = 3;

    for(i =0;i<n_commands;i++)
    {
        pid = fork();

        if(pid < 0 )
        {
            printf("fork failed");
            return 1;
        }
        else if(pid ==0)
        {
            printf("child %d is executing command %s\n",getpid(),commands[i][0]);
                
            execvp(commands[i][0],commands[i]);
            /*exec only returns when it is failed so the next line wont be executed*/
            printf("exec failed");
            exit(1);
        }
       
    }
      for(i=0;i<n_commands;i++)
        {
            wait(NULL);
        }
     printf("All child process are completed\n");
        return 0;

}
