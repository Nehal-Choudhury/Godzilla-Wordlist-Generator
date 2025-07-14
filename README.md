# Godzilla-Wordlist-Generator

Godzilla is a flexible, command-line wordlist generator written in Python 3. This script is designed to be a lightweight and cross-platform alternative to tools like `crunch`, allowing users to create custom wordlists based on character sets, length, and specific patterns.

It is designed to be efficient by using Python's `itertools` library, which generates passwords one by one in memory instead of storing them all before writing to a file.

## Features

-   Generate wordlists based on minimum and maximum length.
-   Use predefined character sets (numeric, alpha, alphanumeric, etc.).
-   Specify a custom character set.
-   Generate words that match a specific pattern.
-   Output directly to the console or save to a file.
-   Progress and summary reporting (start/end time, total words).

## Requirements

-   **Python 3.6+**

The script uses standard Python libraries, so no external packages are required. It should run on any system with a compatible Python interpreter, including Kali Linux, Ubuntu, macOS, and Windows.

## How to Use

1.  **Save the Script:** Save the code as a Python file (e.g., `godzilla.py`).

2.  **Make it Executable (Optional, for Linux/macOS):**
    Open your terminal and run the following command to make the script directly executable:
    ```sh
    chmod +x godzilla.py
    ```

3.  **Run the Script:**
    Execute the script from your terminal, providing the required arguments.

    If you made it executable:
    ```sh
    ./godzilla.py <min> <max> [options]
    ```

    If not, run it with `python3`:
    ```sh
    python3 godzilla.py <min> <max> [options]
    ```

### Arguments

-   `min` (Required): The minimum length of the words to generate.
-   `max` (Required): The maximum length of the words to generate.

### Options

-   `-c, --charset <name>`: Use a predefined character set. This is mutually exclusive with `-s`.
    -   `numeric`: `0123456789`
    -   `alpha`: `abcdefghijklmnopqrstuvwxyz`
    -   `alpha-upper`: `ABCDEFGHIJKLMNOPQRSTUVWXYZ`
    -   `alpha-mixed`: All lowercase and uppercase letters.
    -   `alphanum`: Lowercase letters and numbers.
    -   `alphanum-upper`: Uppercase letters and numbers.
    -   `alphanum-mixed`: All letters (lower and upper) and numbers.
-   `-s, --string <characters>`: Use a custom character set from the provided string.
-   `-p, --pattern <pattern>`: Generate words that match a specific pattern.
    -   `@`: Placeholder for lowercase letters.
    -   `,`: Placeholder for numbers.
    -   `%`: Placeholder for uppercase letters.
    -   `^`: Placeholder for any character from the main charset.
-   `-o, --output <filename>`: The file to save the wordlist to. If omitted, the output is printed to the console.

## Usage Examples

**1. Generate a 4-digit numeric PIN and print to screen:**
```sh
python3 godzilla.py 4 4 -c numeric
```

**2. Generate words from 6 to 8 characters using lowercase letters and numbers, and save to a file:**
```sh
python3 godzilla.py 6 8 -c alphanum -o wordlist.txt
```

**3. Generate 3-character words using a specific custom set of characters:**
```sh
python3 godzilla.py 3 3 -s "ab$12"
```

**4. Generate passwords that start with `user` followed by two numbers:**
The pattern length must be within the min/max range. The main charset (`-s`) must contain all characters used in the pattern.
```sh
python3 godzilla.py 6 6 -s "user0123456789" -p "user,," -o user_pins.txt
```
This will generate `user00`, `user01`, ..., `user99`.

**5. Generate passwords that start with an uppercase letter, followed by three lowercase letters, and end with a number:**
```sh
python3 godzilla.py 5 5 -c alphanum-mixed -p "%@@@," -o complex_pass.txt
```

## Author

* **[Nehal Choudhury]** 
