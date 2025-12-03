#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    const char *filename = "input.txt";
    FILE *f = fopen(filename, "r");
    if (!f)
    {
        perror("Erreur d'ouverture du fichier input.txt");
        return 1;
    }

    char line[4096]; // lignes longues
    long long total = 0;
    int line_number = 0;

    while (fgets(line, sizeof(line), f))
    {
        line_number++;
        int max_joltage = -1;
        int len = strlen(line);

        for (int i = 0; i < len; i++)
        {
            if (line[i] < '0' || line[i] > '9') continue;
            int a = line[i] - '0';

            for (int j = i + 1; j < len; j++)
            {
                if (line[j] < '0' || line[j] > '9') continue;
                int b = line[j] - '0';
                int val = a * 10 + b;

                if (val > max_joltage)
                    max_joltage = val;
            }
        }

        if (max_joltage >= 0)
        {
            total += max_joltage;
            printf("Ligne %d : max joltage = %d\n", line_number, max_joltage);
        }
        else
        {
            printf("Ligne %d : pas de chiffres valides\n", line_number);
        }
    }

    fclose(f);
    printf("Total output joltage = %lld\n", total);
    return 0;
}
