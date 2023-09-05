# 找到进程目录，打开它。然后置于活动前台。

import psutil
import os
import time
import pygetwindow as gw
import subprocess
import ctypes

def open_process():
    # 检查进程中是否存在 HipsDaemon.exe
    if "HipsDaemon.exe" not in (p.name() for p in psutil.process_iter()):
        print("HipsDaemon.exe 未在进程中找到。")
        return

    # 在进程列表中找到 HipsDaemon.exe 并获取其路径
    process_p_path = None
    for process in psutil.process_iter():
        if process.name() == "HipsDaemon.exe":
            process_p_path = process.exe()
            break

    # 启动 HipsMain.exe
    process_path = os.path.join(os.path.dirname(process_p_path), "HipsMain.exe")
    subprocess.Popen(process_path)

    # 等待一段时间以确保 HipsMain.exe 启动
    time.sleep(2)

    # 判断当前活动窗口是否为 HipsMain.exe
    active_window = gw.getActiveWindow()
    if active_window.title != "HipsMain.exe":
        # 检查窗口是否最小化
        if active_window.isMinimized:
            ctypes.windll.user32.ShowWindow(active_window._hWnd, 9)  # 还原窗口

        # 将窗口置于前台活动
        active_window.activate()

if __name__ == "__main__":
    # 调用函数
    open_process()