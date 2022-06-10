import os
import re

from pkg_resources import resource_filename


def handle_multipage(root: str, use_pr_st_template: bool = False) -> None:
    """Enable multipage mode (streamlit native)"""

    # Creating a new folder called "pages"
    os.mkdir(f"{root}/streamlit/pages")

    multipage_page_template = resource_filename("pr_st", "template/multipage/page.py")
    multipage_main_template = resource_filename("pr_st", "template/multipage/main.py")
    with open(multipage_page_template) as f:
        mutlipage_page_content = f.read()

    with open(multipage_main_template) as f:
        multipage_main_content = f.read()

    # Now we need to create a new file called "page1.py"
    with open(f"{root}/streamlit/pages/Page_2.py", "w") as f:
        f.write(
            mutlipage_page_content.replace("{{ PAGE_NUMBER }}", "2").replace(
                "{{ PR_ST_TEMPLATE_CONTENT }}",
                handle_pr_st_template(root, return_content=True)
                if use_pr_st_template
                else "",
            )
        )

    # Now we need to update the app.py file
    with open(f"{root}/streamlit/App.py", "r+") as f:
        content = f.read()

        f.seek(0)
        f.write(content.replace("{{ MULTIPAGE_CONTENT }}", multipage_main_content))
        f.truncate()


def handle_pr_st_template(root: str, return_content: bool = False) -> None:
    """Enable pr-streamlit-template styles (see https://pypi.org/project/pr-streamlit-template/ for more info)"""

    pr_st_template_dir = resource_filename("pr_st", "template/pr_st_template/func.py")
    with open(pr_st_template_dir) as f:
        pr_st_template_content = f.read()

    if return_content:
        return pr_st_template_content

    with open(f"{root}/streamlit/App.py", "r+") as f:
        content = f.read()

        f.seek(0)
        f.write(content.replace("{{ PR_ST_TEMPLATE_CONTENT }}", pr_st_template_content))
        f.truncate()


def handle_hydralit_template(root: str) -> None:
    pass


def clean_macros(root: str) -> None:
    for dir, _, files in os.walk(f"{root}/streamlit/"):
        for file in files:
            with open(f"{dir}/{file}", "r+") as f:
                content = f.read()

                f.seek(0)
                f.write(re.sub(r"\{\{.*?\}\}", "", content))
                f.truncate()
