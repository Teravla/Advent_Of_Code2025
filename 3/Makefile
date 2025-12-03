CC = gcc
CFLAGS = -Wall -Wextra -O2

# Cibles
all: Part_1/part1 Part_2/part2

# Partie 1
Part_1/part1: Part_1/main.c
	$(CC) $(CFLAGS) $< -o $@

# Partie 2
Part_2/part2: Part_2/main.c
	$(CC) $(CFLAGS) $< -o $@

# Règles pour exécuter
run1: Part_1/part1
	cd Part_1 && ./part1

run2: Part_2/part2
	cd Part_2 && ./part2

# Nettoyage
clean:
	rm -f Part_1/part1 Part_2/part2

.PHONY: all run1 run2 clean
