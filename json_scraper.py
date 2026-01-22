#!/usr/bin/env python3
#
# Json_Scraper version 0.1 (12.28.2025)
# A simple script to scrape specified fields from a JSON file.
# Written by Andrew Cecil (@atcecil01)
# https://github.com/atcecil01/json-scraper

import ijson
import argparse

def scrape_json():
    parser = argparse.ArgumentParser(description="Scrape JSON fields from a file.")
    parser.add_argument("--sourcePath", "-s", type=str, help="Path to the JSON file")
    parser.add_argument("--fieldName", "-f", type=str, help="Name of the field to scrape")
    parser.add_argument("--outputPath", "-o", type=str, help="Path to the output file")

    args = parser.parse_args()
    sourcePath = args.sourcePath
    fieldName = args.fieldName
    outputPath = args.outputPath
    values = []

    print() # Initial newline for better console formatting
    print("---------------------------------")
    print("-------JSON Field Scraper--------")
    print("---------------------------------")
    if not sourcePath or not fieldName:
        print("Source path or field name not specified. Exiting...")
        print() # Final newline for better console formatting
        return
    print("Scraping in progress...")


    try:
        with open(sourcePath, "r", encoding="utf-8") as f:
            # Use streaming parser for memory efficiency with large files
            # Parse all events and look for matching field names at any depth
            for prefix, event, value in ijson.parse(f):
                # Match when we encounter a key that matches fieldName (case-insensitive)
                if event == "map_key" and value.lower() == fieldName.lower():
                    # Skip to find the value for this key
                    continue
                # Check if this value belongs to a matching key by examining the prefix
                # Prefix format: "item.key" or "item.0.key" etc
                key_parts = prefix.split(".")
                if key_parts and key_parts[-1].lower() == fieldName.lower():
                    # This is a value for a matching key
                    if value not in values:
                        values.append(value)
    except FileNotFoundError as e:
        print(f"Error reading JSON file: {e}")
        print("Exiting...")
        print() # Final newline for better console formatting
        return
    except (ijson.JSONError, ijson.IncompleteJSONError) as e:
        print(f"Error parsing JSON file: {e}")
        print("Exiting...")
        print() # Final newline for better console formatting
        return

    print(f"{values.__len__()} values scraped.")
    
    if not outputPath:
        print("Output path not specified. Writing to console.")
        print() # Newline
        print(f"Values for '{fieldName}':")
        print("---------------------------------")
        for value in values:
            print(value)
    else:
        if not outputPath.endswith(".txt"):
            outputPath += ".txt"
        with open(outputPath, "w", encoding="utf-8") as outFile:
            for value in values:
                outFile.write(f"{value}\n")
        print(f"Scraped values written to {outputPath}")

    print() # Final newline for better console formatting

if __name__ == "__main__":
    scrape_json()