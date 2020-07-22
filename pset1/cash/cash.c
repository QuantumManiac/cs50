//Takes cash value and gives minimum number of coins to get amount
#include <stdio.h>
#include <cs50.h>
#include <math.h>



int main(void)
{
    int m;
    float n;
    int o = 0;
    do
    {
        n = get_float("Change owed: ");
    }
    while (n <= 0);
    m = round(n * 100);
    while (m - 25 >= 0)
    {
        m = m - 25;
        o++;
    }
    while (m - 10 >= 0)
    {
        m = m - 10;
        o++;
    }
    while (m - 5 >= 0)
    {
        m = m - 5;
        o++;
    }
    while (m - 1 >= 0)
    {
        m = m - 1;
        o++;
    }
    printf("%i\n", o);
}