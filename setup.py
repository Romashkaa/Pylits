from setuptools import setup, find_packages

import shutil
import os

from pylits._version import __version__ as version

# -----------------------------------------------------------------------------
# Clean old build artifacts
# -----------------------------------------------------------------------------

for folder in ("build", "dist"):
    if os.path.exists(folder):
        shutil.rmtree(folder)

for egg in [d for d in os.listdir('.') if d.endswith(".egg-info")]:
    shutil.rmtree(egg)

# -----------------------------------------------------------------------------
# Helpers to read files
# -----------------------------------------------------------------------------

def readme():
    with open('README.md', 'r') as f:
        return f.read()
  
def changelog():
    with open('CHANGELOG.md', 'r') as f:
        return f.read()
    
# -----------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------

setup(
    name='pylits',
    version=version,
    author='romashka',
    author_email='notromashka@gmail.com',
    description='Serialize and store Python literals with ease!',
    long_description=readme() + f"\n\n---\n\n# Changes in version {version}\n\n" + changelog(),
    include_package_data=True,
    long_description_content_type='text/markdown',
    url='https://github.com/Romashkaa/Pylits',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='serialize tools literal store',
    project_urls={
        "GitHub": "https://github.com/Romashkaa/Pylits",
    },
    python_requires=">=3.12"
)

"""
.venv/bin/python setup.py sdist bdist_wheel
twine upload --repository pypi dist/*
"""

print(f"PYLITS VERSION: {version}")