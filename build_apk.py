import os


# MARK: - Main
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# MARK: - Verifications
# MARK: Verify that the `clones` directory exists.
git_clone_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clones")
if (not os.path.exists(git_clone_root)):
    print("Repos not cloned yet.")
    exit(1)


# MARK: Get valid android project dirs
valid_dirs = []
invalid_dirs = []

dirs = os.listdir(git_clone_root)
dirs = [os.path.join(git_clone_root, d) for d in dirs]
dirs = [d for d in dirs if os.path.isdir(d)]

print(dirs)

for d in dirs:
    files = os.listdir(d)
    if ("gradlew" in files):
        valid_dirs.append(d)
    else:
        invalid_dirs.append(d)

# print("Valid Android dirs:")
# print(valid_dirs)
print("Invalid Android dirs (missing `gradlew`):")
print(invalid_dirs)


# TODO: - gradlew assembleDebug
# Source: https://developer.android.com/studio/build/building-cmdline
