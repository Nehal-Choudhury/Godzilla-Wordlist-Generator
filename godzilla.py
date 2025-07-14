#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import itertools
import sys
from datetime import datetime

def get_charset(charset_name):
    """Returns a character set based on the provided name."""
    charsets = {
        'numeric': '0123456789',
        'alpha': 'abcdefghijklmnopqrstuvwxyz',
        'alpha-upper': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'alpha-mixed': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'alphanum': 'abcdefghijklmnopqrstuvwxyz0123456789',
        'alphanum-upper': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
        'alphanum-mixed': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
    }
    return charsets.get(charset_name, None)

def generate_wordlist(min_len, max_len, charset, pattern=None, output_file=None):
    """Generates and writes the wordlist to a file or stdout."""
    start_time = datetime.now()
    count = 0
    
    # Determine the output stream
    if output_file:
        try:
            outfile = open(output_file, 'w', encoding='utf-8')
        except IOError as e:
            print(f"Error: Could not open file {output_file} for writing.")
            print(f"Reason: {e}")
            sys.exit(1)
    else:
        outfile = sys.stdout

    print(f"[*] Starting Godzilla at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[*] Charset: {charset}")
    print(f"[*] Min length: {min_len}, Max length: {max_len}")
    if pattern:
        print(f"[*] Using pattern: {pattern}")
    if output_file:
        print(f"[*] Outputting to: {output_file}")
    print("-" * 30)

    try:
        # Iterate through the specified length range
        for length in range(min_len, max_len + 1):
            # If a pattern is provided, we only generate for the pattern's length
            if pattern and len(pattern) != length:
                continue

            # Use itertools.product to get the cartesian product of the charset
            # This is highly memory-efficient as it generates iterators
            for item in itertools.product(charset, repeat=length):
                word = "".join(item)
                
                # If a pattern is specified, check if the word matches
                if pattern:
                    match = True
                    for i, char in enumerate(pattern):
                        # '@' matches lowercase alpha
                        if char == '@' and word[i] not in get_charset('alpha'):
                            match = False
                            break
                        # ',' matches numeric
                        elif char == ',' and word[i] not in get_charset('numeric'):
                            match = False
                            break
                        # '%' matches uppercase alpha
                        elif char == '%' and word[i] not in get_charset('alpha-upper'):
                            match = False
                            break
                        # '^' is a placeholder for any char from the main charset
                        elif char == '^':
                            continue
                        # Exact character match
                        elif char != word[i]:
                            match = False
                            break
                    if not match:
                        continue

                outfile.write(word + '\n')
                count += 1
                # Flush buffer periodically to see progress in the file
                if count % 100000 == 0:
                    outfile.flush()

    except KeyboardInterrupt:
        print("\n[!] Process interrupted by user.")
    finally:
        end_time = datetime.now()
        print("-" * 30)
        print(f"[*] Wordlist generation finished at {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"[*] Total words generated: {count}")
        print(f"[*] Total duration: {end_time - start_time}")
        if output_file:
            outfile.close()
            print(f"[*] Wordlist saved to {output_file}")

def main():
    """Main function to parse arguments and initiate generation."""
    parser = argparse.ArgumentParser(
        description="Godzilla: A flexible wordlist generator similar to crunch.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  1. Generate a numeric wordlist of length 4 and print to screen:
     %(prog)s 4 4 -c numeric

  2. Generate a mixed-case alphanumeric wordlist from 3 to 5 chars and save to a file:
     %(prog)s 3 5 -c alphanum-mixed -o words.txt

  3. Generate a wordlist using a custom character set:
     %(prog)s 2 2 -s "abc123" -o custom.txt
     
  4. Generate words matching a pattern (e.g., 'Pass' followed by 4 numbers):
     %(prog)s 8 8 -s "Pass0123456789" -p "Pass,,,," -o patterned.txt
     Note: The main charset must contain all characters used in the pattern.
"""
    )
    
    # Positional arguments for min and max length
    parser.add_argument('min', type=int, help='Minimum length of the words.')
    parser.add_argument('max', type=int, help='Maximum length of the words.')
    
    # Group for mutually exclusive charset options
    charset_group = parser.add_mutually_exclusive_group(required=True)
    charset_group.add_argument(
        '-c', '--charset', 
        choices=['numeric', 'alpha', 'alpha-upper', 'alpha-mixed', 'alphanum', 'alphanum-upper', 'alphanum-mixed'],
        help="""Use a predefined character set:
  - numeric: 0123456789
  - alpha: abcdefghijklmnopqrstuvwxyz
  - alpha-upper: ABCDEFGHIJKLMNOPQRSTUVWXYZ
  - alpha-mixed: Both lower and upper case letters
  - alphanum: Lowercase letters and numbers
  - alphanum-upper: Uppercase letters and numbers
  - alphanum-mixed: All letters and numbers"""
    )
    charset_group.add_argument('-s', '--string', help='Use a custom character set from the provided string.')

    # Optional arguments
    parser.add_argument('-p', '--pattern', help="""Define a pattern for the output.
Placeholders:
  @ = lowercase letters
  , = numbers
  %% = uppercase letters
  ^ = any character from the main charset""")
    parser.add_argument('-o', '--output', help='Output file to save the wordlist.')

    args = parser.parse_args()

    if args.min > args.max:
        print("Error: Minimum length cannot be greater than maximum length.")
        sys.exit(1)

    final_charset = ""
    if args.charset:
        final_charset = get_charset(args.charset)
    elif args.string:
        final_charset = "".join(sorted(set(args.string))) # Remove duplicates and sort

    if not final_charset:
        print("Error: A valid charset must be specified.")
        sys.exit(1)
        
    if args.pattern and len(args.pattern) not in range(args.min, args.max + 1):
        print("Error: Pattern length must be within the min/max range.")
        print("Adjusting min/max to match pattern length for this run.")
        args.min = len(args.pattern)
        args.max = len(args.pattern)

    generate_wordlist(args.min, args.max, final_charset, args.pattern, args.output)

if __name__ == '__main__':
    main()