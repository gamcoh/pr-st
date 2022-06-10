# type: ignore[attr-defined]
import shutil

import click
from pkg_resources import resource_filename
from rich.console import Console

from pr_st import version
from pr_st.utils import (
    clean_macros,
    handle_hydralit_template,
    handle_multipage,
    handle_pr_st_template,
)

console = Console()


@click.command(
    name="pr_st",
)
@click.argument(
    "root",
    nargs=1,
    required=False,
    default=".",
    type=click.Path(exists=True, file_okay=False, readable=True, writable=True),
)
@click.version_option(version=version)
@click.option(
    "--use-pr-st-template",
    is_flag=True,
    default=False,
    help="Use the pr-streamlit-template styles (see https://pypi.org/project/pr-streamlit-template/ for more info)",
    show_default=True,
)
@click.option(
    "--multipage",
    is_flag=True,
    default=False,
    help="Enable multipage mode (streamlit native)",
    show_default=True,
)
@click.option(
    "--hydralit",
    is_flag=True,
    default=False,
    help="Enable hydralit mode (see https://github.com/TangleSpace/hydralit for more info)",
    show_default=True,
)
def main(root: str, use_pr_st_template: bool, multipage: bool, hydralit: bool) -> None:
    """PR-ST is a CLI package that helps creates streamlit templates"""

    if multipage and hydralit:
        console.print(
            "[red]Error: [reset]You can't use multipage and hydralit at the same time"
        )
        return

    ascii_logo = resource_filename("pr_st", "assets/images/ascii_logo.txt")
    with open(ascii_logo) as f:
        console.print(f.read(), justify="left", overflow="ellipsis", style="bold blue")

    with console.status("Processing..."):
        template_dir = resource_filename("pr_st", "template/streamlit")
        shutil.copytree(
            template_dir,
            f"{root}/streamlit",
        )
        console.log(f"Copied the base template to {root}")

        if multipage:
            handle_multipage(root, use_pr_st_template=use_pr_st_template)

        requirements = []
        if use_pr_st_template:
            requirements.append("pr-streamlit-template")
            handle_pr_st_template(root)

        if hydralit:
            requirements.append("hydralit")
            handle_hydralit_template(root)

        # Write the dependencies to requirements.txt
        with open(f"{root}/streamlit/requirements.txt", "a") as f:
            f.write("\n".join(requirements))
        console.log("Added dependencies to requirements.txt")

        clean_macros(root)
        console.log("Cleaned the macros")


if __name__ == "__main__":
    main()
