import os
import sys

from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from subprocess import check_call

# Package meta-data.
NAME = "dacon"
DESCRIPTION = 'A tool to collect data for Solidity smart contract for static analysis'
URL = "xxx"
AUTHOR = "isctae"
AUTHOR_MAIL = "isctae@gmail.com"
REQUIRES_PYTHON = ">=3.6.0"
here = os.path.abspath(os.path.dirname(__file__))

def get_requirements():
    """
    Return requirements as list.
    Handles cases where git links are used.

    """
    with open(os.path.join(here, "requirements.txt")) as f:
        packages = []
        for line in f:
            line = line.strip()
            # let's also ignore empty lines and comments
            if not line or line.startswith("#"):
                continue
            if "https://" not in line:
                packages.append(line)
                continue

            rest, package_name = line.split("#egg=")[0], line.split("#egg=")[1]
            if "-e" in rest:
                rest = rest.split("-e")[1]
            package_name = package_name + "@" + rest
            packages.append(package_name)
    return packages
REQUIRED = get_requirements()


class InstallCommand(_install):
    def run(self):
        check_call([sys.executable, "-m", "pip", "install", "cython"])
        _install.run(self)

setup(
    name='dacon',
    version='0.1.0',
    description=DESCRIPTION,
    author=AUTHOR,
    email=AUTHOR_MAIL,
    packages=find_packages(exclude=[]),
    license="MIT",
    keywords="Solidity smart contracts",
    install_requires=REQUIRED,
    # tests_require=TESTS_REQUIRE,
    python_requires=REQUIRES_PYTHON,
    # extras_require=EXTRAS,
    package_data={"contracts": ["*"]},
    include_package_data=True,
    entry_points={"console_scripts": ["extract=dacon.cli:main"]},
    cmdclass={"install": InstallCommand},
)
