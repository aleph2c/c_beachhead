# Easy Setup for C Programming on WSL2 with VS Code in Windows 11

Quickly turn on a WSL2 C programming project and then use VS Code in Windows 11
to develop, build and debug it. (This turns your Windows 11 VS Code into a C IDE
for your WSL2 Linux distribution.)

How it works:

A temporary Python environment is used to create a C programming configuration
that can span across the two operating systems.  Once you have confirmed that
``VS Code`` in Windows 11 can build and debug your C code on the WSL2, you can
remove the Python environment so that you don't have extraneous files in your C
project.  This removal will also over-write this README.md file with contents
that relate to your C project.

To use this project follow these steps:

- Install prerequisites in the WSL2 and in VS Code
- Use this template repo to create your own repo
- Clone your repo onto your machine
- Setup a Python environment
- Run a command provided by the Python environment to create a C environment that VS Code can work with in Windows 11.
- Open VS Code in Windows 11
- Confirm your C environment is working
- Run another command to remove the Python environment
- Use your VS Code as a C IDE for the WSL2
- Write your README.md file

## Environment Prerequisites

Packages needed in the WSL2 in Ubuntu (v22.0.4):

```bash
sudo apt update
sudo apt install build-essential  # installs gcc, gcc+ and make
sudo apt install gdb # a C debugger that VS code will use from windows 11
sudo apt install cmake 
```

VS Code (v1.78.2) extensions that were used while building this tool:

- C/C++ v1.15.4 (microsoft)
- C/C++ Extension Pack v1.3.0 (microsoft)
- CMake v0.0.17, Extension Pack v1.3.0 (microsoft)
- CMake Tools v1.14.31
- Makefile Tools v0.7.0 (microsoft)
- Markdown Preview Enhanced v0.6.8

**Note:** All of the above tools were enabled on ``WSL: Ubuntu-22.0.4``

## Quick Start

After you have clicked on "Use this template", you will select a ``<repo_name>``
for your derived repo.

```bash
# Clone your repo onto your machine
git clone git@github.com:aleph2c/<repo_name>.git
cd <repo_name>

# Setup a Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# Run a command provided by the Python environment to create a C environment
# that VS Code will be able to work with in Windows 11
wsl2vs c new <program_name>
```

The above command will create:
- ``/src/main.c``
- ``/src/<program_name>.c``
- ``/inc/<program_name>.h``
- ``CMakeLists.txt`` configured to create ``<project_name>.c``
- ``.vscode/`` directory with all of the configuration files required for VS
Code (running on Windows 11) to build and debug your C programs within the WSL.

---

Open VS Code in Windows 11

```bash
code .
```

Try the build and debug features, try changing a file and rebuilding.

---

Once you are happy with your VS Code integration, you can remove the Python
Environment and it's helper commands to only leave the C project.

```bash
# Remove the Python Environment 
wsl2vs remove
```

The above command will also over-write this boiler-plate README.md file with
something that will work for your C project.

## A Deeper Look

This project uses the `click` Python command library to create a command called `wsl2vc`. The `wsl2vc c new <program_name>` command, creates a new WSL C
project by generating the following:

- `.vscode/tasks.json`: Configures the `make`, `cmake`, and `C/C++: gcc build active file` tasks, which are necessary for creating the executable.
- `.vscode/launch.json`: Configures VS Code to utilize the gdb debugger within the WSL.
- `.vscode/c_cpp_properties.json`: Configures the settings for C and C++ IntelliSense and browsing in VS Code.
- `/build/`: Contains the executables.
- `/src/main.c`: Contains the main C file.
- `/src/<program_name>.c`: A skeleton for your business logic.
- `/inc/<program_name>.h`: Contains the public header for your ``<program_name>.c`` file.
- `CMakeLists.txt`: Contains the CMake instructions used to build the project.

As you grow and extend your project, you will need to adjust your
``CMakeLists.txt``.  To confirm your build is working within the WSL

```bash
cd ./build
cmake ..
make
```
If your build process is working in the WSL, it should also work within the VS Code IDE.

