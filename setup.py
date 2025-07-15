from setuptools import setup, find_packages

setup(
    name="wifi-reaper",
    version="0.1",
    author="sudo-cyfrin",
    description="🧟 WiFi Attack Toolkit: Monitor, Capture, Crack, and Haunt",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "scapy",
        "argparse"
    ],
    entry_points={
        "console_scripts": [
            "wifi-reaper=wifi_reaper.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux"
    ],
    python_requires='>=3.6',
)
