import flet as ft
import ffmpeg
import os
import subprocess
import time
import re

def main(page:ft.Page):
    page.title = "ffmpegGUI"
    page.window_height = 600
    page.window_width = 800
    page.padding = 16
    useGPU = False

    def printText(e):
        openpickdialog()

    
    # ファイルを選択するなど
    class FilePick:
        def __init__(self):
                self.inputFile = ""
                self.inputFile_path = ""
                self.inputFile_dir = ""
                self.inputFile_name = ""
        def on_file_picked(self, e: ft.FilePickerResultEvent):
            if e.files:
                self.inputFile_path = e.files[0].path
                self.inputFile = e.files[0].name
                self.inputFile_name = os.path.splitext(os.path.basename(self.inputFile))[0]
                self.inputFile_dir = os.path.dirname(self.inputFile_path)
                kakunin()
    
    file_picked = FilePick()

    default_kakunin = f"ファイル名: \nファイル: \nパス: \nフルパス: "

    def openpickdialog():
        pick_file_dialog.pick_files(allow_multiple=False,allowed_extensions=["mp4","mp3","avi","wav","flac","mov","webm"])
    def kakunin():
        kakunin_text.value = f"ファイル名: {file_picked.inputFile_name}\nファイル: {file_picked.inputFile}\nパス: {file_picked.inputFile_dir}\nフルパス: {file_picked.inputFile_path}"
        kakunin_text.update()

    def format_change(e):
        if format_dd.value == "mp4":
            GPUsw.disabled = False
            GPUsw.visible = True
            GPUsw.update()
        else:
            GPUsw.disabled = True
            GPUsw.visible = False
            GPUsw.update()

    def conv(input,output,fmt,opt):
        if fmt == "mp4":
            if opt == True:
                cmd = f'ffmpeg -i "{input}" -vcodec h264_nvenc -b:v 8M "{output}"'
                p = subprocess.Popen(cmd,shell=True)
                p.wait()
                return p.returncode
            else:
                cmd = f'ffmpeg -i "{input}" -vcodec libx264 -b:v 8M "{output}"'
                p = subprocess.Popen(cmd,shell=True)
                p.wait()
                return p.returncode
        elif fmt == "mp3":
            cmd = f'ffmpeg -i "{input}" -acodec mp3 -b:a 192k "{output}"'
            p = subprocess.Popen(cmd,shell=True)
            p.wait()
            return p.returncode
        elif fmt == "wav":
            cmd = f'ffmpeg -i "{input}" "{output}"'
            p = subprocess.Popen(cmd,shell=True)
            p.wait()
            return p.returncode

    def start_process(e):
        if file_picked.inputFile_path and format_dd.value:
            error_text.value = "処理しています"
            start_btn.disabled = True
            progress.visible = True
            progress.update()
            error_text.update()
            start_btn.update()
            output = f"{file_picked.inputFile_dir}/{file_picked.inputFile_name}.{format_dd.value}"
            while os.path.exists(output):
                base_name,extension = os.path.splitext(output)
                output = f"{base_name}-conv{extension}"

            result = conv(file_picked.inputFile_path,output,format_dd.value,GPUsw.value)

            if result == 0:
                print("処理が正常に終了しました")
                error_text.value = "完了しました!!"
                start_btn.disabled = False
                error_text.update()
                start_btn.update()
                progress.visible = False
                progress.update()
                time.sleep(3)
                error_text.value = ""
                error_text.update()
            else:
                print("エラーが発生しました。")
        else:
            error_text.value = "ファイル・フォーマットを選択してください。"
            error_text.update()
            time.sleep(3)
            error_text.value = ""
            error_text.update()
            return
        
    
    file_picked = FilePick()

    # 要素など
    logo = ft.Text("ffmpegGUI",style=ft.TextThemeStyle.HEADLINE_MEDIUM)
    file_pick_btn = ft.FilledButton("ファイルを選択",width=page.window_width,on_click=printText,expand=True)
    kakunin_text = ft.TextField(label="選択したファイル情報",multiline=True,min_lines=4,max_lines=4,read_only=True,value=default_kakunin,)
    start_btn = ft.FilledButton("開始",icon=ft.icons.PLAY_ARROW,on_click=start_process)
    format_dd = ft.Dropdown(label="フォーマット",prefix_icon=ft.icons.AUDIO_FILE,options=[ft.dropdown.Option("mp4"),ft.dropdown.Option("mp3"),ft.dropdown.Option("wav")],on_change=format_change)
    GPUsw = ft.Switch(label="NVENCでエンコード",value=False,disabled=True,visible=False)
    progress = ft.ProgressBar(width=page.window_width,visible=False)
    error_text = ft.Text("")
    start_aria = ft.Row([
        start_btn,error_text,
    ],)
    
    # FilePicker
    pick_file_dialog = ft.FilePicker(on_result=file_picked.on_file_picked)
    page.overlay.append(pick_file_dialog)
    

    page.add(
        logo,
        ft.Row([file_pick_btn,]),
        kakunin_text,
        format_dd,
        GPUsw,
        start_aria,
        progress,
    )

ft.app(target=main)