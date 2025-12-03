#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Number of digits to select for each battery bank
#define K 12

// Maximum line length to read from the input file
#define MAX_LINE 256

int main(void)
{
    // The name of the input file containing the battery sequences
    const char *filename = "input.txt";

    // Open the file for reading
    FILE *f = fopen(filename, "r");
    if (!f)
    {
        perror("Error opening input.txt"); // Print an error if the file cannot be opened
        return 1;                          // Exit with error code
    }

    char line[MAX_LINE];          // Buffer to hold each line from the file
    unsigned long long total = 0; // Variable to accumulate the total joltage

    // Read the file line by line
    while (fgets(line, sizeof(line), f))
    {
        // Remove any newline characters at the end of the line
        line[strcspn(line, "\r\n")] = 0;

        int len = strlen(line); // Length of the current line

        if (len <= K)
        {
            // If the line has K or fewer digits, we just take all of them
            total += strtoull(line, NULL, 10);
            continue; // Move to the next line
        }

        // Array to store the selected K digits forming the largest joltage
        char result[K + 1]; // +1 for the null terminator
        int res_index = 0;  // Current index in the result array

        // Iterate through each digit of the input line
        for (int i = 0; i < len; i++)
        {
            // While the last digit in the result is smaller than the current digit
            // and there are enough remaining digits to reach K, remove it
            while (res_index > 0 &&
                   result[res_index - 1] < line[i] &&
                   (len - i - 1 + res_index) >= K)
            {
                res_index--; // Remove the smaller digit to make room for a bigger one
            }

            // If we still have space in the result array, add the current digit
            if (res_index < K)
            {
                result[res_index++] = line[i];
            }
        }

        result[K] = '\0';                    // Null-terminate the string
        total += strtoull(result, NULL, 10); // Convert to number and add to total
    }

    // Close the input file
    fclose(f);

    // Print the final total joltage
    printf("%llu\n", total);

    return 0; // Exit successfully
}
