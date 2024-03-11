# JD Librarian: Command Line Tool for Managing Johnny Decimal Libraries

JD Librarian is a Python-based command line tool designed for managing Johnny Decimal system libraries. The Johnny Decimal system is a method for organizing and retrieving information efficiently, using a simple numerical method to categorize and file items. This tool allows users to interact with their Johnny Decimal library through various commands, including searching, adding categories, and adding identifiers.

## Features

- **Environment Variable Support:** Set your Johnny Decimal library root with an environment variable (`JD_ROOT`) or via command line argument.
- **Dry Run Option:** Preview changes without affecting your actual library with the `--dry_run` flag.
- **Search Functionality:** Search through your Johnny Decimal library with customizable options to include categories and files in the search results.
- **Category and Identifier Management:** Easily add new categories and identifiers to your library to keep your information organized.

## Installation

1. Ensure Python 3.6 or later is installed on your system.
2. Download or clone this repository to your local machine.
3. Install required dependencies by running `pip install -r requirements.txt` (if applicable).

## Usage

### Setting Up Your Library

1. Set the `JD_ROOT` environment variable to the root directory of your Johnny Decimal library or use the `--jd_root` argument with the path to your library.

### Basic Commands

- **Search the Library:**

    ```bash
    python jd_librarian.py search "search term" [--include_category] [--include_files]
    ```
- **Add a New Category**
    ```
    python jd_librarian.py add_category <area_id> <new_category_name> [--dry_run]
    ```

- **Add a New Identifier**
    ```
    python jd_librarian.py add_id <category_id> <new_identifier_name> [--dry_run]
    ```

### Dry Run 
To preview changes without making any actual changes to the library, use the --dry_run option with any command.

### Extending the Tool
The script is designed to be easily extendable. Developers can add more functionalities by adding new subparsers and defining corresponding functions in the core module. Ensure new features align with the Johnny Decimal principles for consistency and usability.

### Contributing
Contributions to improve JD Librarian are welcome. Please submit pull requests or open an issue to suggest enhancements or report bugs.

### License
This project is licensed under the MIT License - see the LICENSE file for details.