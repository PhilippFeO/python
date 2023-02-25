import os


"""
This scripts adds first level subpages of a page to the page itself for Zim Wiki.
It is only consistent if no subpages have been added yet, i. e. if it is executed more than once
every subpage is added a second time.
"""

directory: str = "/home/kali/zim_wiki/MeinWiki"


def main():
    # iterate over every page of the wiki
    for page in os.listdir(directory):
        # Filter for pages (in this directory may additional content like png-files also be stored
        if page.endswith(".txt"):
            pagename = page.split(".")[0].replace("_", " ")
            # Start recursion
            if os.path.isdir(directory + os.sep + pagename):
                helper(pagename)


def helper(*dirs):
    """
    This function recursively collects the subpages of the last page in *dirs.
    *dirs (*args-technique) used because it is not obvious how deep subpages are nested.
    """
    path = directory + os.sep + os.sep.join(dirs)
    print(path)
    heading = True  # helper variable, s. below
    for page in os.listdir(path):
        # Again, filter for pages and skip additional stuff
        if page.endswith(".txt"):
            subpage = page.split(".")[0]
            # compose link in the Zim Wiki syntax: :Page:Subpage1:Subpage2:...:SubpageN
            l = list(dirs)
            l.append(subpage)
            page_link = ":".join(l).replace("_", " ")
            page_link_text = f"[[:{page_link}|:{page_link}]]"
            print(page_link_text)
            # Append first level subpage link to page
            with open(path + ".txt", "a") as f:
                # Inset a heading referring to the subpages
                if heading:
                    f.write("===== Unterseiten =====\n")
                    # This variable guarantees heading is set once
                    heading = False
                f.write(f"* {page_link_text}\n")
            # In case further subpages are present (saved in a folder with the name of current subpage)
            # do next recursion step
            if os.path.isdir(path + os.sep + subpage):
                print()
                helper(*dirs, subpage)


if __name__ == "__main__":
    main()

