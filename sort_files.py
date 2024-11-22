import os
import shutil


def sort_evcg(current_dir):
    files = os.listdir(current_dir)
    for filename in files:
        # if os.path.basename(filename) != "sort_files.py":
        #     parts = os.path.basename(filename).split('_')
        #     folder_dir = os.path.join(current_dir, parts[0])
        #     if not os.path.exists(folder_dir):
        #         os.makedirs(folder_dir)
        #     diff_dir = os.path.join(folder_dir, "差分")
        #     if not os.path.exists(diff_dir):
        #         os.makedirs(diff_dir)
        #     if parts[3][:2] == "ev":
        #         shutil.move(filename, folder_dir)
        #         print(f"Move {filename} to {folder_dir}")
        #     else:
        #         shutil.move(filename, diff_dir)
        #         print(f"Move {filename} to {diff_dir}")
        parts=os.path.basename(filename).split('.')[0].split('_')
        folder_dir=os.path.join(current_dir,"_".join(parts[0:2]))
        if not os.path.exists(folder_dir):
            os.makedirs(folder_dir)
        diff_dir = os.path.join(folder_dir, "差分")
        if not os.path.exists(diff_dir):
            os.makedirs(diff_dir)
        if len(parts)==2:
            shutil.move(filename, folder_dir)
            print(f"Move {filename} to {folder_dir}")
        else:
            shutil.move(filename, diff_dir)
            print(f"Move {filename} to {diff_dir}")


def sort_chr(current_dir):
    files = os.listdir(current_dir)
    for filename in files:
        if os.path.basename(filename) != "sort_files.py":
            parts = os.path.basename(filename).split('_')
            folder_dir = os.path.join(current_dir, parts[0])
            if not os.path.exists(folder_dir):
                os.makedirs(folder_dir)
            diff_dir = os.path.join(folder_dir, "差分")
            if not os.path.exists(diff_dir):
                os.makedirs(diff_dir)
            if parts[3][:2] == "ch":
                shutil.move(filename, folder_dir)
                print(f"Move {filename} to {folder_dir}")
            else:
                shutil.move(filename, diff_dir)
                print(f"Move {filename} to {diff_dir}")


def sort_bgm(dir):
    folders = os.listdir(dir
                         )
    for folder in folders:
        subfolder = os.path.join(dir, folder, "acb", "awb")
        files = os.listdir(subfolder)
        for file in files:
            shutil.move(os.path.join(subfolder, file), os.path.join(dir, file))


def sort_png(current_dir):
    files = os.listdir(current_dir)
    for file in files:
        if os.path.basename(file) != "sort_files.py":
            type = os.path.basename(file).split('_')[0]
            type_folder = os.path.join(current_dir, type)
            if not os.path.exists(type_folder):
                os.makedirs(type_folder)
            shutil.move(os.path.join(os.path.dirname(file), os.path.basename(file)),
                        os.path.join(type_folder, os.path.basename(file)))
            print(f"Move {file} to {type_folder}")
    print("Done")




sort_evcg(os.getcwd())
