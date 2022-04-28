from pathlib import Path
from typing import Optional

import typer
from typer import Typer

from media_extractor.core import extract_directory_media

app = Typer()


@app.command()
def extract(
    source_path: Path = typer.Argument(..., exists=True, dir_okay=True, readable=True, resolve_path=True),
    dest_path: Path = typer.Argument(..., writable=True),
    media_types: str = typer.Option("video,image"),
    max_file_size_in_mb: Optional[int] = typer.Option(100)
):
    total_files, total_size, total_failed = extract_directory_media(source_path, dest_path, tuple(media_types.split(",")), max_file_size_in_mb)
    typer.echo(f"Files extracted: {total_files}. Total size: {total_size:,.0f} MB. Total failed: {total_failed}.")
