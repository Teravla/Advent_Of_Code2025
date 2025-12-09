# Makefile for Tachyon DP

CC = gcc
CFLAGS = -O2 -Wall -std=c11
TARGET = main
SRC = main.c
BIN_DIR = bin

# Default: build the executable
all: $(BIN_DIR)/$(TARGET)

# Build the target in bin/
$(BIN_DIR)/$(TARGET): $(SRC) | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $(SRC)

# Ensure bin directory exists
$(BIN_DIR):
	mkdir -p $(BIN_DIR)

# Remove the executable
clean:
	rm -rf $(BIN_DIR)/$(TARGET)

# Build and run
run: $(BIN_DIR)/$(TARGET)
	./$(BIN_DIR)/$(TARGET)

time: $(BIN_DIR)/$(TARGET)
	/usr/bin/time -v ./$(BIN_DIR)/$(TARGET)