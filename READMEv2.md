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

`LOG_TYPE` - DEBUG or something 



1. they can be set in the file ".atf" in your user/username/ path 
2. they can be set by cli with "-D" before using a command e.g. "atf -Dname=value subcommand"
3. They can be set by "atf set name value" - it saves 
3.5 it can be unset by atf unset name 


it is saved in /User/[username]/.atf - you can save it also manually
atf -E --envfile[envfile (absolute?) filepath] - examples are in the folder examples

# env module 
basically env module serves the purpose of loading the environmental variables either fqrom files or options passed in the command 


# create new module 

module name /
- __init__.py
- function_name.py
- steps/
--- __init__.py
---function_step_name.py

# collector 

collector is a module that let you download data from the list of external sources and save it 
for now supported sources are 
twitter 
xtb
yfinance 

collector arguments are listed in ... atf collect --help 

https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases - pandas way of timeseries formats 

yfinance options [1m, 2m, 5m]
https://www.qmr.ai/wp-content/uploads/2022/08/image-23.png

Twitter requires TWITTER_BEARER_TOKEN set 


### Downloading Datasets from Drive
1. Download a file from drive using command below (you can also run `atf.py copy --help` to see additional options)
    ```bash
    python -m atf copy git:datasets/train/M30_H1 M30_H1.zip 
    ```
    Data files are in different branches of datasets repository. The list is available at https://github.com/S-P-2137/data

   - requires env var: GIT_DRIVE_REPO_URL=https://github.com/S-P-2137???
   - it also requires to be logged in [github](
   https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git?platform=linux)