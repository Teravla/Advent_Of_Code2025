#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * Program description:
 * -------------------
 * This program reads a text file named "input.txt", where each line contains
 * a sequence of digits and possibly other characters.
 *
 * For each line, it identifies the largest two-digit number that can be
 * formed by any two digits in the line (digits do not need to be consecutive).
 *
 * It accumulates the maximum numbers from all lines to compute a total output joltage.
 *
 * The program prints the maximum joltage for each line and the final total.
 */

int main(void)
{
    // Input file name
    const char *filename = "input.txt";

    // Open the input file for reading
    FILE *f = fopen(filename, "r");
    if (!f)
    {
        perror("Error opening input.txt"); // Print an error message if the file cannot be opened
        return 1;                          // Exit with error code
    }

    char line[4096];     // Buffer to hold each line; large enough for long lines
    long long total = 0; // Accumulator for the total joltage
    int line_number = 0; // Line counter for reporting

    // Read the file line by line
    while (fgets(line, sizeof(line), f))
    {
        line_number++;          // Increment line number
        int max_joltage = -1;   // Initialize maximum joltage for this line
        int len = strlen(line); // Get the length of the current line

        // Iterate through all characters to find the first digit
        for (int i = 0; i < len; i++)
        {
            // Skip non-digit characters
            if (line[i] < '0' || line[i] > '9')
                continue;

            int a = line[i] - '0'; // Convert character to integer

            // Iterate through subsequent characters to form a two-digit number
            for (int j = i + 1; j < len; j++)
            {
                // Skip non-digit characters
                if (line[j] < '0' || line[j] > '9')
                    continue;

                int b = line[j] - '0'; // Convert character to integer
                int val = a * 10 + b;  // Form two-digit number

                if (val > max_joltage) // Update maximum if this number is larger
                    max_joltage = val;
            }
        }

        // Check if a valid maximum was found for this line
        if (max_joltage >= 0)
        {
            total += max_joltage; // Add to total output joltage
            printf("Line %d: max joltage = %d\n", line_number, max_joltage);
        }
        else
        {
            printf("Line %d: no valid digits found\n", line_number);
        }
    }

    // Close the input file
    fclose(f);

    // Print the final total output joltage
    printf("Total output joltage = %lld\n", total);

    return 0; // Exit successfully
}
