# Duplicate-removal
This program identifies duplicated folders and subfolders. Not duplicated files! The purpose is shallow but fast
identification of duplicated folders in a relative's external backup HDD, which contained a terabyte of data
mostly comprised of dozens of copies of the same few folders. It succesfully fulfilled this task.

The program creates a dictionary of all subfolders within the chosen directory, each paired with their size, and then compares
only the contents of folders with the same weight, to prevent unnecessary comparisons. Finally, it prints the results
to the console, and offers to delete duplicated folders for you.

This program will not address folders that are not identical: it will only help cull perfect copies.
Hidden files or those whose name begins with "." or ".." aren't accounted for.

It is a simple script and should run in the command line without issues.

Lightly tested on Windows 10.
