# Currency Converter

Thanks to [itsMalb](https://github.com/itsMalb) for the original idea.

Convert monetary values between currencies with up-to-date exchange rates.

## Requirements

### Python File

- [Python 3.9](https://www.python.org/downloads/) or higher
- Packages listed in [`requirements.txt`](requirements.txt)

### Windows Systems

Optional executable file for Windows users. Python and the required packages are included in the executable.

- 10 MB of free space for the executable
- 12 MB of free space for temporary files

## Usage

Download the source code, or optionally the executable if you're on Windows, from the [latest release](https://github.com/lemonyte/currency-converter/releases/latest).

Select an input currency and an output currency, then click the "Convert" button. The currency converter will request exchange rates for the input currency, and save the exchange rates to a file `rates.json`. This file allows for caching and later offline use. Saved exchange rates are updated if they are older than 24 hours. You may delete the `rates.json` file if you wish, the program will just download the exchange rates again next time it is used.

## License

[MIT License](license.txt)
