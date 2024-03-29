from setuptools import setup, find_packages

setup(
    name="algorithmic-trading-framework",
    description="tool for managing, training, and deploying machine learning models for trading",
    version="0.1.0",

    url="https://github.com/lpiekarski/algo-trading-lp",
    author="Łukasz Piekarski",
    author_email="lukasz.piekarski.001@gmail.com",

    packages=find_packages(),
    py_modules=[
        "atf"
    ],
    scripts=[
        "atf"
    ],
    dependency_links=[
        "https://download.pytorch.org/whl/cu117"
    ],
    install_requires=[
        "clearml==1.8.3",
        "pandas==1.5.2",
        "numpy==1.24.1",
        "python-dateutil==2.8.2",
        "click==8.1.3",
        "tqdm==4.64.1",
        "bokeh==2.4.3",
        "Backtesting==0.3.3",
        "scikit-learn==1.2.0",
        "pytest==7.2.0",
        "torch==1.13.1",
        "lightgbm==3.3.3",
        "yfinance==0.2.3",
        "pandas-ta==0.3.14b0",
        "split-file-reader==0.1.0",
        "autopep8==2.0.1",
        "pytest-cov==4.0.0",
        "PyYAML==6.0",
        "tweepy==4.12.1",
        "sortedcontainers==2.4.0",
        "nltk==3.8.1"
    ]
)