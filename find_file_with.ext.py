import os
from genericpath import isdir, isfile
from pathlib import Path
import shutil


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


DOWNLOADS_FOLDER = str(Path.home() / "Downloads")
os.chdir(DOWNLOADS_FOLDER)
CWD = os.getcwd()

print(CWD)

# DONE file extension menu repeat if no files found - if files found main_menu_options else no files found options
# DONE submenus for search in files
# DONE Move files -> list available dirs and choose one or create new one to move files to
# TODO auto organizer -> create dirs named with files extension and move each file with that extension into it
# DONE Add menu to list all available extensions
# TODO Add comments

main_menu_options = {
    1: "Delete files",
    2: "Search in files",
    3: "Move files",
    4: "Search for another extension",
    5: "List all extensions in the folder",
    6: 'AutoOrganizer*',
    9: "Exit",
}

confirm_options = {1: "Yes", 2: "No - go back"}

auto_organizer_options = {1: "Run AutoOrganizer*", 2: "No - go back"}

global file_list
file_list = []


def print_files():
    print(f"{bcolors.OKGREEN}{len(file_list)} files found: {bcolors.ENDC}")
    for file in file_list:
        print(file)


def fill_file_list(ext):
    if ext == "*":
        for file in os.listdir(CWD):
            if isfile(file):
                file_list.append(file)
    else:
        for file in os.listdir(CWD):
            if isfile(file) and file.endswith(ext):
                file_list.append(file)


def extension_select_menu():
    ext = input(
        f"{bcolors.HEADER}Please specify file extension (Fill * to choose all files): {bcolors.ENDC}"
    ).lower()

    fill_file_list(ext)

    while True:
        if len(file_list) == 0:
            print("No files with that extension found. Try another")
            ext = input(
                f"{bcolors.HEADER}Please specify another file extension (Fill * to choose all files): {bcolors.ENDC}"
            ).lower()

            fill_file_list(ext)
        else:
            print_files()
            break


def print_menu(options):
    print(f"{bcolors.OKBLUE}Select option: {bcolors.ENDC}")
    for key in options.keys():
        print(f"{bcolors.UNDERLINE}{key} -- {options[key]}{bcolors.ENDC}")


def delete_files():
    for file in file_list:
        try:
            os.remove(file)
            print(f"{bcolors.OKGREEN}{file} deleted. {bcolors.ENDC}")
        except:
            print(f"The file {file} doesn't exist or could not be deleted")
            pass


def search_in_files(search_string):
    for fname in file_list:
        f = open(fname, "r", encoding="utf8")

        if search_string in f.read():
            print(
                f"Found search string in {bcolors.OKGREEN}{fname}{bcolors.ENDC}")
            print(f"{bcolors.BOLD}Results in the file: {bcolors.ENDC}")

            with open(fname, encoding="utf8") as f:
                lines = [line.rstrip() for line in f]

            count = 0
            for line in lines:
                if search_string in line:
                    count = 1
                    print(f"Line {count}: {line}")
            print()


def move_files():
    directories = [d for d in os.listdir(CWD) if isdir(d)]
    print("List of directories:")
    for dir in directories:
        print(dir)
    selected_folder = input(
        f"{bcolors.OKCYAN}Please copy/paste folder you wish to move files to (if it does not exist it will be created): {bcolors.ENDC}")
    if selected_folder not in directories:
        print(
            f"{bcolors.FAIL}The folder {selected_folder} was not found! Create this folder?")
        print_menu(confirm_options)
        action = int(
            input(f"{bcolors.OKBLUE}Please select option: {bcolors.ENDC}"))

        if action == 1:
            os.mkdir(selected_folder)
            print(
                f"{bcolors.OKGREEN}Created directory {selected_folder}{bcolors.ENDC}")

    print(f"Moving files to {selected_folder} subfolder")

    for file in file_list:
        source = CWD + "\\" + file
        destination = CWD + "\\" + selected_folder + "\\" + file
        shutil.move(source, destination)
        print(f"{file} moved in {destination}")


def delete_files_menu():
    while True:
        print_menu(confirm_options)
        try:
            option = int(
                input(f"{bcolors.OKBLUE}Please select option: {bcolors.ENDC}"))
        except:
            print("Wrong input. Please enter a number ...")

        if option == 1:
            delete_files()
            break
        else:
            break


def search_in_files_menu():
    search_string = input(
        f"{bcolors.OKCYAN}Please specify string you want to look for into the selected files: {bcolors.ENDC}"
    )
    while True:

        search_in_files(search_string)
        print_menu(confirm_options)
        try:
            option = int(
                input(f"{bcolors.OKBLUE}Search another string? {bcolors.ENDC}")
            )
        except:
            print("Wrong input. Please enter a number ...")
        if option == 1:
            search_string = input(
                f"{bcolors.OKCYAN}Please specify string you want to look for into the selected files: {bcolors.ENDC}"
            )
            search_in_files(search_string)
        else:
            break


def list_all_extensions():
    extensions = {}
    for file in os.listdir(CWD):
        if isfile(file):
            file_name_splitter = file.split(".")
            if len(file_name_splitter) > 1:
                extension = file_name_splitter[-1]
                if extension in extensions:
                    extensions[extension] += 1
                else:
                    extensions[extension] = 1
    for ext, count in extensions.items():
        print(f"{ext}: found {count}")




def auto_organizer():
    print('This is AutoOrganizer*')
    print("It will find all files in the root of this folder, check for their extensions, create folders named after each extension (if it doesn't exist) and move files into the corresponding directory")
    print_menu(auto_organizer_options)
    option = int(
        input(f"{bcolors.OKBLUE}Please select option: {bcolors.ENDC}"))
    if option == 1:
        extensions = []
        for file in os.listdir(CWD):
            if isfile(file):
                file_name_splitter = file.split(".")
                if len(file_name_splitter) > 1:
                    extension = file_name_splitter[-1]
                    extensions.append(extension)
        
        list_dir = [d for d in os.listdir(CWD) if isdir(d)]
        
        for ext in extensions:
            current_files = [f for f in os.listdir(CWD) if isfile(f) and f.endswith(ext)]
            if ext.upper() not in list_dir:
                os.mkdir(ext.upper())
                list_dir.append(ext.upper())
                print(f"{bcolors.OKGREEN}Created subdirectory named {ext.upper()}{bcolors.ENDC}")

            for file in current_files:
                source = CWD + "\\" + file
                destination = CWD + "\\" + ext.upper() + "\\" + file
                shutil.move(source, destination)
                print(
                    f"{bcolors.OKGREEN}{file} moved in {destination}{bcolors.ENDC}")

        f"{bcolors.OKGREEN}All files moved{bcolors.ENDC}"

        for dir in list_dir:
            files_count = len(os.listdir(dir))
            new_dir_name = f"AutoOptimizer-{dir}--has-{files_count}-in-it"
            os.rename(dir, new_dir_name)
                



def main():
    extension_select_menu()
    while True:
        print()
        print_menu(main_menu_options)
        option = ""
        try:
            option = int(
                input(f"{bcolors.OKBLUE}Please select option: {bcolors.ENDC}"))
        except:
            print("Wrong input. Please enter a number ...")

        if option == 1:
            delete_files_menu()
        elif option == 2:
            search_in_files_menu()
        elif option == 3:
            move_files()
        elif option == 4:
            global file_list
            file_list = []
            extension_select_menu()
        elif option == 5:
            list_all_extensions()
        elif option == 6:
            auto_organizer()
        elif option == 9:
            print("Exiting script...")
            exit()
        else:
            print("Wrong input. Please enter number from 1 to 4 to select action")


if __name__ == "__main__":
    main()
