from pathlib import Path

from setuptools import setup

setup(
    name="metovhooks",
    version="0.1.0",
    description="My personal git hooks.",
    url="https://github.com/metov/metovhooks",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Azat Akhmetov",
    author_email="azatinfo@yandex.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
    ],
    install_requires=["coloredlogs", "docopt", "packaging", "pre_commit_hooks", "toml"],
    entry_points={
        "console_scripts": [
            "require_version_bump = metovhooks.require_version_bump:main",
        ]
    },
)