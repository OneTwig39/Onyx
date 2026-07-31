# Onyx
Onyx is a free and open source and cross platform build tool designed for compiling multi language projects.<br>
Onyx is still in beta and documentation has not finished yet.<br>
## App Structure
Create a file called "app" and a folder called "src", each line in app defines a script in src.<br>
Each line must include the name and the path, for example: if the line is: "script/path/to/file.py" that defines a script called "script" at "src/path/to/file.py".<br>
Optionally you can include a module like "script/path/to/file.py?python" or a version like "script/path/to/file.py?python@2026.7.18.3.14.6".<br>
Note you should always use the forwrd slash "/" no matter what your os separator is.<br>
The script named main is the one that is ran by default, every other one will be a library.<br>
Optionally in the root of your project you can have a file names icon with the respective extension to set an image on your app (appimage only).<br>
## Installing/using Modules
To install a module click on one of the links below and extract the files and take the folder inside and move it to where the modules name implies.<br>
Eg: if the module name is Linux Amd 64 Python 2026.7.18.3.14.6 put it in the same folder as the onyx binary under module/linux/amd/64/go/1.25.12 with 1.25.12 being the name of the folder.<br>
All modules are named "Os Arch Bits Name Version" and you can download them from the links below:<br>
[Linux Amd 64 Go 1.25.12](https://go.dev/dl/go1.25.12.linux-amd64.tar.gz)<br>
[Linux Amd 64 Python 2026.7.18.3.14.6](https://github.com/astral-sh/python-build-standalone/releases/download/20260718/cpython-3.14.6+20260718-x86_64-unknown-linux-gnu-install_only.tar.gz)<br>
## Calling Libraries
You can call a library by importing it by the name you gave it in "app" for example if you did "library/path/to/lib.py", you could call it from these languages like this:<br>
### Python
```python
import library

library(["Go"]) # Returns subprocess.Popen object
```
## Dependancies
If you wish to make linux appimages, install this dependency for your system and in the same folder as the onyx binary put it under dependency/appimagetool.appimage.<br>
Dont forget to make it executable with chmod +x.<br>
[Linux Amd 64](https://github.com/AppImage/appimagetool/releases/download/1.9.1/appimagetool-x86_64.AppImage)<br>
If you wish to give your apps icons, install this dependency for your system and in the same folder as the onyx binary put it under dependency/magick.appimage.<br>
Dont forget to make it executable with chmod +x.<br>
[Linux Amd 64](https://github.com/ImageMagick/ImageMagick/releases/download/7.1.2-29/ImageMagick-7.1.2-29-gcc-x86_64.AppImage)<br>
*Copyright (C) 2026  OneTwig39*
