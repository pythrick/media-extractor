import logging
import os
import mimetypes
import shutil
from pathlib import Path

mimetypes.init()


def extract_directory_media(directory_path: Path, base_dest_path: Path, media_types: tuple[str, ...], max_file_size_in_mb: int | None = None) -> tuple[int, float, int]:
    total_size = 0
    total_files = 0
    total_failed = 0
    ignore_file_size = max_file_size_in_mb is None
    for root, dirs, files in os.walk(directory_path):
        dest_path = base_dest_path / root.replace(str(directory_path), "").strip("/")
        for file in files:
            file_path = os.path.join(root, file)
            logging.debug(f"Extracting '{file_path}'...")
            media_type = mimetypes.guess_type(file_path)[0]
            if media_type is None:
                continue
            mime_start = media_type.split('/')[0]
            if mime_start not in media_types:
                continue
            file_size = get_megabytes(os.path.getsize(file_path))
            if not ignore_file_size and file_size > max_file_size_in_mb:
                should_proceed = input(f"File '{file_path}' has {file_size:,.0f} MB. Would you like to proceed? [Y]es/[n]o /[a]lways)").lower()
                if should_proceed == "n":
                    continue
                if should_proceed == "a":
                    ignore_file_size = True
            if not dest_path.exists():
                dest_path.mkdir(parents=True, exist_ok=True)
            dest_file_path = dest_path / file_path

            if dest_file_path.exists() and os.path.getsize(dest_file_path) == file_size:
                continue
            try:
                shutil.copy2(file_path, dest_path)
            except Exception as e:
                logging.warning(f"File '{file_path}' failed.", exc_info=e)
                total_failed += 1
            total_size += file_size
            total_files += 1
    return total_files, total_size, total_failed


def get_megabytes(value):
    return value / float(1 << 20)
