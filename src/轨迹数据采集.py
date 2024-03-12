import tkinter as tk
import pandas as pd
import time

canvas_width = 500
canvas_height = 500

center_x = canvas_width / 2
center_y = canvas_height / 2

count = 0

# 中心点半径
cpr = 5

# 开始时间
bt = 0
# 结束时间
# 创建主窗口
window = tk.Tk()
window.title('Mouse Paint') 

# 创建画布
canvas = tk.Canvas(window, 
                   width=canvas_width,
                   height=canvas_height,
                   bg='white')
canvas.pack()

# 绘制半径为5的圆
# canvas.create_oval(center_x-cpr, center_y-cpr, center_x+cpr, center_y+cpr, fill='black')

# 存储点击坐标
points = []

# 创建菜单
menu = tk.Menu(window, tearoff=0)

# 鼠标右键绑定,显示菜单
def show_menu(event):
    menu.post(event.x_root, event.y_root)

def gt():
    return round(time.time(), 4)

# 鼠标点击事件
def mouse_click(event):
    points.clear() # 清空坐标
    points.append([event.x, event.y, gt()]) # 添加起始点坐标

# 鼠标移动事件  
def mouse_move(event):
    points.append([event.x, event.y, gt()])
    line = canvas.create_line(points[-2][0], points[-2][1], 
                       points[-1][0], points[-1][1])
    canvas.addtag_withtag('line', line)

# 保存轨迹点
def save_points(event=None):
    global count
    count += 1
    # points[0]
    df = pd.DataFrame(points, columns=['x', 'y', 'time'], index=None)
    df.to_csv(f'user-{count}.csv')
    canvas.delete('all')

# 清空画布
def clear_canvas(event=None):
    canvas.delete('line')

# # 鼠标进入画布事件
# def mouse_enter(event):
#     canvas.winfo_pointerx() # 返回鼠标x坐标
#     canvas.winfo_pointery() # 返回鼠标y坐标
    
#     # 设置鼠标位置到中心
#     canvas.winfo_toplevel().winfo_pointerxy(center_x, center_y)

# 添加两个菜单命令
# menu.add_command(label='保存轨迹点', command=save_points) 
# menu.add_command(label='清空画布', command=clear_canvas)

# 绑定事件
canvas.bind('<Button-1>', mouse_click)   # 鼠标左键点击
canvas.bind('<B1-Motion>', mouse_move)  # 鼠标左键点击后移动
# canvas.bind('<Enter>', mouse_enter)
# canvas.bind('<ButtonRelease-1>', mouse_release)  # 鼠标左键点击后释放
# canvas.bind('<Button-3>', show_menu)  # 鼠标右键
window.bind('<Control-s>', save_points)  # ctrl + s
window.bind('<Control-c>', clear_canvas)  # ctrl + c
window.mainloop()
