import base64
from pathlib import Path


def get_base64_image(image_file: str, external: bool = False) -> str:
    """Gets the image from path

    :param image_file: name of the image
    :param external: if image is not in assets folder, defaults to False
    :return: string value of encoded image
    """
    if not external:
        image_path = Path(__file__).parent.parent.parent / "assets" / image_file
    return base64.b64encode(open(image_path, "rb").read()).decode("ascii")
