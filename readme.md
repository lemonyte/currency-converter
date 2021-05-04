# Currency Converter
By [LemonPi314](https://github.com/LemonPi314)

Convert monetary values between currencies with up-to-date conversion rates.
## Requirements
### Python File
Any operating system with Python.
- [Python 3.9](https://www.python.org/downloads/release/python-394/) or higher
- [`PySimpleGUI`](https://pypi.org/project/pysimplegui)
### Windows Systems
Optional executable file for Windows users.
Python and the required packages are included in the executable.
- 30 MB of free space for the executable
- 70 MB of free space for temporary files
## Usage
Select an input currency and an output currency, then click the "Convert" button. The currency converter will request conversion rates for the input currency, and save the conversion rates to a file `rates.json`. This file allows for caching and later offline use. Saved rates are updated if they are older than 24 hours. You may delete the `rates.json` file if you wish, the program will just download the conversion rates again next time it is used.
## License
[MIT License](https://choosealicense.com/licenses/mit/)