# Makefile for ANTLR grammar

ANTLR=antlr4
GRAMMAR=scheme.g4
OUTPUT_DIR=src/generated
GENERATED_FILES=$(OUTPUT_DIR)/schemeLexer.py $(OUTPUT_DIR)/schemeParser.py $(OUTPUT_DIR)/schemeVisitor.py
INIT_FILE=$(OUTPUT_DIR)/__init__.py
MAKEFILE=Makefile

.PHONY: all clean

all: $(GENERATED_FILES) $(INIT_FILE) $(MAKEFILE)

# Rule to generate the files only if the grammar changes
$(GENERATED_FILES): $(GRAMMAR) | $(OUTPUT_DIR)
	$(ANTLR) -Dlanguage=Python3 -no-listener -visitor -o $(OUTPUT_DIR) $(GRAMMAR)

# Rule to generate the __init__.py file
$(INIT_FILE): $(GENERATED_FILES)
	echo '"""\nInitialization for the src.generated package.\nGenerated files for the Scheme interpreter.\n"""' > $(INIT_FILE)

# Ensure the output directory exists
$(OUTPUT_DIR):
	mkdir -p $(OUTPUT_DIR)

clean:
	rm -rf $(OUTPUT_DIR)
