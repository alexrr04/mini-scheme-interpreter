# Makefile for ANTLR grammar

ANTLR=antlr4
GRAMMAR=scheme.g4
OUTPUT_DIR=generated
GENERATED_FILES=$(OUTPUT_DIR)/schemeLexer.py $(OUTPUT_DIR)/schemeParser.py $(OUTPUT_DIR)/schemeVisitor.py

.PHONY: all clean

all: $(GENERATED_FILES)

# Rule to generate the files only if the grammar changes
$(GENERATED_FILES): $(GRAMMAR) | $(OUTPUT_DIR)
	$(ANTLR) -Dlanguage=Python3 -no-listener -visitor -o $(OUTPUT_DIR) $(GRAMMAR)

# Ensure the output directory exists
$(OUTPUT_DIR):
	mkdir -p $(OUTPUT_DIR)

clean:
	rm -rf $(OUTPUT_DIR)
