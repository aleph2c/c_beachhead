from setuptools import setup

setup(
  name="c_template",
  version="0.1",
  py_modules=["c_template"],
  install_requires=[
    'Click',
    'Jinja2',
    'PyYaml',
  ],
  entry_points="""
  [console_scripts]
  wsl2vs=cli.cli:cli
  """
)
