#!/bin/bash

# Define the target folder where files will be copied
TARGET_FOLDER="$HOME/ws/simple_rag_system/documents_db/raw"

# Find and copy all files with specified extensions
find "$HOME" -type f \( -iname "*.pdf" -o -iname "*.docx" \) -exec cp {} "$TARGET_FOLDER" \;

echo "Files copied to $TARGET_FOLDER"
