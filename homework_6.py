import sys
import shutil
# import zipfile
from pathlib import Path
from pprint import pprint

sorted_files_dict = {
    'archives': [],
    'audio': [],
    'documents': [],
    'images': [],
    'video': [],
    'unknown': []
}

# folders_to_ignore = tuple(list(sorted_files_dict.keys())[:-1])
folders_to_ignore = tuple(list(sorted_files_dict.keys()))

archives_ext_list = ['.zip', '.gz', '.tar']
audio_ext_list = ['.mp3', '.ogg', '.wav', '.amr']
documents_ext_list = ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx']
images_ext_list = ['.jpeg', '.png', '.jpg', '.svg']
video_ext_list = ['.avi', '.mp4', '.mov', '.mkv']

# archives_list = []
# audio_list = []
# documents_list = []
# images_list = []
# video_list = []
# unknown_list = []
found_extensions_list = []

CYRILLIC_SYMBOLS = list("абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ")
# TRANSLATION = list("abcdefghijklmnopqrstuvwxyz")
TRANSLATION = ("a", "b", "v", "h", "d", "e", "yo", "zh", "z", "i", "i", "k", "l", "m",
               "n", "o", "p", "r", "s", "t", "u", "f", "kh", "ts", "ch", "sh", "shch",
               "", "y", "", "e", "yu", "ya", "ie", "i", "i", "g")
BAD_SYMBOLS = ("%", "*", " ", "-", "'")

TRANS = {}
for cyr, lat in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyr)] = lat
    TRANS[ord(cyr.upper())] = lat.upper()

for i in BAD_SYMBOLS:
    TRANS[ord(i)] = "_"


def normalize(name: str) -> str:

    trans_name = name.translate(TRANS)
    return trans_name


def move_file(file: Path, root_folder: Path, category: str):
    target_folder = root_folder / category
    if not target_folder.exists():
        target_folder.mkdir()
    target_file = target_folder.joinpath(normalize(file.name))
    if target_file.exists():
        return file.replace(target_folder.joinpath(target_file.stem + '_' + target_file.suffix))
    else:
        return file.replace(target_file)


def sort_files(root_path: Path, target_path: Path):

    # for item in target_path.glob('**/*'):
    for item in target_path.glob('*'):
        if item.is_dir():
            if item.name in folders_to_ignore:
                continue
            else:
                sort_files(root_path, item)
                item.rmdir()

        if item.is_file():
            if item.suffix.lower() in archives_ext_list:
                # print(f'Archive: {item.name}')
                cat = 'archives'
                sorted_files_dict[cat].append(item)
                replaced_file = move_file(item, root_path, cat)
                # with zipfile.ZipFile(replaced_file, 'r') as zf:
                #    print(zf.namelist())
                shutil.unpack_archive(
                    replaced_file, replaced_file.parent.joinpath(replaced_file.stem))
                replaced_file.unlink()

            elif item.suffix.lower() in audio_ext_list:
                # print(f'Audio: {item.name}')
                cat = 'audio'
                sorted_files_dict[cat].append(item)
                move_file(item, root_path, cat)
            elif item.suffix.lower() in documents_ext_list:
                # print(f'Documents: {item.name}')
                cat = 'documents'
                sorted_files_dict[cat].append(item)
                move_file(item, root_path, cat)
            elif item.suffix.lower() in images_ext_list:
                # print(f'Images: {item.name}')
                cat = 'images'
                sorted_files_dict[cat].append(item)
                move_file(item, root_path, cat)
            elif item.suffix.lower() in video_ext_list:
                # print(f'Video: {item.name}')
                cat = 'video'
                sorted_files_dict[cat].append(item)
                move_file(item, root_path, cat)
            else:
                # print(f'Unknown: {item.name}')
                cat = 'unknown'
                sorted_files_dict[cat].append(item)
                move_file(item, root_path, cat)

            found_extensions_list.append(item.suffix.lower())


def main():
    try:
        target_folder = Path(sys.argv[1])
        # target_folder = Path(
        #    r'/Users/alex/Documents/Python_Test/Unsorted_Files')
    except IndexError:
        return 'You need to write the target folder as a parameter.'
        # print(Path.cwd())

    if not target_folder.exists():
        return 'Sorry, this folder does not exist.'

    sort_files(target_folder, target_folder)

    if len(found_extensions_list) > 0:
        pprint(sorted_files_dict)
        found_extensions = set(found_extensions_list)
        print(f"Found_extensions: {found_extensions}")
        # print(TRANS)
    else:
        print("Nothing to sort...")
    return "All done!"


if __name__ == "__main__":
    print(main())
