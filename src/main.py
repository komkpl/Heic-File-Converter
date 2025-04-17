import flet as ft
from PIL import Image
import pillow_heif
import os
from pathlib import Path

def make_output_path(input_path: Path, output_extention: str) -> Path:
    return Path(os.path.splitext(input_path)[0] + "." + output_extention)

def convert_heic_to_others(input_path: Path, output_extention: str) -> Path:
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
    return output_path


def main(page: ft.Page):
    page.title = "HEIC to JPG Converter"
    selected_paths: list[str] = []

    progress_bar = ft.ProgressBar(width=400, value=0)
    progress_text = ft.Text(value="Progress: 0 / 0")
    selected_files = ft.Text()
    converted_files = ft.Text()
    selected_files.value = "No files selected"
    
    def pick_files_result(e: ft.FilePickerResultEvent):
        if not e.files:
            selected_files.value = "Cancelled"
            page.update()
            return
        
        selected_files.value = "\n".join(f.name for f in e.files)
        selected_paths.clear()
        selected_paths.extend(f.path for f in e.files)
        print(f"選択されたファイル: {selected_files.value}")

        # 進捗バーの初期化
        progress_bar.value = 0
        progress_text.value = f"Progress: 0 / {len(selected_paths)}"
        page.update()

    
    # HEIC -> JPGに変換
    def convert_button_clicked(e):
        total = len(selected_paths)
        if total == 0:
            converted_files.value = "No files selected"
            return
        for i, path in enumerate(selected_paths, start=1):
            try:
                output_path = convert_heic_to_others(path, "jpg")
                converted_files.value = f"変換完了: {output_path}"

            except Exception as e:
                print(f"変換失敗: {path} -> {e}")
                converted_files.value = f"変換失敗: {path} -> {e}"
                return
            
            # 進捗更新
            progress_bar.value = i / total
            progress_text.value = f"Progress: {i} / {total}"
            page.update()
        
        progress_text.value += "✅ Done!"
        page.update()


    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)

    # UI配置
    page.add(
        ft.Column(
            [
                ft.Column(
                    [
                        ft.Row(
                        [
                            ft.ElevatedButton(
                                "Pick HEIC Files",
                                icon=ft.Icons.UPLOAD_FILE,
                                on_click=lambda _: pick_files_dialog.pick_files(
                                    allow_multiple=True,
                                    allowed_extensions=["heic", "HEIC"],
                                    dialog_title="Select HEIC files to convert",
                                ),
                            ),
                            selected_files,
                        ],
                    ),
                        ft.ElevatedButton(
                            "Convert",
                            icon=ft.Icons.SAVE,
                            on_click=convert_button_clicked,
                        ),
                        converted_files,
                    ],
                    spacing=20,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([progress_bar], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Row([progress_text], alignment=ft.MainAxisAlignment.CENTER),
                        ],
                        spacing=5,
                    ),
                    padding=10,
                    alignment=ft.alignment.bottom_center,
                )
            ],
            spacing=20,
            expand=True,
        )
    )



ft.app(main)