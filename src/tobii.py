import tobii_research as tr
import time
import tkinter as tk
import pandas as pd
import time

# gaze raw data
gazes = []

# TODO: Active display coordinate system (adcs)
canvas_width = 1200
canvas_height = 770

# TODO: Active display area
aw = 1200
ah = 770

# TODO: Radius of the gaze central point set
cpr = 2

# Calculate the central point of the left eye gaze point and the right eye gaze point
center = lambda gaze: ((gaze[0] + gaze[2]) / 2 * aw, (gaze[1] + gaze[3]) / 2 * ah)

class TobiiTracker:
    gazes = []
    def __init__(self, canvas) -> None:
        self.canvas = canvas
        found_eyetrackers = tr.find_all_eyetrackers()
        self.my_eyetracker = found_eyetrackers[0]
        print("Address: " + self.my_eyetracker.address)
        print("Model: " + self.my_eyetracker.model)
        print("Name (It's OK if this is empty): " + self.my_eyetracker.device_name)
        print("Serial number: " + self.my_eyetracker.serial_number)

    def gaze_data_callback(self, gaze_data):
        # Print gaze points of left and right eye
        gaze = gaze_data['left_gaze_point_on_display_area'] + gaze_data['right_gaze_point_on_display_area']
        print('gaze point set: ', gaze)
        # the central point of the gaze
        gc = center(gaze)
        self.gazes.append(gaze)
        # plot the gaze central point
        self.canvas.create_oval(gc[0] - cpr, gc[1] - cpr, gc[0] + cpr, gc[1] + cpr)

    def subscribe(self):
        self.my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback, as_dictionary=True)

    def unsubscribe(self):
        self.my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback)

class TobiiWindow():
    def __init__(self) -> None:
        # Create the main window
        self.window = tk.Tk()
        # self.window.geometry(f"{canvas[0]}x{canvas[1]}
        # +{screen[0] // 2}+{screen[1] // 2}")
        self.window.geometry(f"{canvas_width}x{canvas_height}")
        self.window.title('Gaze Scraper')
        # Create the plot figure
        self.canvas = tk.Canvas(self.window, 
                        width=canvas_width,
                        height=canvas_height,
                        bg='white')
        self.canvas.pack()
        # 眼动仪
        self.tt = TobiiTracker(self.canvas)

        self.count = 0

        # Bind event of the tkinter application
        self.canvas.bind('<Button-1>', self.mouse_click)   # left key of the mouse click event
        self.window.bind('<Control-s>', self.save_points)  # ctrl + s
        self.window.bind('<Control-c>', self.clear_canvas)  # ctrl + c
        self.window.bind('<Control-w>', self.close)
    
    def open(self):
        self.window.mainloop()

    def close(self, event):
        self.window.quit()

    # Mouse click event
    def mouse_click(self, event):
        self.tt.gazes.clear() # clear the historical gaze points
        self.tt.subscribe()  # start to receive the real-time gaze time

    # Save the raw gaze points to local csv file
    def save_points(self, event=None):
        self.count += 1
        self.tt.unsubscribe()  # stop to receive the real-time gaze time
        df = pd.DataFrame(self.tt.gazes, columns=['lx', 'ly', 'rx', 'ry'], index=None)
        df.to_csv(f'user-{self.count}.csv', mode='w')
        self.canvas.delete('all')
    
    # Clear the plot figure
    def clear_canvas(self, event=None):
        self.tt.unsubscribe()  # stop to receive the real-time gaze time
        self.canvas.delete('all')


