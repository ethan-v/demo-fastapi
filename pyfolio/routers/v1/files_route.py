from fastapi import APIRouter, UploadFile, BackgroundTasks
from os import path
from PIL import Image
from pyfolio.configs.app import appConfigs

router = APIRouter()


# Resize images for different devices
def resize_image(file_path: str):
    sizes = [{
        "width": 1280,
        "height": 720
    }, {
        "width": 640,
        "height": 480
    }]

    basename = path.basename(file_path)
    file_name, file_extension = path.splitext(basename)

    for size in sizes:
        size_defined = size['height'], size['width']
        file_path_sized = f"{path.dirname(file_path)}/{file_name}_{str(size['height'])}{file_extension}"
        image = Image.open(file_path, mode="r")
        image.thumbnail(size_defined)
        image.save(file_path_sized)
        print(f"[SUCCESS] Resize images: {file_path_sized}")


@router.post("/upload/")
async def create_upload_file(file: UploadFile, background_tasks: BackgroundTasks):

    # Save original file
    file_path = f'{appConfigs.STATICS_PATH}/{file.filename}'
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
        f.close()

    # Resize image
    background_tasks.add_task(resize_image, file_path=file_path)

    return {"filename": file.filename}
