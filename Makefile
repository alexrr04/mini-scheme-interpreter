# Makefile for ANTLR grammar

ANTLR=antlr4
GRAMMAR=scheme.g4
OUTPUT_DIR=generated

.PHONY: all clean

all: $(OUTPUT_DIR)
	$(ANTLR) -Dlanguage=Python3 -no-listener -visitor -o $(OUTPUT_DIR) $(GRAMMAR)

$(OUTPUT_DIR):
	mkdir -p $(OUTPUT_DIR)

clean:
	rm -rf $(OUTPUT_DIR)
