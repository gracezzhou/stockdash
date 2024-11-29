# File: setup.py
"""
Setup file for the project to ensure proper installation
"""
from setuptools import setup, find_packages

setup(
    name="stock_dashboard",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'dash==2.14.2',
        'pandas==2.1.4',
        'yfinance==0.2.50',
        'plotly==5.18.0',
        'numpy==1.26.2',
        'python-dateutil==2.8.2',
        'requests==2.31.0',
    ]
)