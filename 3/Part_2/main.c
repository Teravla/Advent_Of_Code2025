#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * Program Description:
 * -------------------
 * This program reads a text file named "input.txt", where each line contains
 * a sequence of digits representing a battery bank. For each line, the program
 * selects exactly K digits to form the largest possible number (joltage) while
 * preserving the order of digits.
 *
 * The program accumulates the largest numbers from all lines to compute a
 * total output joltage. Lines with fewer than K digits are taken as-is.
 *
 * Key Points:
 * - Uses a greedy algorithm (monotone stack approach) to select K digits.
 * - Preserves the original order of digits.
 * - Handles lines shorter than K digits gracefully.
 */

#define K 12         // Number of digits to select for each battery bank
#define MAX_LINE 256 // Maximum length of a line in the input file

int main(void)
{
    const char *filename = "input.txt"; // Input file containing battery sequences

    // Open the input file for reading
    FILE *f = fopen(filename, "r");
    if (!f)
    {
        perror("Error opening input.txt"); // Print an error message if the file cannot be opened
        return 1;                          // Exit with error code
    }

    char line[MAX_LINE];          // Buffer to hold each line from the file
    unsigned long long total = 0; // Accumulator for the total output joltage

    // Read the file line by line
    while (fgets(line, sizeof(line), f))
    {
        // Remove newline or carriage return characters at the end of the line
        line[strcspn(line, "\r\n")] = 0;

        int len = strlen(line); // Length of the current line

        // If the line has K or fewer digits, convert the entire line to a number
        if (len <= K)
        {
            total += strtoull(line, NULL, 10);
            continue;
        }

        // Array to store the selected K digits forming the largest joltage
        char result[K + 1]; // +1 for the null terminator
        int res_index = 0;  // Current index in the result array

        // Iterate through each digit of the input line
        for (int i = 0; i < len; i++)
        {
            // Skip non-digit characters (optional safety check)
            if (line[i] < '0' || line[i] > '9')
                continue;

            // While the last digit in the result is smaller than the current digit
            // and there are enough remaining digits to reach K, remove the last digit
            while (res_index > 0 &&
                   result[res_index - 1] < line[i] &&
                   (len - i - 1 + res_index) >= K)
            {
                res_index--; // Remove smaller digit to allow larger digits in result
            }

            // If there is still space in the result array, add the current digit
            if (res_index < K)
            {
                result[res_index++] = line[i];
            }
        }

        result[K] = '\0';                    // Null-terminate the result string
        total += strtoull(result, NULL, 10); // Convert result to number and add to total
    }

    fclose(f); // Close the input file

    // Print the final total output joltage
    printf("%llu\n", total);

    return 0; // Exit successfully
}
