# Easy C Programming Setup

The project removes the complexity of setting a C project within the WSL and having access to it's build and debug (via gdb) from within VS Code running on Windows 11.

## Quick Start

Follow these steps to quickly set up your C project:

```bash
git clone git@github.com:aleph2c/c_template.git <project_name>
cd <project_name>
python -m venv .venv
source .venv/bin/activate
pip install -e .
wsl2vs new c <program_name>
```

To remove the Python and only leave the C project:

```
wls2vs remove
```

The above command will remove all python and the wls2vs command and create a new README.md file for your C project.

## Example: Setting Up a C Program

Here's an example of setting up a C program called "hey" in the WSL:

```bash
git clone git@github.com:aleph2c/c_template.git hey_project
cd hey_project
python -m venv .venv
source .venv/bin/activate
pip install -e .
wsl2vs new c hey
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
./<program_name>
```

If you are happy with your C project, unclutter your directory by removing the ``wsl2vc`` command and all of its supporting python:

```
wsl2vs remove
```

## A Deeper Look

This project uses the `click` Python command library to create a command called `new`. The `new` command, when supplied with a name, initiates a new C
project. 

Running the `new` command generates the following:

- `.vscode/tasks.json`: Configures the `make`, `cmake`, and `C/C++: gcc build active file` tasks, which are necessary for creating the executable.
- `.vscode/launch.json`: Configures VS Code to utilize the gdb debugger within the WSL.
- `.vscode/c_cpp_properties.json`: Configures the settings for C and C++ IntelliSense and browsing in VS Code.
- `/build/`: Contains the executables.
- `/src/<program_name>.c`: Contains the main C file.
- `/inc/<program_name>.h`: Contains the public header files.
- `CMakeLists.txt`: Contains the CMake instructions used to build the project.
