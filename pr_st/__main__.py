import click

from pr_st import version
from pr_st.commands.new.cli import new


@click.group()
@click.version_option(version=version)
def main():
    """
    PR-ST is a CLI package that helps creates streamlit templates
    """
    pass


main.add_command(new)
