import os
import sys
import hashlib
from os import path
from glob import glob
from multiprocessing import Pool


CHUNK_SIZE = 100 * 1024 * 1024

def md5sum(file_path: str, chunk_size: int=CHUNK_SIZE) -> str:
    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            md5.update(chunk)
    return file_path, md5.hexdigest()


def main(files_dir: str, file_extension: str, reference: str) -> None:
    md5, ref = dict(), dict()
    input_files = glob(path.join(files_dir, f"*{file_extension}"))
    nproc = min(2 * os.cpu_count(), len(input_files))
    with Pool(nproc) as pp:
        md5_results = pp.map_async(md5sum, input_files)

        with open(reference, "rt") as f:
            for ln in filter(None, map(str.strip, f)):
                hash_value, file_path = ln.split(maxsplit=1)
                ref[path.basename(file_path)] = hash_value

        for file_path, hash_value in md5_results.get():
            md5[path.basename(file_path)] = hash_value

    for file_name, hash_value in ref.items():
        if md5.get(file_name, '') == hash_value:
            status = "OK"
        else:
            status = "FAIL"
        print(f"{file_name:>35} ------------------------------- {status}")


if __name__ == "__main__":
    main(*sys.argv[1:]) 
