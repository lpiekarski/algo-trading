# Algorithmic Trading Framework
The Algorithmic Trading Framework is a project that provides a set of tools for training and testing machine learning models for algorithmic trading. The Project includes a command-line interface that allows users to manage datasets, train models, and test them on historical data. In order to use the Framework, users must have Python 3.10 or later and Git installed on their system. The project uses environment variables to specify the location of data repositories and other settings, making it easy to customize the behavior of the framework. Overall, the Algorithmic Trading Framework offers a convenient and powerful set of tools for exploring and experimenting with algorithmic trading strategies.

## Installation
### Prerequisites
To use the framework, users must have Python 3.10 and git installed on their system.

#### Steps On Ubuntu
1. Clone the repository
   ```bash
   git clone https://github.com/lpiekarski/algo-trading.git
   cd algo-trading
   ```
2. Create python virtual environment
   ```bash
   python3 -m venv venv --upgrade-deps
   ```
3. Activate the environment
   ```bash
   . ./venv/bin/activate
   ```
4. Install required python dependencies
   ```bash
   pip install .
   ```
a#### Setting Up Environment After Installation
There are a few environmental variables that are expected to be set by some parts of the framework:

`GIT_DRIVE_REPO_URL` - URL of the git repository that is being used as a data source for git drive

`DRIVE` - Default drive type. Can be `local` or `git` (Each file in `core/drive` not starting with `__` corresponds to a drive type) 

1. they can be set in the file ".atf" in your user/username/ path 
2. they can be set by cli with "-D" before using a command e.g. "atf -Dname=value subcommand"
3. They can be set by "atf set name value" - it saves 
3.5 it can be unset by atf unset name 


# env module 
basically env module serves the purpose of loading the environmental variables either fqrom files or options passed in the command 

1. po prostu odpalenie ze srodowiskiem z ta zmienna
2. ustawienie na stale wartosci poprzez "atf set nazwa wartosc"
3. przez argument w cli np "atf -Dnazwa=wartosc subkomenda ... "

4. przez plik ze zmiennymi w formacie nazwa=wartosc w osobnych liniach i potem w cli "atf -E sciezka/do/pliku.env subkomenda ..."

w examples sa takie przykladowe pliki
