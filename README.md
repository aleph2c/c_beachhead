# Easy C Programming Setup

This project removes the complexity of setting a C project within the WSL and
having access to it's build (via CMake) and debug (via gdb) from within VS Code
running on Windows 11.

## Quick Start

After you have clicked on "Use this template", you will select a ``<repo_name>`` for your derived repo.

Once you have your ``<repo_name>`` follow these steps to quickly set up your C project:

```bash
git clone git@github.com:aleph2c/<repo_name>.git
cd <repo_name>
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
wsl2vs c new -p <program_name>
code . # open VS code and write/build/debug your c files
```

The above command will create:
- ``/src/<program_name>.c``
- ``/inc/<program_name>.h``
- ``CMakeLists.txt`` configured to create ``<project_name>.c``
- ``.vscode/`` directory with all of the configuration files required for VS
Code (running on Windows 11) to build and debug your C programs within the WSL.

---
Once you are happy with your environment, you can remove the Python and it's
helper commands to only leave the C project:

```
wls2vs remove
```

The above command will remove all python and the wls2vs command and create a new README.md file for your C project.

## Example: Setting Up a C Program

Here's an example of setting up a C program called "hey" in the WSL:

```bash
git clone git@github.com:aleph2c/<repo_name>.git
cd <repo_name>
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
wsl2vs c new -p hey
```

To open the project in VS Code, use the following command:
```
code .
```

Inside VS Code, navigate to the `./src/hey.c` file. You can make your changes and then build or debug the file.

If you wanted to build and run your program within the WSL:

```
cd build
cmake ..
make

# to run the program
./hey
```

If you are happy with your C project, unclutter your directory by removing the ``wsl2vc`` command and all of its supporting python:

```
wsl2vs remove
```

## A Deeper Look

This project uses the `click` Python command library to create a command called `wsl2vc`. The `wsl2vc c new <program_name>` command, creates a new WSL C
project by generating the following:

- `.vscode/tasks.json`: Configures the `make`, `cmake`, and `C/C++: gcc build active file` tasks, which are necessary for creating the executable.
- `.vscode/launch.json`: Configures VS Code to utilize the gdb debugger within the WSL.
- `.vscode/c_cpp_properties.json`: Configures the settings for C and C++ IntelliSense and browsing in VS Code.
- `/build/`: Contains the executables.
- `/src/<program_name>.c`: Contains the main C file.
- `/inc/<program_name>.h`: Contains the public header files.
- `CMakeLists.txt`: Contains the CMake instructions used to build the project.
