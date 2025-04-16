from PIL import Image
import pillow_heif
import os
from pathlib import Path

def make_output_path(input_path: Path, output_extention: str) -> Path:
    return Path(os.path.splitext(input_path)[0] + "." + output_extention)

def convert_heic_to_others(input_path: Path, output_extention: str) -> None:
    heif_file = pillow_heif.read_heif(input_path)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
    )

    output_path = make_output_path(input_path, output_extention)
    image.save(output_path)
    print(f"変換完了: {output_path}")

if __name__ == "__main__":
    input_path = Path("example.HEIC")
    output_extention = "jpg"  # 変換先の拡張子を指定
    convert_heic_to_others(input_path, output_extention)