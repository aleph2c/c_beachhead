from setuptools import setup

setup(
  name="c_template",
  version="0.1",
  py_modules=["c_template"],
  install_requires=[
    'Click',
    'Jinja2',
    'PyYaml',
    'colorama'
  ],
  entry_points="""
  [console_scripts]
  try=cli.cli:cli
  """
)
