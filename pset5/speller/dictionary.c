// Implements a dictionary's functionality
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

#include "dictionary.h"

// Pointer for linked list
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Size of hash table
#define SIZE 1000

// Create hash table
node *hashtable[SIZE] = {NULL};

// Create hash func
int hash(const char *word)
{
    int w;
    int hash = 0;
    for (int i = 0; word[i] != '\0'; i++)
    {
        // Letter
        if (isalpha(word[i]))
        {
            w = word [i] - 'a' + 1;
        }

        // Comma
        else
        {
            w = 27;
        }

        hash = ((hash << 3) + w) % SIZE;
    }
    return hash;
}

int dictionary_size = 0;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    // Array for word storage
    char word[LENGTH + 1];

    // Scan through file and load words to hash
    while (fscanf(file, "%s\n", word) != EOF)
    {
        dictionary_size++;
        node *new_word = malloc(sizeof(node));
        strcpy(new_word->word, word);
        int index = hash(word);
        if (hashtable[index] == NULL)
        {
            hashtable[index] = new_word;
            new_word->next = NULL;
        }
        else
        {
            new_word->next = hashtable[index];
            hashtable[index] = new_word;
        }
    }
    fclose(file);
    return true;
}

// Returns true if word is in dictionary else false.
bool check(const char *word)
{
    char temp[LENGTH + 1];
    int len = strlen(word);
    for (int i = 0; i < len; i++)
    {
        temp[i] = tolower(word[i]);
    }
    temp[len] = '\0';
    int index = hash(temp);
    if (hashtable[index] == NULL)
    {
        return false;
    }
    // Cursor to compare
    node *cursor = hashtable[index];

    while (cursor != NULL)
    {
        if (strcmp(temp, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

//Returns number of words in dictionary if loaded else 0 if not yet loaded.
unsigned int size(void)
{
    // If loaded, return size of dictionary
    if (dictionary_size > 0)
    {
        return dictionary_size;
    }
    // If dictionary load fails
    else
    {
        return 0;
    }
}

// Unloads dictionary from memory.  Returns true if successful else false.
bool unload(void)
{
    int index = 0;
    // Go through entire hashtable
    while (index < SIZE)
    {
        // Is hashtable is empty, next index
        if (hashtable[index] == NULL)
        {
            index++;
        }
        // If hashtable is not empty, free at cursor
        else
        {
            while (hashtable[index] != NULL)
            {
                node *cursor = hashtable[index];
                hashtable[index] = cursor->next;
                free(cursor);
            }
            // Go to next index
            index++;
        }
    }
    // Success
    return true;
}