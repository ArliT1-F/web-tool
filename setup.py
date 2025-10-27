from setuptools import setup, find_packages

setup(
    name="websecscan",
    version="1.0.0",
    author="Your Name",
    description="Advanced Website Security Scanner",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "aiohttp",
        "beautifulsoup4",
        "dnspython",
        "python-whois",
        "rich",
        "Jinja2"
    ],
    entry_points={
        'console_scripts': [
            'websecscan = scanner.core:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7',
)
