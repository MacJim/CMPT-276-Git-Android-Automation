import os
import shutil


# MARK: - Main
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# MARK: - Verifications
# MARK: Directories
git_clone_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clones")
if (not os.path.exists(git_clone_root)):
    print("Repos not cloned yet.")
    exit(1)

apk_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apks")
if (not os.path.exists(apk_dir)):
    os.mkdir(apk_dir)


# MARK: Get valid android project dirs
valid_dirs = []
invalid_dirs = []

dirs = os.listdir(git_clone_root)
dirs = [os.path.join(git_clone_root, d) for d in dirs]
dirs = [d for d in dirs if os.path.isdir(d)]

print(dirs)

for d in dirs:
    filenames = os.listdir(d)
    if ("gradlew" in filenames):
        valid_dirs.append(d)
        gradlew_filename = os.path.join(d, "gradlew")
        os.chmod(gradlew_filename, 0o700)
    else:
        invalid_dirs.append(d)


# MARK: - gradlew assembleDebug
# Source: https://developer.android.com/studio/build/building-cmdline
print("\nStart building APKs.")
build_success_dirs = []
build_fail_dirs = dict()

for d in valid_dirs:
    print("Building " + d)
    os.chdir(d)
    exit_code = os.system("./gradlew assembleDebug")
    if (exit_code == 0):
        build_success_dirs.append(d)
    else:
        build_fail_dirs[d] = exit_code

print("Successfully built:", build_success_dirs)
print("Failed to build:", build_fail_dirs)
print("Invalid Android dirs (missing `gradlew`):", invalid_dirs)


# MARK: - Copy APKs to the convenience folder.
for d in build_success_dirs:
    output_dir = os.path.join(d, "app/build/outputs/apk/debug")
    filenames = os.listdir(output_dir)
    for f in filenames:
        if (f.endswith(".apk")):
            # Copy
            f = os.path.join(output_dir, f)

            if (d.endswith("/")):
                d = d[:-1]
            destination_filename = d.split("/")[-1]
            destination_filename += ".apk"
            destination_filename = os.path.join(apk_dir, destination_filename)

            shutil.copyfile(f, destination_filename)
            break
