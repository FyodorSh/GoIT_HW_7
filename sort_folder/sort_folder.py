import re
import sys
import os
import zipfile
import py7zr
import patoolib

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

EXTENSIONS = {('JPEG', 'PNG', 'JPG', 'SVG'): "images", ('AVI', 'MP4', 'MOV', 'MKV'): "video",
              ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'): "documents",  ('MP3', 'OGG', 'WAV', 'AMR'): "audio",
              ('ZIP', 'RAR', '7ZIP', '7Z', 'GZ', 'TAR'): "archives"}

SORT_DIRS = {}
SORT_DIRS_LIST = []

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def translit(input_string: str) -> str:
    return input_string.translate(TRANS)


def normalize(file_name: str):
    regex = r"[^a-zA-Z0-9.]"
    subst = "_"
    file_name = re.sub(regex, subst, translit(file_name), 0, re.MULTILINE)
    return file_name


def check_dir(current_path: str, if_empty_delete=False):
    for file in os.listdir(current_path):
        file_path = os.path.join(current_path, file)
        if file_path in SORT_DIRS_LIST:
            continue

        if os.path.isdir(file_path):
            if len(os.listdir(file_path)) == 0:
                if if_empty_delete:
                    os.removedirs(file_path)
                    continue
            else:
                check_dir(file_path)
                continue
        file_name_split = os.path.splitext(file)
        file_ext = file_name_split[1].replace(".", "").upper()

        for ext in EXTENSIONS:
            if file_ext in ext:
                directory = EXTENSIONS.get(ext)
                sort_dir = SORT_DIRS.get(directory)
                new_file_name = os.path.join(sort_dir, normalize(file))
                os.replace(file_path, new_file_name)
                if directory == "archives":
                    try:
                        extract_path = os.path.join(sort_dir, normalize(file_name_split[0]))
                        if file_ext == "7Z":
                            archive = py7zr.SevenZipFile(new_file_name, mode='r')
                            archive.extractall(path = extract_path)
                            archive.close()
                        elif file_ext == "RAR":
                            patoolib.extract_archive(new_file_name, outdir=extract_path, interactive=False)
                        else:
                            with zipfile.ZipFile(new_file_name, 'r') as zip_ref:
                                zip_ref.extractall(extract_path)
                        os.remove(new_file_name)
                        print(f"{new_file_name} extracted")
                    except:
                        print(f"{file} not zip archive")
                else:
                    print(f'"{file}" removed and renamed to folder "{directory}"')


def create_sort_dir(start_path: str):
    for ext in EXTENSIONS:
        sort_dir = EXTENSIONS.get(ext)
        sort_dir_path = os.path.join(start_path, sort_dir)
        if not os.path.exists(sort_dir_path):
            os.mkdir(sort_dir_path)
        SORT_DIRS.update({sort_dir: sort_dir_path})
        SORT_DIRS_LIST.append(sort_dir_path)


def clean():
    if len(sys.argv) < 2:
        print('Enter path to folder which should be cleaned')
        exit()

    start_path = sys.argv[1]
    create_sort_dir(start_path)
    check_dir(start_path)
    check_dir(start_path, True) # delete empty folders
    print("Sorting complete.")


if __name__ == '__main__':
    clean()