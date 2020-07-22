// Makes stairs like the one at the end of World 1-1 in Super Mario Bros.
#include <stdio.h>
#include <cs50.h>



int main(void)
{
    int h;

    do
    {
        h = get_int("Height:");
    }
    while (h < 0 || h > 23);

    for (int i = 0; i < h; i++)
    {
        // Making spaces before stairs
        for (int j = 0; j < h - (i + 1); j++)
        {
            printf(" ");
        }
        // Making Hashes for stairs
        for (int k = 0; k < i + 2; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}
