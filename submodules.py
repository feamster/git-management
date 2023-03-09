#!/usr/bin/env python3

import os
import sys
import re
import subprocess
import argparse

def create_submodules(path):

    # Create submodules in the current directory
    # from the repositories in the specified path

    # initialize a git repository in the current directory if it doesn't exist
    if not os.path.isdir(".git"):
        subprocess.run(["git", "init"], check=True)

    # create a set of domains to skip
    skip_domains = set()
    skip_domains = skip_domains.union({"gatech.edu", "git.overleaf.com", "gtnoise.net", "openflowswitch.org", "strozfriedberg.com"})

    # initialize an empty set of current URLs
    # the current urls refer to the URLs of git repositories in the current directory
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
                        if new_dest == "c":
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

def delete_submodule(submodule):
    # delete the specified submodule
    subprocess.call(["git", "submodule", "deinit", submodule])
    subprocess.call(["git", "rm", submodule])
    subprocess.call(["rm", "-rf", ".git/modules/" + submodule])
    subprocess.call(["git", "config", "--remove-section", "submodule." + submodule])
    subprocess.call(["git", "commit", "-m", "'remove " + submodule + " submodule'."])
    subprocess.call(["git", "push"])

def move_submodule(old_path, new_path):
    
    repo_path = os.getcwd()

    # Step 1: Remove the submodule from the parent repository
    subprocess.call(["git", "submodule", "deinit", old_path], cwd=repo_path)

    # Step 3: Move the submodule to its new location
    subprocess.call(["mv", old_submodule_path, new_path], cwd=repo_path)

    # Step 2: Remove the submodule from the Git index
    subprocess.call(["git", "rm", old_path], cwd=repo_path)


    # Step 4: Stage the new submodule in the Git index
    subprocess.call(["git", "add", new_path], cwd=repo_path)

    # Step 5: Update the submodule's location in the .gitmodules file
    subprocess.call(["git", "mv", old_path, new_path], cwd=repo_path)

    # Step 6: Commit the changes to the parent repository
    commit_message = "Moved and renamed submodule"
    subprocess.call(["git", "commit", "-m", commit_message], cwd=repo_path)

    # Step 7: Update the submodule in the parent repository
    subprocess.call(["git", "submodule", "update"], cwd=repo_path)




def main():

    # parse command line arguments
    parser = argparse.ArgumentParser()

    # switch to create submodules with the specified path
    parser.add_argument("-c", "--create", help="create submodules", nargs=1)
    
    # switch argument to remove submodule
    parser.add_argument("-d", "--delete-submodule", help="delete submodule", nargs=1)
    # switch argument to move submodule that takes two arguments: old name and new name
    parser.add_argument("-m", "--move-submodule", help="move submodule", nargs=2)

    # switch argument to list respositories
    parser.add_argument("-r", "--list-repos", help="list respositories", action="store_true")
    # switch argument to list submodules
    parser.add_argument("-s", "--list-submodules", help="list submodules", action="store_true")
    args = parser.parse_args()

    if args.create:
        create_submodules(args.create[0])
    elif args.move_submodule:
        move_submodule(args.move_submodule[0], args.move_submodule[1])
    elif args.delete_submodule:
        delete_submodule(args.delete_submodule[0])
    elif args.list_repos:
        list_repos(args.path)
    elif args.list_submodules:
        list_submodules()
    else:
        parser.print_help()
    
__name__ == "__main__" and main()
