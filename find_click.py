# 以手动火绒升级为例子

"""
1.首先判断是否存在火绒窗口，如没有，则打开进程  pygetwindow
2.判断火绒窗口是否为前置，如没有，则前置
3.对当前屏幕截图，与images目录中图片进行对比
4.对匹配大于99的位置，定位坐标系
5.对坐标系单击  pyautogui
"""

import os
import cv2
import numpy as np
import pyautogui

def find_and_click_images():
    # 创建保存截图的目录
    screenshot_folder = './screenshot'
    os.makedirs(screenshot_folder, exist_ok=True)

    # 获取当前目录中的子目录中的images文件夹路径
    images_folder = os.path.join(f'./images')

    # 获取images文件夹中的所有图像文件
    image_files = sorted([f for f in os.listdir(images_folder) if f.endswith('.png')])

    # 循环处理每个图像文件
    for image_file in image_files:
        retry_count = 5  # 重试次数
        while retry_count > 0:
            # 加载当前屏幕截图
            screenshot = pyautogui.screenshot()
            screenshot = np.array(screenshot)
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

            # 加载当前图像文件
            image_path = os.path.join(images_folder, image_file)
            template = cv2.imread(image_path)

            # 解析图像文件名中的参数
            params = image_file[:-4].split('-')
            order = int(params[0])
            position = params[1]
            offset_x = int(params[2])
            offset_y = int(params[3])

            # 使用模板匹配找到图像在屏幕截图中的位置
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            print("匹配图为",image_file,"匹配值为",max_val,"匹配坐标为",max_loc)

            # 如果匹配值大于98，则确认位置并保存匹配的截图
            if max_val > 0.98:

                # 计算匹配的坐标
                # 坐标系，减法-x为向左，-y为向下。+x为向右,+y为向上
                if position == 'left':
                    match_x, match_y = max_loc[0] + offset_x, max_loc[1] + offset_y     # 左上角为顶点，向右下添加偏移
                elif position == 'mid':
                    match_x, match_y = max_loc[0] + template.shape[1] // 2 + offset_x, max_loc[1] + template.shape[0] // 2 + offset_y   # 匹配的坐标系中间，向右下添加偏移
                elif position == 'right':
                    match_x, match_y = max_loc[0] + template.shape[1] - offset_x, max_loc[1] + template.shape[0] - offset_y     #右下角向左上偏移
                    # match_x, match_y = max_loc[0] + template.shape[1] - offset_x, max_loc[1] + template.shape[0] + offset_y  右下角向左下偏移
                    # match_x, match_y = max_loc[0] + template.shape[1] + offset_x, max_loc[1] + template.shape[0] - offset_y  右下角向右上偏移
                # 截取60x60的图片
                cropped_image = screenshot[match_y:match_y+60, match_x:match_x+60]

                # 保存截图
                sc_filename = f"sc-{order:04d}.png"
                sc_filepath = os.path.join(screenshot_folder, sc_filename)
                cv2.imwrite(sc_filepath, cropped_image)
                
                pyautogui.click(match_x, match_y)
                break  # 跳出重试循环

            retry_count -= 1
            pyautogui.sleep(1)
            
if __name__ == "__main__":
    find_and_click_images()