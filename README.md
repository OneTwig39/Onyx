# Onyx
Onyx is a free and open source and cross platform build tool designed for compiling multi language projects.
Onyx is still in beta and documentation has not finished yet.
## App Structure
Create a file called "app" and a folder called "src", each line in app defines a script in src.
Each line must include the name and the path, for example: if the line is: "script/path/to/file.py" that defines a script called "script" at "src/path/to/file.py".
Optionally you can include a module like "script/path/to/file.py?python" or a version like "script/path/to/file.py?python@2026.7.18.3.14.6".
Note you should always use the forwrd slash "/" no matter what your os separator is.
The script named main is the one that is ran by default, every other one will be a library.
## Installing/using Modules
To install a module click on one of the links below and extract the files and take the folder inside and move it to where the modules name implies.
Eg: if the module name is Linux Amd 64 Python 2026.7.18.3.14.6 put it in the same file as the onyx binary under bin/module/linux/amd/64/go/1.25.12 with 1.25.12 being the name of the folder
All modules are named "Os Arch Bits Name Version" and you can download them from the links below
[Linux Amd 64 Go 1.25.12](https://go.dev/dl/go1.25.12.linux-amd64.tar.gz)
[Linux Amd 64 Python 2026.7.18.3.14.6](https://github.com/astral-sh/python-build-standalone/releases/download/20260718/cpython-3.14.6+20260718-x86_64-unknown-linux-gnu-install_only.tar.gz)
## Calling Libraries
You can call a library by importing it by the name you gave it in "app" for example if you did "library/path/to/lib.py", you could call it from these languages like this:
### Python
```python
import library

library(["Go"]) # Returns subprocess.Popen object
```
