#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int r = image[i][j].rgbtRed;
            int g = image[i][j].rgbtGreen;
            int b = image[i][j].rgbtBlue;

            int average = round((r + g + b) / 3.0);

            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int originalRed = image[i][j].rgbtRed;
            int originalGreen = image[i][j].rgbtGreen;
            int originalBlue = image[i][j].rgbtBlue;

            int sepiaRed = round((0.393 * originalRed) + (0.769 * originalGreen) + (0.189 * originalBlue));
            int sepiaGreen = round((0.349 * originalRed) + (0.686 * originalGreen) + (0.168 * originalBlue));
            int sepiaBlue = round((0.272 * originalRed) + (0.534 * originalGreen) + (0.131 * originalBlue));

            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;

            if (sepiaRed > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            if (sepiaGreen > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
        }
    }

    return;
}

// Reflect image horizontally
void swap(RGBTRIPLE *a, RGBTRIPLE *b);

void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            swap(&image[i][j], &image[i][width - 1 - j]);
        }
    }

    return;
}

void swap(RGBTRIPLE *a, RGBTRIPLE *b)
{
    RGBTRIPLE tmp = *a;
    *a = *b;
    *b = tmp;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = 0;
            int green = 0;
            int blue = 0;
            float pixel = 0.00;

            for (int x = -1; x < 2; x++)
            {
                for (int y = -1; y < 2; y++)
                {
                    if (i + x < 0 || i + x > height - 1 || j + y < 0 || j + y > width - 1)
                    {
                        continue;
                    }

                    red += image[i + x][j + y].rgbtRed;
                    green += image[i + x][j + y].rgbtGreen;
                    blue += image[i + x][j + y].rgbtBlue;
                    pixel++;
                }
            }

            copy[i][j].rgbtRed = round(red / pixel);
            copy[i][j].rgbtGreen = round(green / pixel);
            copy[i][j].rgbtBlue = round(blue / pixel);
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = copy[i][j].rgbtRed;
            image[i][j].rgbtGreen = copy[i][j].rgbtGreen;
            image[i][j].rgbtBlue = copy[i][j].rgbtBlue;
        }
    }

    return;
}
