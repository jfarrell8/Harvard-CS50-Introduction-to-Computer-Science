// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: copy infile outfile\n");
        return 1;
    }

    // remember filenames
    char *number = argv[1]; // positive integer inputted
    char *infile = argv[2];
    char *outfile = argv[3];

    int n = atoi(number);

    // check that integer inputted is positive and <=100
    if (n <= 0 || n > 100)
    {
        printf("n must be a positive integer less than or equal to 100.\n");
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
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    LONG biWidthOld = bi.biWidth;
    bi.biWidth *= n;

    LONG biHeightOld = bi.biHeight;
    bi.biHeight *= n;

    // determine padding (old and new) for scanlines
    int paddingOld = (4 - (biWidthOld * sizeof(RGBTRIPLE)) % 4) % 4;
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    bi.biSizeImage = ((sizeof(RGBTRIPLE)*bi.biWidth) + padding)*abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);


    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);


    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(biHeightOld); i < biHeight; i++)
    {
        // will iterate new horizontal outfile lines n times before moving to next infile pixel
        for (int j = 0; j < n; j++)
        {
            // iterate over pixels in scanline horizontally
            for (int k = 0; k < biWidthOld; k++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                for (int l = 0; l < n; l++)
                {
                // write each pixel to outfile n times before moving onto the next pixel
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // add padding
            for (int m = 0; m < padding; m++)
            {
                fputc(0x00, outptr);
            }

            // check if you need to iterate more times vertically (downward), and if so, move the position of the infile back to the beginning of bitmap pixels
            if (j < n - 1)
                fseek(inptr, -(biWidthOld * sizeof(RGBTRIPLE)), SEEK_CUR);
        }
        // skip over padding, if any
        fseek(inptr, paddingOld, SEEK_CUR);
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}