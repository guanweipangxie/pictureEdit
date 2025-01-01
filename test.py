import cv2
import os
import easyocr
import numpy as np
from PIL import Image, ImageTk
import time
from tkinter import Tk, Button, Label, filedialog

# 加载EasyOCR读取器，加载英文和中文模型，支持多种语言
reader = easyocr.Reader(['en', 'ch_sim']) 

def select_and_recognize_image():
    """
    选择图片并进行识别，在界面上展示结果
    """
    file_path = filedialog.askopenfilename()
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在，请检查路径！")
        return
    # 加载图像
    start_time = time.time()    # 记录开始时间
    image = cv2.imread(file_path)
    if image is None:
        print(f"无法加载图像，路径可能错误或文件损坏：{file_path}")
        return
    # 使用EasyOCR自动识别车牌
    result = reader.readtext(image)
    if result:
        for detection in result:
            text = detection[1]
            print(f"识别到的车牌号码是: {text}")
            # 绘制车牌边界框
            top_left = (int(detection[0][0][0]), int(detection[0][0][1]))
            bottom_right = (int(detection[0][2][0]), int(detection[0][2][1]))
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
            cv2.putText(image, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # 提取车牌区域
            x1, y1 = top_left
            x2, y2 = bottom_right
            plate_roi = image[y1:y2, x1:x2]
            # 放大车牌区域图像，这里设置放大倍数为2倍，可根据实际需求调整
            if plate_roi is not None and plate_roi.size > 0:
                enlarged_plate = cv2.resize(plate_roi, (0, 0), fx=2, fy=2)
            else:
                print("车牌区域提取失败！")
            # 将OpenCV图像格式转换为PIL图像格式，以便在Tkinter中显示
            pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            pil_enlarged_plate = Image.fromarray(cv2.cvtColor(enlarged_plate, cv2.COLOR_BGR2RGB))
             # 创建Tkinter可用的图像对象
            tk_image = ImageTk.PhotoImage(pil_image.resize((250, 200)))
            tk_enlarged_plate = ImageTk.PhotoImage(pil_enlarged_plate.resize((200, 50)))
            # 显示原始图像和放大后的车牌图像以及车牌号码文字信息
            image_label.config(image=tk_image)
            image_label.image = tk_image
            enlarged_plate_label.config(image=tk_enlarged_plate)
            enlarged_plate_label.image = tk_enlarged_plate
            plate_number_label.config(text=f"车牌号码: {text}")
    else:
        print("没有找到车牌区域！")

    stop_time = time.time() # 记录结束时间
    print(f"处理时间: {stop_time - start_time:.6f}秒")


# 创建主窗口
root = Tk()
root.title("车牌识别系统")
root.geometry("600x400") 


# 创建用于显示原始图像的标签，并设置布局
image_label = Label(root, text="原图:", font=("Arial", 12))
image_label.grid(row=0, column=0, padx=10, pady=10)

# 创建用于显示原始图像的标签
original_image_label = Label(root)
original_image_label.grid(row=0, column=1, padx=10, pady=10)

# 创建用于显示放大后车牌图像的标签，并设置布局
enlarged_plate_label = Label(root, text="形状定位车牌位置:", font=("Arial", 12))
enlarged_plate_label.grid(row=1, column=0, padx=10, pady=10)

# 创建用于显示放大后车牌图像的标签
enlarged_plate_image_label = Label(root)
enlarged_plate_image_label.grid(row=1, column=1, padx=10, pady=10)

# 创建用于显示车牌号码文字信息的标签，并设置布局
plate_number_label = Label(root, text="", font=("Arial", 16))
plate_number_label.grid(row=2, column=0, columnspan=2, pady=10)

# 创建按钮，并设置布局
select_button = Button(root, text="选择图片进行识别", command=select_and_recognize_image)
select_button.grid(row=3, column=0, columnspan=2, pady=20)

root.mainloop()