// Program that encrypts messages using "Caesar's Cipher"
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    string s;
    int k = 0;
    // check for argument
    if (argc == 2)
    {
        k = atoi(argv[1]);
    }
    else
    {
        printf("usage: caesar k\n");
        return 1;
    }
    // check for positive integer
    if (k > 0)
    {
        s = get_string("plaintext: ");
    }
    else
    {
        printf("usage: caesar k\n");
        return 1;
    }
    printf("ciphertext: ");
    for (int i = 0; i < strlen(s); i++)
    {
        // changing lower-case letters
        if (islower(s[i]))
        {
            printf("%c", (s[i] - 'a' + k) % 26 + 'a');
        }
        // changing upper-case letters
        else if (isupper(s[i]))
        {
            printf("%c", (s[i] - 'A' + k) % 26 + 'A');
        }
        // keeping everything else the same
        else
        {
            printf("%c", s[i]);
        }
    }
    printf("\n");
    return 0;
}