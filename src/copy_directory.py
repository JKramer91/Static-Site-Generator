import os
import shutil

def source_to_destination(src, dst):
    directory = os.listdir(src)
    for item in directory:
        src_path = os.path.join(src, item)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst)
        else:
            dst_path = os.path.join(dst, item)
            os.mkdir(dst_path)
            source_to_destination(src_path, dst_path)