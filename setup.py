import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name='metaphor-tunnel',
    version='1.0.0',
    author='Metaphorme',
    author_email="",
    url="https://github.com/Metaphorme/MetaphorTunnel",
    description="",
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=setuptools.find_packages(),
    install_requires = [
        'pycryptodome',
        'requests',
        'websockets',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)