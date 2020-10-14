import os
import shutil

TARGET_BASE_PATH = "G:\\Shared drives\\CWRUbotix\\Resources\\Hardware\\Altium\\Library\\Components"
def main():
    base = os.getcwd()
    for f in os.listdir():
        path = "{}\\{}".format(base, f)
        if not os.path.isfile(path):
            for g in os.listdir(path):
                if ".IntLib" in g:
                    src = "{}\\{}".format(path, g)
                    dest = "{}\\{}".format(TARGET_BASE_PATH, g)
                    print("Copying {} to {}".format(src, dest))
                    shutil.copy(src, dest)


if __name__ == '__main__':
    main()