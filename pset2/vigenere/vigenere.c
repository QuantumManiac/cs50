// Program that encrypts messages using "Vigenère's Cipher"
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    string s;
    string k;
    char r;
    int l = 0;
    if (argc == 2)
    {
        k = argv[1];
    }
    else
    {
        printf("usage: vigenere k\n");
        return 1;
    }
    // check for letters
    for (int j = 0; j < strlen(k); j++)
    {
        //!isaplha can be used instead of != statement
        if (!isalpha(argv[1][j]))
        {
            printf("usage: vigenere k\n");
            return 1;
        }

    }
    s = get_string("plaintext: ");
    printf("ciphertext: ");
    for (int i = 0; i < strlen(s); i++)
    {
        //Make "key" to encode letters wih
        r = tolower(k[l % strlen(k)]) - 'a';
        // changing lower-case letters
        if (islower(s[i]))
        {
            printf("%c", (s[i] - 'a' + r) % 26 + 'a');
            l++;
        }
        // changing upper-case letters
        else if (isupper(s[i]))
        {
            printf("%c", (s[i] - 'A' + r) % 26 + 'A');
            l++;
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