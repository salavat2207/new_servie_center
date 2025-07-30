import uuid
from fastapi import UploadFile
from pathlib import Path

UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def upload_image(file: UploadFile, folder: str = "") -> str:
    """Сохраняет изображение и возвращает путь к файлу."""
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    target_folder = UPLOAD_DIR / folder
    target_folder.mkdir(parents=True, exist_ok=True)

    file_path = target_folder / filename
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return str(file_path.relative_to("static"))