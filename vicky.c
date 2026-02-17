```c
#include <stdio.h>

int main() {
    long long int fact(int n) {
        if (n == 0)
            return 1;
        else
            return n * fact(n - 1);
    }

    int num;
    printf("Enter a number: ");
    scanf("%d", &num);

    printf("Factorial of %d = %lld\n", num, fact(num));

    return 0;
}
```