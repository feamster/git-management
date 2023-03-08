#!/usr/bin/env python3

import os
import sys
import re
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: git-submodules.py <path>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.isdir(path):
        print("Directory does not exist: " + path)
        sys.exit(1)

    # initialize a git repository in the current directory if it doesn't exist
    if not os.path.isdir(".git"):
        subprocess.run(["git", "init"], check=True)

    # make an old directory if it does not exist
    old_path = os.path.join(path, ".")
    if not os.path.isdir(old_path):
        os.mkdir(old_path)

    # create a set of domains to skip
    skip_domains = set()
    skip_domains.add("gatech.edu")
    skip_domains.add("git.overleaf.com")

    # initialize an empty set of current URLs
    current_urls = set()

    # search .git directory in this directory and all subdirectories for config files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == "config":
                config_path = os.path.join(root, file)
                print("Found config file: " + config_path)

                # read each line of the config file
                with open(config_path, "r") as f:
                    lines = f.readlines()

                    # find the url of the submodule
                    for line in lines:
                        if line.startswith("\turl = "):
                            url = line[7:].strip()
                            current_urls.add(url)

    for root, dirs, files in os.walk(path):
        if ".git" in dirs:

            # find config file
            config = os.path.join(root, ".git", "config")

            # read config file
            with open(config, "r") as f:
                lines = f.readlines()
                # find url line
                for line in lines:
                    if line.startswith("\turl"):
                        # print directory
                        print(root)

                        # print url
                        print(line.split("=")[1].strip())
                        # assign the url to a variable
                        url = line.split("=")[1].strip()

                        # continue if the url is already in the set
                        if url in current_urls:
                            print(url + " already in set")
                            continue


                        # continue if the url string matches a domain in the skip_domains set
                        match = False
                        for domain in skip_domains:
                            # perform a regular expression match
                            if re.search(domain, url):
                                print("Skipping " + url)
                                match = True
                        if match is True:
                            continue


                        # dest is the name of the git repo
                        dest = line.split("/")[-1].strip()
                        dest = dest.split(".")[0]

                        # reassign dest unless user hits enter
                        new_dest = input("New name? [N/name/[Continue]] : ")
                        if new_dest == "C":
                            continue
                        if new_dest != "":
                            dest = new_dest

                        # ask the user if this repository is old
                        if input("Is this repository old? [y/N] ").lower() == "y":
                            destdir = "old/" +  dest
                        else:
                            destdir = dest

                        try:
                            subprocess.check_output("git submodule add " + line.split("=")[1].strip() + " " + destdir, shell=True, timeout=10)
                        except subprocess.TimeoutExpired:
                            print("Timeout expired")
                            continue
                        except subprocess.CalledProcessError:
                            print("Called process error")
                            continue


__name__ == "__main__" and main()
