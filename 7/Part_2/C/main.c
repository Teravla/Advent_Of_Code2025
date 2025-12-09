#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ROWS 10000 // maximum rows in the input
#define MAX_COLS 10000 // maximum columns in the input

// Load the grid from a file
int load_grid(const char *filename, char ***grid, int *rows, int *cols)
{
    FILE *file = fopen(filename, "r");
    if (!file)
    {
        perror("Failed to open file");
        return 0;
    }

    char line[MAX_COLS];
    *rows = 0;
    *cols = 0;

    // Allocate temporary array of pointers
    *grid = malloc(MAX_ROWS * sizeof(char *));
    if (!*grid)
    {
        perror("malloc failed");
        fclose(file);
        return 0;
    }

    while (fgets(line, sizeof(line), file))
    {
        size_t len = strlen(line);
        if (len > 0 && line[len - 1] == '\n')
        {
            line[len - 1] = '\0';
            len--;
        }
        (*grid)[*rows] = malloc(len * sizeof(char));
        memcpy((*grid)[*rows], line, len);
        if ((int)len > *cols)
            *cols = (int)len;
        (*rows)++;
    }

    fclose(file);
    return 1;
}

void free_grid(char **grid, int rows)
{
    for (int i = 0; i < rows; i++)
        free(grid[i]);
    free(grid);
}

// Find start 'S'
void find_start(char **grid, int rows, int cols, int *start_r, int *start_c)
{
    for (int r = 0; r < rows; r++)
    {
        for (int c = 0; c < cols; c++)
        {
            if (grid[r][c] == 'S')
            {
                *start_r = r;
                *start_c = c;
                return;
            }
        }
    }
    fprintf(stderr, "Start 'S' not found\n");
    exit(EXIT_FAILURE);
}

// Count timelines using dynamic programming
unsigned long long count_timelines(char **grid, int rows, int cols)
{
    // Allocate dp array on heap
    unsigned long long **dp = malloc(rows * sizeof(unsigned long long *));
    for (int r = 0; r < rows; r++)
    {
        dp[r] = calloc(cols, sizeof(unsigned long long));
    }

    int start_r, start_c;
    find_start(grid, rows, cols, &start_r, &start_c);
    if (start_r + 1 < rows)
        dp[start_r + 1][start_c] = 1;

    for (int r = start_r + 1; r < rows; r++)
    {
        for (int c = 0; c < cols; c++)
        {
            unsigned long long count = dp[r][c];
            if (count == 0)
                continue;
            char cell = grid[r][c];

            if (cell == '.')
            {
                if (r + 1 < rows)
                    dp[r + 1][c] += count;
            }
            else if (cell == '^')
            {
                if (r + 1 < rows)
                {
                    if (c - 1 >= 0)
                        dp[r + 1][c - 1] += count;
                    if (c + 1 < cols)
                        dp[r + 1][c + 1] += count;
                }
            }
        }
    }

    unsigned long long total = 0;
    for (int c = 0; c < cols; c++)
        total += dp[rows - 1][c];

    // Free dp
    for (int r = 0; r < rows; r++)
        free(dp[r]);
    free(dp);

    return total;
}

int main()
{
    char **grid;
    int rows, cols;
    const char *filename = "../../resources.txt";

    if (!load_grid(filename, &grid, &rows, &cols))
        return EXIT_FAILURE;

    unsigned long long total = count_timelines(grid, rows, cols);
    printf("Total timelines: %llu\n", total);

    free_grid(grid, rows);
    return 0;
}
