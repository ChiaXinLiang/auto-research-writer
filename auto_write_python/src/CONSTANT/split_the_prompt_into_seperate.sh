#!/bin/bash

# Define the source file and output directory
SOURCE_FILE="PROMPT.py"
OUTPUT_DIR="PROMPTS"

# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Function to extract and save a prompt
extract_prompt() {
    local prompt_name="$1"
    local start_pattern="$2"
    local end_pattern="$3"
    local output_file="$OUTPUT_DIR/${prompt_name}.py"

    sed -n "/$start_pattern/,/$end_pattern/p" "$SOURCE_FILE" > "$output_file"
    echo "Extracted $prompt_name to $output_file"
}

# Extract each prompt
extract_prompt "CRITERIA_BASED_JUDGING_PROMPT" "CRITERIA_BASED_JUDGING_PROMPT.*=" "'''"
extract_prompt "NLI_PROMPT" "NLI_PROMPT.*=" "'''"
extract_prompt "ROUGH_OUTLINE_PROMPT" "ROUGH_OUTLINE_PROMPT.*=" "'''"
extract_prompt "MERGING_OUTLINE_PROMPT" "MERGING_OUTLINE_PROMPT.*=" "'''"
extract_prompt "SUBSECTION_OUTLINE_PROMPT" "SUBSECTION_OUTLINE_PROMPT.*=" "'''"
extract_prompt "EDIT_FINAL_OUTLINE_PROMPT" "EDIT_FINAL_OUTLINE_PROMPT.*=" "'''"
extract_prompt "CHECK_CITATION_PROMPT" "CHECK_CITATION_PROMPT.*=" "'''"
extract_prompt "SUBSECTION_WRITING_PROMPT" "SUBSECTION_WRITING_PROMPT.*=" "'''"
extract_prompt "LCE_PROMPT" "LCE_PROMPT.*=" "'''"

echo "All prompts have been extracted and saved in the $OUTPUT_DIR directory."
