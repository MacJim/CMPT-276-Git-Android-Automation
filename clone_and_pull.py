import os
import concurrent.futures

import git


# MARK: - Settings
# Do not use a big setting here. I used 8 and got banned immediately.
thread_count = 2


# MARK: - Main
os.chdir(os.path.dirname(os.path.abspath(__file__)))

git_clone_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clones")
if (not os.path.exists(git_clone_root)):
    os.mkdir(git_clone_root)


# MARK: - Git clone/pull
# MARK: Helper functions
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
        # print("Pulling from " + url)
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
        # print("Cloning from " + url)
        repo = git.Repo.clone_from(url, repo_path)

    return repo_path


def clone_thread(git_clone_url: str):
    try:
        cloned_dir = git_clone(git_clone_url, git_clone_root)
        cloned_dirs.append(cloned_dir)
    except FileExistsError:
        print("A file exists for " + git_clone_url)
    except FileNotFoundError:
        print("A folder exists without the \".git\" directory for " + git_clone_url)
    except:
        print("Unknown exception for " + git_clone_url)


# MARK: Get Git URLs
git_clone_urls = []

with open("urls.txt", "r") as urls_file:
    for line in urls_file:
        line = line.strip("\n ")
        if ((len(line) > 0) and (line[0] != '#')):
            # print("Valid Git URL:", line)
            git_clone_urls.append(line)

print("URLs found:", len(git_clone_urls))


# MARK: Clone using `thread_count` threads.
cloned_dirs = []

with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
    executor.map(clone_thread, git_clone_urls)

print("Cloned directories:", cloned_dirs)
