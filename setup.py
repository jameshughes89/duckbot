import os
import subprocess

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install


def run_code_formatters():
    for tool in ["isort .", "black .", "mdformat .", "flake8 duckbot tests *.py", "mdformat --check duckbot tests wiki *.md"]:
        print(f"running `{tool}`")
        subprocess.run(tool, shell=True)


def download_nltk_data():
    import nltk
    import textblob.download_corpora

    venv = os.getenv("VIRTUAL_ENV")
    base = venv if venv else os.getenv("HOME")
    download_dir = os.path.join(base, "nltk_data")
    original_download = nltk.download
    nltk.download = lambda x: original_download(x, download_dir=download_dir)
    nltk.download("cmudict")
    textblob.download_corpora.main()


class PostDevelop(develop):
    def run(self):
        develop.run(self)
        self.execute(download_nltk_data, [], msg="Download NLTK Data")


class PostInstall(install):
    def run(self):
        install.run(self)
        self.execute(download_nltk_data, [], msg="Download NLTK Data")


if __name__ == "__main__":
    setup(
        name="duckbot",
        version="1.0",
        url="https://github.com/duck-dynasty/duckbot",
        python_requires=">=3.10",
        packages=find_packages(),
        cmdclass={"develop": PostDevelop, "install": PostInstall},
        install_requires=[
            "discord.py[voice]==2.5.0",
            "beautifulsoup4==4.13.3",
            "requests==2.32.3",
            "pytz==2025.1",
            "timezonefinder==6.5.8",
            "holidays==0.67",
            "pyowm==3.3.0",  # openweather
            "psycopg2==2.9.10",
            "SQLAlchemy==2.0.37",
            "d20==1.1.2",
            "nltk==3.9.1",  # also in pyproject.toml, required for setup script above
            "textblob==0.19.0",  # also in pyproject.toml, required for setup script above
            "pyfiglet==1.0.2",
            "matplotlib==3.10.1",
            "PyGithub==2.1.1",
            "wolframalpha==5.1.3",
            "yfinance==0.2.52",
            "mip==1.15.0",
            "anthropic==0.45.2",  # sdk for llm
        ],
        extras_require={
            "dev": [
                "pytest==8.3.4",
                "pytest-asyncio==0.25.3",
                "pytest-xdist[psutil]==3.6.1",
                "flake8==7.1.2",
                "black==25.1.0",
                "flake8-black==0.3.6",
                "isort==6.0.0",
                "flake8-isort==6.1.2",
                "pep8-naming==0.14.1",
                "mdformat==0.7.22",
                "mdformat-gfm==0.4.1",
                "mdformat-black==0.1.1",
                "responses==0.25.6",
                "pytest-blockage==0.2.4",
                "pytest-sugar==1.0.0",
                "pytest-icdiff==0.9",
                "pytest-cov==6.0.0",
            ],
            "cdk": [
                "aws-cdk.core==1.204.0",
                "aws-cdk.aws-ec2==1.204.0",
                "aws-cdk.aws-ecs==1.204.0",
                "aws-cdk.aws-autoscaling==1.204.0",
                "aws-cdk.aws-efs==1.204.0",
                "aws-cdk.aws-iam==1.204.0",
                "aws-cdk.aws-logs==1.204.0",
                "aws-cdk.aws-ssm==1.204.0",
                "boto3==1.37.4",
            ],
        },
        entry_points={
            "console_scripts": [
                f"format = setup:{run_code_formatters.__name__} [dev]",
            ]
        },
    )
