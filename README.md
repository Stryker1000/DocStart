# DocStart

A small work in progress repository that can spit out a quickstart page when given the documentation of a library, language, or repository using AI. 

## Installation
Because this package is still in very early beta it's not able to be downloaded directly from application installation tools. Currently the best way to install DocStart is by following the steps below:\
1. Install Pipx, you can follow the instructions in [this](https://pipx.pypa.io/stable/installation/) link
2. Download this repository and unzip it
3. Navigate to the unzipped folder in the command prompt or terminal
4. Run the command `pipx install .`
   
## Usage
An [OpenAI api key](https://platform.openai.com/api-keys) is necessary to run this program. Once you have the api key you can enter it as an environment variable.\
This package uses the command line. Once it is installed there are two commands that can be used, summarizefiledocs, and summarizesitedocs. 

### Summarize Documentation Files
summarizefiledocs takes an api key and a file path as arguments. The file path should link to the top level folder of the documentation you wish to summarize.\
Example:
`summarizefiledocs OPENAI_API_KEY C:/path/to/documentation`

### Summarize Documentation Site
summarizesitedocs takes an api key and a url as arguments. The url should link to the home page of a documentation site. An example would be [https://docs.python.org/3/](https://docs.python.org/3/).\
Example:
`summarizesitedocs OPENAI_API_KEY https://docs.python.org/3/`

## To-Do
- ~~Add ability to run the script as a command in the command line~~
- Increase focus on important parts of docs
- Increase amount of documentation pages it will read efficiently
- ~~Add ability to read from files~~
