import os
from pathlib import Path

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# DONE file extension menu repeat if no files found - if files found main_menu_options else no files found options 
# DONE submenus for search in files
# TODO Move files -> list available dirs and choose one or create new one to move files to
# TODO auto organizer -> create dirs named with files extension and move each file with that extension into it
# TODO try to add menu to list all available extensions

DOWNLOADS_FOLDER = str(Path.home() / 'Downloads')
os.chdir(DOWNLOADS_FOLDER)
CWD = os.getcwd()


global file_list
file_list = []

def print_files():
    print(f"{bcolors.OKGREEN}{len(file_list)} files found: {bcolors.ENDC}")
    for file in file_list:
            print(file)

def fill_file_list(ext):
    for file in os.listdir(CWD):
                if file.endswith(ext):
                    file_list.append(file)

def extension_select_menu():
    ext = input(f"{bcolors.HEADER}Please specify file extension: {bcolors.ENDC}").lower()

    fill_file_list(ext)

    while True:
        if len(file_list) == 0:
            print("No files with that extension found. Try another")
            ext = input(f"{bcolors.HEADER}Please specify another file extension: {bcolors.ENDC}").lower()

            fill_file_list(ext)
        else: 
            print_files()
            break

extension_select_menu()

main_menu_options = {
    1: 'Delete files',
    2: 'Search in files',
    3: 'Move files',
    4: 'Search for another extension',
    5: 'List all extensions in the folder -- TODO',
    6: 'Exit',
}

delete_files_options = {
    1: 'Yes',
    2: 'No - go back'
}

search_files_options = {
    1: 'Yes',
    2: 'No - go back'
}


def print_menu(options):
    print(f'{bcolors.OKBLUE}Select option: {bcolors.ENDC}')
    for key in options.keys():
        print (f"{bcolors.UNDERLINE}{key} -- {options[key]}{bcolors.ENDC}" )

def delete_files():
    for file in file_list:
        try:
            os.remove(file)
            print(f'{bcolors.OKGREEN}{file} deleted. {bcolors.ENDC}')
        except:
            print(f"The file {file} doesn't exist or could not be deleted")
            pass

def search_in_files(search_string):
    for fname in file_list:
        f = open(fname, 'r', encoding='utf8')

        if search_string in f.read():
            print(f"Found search string in {bcolors.OKGREEN}{fname}{bcolors.ENDC}")
            print(f"{bcolors.BOLD}Results in the file: {bcolors.ENDC}")
            
            with open(fname, encoding='utf8') as f:
                lines = [line.rstrip() for line in f]
            
            count = 0
            for line in lines:
                if search_string in line:
                    count +=1
                    print(f"Line {count}: {line}")
            print()


def move_files():
    print(f'{bcolors.WARNING}Files moved. {bcolors.ENDC}')



def main():
    while True:
        print()
        print_menu(main_menu_options)
        option = ''
        try: 
            option = int(input(f'{bcolors.OKBLUE}Please select option: {bcolors.ENDC}'))
        except: 
            print('Wrong input. Please enter a number ...')
           
        if option == 1:
            while True:
                print_menu(delete_files_options)
                try:
                    option = int(input(f'{bcolors.OKBLUE}Please select option: {bcolors.ENDC}'))
                except: 
                    print('Wrong input. Please enter a number ...')

                if option == 1:
                    delete_files()
                    break
                else:
                    break
        elif option == 2:
            search_string = input(f"{bcolors.OKCYAN}Please specify string you want to look for into the selected files: {bcolors.ENDC}")
            while True:
                
                search_in_files(search_string)

                print_menu(search_files_options)
                try:
                    option = int(input(f'{bcolors.OKBLUE}Search another string? {bcolors.ENDC}'))
                except:
                    print('Wrong input. Please enter a number ...')

                if option == 1:
                    search_string = input(f"{bcolors.OKCYAN}Please specify string you want to look for into the selected files: {bcolors.ENDC}")
                    search_in_files(search_string)
                else:
                    break
                

        elif option == 3:
            move_files()
        elif option == 4:
            global file_list
            file_list = []
            extension_select_menu()
        elif option == 5:
            print('Exiting script...')
            exit()
        else:
             print('Wrong input. Please enter number from 1 to 4 to select action')


if __name__ == "__main__":
    main()

