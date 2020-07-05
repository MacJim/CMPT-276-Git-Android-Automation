# Clones a Git repo.

import os

import git


def git_clone(url: str, destination_dir: str, repo_name: str = None) -> str:
    """
    Clone a git repo.

    :param url: The Git repo URL.
    :param destination_dir: The folder where we clone into.
    :param repo_name: The cloned repo's folder name.
    :return: The cloned repo folder's full path.
    """
    if (repo_name is None):
        # repo_name = url.split(".")[-2].split("/")[-1]    # Don't use this. The projects names are all `prj`. They only differ in terms of group names.
        repo_name = url.split(".")[-2].split(":")[-1]
        repo_name = repo_name.replace("/", "-")

    repo_path = os.path.join(destination_dir, repo_name)

    if (os.path.isfile(repo_path)):
        raise FileExistsError
    elif (os.path.isdir(repo_path)):
        # Find the ".git" folder.
        if (".git" not in os.listdir(repo_path)):
            print(repo_path + " does not contain the \".git\" folder.")
            raise FileNotFoundError

        # This is a valid git working directory. Try to pull.
        print("Pulling from " + url)
        repo = git.Repo(repo_path)
        origin = repo.remotes[0]
        origin.fetch()
        pull_info = origin.pull()

        # TODO: Maybe I should handle the pull info.
        # https://gitpython.readthedocs.io/en/stable/reference.html?highlight=FetchInfo#git.remote.FetchInfo
        # HEAD_UPTODATE
        # ERROR, REJECTED
        # print(pull_info[0].flags)
    else:
        # No repo exists here. Try to clone.
        print("Cloning from " + url)
        repo = git.Repo.clone_from(url, repo_path)

    return repo_path
