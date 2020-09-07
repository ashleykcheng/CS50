#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <stdint.h>
#define BLOCK_SIZE 512
#define FILE_NAME_SIZE 8

typedef uint8_t BYTE;

//make sure is jpeg
bool new_jpeg(BYTE buffer[])
{
    return buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && ((buffer[3] & 0xf0) == 0xe0);

}

int main(int argc, char *argv[])
{
    //two arguments
    if (argc != 2)
    {
        
        return 1;
    }

    FILE *infile = fopen(argv[1], "r");
    if (infile == NULL)
    {
       
        return 1;
    }

    BYTE buffer[BLOCK_SIZE];

    bool found_first_jpg = false;
    int file_index = 0;
    FILE *outfile;
    while (fread(buffer, BLOCK_SIZE, 1, infile))
    {
        //if first jpeg
        if (new_jpeg(buffer))
        {
            if (!found_first_jpg)
            {
                found_first_jpg = true;
            }
            else
            {
                //close file
                fclose(outfile);
            }

            char filename[FILE_NAME_SIZE];
            //name file
            sprintf(filename, "%03i.jpg", file_index++);
            outfile = fopen(filename, "w");

            if (outfile == NULL)
            {
                return 1;
            }
            fwrite(buffer, BLOCK_SIZE, 1, outfile);

        }
        else if (found_first_jpg)
        {
            fwrite(buffer, BLOCK_SIZE, 1, outfile);

        }

    }
    fclose(outfile);
    fclose(infile);

}
