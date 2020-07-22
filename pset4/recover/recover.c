// Takes a raw file and attempts to recover JPG pictures from it
#include <stdio.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "usage: recover file\n");
        return 1;
    }

    // Open input file
    char *input = argv[1];
    FILE *raw = fopen(input, "r");
    if (raw == NULL)
    {
        fprintf(stderr, "file cannot be opened\n");
        return 1;
    }

    // Output file
    FILE *jpg = NULL;

    // Create buffer
    unsigned char buffer[512];

    // Check if currently on a JPG
    int currentjpg = 0;

    // Filename count
    int count = 0;

    // Read through all blocks
    while (fread(buffer, 512, 1, raw) == 1)
    {
        // Check if signature exists. If so, create file with proper name
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff)
        {
            if (currentjpg == 1)
            {
                fclose(jpg);
            }
            else
            {
                currentjpg = 1;
            }
            char jpgname[8];
            sprintf(jpgname, "%03d.jpg", count);
            jpg = fopen(jpgname, "a");
            count++;
        }

        // Write to file once jpg is found
        if (currentjpg == 1)
        {
            fwrite(buffer, 512, 1, jpg);
        }
    }

    // Close files
    fclose(raw);
    fclose(jpg);

    // Success
    return 0;
}