# Arduino Projects for Watlock System

## What are these?
These are [PlatformIO](https://docs.platformio.org/en/latest/what-is-platformio.html) arduino projects. They're basically a souped-up version of a
standard arduino project. Lets look at the components:
- `./.pio`\
  This directory contains the compiled binaries for our project... We probably never need to look in this directory.
- `./.vscode`\
  This directory contains configuration for your specific system and files. PlatformIO writes these files automatically, So you probably dont need to touch this.
- `./include`\
All C and C++ headers and source files inside this directory will be compiled with the project, as if they were `#include`'ed.
- `./lib`\
This is the library directory for this project. If you have libraries that are specific to this 1 arduino project (not general sensor libraries), they should go inside this directory (inside their own folder).
- `./src`\
This is the primary source file directory. This is where you should write your code. The `main.cpp` file is the primary file. If you have big functions or class declarations, you should create extra header/source files and `#include` them.
- `./test`\
This is the folder for [PlatformIO unit tests](https://docs.platformio.org/en/latest/plus/unit-testing.html). You are welcome to use these, but they are a more advanced functionality.
- `./.gitignore`\
This is for git to ignore the files we dont want to send to github, Notice the `./.pio` and `/.vscode` directories are ignored, This means they wont show up for a newly-cloned repo. But they will be created when you start using PlatformIO.
- `./platformio.ini`\
This is the primary configuratio file for the PlatformIO project. This file contains compile and configuration instructions. It also creates a reference to the `Shared_libs` folder to allow `main.src` to pull libraries from that folder.

## Is that a Template?
Yup! And its easy to get started with.
Just make a copy of the `Template_Project` directory, rename it to whatever seems right, And then start editing the code in `main.cpp`.\
Then, make sure you commit and push your changes to a new branch, and create a pull request.

## How do I use PlatformIO?
PlatformIO is very similair to the Arduino IDE, but it all happens inside the VScode window. Since PlatformIO has a lot more functionality, it can seem more complicated at first. Here is how you start using it:
1. Install PlatformIO on VScode\
    \
    ![](.resources/ScreenGIF%20-%20PlatformIO%20Install.gif)

2. Open the project you want to work on in a new VScode window.\
    You dont want to open the entire *Data_Acquisition* project because PlatformIO wont know which project to work with. So just open the project you are working on.\
    \
    ![](.resources/Screenshot%20-%20PlatformIO%20project.jpg)

3. Edit the `main.cpp` to create the code for you arduino!\
    \
    ![](.resources/Screenshot%20-%20PlatformIO%20edit%20source.jpg)

4. Compile your code and see if it creates any errors.\
    \
    ![](.resources/ScreenGIF%20-%20PlatformIO%20compile%20Project.gif)

5. Flash your code to the Arduino!\
    \
    ![](.resources/ScreenGIF%20-%20PlatformIO%20Flash%20Project.gif)

6. The *monitor* and *upload and monitor* options allow you to read and write to the USB serial of the arduino. These are very useful for debugging!\
    \
    ![](.resources/Screenshot%20-%20PlatformIO%20monitor.jpg)