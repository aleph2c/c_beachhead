import os
import click
import shutil
import subprocess
from colorama import Fore, Style, init
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class Cli:
  def __init__(self):
    self.this_dir = Path(__file__).parent.parent

  def create_directories(self):
    this_dir = self.this_dir

    src_path = str(this_dir / 'src')
    inc_path = str(this_dir / 'inc')
    build_path = str(this_dir / 'build')
    test_path = str(this_dir / 'test')
    vscode_path = str(this_dir / '.vscode')

    for _dir in [src_path, inc_path, test_path, build_path, vscode_path]:
      if not os.path.exists(_dir):
        os.makedirs(_dir)

  def hydrate_templates(self, project, program):
    click.echo(f'project: {project}')
    click.echo(f'program: {program}')
    template_path = (Path(__file__).parent / ".." / ".templates").resolve()
    project_root = (Path(__file__).parent / ".." ).resolve()

    cmake_list_txt_template = template_path / 'CMakeLists.txt.j2'
    launch_json_template = template_path / 'launch.json.j2'
    tasks_json_template = template_path / 'tasks.json.j2'
    c_cpp_properties_template = template_path / 'c_cpp_properties.json.j2'

    c_main_template = template_path / 'main.c.j2'
    c_template = template_path / 'c_file.c.j2'
    h_template = template_path / 'h_file.h.j2'

    c_main_test_template = template_path / 'main_test.c.j2'
    c_test_template = template_path / 'c_file_test.c.j2'
    h_test_template = template_path / 'h_file_test.h.j2'

    assert cmake_list_txt_template.exists()
    assert launch_json_template.exists()
    assert tasks_json_template.exists()

    cmake_lists_text = project_root / 'CMakeLists.txt'
    launch_json = project_root / '.vscode' / 'launch.json'
    tasks_json = project_root / '.vscode' / 'tasks.json'
    c_cpp_properties = project_root / '.vscode' / 'c_cpp_properties.json'
    main_c_path = project_root / "main.c"
    program_c_path = project_root / 'src' / f"{program}.c"
    program_h_path = project_root / 'inc' / f"{program}.h"

    main_c_test_path = project_root / 'test' / "main.c"
    program_c_test_path = project_root / 'test' / f"{program}_test.c"
    program_h_test_path = project_root / 'test' / f"{program}_test.h"

    data = {'project' : project, 'program' : program }

    self.render_templates(data=data,
        list_of_pairs=
          [
            [c_main_template, main_c_path],
            [c_template, program_c_path],
            [h_template, program_h_path],
            [c_main_test_template, main_c_test_path],
            [c_test_template, program_c_test_path],
            [h_test_template, program_h_test_path],
            [cmake_list_txt_template, cmake_lists_text],
            [c_cpp_properties_template, c_cpp_properties],
            [launch_json_template, launch_json],
            [tasks_json_template, tasks_json]
          ]
        )

  def render_templates(self, data, list_of_pairs):
    for template_path, output_file_path in list_of_pairs:
      env = Environment(
        loader=FileSystemLoader([str(template_path.parent)]),
        trim_blocks=True,
        lstrip_blocks=True
      )
      template = env.get_template(str(template_path.name))
      output_string = template.render(**data)
      with open(output_file_path, "w") as fp:
        fp.write(output_string)

  def remove_file(self, name):
    path_to_file = Path(__file__).parent / '..' / name
    if path_to_file.exists():
      path_to_file.unlink()

  def remove_dir(self, dirname):
    path_to_dir = Path(__file__).parent / '..' / dirname
    if path_to_dir.exists():
      shutil.rmtree(path_to_dir)

  def get_program_name(self):
    src_path = (Path(__file__).parent / ".." / "src").resolve()
    c_files = list(Path(src_path).glob("*.c"))
    name = None
    if len(c_files):
      name = c_files[0].stem
    return name

  def get_project_name(self):
    base_path = Path(__file__).parent
    project = base_path.parent.stem
    return project

  def hydrate_readme_from_template(self):
    project = self.get_project_name()
    program = self.get_program_name()

    click.echo(f'project: {project}')
    click.echo(f'program: {program}')

    template_path = (Path(__file__).parent / ".." / ".templates").resolve()
    project_root = (Path(__file__).parent / ".." ).resolve()

    readme_template = template_path / 'README.md.j2'

    assert readme_template.exists()

    readme_md = project_root / 'README.md'

    data = {'project' : project, 'program' : program }

    self.render_templates(data=data, list_of_pairs=[
        [readme_template, readme_md],
      ]
    )

cli_ctx = click.make_pass_decorator(Cli, ensure=True)

@click.group()
@cli_ctx
def cli(ctx, project=None, program=None):
  pass

@cli.command()
@click.argument("program", nargs=1)
@cli_ctx
def new(ctx, program=None):
  '''Create a new C program that works with the WSL and VS Code'''
  this_dir = Path(__file__).parent.parent
  project = this_dir.name
  if program is None:
    program = project

  ctx.create_directories()
  ctx.hydrate_templates(project, program)


@cli.command()
@click.option("-d", "--dry-run", is_flag=True, default=False, help="Dry run the removal")
@cli_ctx
def remove(ctx, dry_run):
  '''Remove all setup code and only leave to created project'''
  if dry_run:
    click.echo("removing README.md")
    click.echo("writing new README.md")
    click.echo("removing .venv/*")
    click.echo("removing .templates/*")
    click.echo(f"removing {ctx.get_project_name()}.egg-info/*")
    click.echo("removing cli/*")
    click.echo("removing setup.py")
  else:
    confirm_string = "Are you sure you want to remove the wls2vc command and it's supporting code"
    user_result = click.confirm(confirm_string)
    if user_result:
      click.echo("removing README.md")
      ctx.remove_file("README.md")
      ctx.hydrate_readme_from_template()
      click.echo("writing new README.md")
      click.echo("removing .venv/*")
      ctx.remove_dir('.venv')
      click.echo("removing .templates/*")
      ctx.remove_dir('.templates')
      click.echo(f"removing {ctx.get_project_name()}.egg-info/*")
      ctx.remove_dir(f'{ctx.get_project_name()}.egg-info')
      click.echo("removing cli/*")
      ctx.remove_dir('cli')
      click.echo("removing setup.py")
      ctx.remove_file('setup.py')

@cli.command()
@cli_ctx
def make(ctx):
  """Make the C project"""
  init()
  build_dir = (ctx.this_dir / 'build').resolve()
  assert build_dir.exists()

  if not (build_dir / 'Makefile').exists():
    result_blob = subprocess.run("cmake ..", shell=True, cwd=str(build_dir), capture_output=True, text=True)
  result_blob = subprocess.run("make", shell=True, cwd=str(build_dir), capture_output=True, text=True)
  lines = result_blob.stdout.split('\n')
  err_lines = result_blob.stderr.split('\n')
  for line in lines:
    if 'Built' in line:
      print(Fore.GREEN + line + Style.RESET_ALL)
    else:
      print(line)
  for line in err_lines:
    if 'error:' in line:
      print(Fore.RED + line + Style.RESET_ALL)
    else:
      print(line)

@cli.command()
@cli_ctx
def tests(ctx):
  """Make the C project and run the tests"""
  init()
  build_dir = (ctx.this_dir / 'build').resolve()
  assert build_dir.exists()

  if not (build_dir / 'Makefile').exists():
    result_blob = subprocess.run("cmake ..", shell=True, cwd=str(build_dir), capture_output=True, text=True)

  result_blob = subprocess.run("make", shell=True, cwd=str(build_dir), capture_output=True, text=True)
  err_lines = result_blob.stderr.split('\n')
  for line in err_lines:
    if 'error:' in line:
      print(Fore.RED + line + Style.RESET_ALL)
    else:
      print(line)
  if result_blob.returncode != 0:
    exit(1)

  result_blob = subprocess.run("ctest --output-on-failure", shell=True, cwd=str(build_dir), capture_output=True, text=True)
  test_lines = result_blob.stdout.split('\n')
  for line in test_lines:
    if 'error:' in line:
      print(Fore.RED + line + Style.RESET_ALL)
    if '100%' in line:
      print(Fore.GREEN + line + Style.RESET_ALL)
    else:
      print(line)

