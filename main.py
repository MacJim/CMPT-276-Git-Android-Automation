import os
import concurrent.futures
import time

from git_helper import git_clone


# MARK: - Settings
# Do not use a big setting here. I used 8 and got banned immediately.
thread_count = 2


# MARK: - Main
os.chdir(os.path.dirname(os.path.abspath(__file__)))

git_clone_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clones")
if (not os.path.exists(git_clone_root)):
    os.mkdir(git_clone_root)


# MARK: - Git clone/pull
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


with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
    executor.map(clone_thread, git_clone_urls)

print("Cloned directories:", cloned_dirs)
