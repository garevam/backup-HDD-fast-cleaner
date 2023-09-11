import os
import filecmp
import shutil

"""
This program identifies duplicated folders and subfolders. Not duplicated files! The purpose is shallow but fast
identification of duplicated folders in my wife's offline backup external drive, which contains a terabyte of data
mostly comprised of dozens of copies of the same few folders.

It creates a dictionary of all subfolders within the chosen directory, each paired with their size, and then compares
only the contents of folders with the same weight, to prevent unnecessary comparisons. Finally, it prints the results
to the console, and offers to delete duplicated folders for you. The deleting function has not been thoroughly tested
and might misbehave, although it has worked well for me.

This program will not address folders that are not identical: it will only help cull perfect copies.
Hidden files or those whose name begins with "." or ".." aren't accounted for.

Lightly tested on Windows 10.
"""

duplicateslist = set()


def get_directory():
    print("\nThis program looks through a directory, including all subdirectories, and identifies duplicated files.")
    while True:
        userinput = input("Enter directory or enter \"q\" to quit program:\n")
        if os.path.isdir(userinput):
            return userinput
        elif userinput in {"q", "Q"}:
            exit()
        else:
            print("Not a valid directory\n")


def map_directory(directorypath):
    directories = {}
    for root, dirs, files in os.walk(directorypath, topdown=True):
        for name in dirs:
            path = os.path.join(root, name)
            size = get_folder_size(path)
            directories[path] = size
    return directories


def get_folder_size(folder):
    totalsize = 0
    for root, dirs, files in os.walk(folder):
        for file in files:
            filepath = os.path.join(root, file)
            totalsize += os.path.getsize(filepath)
    return totalsize


def compare_directory(directorydictionary):
    duplicatesdict = {}
    for key, value in directorydictionary.items():  # Reverse keys and values
        if value in duplicatesdict:
            duplicatesdict[value].append(key)
        else:
            duplicatesdict[value] = [key]
    for size, folders in duplicatesdict.items():  # Compare contents of the folders to mark real duplicates
        if len(folders) > 1:
            for i in range(len(folders)):
                for j in range(i + 1, len(folders)):
                    compareobject = filecmp.dircmp(folders[i], folders[j])
                    if not compareobject.diff_files and not compareobject.left_only and not compareobject.right_only:
                        duplicateslist.add(folders[j])
    return


def delete_duplicates():
    while True:
        userinput = input("\nWould you like to delete the duplicated folders, including ALL their contents? This action cannot be undone. WARNING: this function was barely tested. y/n\n")
        if userinput in {"n", "no", "N", "No", "q", "Q"}:
            print("The duplicated folders won't be deleted. Exiting program")
            return
        elif userinput in {"y", "yes", "Y", "Yes"}:
            userinput = input("Are you sure? This function has not been tested thoroughly! y/n\n")
            if userinput in {"n", "no", "N", "No", "q", "Q"}:
                print("The duplicated folders won't be deleted. Exiting program\n")
                return
            elif userinput in {"y", "yes", "Y", "Yes"}:
                print("Deleting...")
                for directory in duplicateslist:
                    try:
                        print("Deleting " + directory)
                        shutil.rmtree(directory)
                    except PermissionError as e:
                        print(f"Permission error found: {e}. Try running this program as Administrator. Exiting program\n")
                        pass
                print("\nThe duplicated folders should have been deleted now. Exiting program\n")
                return
            else:
                print("Please enter y to delete duplicated folders or n to close the program")
        else:
            print("Please enter y to delete duplicated folders or n to close the program")


def main():
    compare_directory(map_directory(get_directory()))
    if not duplicateslist:
        print("No duplicated folders found! Exiting program\n")
        return
    else:
        print("\nThe following folders are perfect copies of other already existing ones")
        for directory in duplicateslist:
            print(directory)
        delete_duplicates()
    return


if __name__ == '__main__':
    main()
