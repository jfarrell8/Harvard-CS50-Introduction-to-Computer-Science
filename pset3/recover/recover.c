#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{

    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: copy infile outfile\n");
        return 1;
    }

    // remember infile name
    char *infile = argv[1];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // create unsigned integer array (unsigned so integers are positive) of 512 bytes (JPEG block size)
    uint8_t buffer[512];

    // establish counter and NULL image pointer file. counter will update in loop to create XXX.jpg filenames
    int counter = 0;
    FILE *img = NULL;

    // condition to check EOF
    while (fread(buffer, sizeof(buffer), 1, inptr))
    {
        // Check if start of JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {

            // if there's an image open, close it (because you found a new JPEG)
            if (img != NULL)
            {
                fclose(img);
            }

            // Create JPEG file (filename)
            char filename[8];
            sprintf(filename, "%03i.jpg", counter);

            // Open a new JPEG file ("img") for writing
            img = fopen(filename, "w");

            // Update the counter so the next image filename will be the next 00X
            counter++;

        }

        // Continue writing buffer to img file as long as there exists an image file
        if (img != NULL)
        {
            fwrite(buffer, sizeof(buffer), 1, img);
        }

    }

    // close the last image file
    fclose(img);

    //close the input file (card.raw)
    fclose(inptr);

return 0;
}
