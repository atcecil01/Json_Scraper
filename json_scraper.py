#!/usr/bin/env python3
#
# Json_Scraper version 0.1 (12.28.2025)
# A simple script to scrape specified fields from a JSON file.
# Written by Andrew Cecil (@atcecil01)
# https://github.com/atcecil01/json-scraper

import json
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
            content = json.load(f)
    except FileNotFoundError as e:
        print(f"Error reading JSON file: {e}")
        print("Exiting...")
        print() # Final newline for better console formatting
        return

    def extract_values(obj, key):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k.lower() == key and v not in values:
                    values.append(v)
                extract_values(v, key)
        elif isinstance(obj, list):
            for item in obj:
                extract_values(item, key)

    extract_values(content, fieldName)

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