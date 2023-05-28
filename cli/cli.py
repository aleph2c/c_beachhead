import os
import click
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

class Cli:
  def __init__(self):
    pass

  def create_directories(self):
    this_dir = Path(__file__).parent.parent

    src_path = str(this_dir / 'src')
    inc_path = str(this_dir / 'inc')
    build_path = str(this_dir / 'build')
    vscode_path = str(this_dir / '.vscode')

    for _dir in [src_path, inc_path, build_path, vscode_path]:
      if not os.path.exists(_dir):
        os.makedirs(_dir)

  def write_config_files(self, project, program):
    click.echo(f'project: {project}')
    click.echo(f'program: {program}')
    template_path = (Path(__file__).parent / ".." / ".templates").resolve()
    project_root = (Path(__file__).parent / ".." ).resolve()

    cmake_list_txt_template = template_path / 'CMakeLists.txt.j2'
    launch_json_template = template_path / 'launch.json.j2'
    tasks_json_template = template_path / 'tasks.json.j2'
    c_cpp_properties_template = template_path / 'c_cpp_properties.json.j2'

    c_template = template_path / 'c_file.c.j2'
    h_template = template_path / 'h_file.h.j2'

    assert cmake_list_txt_template.exists()
    assert launch_json_template.exists()
    assert tasks_json_template.exists()

    cmake_lists_text = project_root / 'CMakeLists.txt'
    launch_json = project_root / '.vscode' / 'launch.json'
    tasks_json = project_root / '.vscode' / 'tasks.json'
    c_cpp_properties = project_root / '.vscode' / 'c_cpp_properties.json'
    program_c_path = project_root / 'src' / f"{program}.c"
    program_h_path = project_root / 'inc' / f"{program}.h"

    data = {'project' : project, 'program' : program }

    for template_path, output_file_path in [
        [c_template, program_c_path],
        [h_template, program_h_path],
        [cmake_list_txt_template, cmake_lists_text],
        [c_cpp_properties_template, c_cpp_properties],
        [launch_json_template, launch_json],
        [tasks_json_template, tasks_json]]:
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

  def write_readme_file_after_remove(self):
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

    for template_path, output_file_path in [
        [readme_template, readme_md],
        ]:
      env = Environment(
        loader=FileSystemLoader([str(template_path.parent)]),
        trim_blocks=True,
        lstrip_blocks=True
      )
      template = env.get_template(str(template_path.name))
      output_string = template.render(**data)
      with open(output_file_path, "w") as fp:
        fp.write(output_string)

cli_ctx = click.make_pass_decorator(Cli, ensure=True)

@click.group()
@cli_ctx
def cli(ctx, project=None, program=None):
  pass

@cli.group()
@cli_ctx
def c(ctx):
  '''Commands to create and control a C project'''
  pass

@cli.command()
@click.option("-d", "--dry-run", is_flag=True, default=False, help="Dry run the removal")
@cli_ctx
def remove(ctx, dry_run):
  '''Remove all setup code and only leave to created project'''
  if dry_run:
    click.echo(f"removing README.md")
    click.echo(f"writing new README.md")
    click.echo(f"removing .venv/*")
    click.echo(f"removing .templates/*")
    click.echo(f"removing {ctx.get_project_name()}.egg-info/*")
    click.echo(f"removing cli/*")
    click.echo(f"removing setup.py")
  else:
    confirm_string = "Are you sure you want to remove the wls2vc command and it's supporting code"
    user_result = click.confirm(confirm_string)
    if user_result:
      click.echo(f"removing README.md")
      ctx.remove_file("README.md")
      ctx.write_readme_file_after_remove()
      click.echo(f"writing new README.md")
      click.echo(f"removing .venv/*")
      ctx.remove_dir('.venv')
      click.echo(f"removing .templates/*")
      ctx.remove_dir('.templates')
      click.echo(f"removing {ctx.get_project_name()}.egg-info/*")
      ctx.remove_dir(f'{ctx.get_project_name()}.egg-info')
      click.echo(f"removing cli/*")
      ctx.remove_dir(f'cli')
      click.echo(f"removing setup.py")
      ctx.remove_file(f'setup.py')

@c.command()
@click.argument("program", nargs=1)
@cli_ctx
def new(ctx, program=None):
  '''Create a new C program that works with the WSL and VS Code'''
  this_dir = Path(__file__).parent.parent
  project = this_dir.name
  if program is None:
    program = project

  ctx.create_directories()
  ctx.write_config_files(project, program)

