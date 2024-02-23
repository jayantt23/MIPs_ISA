#include <stdio.h>

int factorial(int n)
{
    int result = 1;
    for (int i = 1; i <= n; ++i)
    {
        result *= i;
    }
    return result;
}

int main()
{
    int n = 10;
    int ans = factorial(n);
    printf("%d\n", ans);
    return 0;
}
