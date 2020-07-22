// Takes a BMP file and then resizes it by a given factor

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: resize factor infile outfile\n");
        return 1;
    }

    // remember filenames and factor
    int factor = atoi(argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];

    //check if valid factor
    if (factor < 0 || factor > 100)
    {
        fprintf(stderr, "Factor must be a positive integer no more than 100");
        return 2;
    }

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 3;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 4;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf, bfnew;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    bfnew = bf;

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi, binew;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    binew = bi;

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 5;
    }

    // Find new dimensions
    binew.biWidth = bi.biWidth * factor;
    binew.biHeight = bi.biHeight * factor;

    // Find old and new paddings
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int paddingnew = (4 - (binew.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // Find new bfSize and biSizeImage
    binew.biSizeImage = abs(binew.biHeight) * (binew.biWidth * sizeof(RGBTRIPLE) + paddingnew);
    bfnew.bfSize = binew.biSizeImage + 54;


    // write outfile's BITMAPFILEHEADER
    fwrite(&bfnew, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&binew, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // read scanlines factor times
        for (int j = 0; j < factor; j++)
        {

            // move pointer to start of line
            fseek(inptr, 54 + (bi.biWidth * 3 + padding) * i, SEEK_SET);

            // iterate over pixels in scanline
            for (int k = 0; k < bi.biWidth; k++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                // write RGB triple to outfile after resizing
                for (int l = 0; l < factor; l++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // add new padding to fit with factor
            for (int k = 0; k < paddingnew; k++)
            {
                fputc(0x00, outptr);
            }
        }
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
