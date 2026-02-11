#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

void cpu_task(const char *name)
{
    for (long i = 0; i < 500000000; i++)
    {
        if (i % 100000000 == 0)
            printf("%s running...\n", name);
    }
}

int main()
{
    pid_t pid1, pid2;

    pid1 = fork();
    if (pid1 == 0)
    {
        nice(-25);   // higher priority
        cpu_task("High Priority Process");
        return 0;
    }

    pid2 = fork();
    if (pid2 == 0)
    {
        nice(10);    // lower priority
        cpu_task("Low Priority Process");
        return 0;
    }

    wait(NULL);
    wait(NULL);

    printf("Parent: All processes completed\n");
    return 0;
}
