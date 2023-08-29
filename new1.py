# Real Time Human Detection & Counting
# imported necessary library
from tkinter import *
import tkinter as tk
import tkinter.messagebox as mbox
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
import argparse
from persondetection import DetectorAPI
import matplotlib.pyplot as plt
from fpdf import FPDF

# Main Window & Configuration
window = tk.Tk()
window.title("Real Time Human Detection and People Counting - Arpita Singh (2018715)")
window.iconbitmap('Images/icon.ico')
window.geometry('1000x700')

# top label
start1 = tk.Label(text = "REAL TIME HUMAN\nDETECTION  &  COUNTING", font=("Calibri", 50,"underline"), fg="magenta") # same way bg
start1.place(x = 70, y = 10)

# function defined to start the main application
def start_fun():
    window.destroy()

# created a start button
Button(window, text="▶ START",command=start_fun,font=("Calibri", 25), bg = "orange", fg = "blue", cursor="hand2", borderwidth=3, relief="raised").place(x =130 , y =570 )

# image on the main window
path1 = "Images/front2.png"
img2 = ImageTk.PhotoImage(Image.open(path1))
panel1 = tk.Label(window, image = img2)
panel1.place(x = 90, y = 250)

# image on the main window
path = "Images/front1.png"
img1 = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(window, image = img1)
panel.place(x = 380, y = 180)

exit1 = False
# function created for exiting from window
def exit_win():
    global exit1
    if mbox.askokcancel("Exit", "Do you want to exit?"):
        exit1 = True
        window.destroy()

# exit button created
Button(window, text="❌ EXIT",command=exit_win,font=("Calibri", 25), bg = "red", fg = "blue", cursor="hand2", borderwidth=3, relief="raised").place(x =680 , y = 570 )

window.protocol("WM_DELETE_WINDOW", exit_win)
window.mainloop()

if exit1==False:
    # Main Window & Configuration of window1
    window1 = tk.Tk()
    window1.title("Real Time Human Detection & Counting Arpita Singh (2018715)")
    window1.iconbitmap('Images/icon.ico')
    window1.geometry('1000x700')

    filename=""
    filename1=""
    filename2=""

    def argsParser():
        arg_parse = argparse.ArgumentParser()
        arg_parse.add_argument("-v", "--video", default=None, help="path to Video File ")
        arg_parse.add_argument("-o", "--output", type=str, help="path to optional output video file")
        args = vars(arg_parse.parse_args())
        return args

# ---------------------------- video section ------------------------------------------------------------
    def video_option():
        # new windowv created for video section
        windowv = tk.Tk()
        windowv.title("Human Detection from Video")
        windowv.iconbitmap('Images/icon.ico')
        windowv.geometry('1000x700')

        max_count2 = 0
        framex2 = []
        county2 = []
        max2 = []
        avg_acc2_list = []
        max_avg_acc2_list = []
        max_acc2 = 0
        max_avg_acc2 = 0

        # function defined to open the video
        def open_vid():
            global filename2, max_count2, framex2, county2, max2, avg_acc2_list, max_avg_acc2_list, max_acc2, max_avg_acc2
            max_count2 = 0
            framex2 = []
            county2 = []
            max2=[]
            avg_acc2_list = []
            max_avg_acc2_list = []
            max_acc2 = 0
            max_avg_acc2 = 0

            filename2 = filedialog.askopenfilename(title="Select Video file", parent=windowv)
            path_text2.delete("1.0", "end")
            path_text2.insert(END, filename2)

        # function defined to detect inside the video
        def det_vid():
            global filename2, max_count2, framex2, county2, max2, avg_acc2_list, max_avg_acc2_list, max_acc2, max_avg_acc2
            max_count2 = 0
            framex2 = []
            county2 = []
            max2 = []
            avg_acc2_list = []
            max_avg_acc2_list = []
            max_acc2 = 0
            max_avg_acc2 = 0

            video_path = filename2
            if (video_path == ""):
                mbox.showerror("Error", "No Video File Selected!", parent = windowv)
                return
            info1.config(text="Status : Detecting...")
            # info2.config(text="                                                  ")
            mbox.showinfo("Status", "Detecting, Please Wait...", parent=windowv)
            # time.sleep(1)

            args = argsParser()
            writer = None
            if args['output'] is not None:
                writer = cv2.VideoWriter(args['output'], cv2.VideoWriter_fourcc(*'MJPG'), 10, (600, 600))

            detectByPathVideo(video_path, writer)

        # the main process of detection in video takes place here
        def detectByPathVideo(path, writer):
            global filename2, max_count2, framex2, county2, max2, avg_acc2_list, max_avg_acc2_list, max_acc2, max_avg_acc2
            max_count2 = 0
            framex2 = []
            county2 = []
            max2 = []
            avg_acc2_list = []
            max_avg_acc2_list = []
            max_acc2 = 0
            max_avg_acc2 = 0

            # function defined to plot the people detected in video

            video = cv2.VideoCapture(path)
            odapi = DetectorAPI()
            threshold = 0.7

            check, frame = video.read()
            if check == False:
                print('Video Not Found. Please Enter a Valid Path (Full path of Video Should be Provided).')
                return

            x2 = 0
            while video.isOpened():
                # check is True if reading was successful
                check, frame = video.read()
                if(check==True):
                    img = cv2.resize(frame, (800, 500))
                    boxes, scores, classes, num = odapi.processFrame(img)
                    person = 0
                    acc = 0
                    for i in range(len(boxes)):
                        if classes[i] == 1 and scores[i] > threshold:
                            box = boxes[i]
                            person += 1
                            cv2.rectangle(img, (box[1], box[0]), (box[3], box[2]), (255, 0, 0), 2)  # cv2.FILLED
                            cv2.putText(img, f'P{person, round(scores[i],2)}', (box[1]-30, box[0]-8), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255), 1 )#(75,0,130),
                            #acc+=scores[i]
                            #if(scores[i]>max_acc2):
                                #max_acc2 = scores[i]

                    if(person>max_count2):
                        max_count2 = person
                    county2.append(person)
                    x2+=1
                    framex2.append(x2)
                    #if(person>=1):
                        #avg_acc2_list.append(acc/person)
                        #if((acc/person)>max_avg_acc2):
                            #max_avg_acc2 = (acc/person)
                    #else:
                        #avg_acc2_list.append(acc)

                    if writer is not None:
                        writer.write(img)

                    cv2.imshow("Human Detection from Video", img)
                    key = cv2.waitKey(1)
                    if key & 0xFF == ord('q'):
                        break
                else:
                    break

            video.release()
            info1.config(text="                                                  ")
            # info2.config(text="                                                  ")
            info1.config(text="Status : Detection & Counting Completed")
            # info2.config(text="Max. Human Count : " + str(max_count2))
            cv2.destroyAllWindows()

            for i in range(len(framex2)):
                max2.append(max_count2)
                #max_avg_acc2_list.append(max_avg_acc2)

        # funcion defined to preview the selected video
        def prev_vid():
            global filename2
            cap = cv2.VideoCapture(filename2)
            while (cap.isOpened()):
                ret, frame = cap.read()
                if ret == True:
                    img = cv2.resize(frame, (800, 500))
                    cv2.imshow('Selected Video Preview', img)
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break
                else:
                    break
            cap.release()
            cv2.destroyAllWindows()

        lbl1 = tk.Label(windowv, text="DETECT  FROM\nVIDEO", font=("Calibri", 50, "underline"), fg="brown")
        lbl1.place(x=230, y=20)
        lbl2 = tk.Label(windowv, text="Selected Video", font=("Calibri", 30), fg="green")
        lbl2.place(x=80, y=200)
        path_text2 = tk.Text(windowv, height=1, width=37, font=("Calibri", 30), bg="light yellow", fg="orange", borderwidth=2,relief="solid")
        path_text2.place(x=80, y=260)

        Button(windowv, text="SELECT", command=open_vid, cursor="hand2", font=("Calibri", 20), bg="light green", fg="blue").place(x=220, y=350)
        Button(windowv, text="PREVIEW", command=prev_vid, cursor="hand2", font=("Calibri", 20), bg="yellow", fg="blue").place(x=410, y=350)
        Button(windowv, text="DETECT", command=det_vid, cursor="hand2", font=("Calibri", 20), bg="orange", fg="blue").place(x=620, y=350)

        info1 = tk.Label(windowv, font=("Calibri", 30), fg="gray")  # same way bg
        info1.place(x=100, y=440)
        # info2 = tk.Label(windowv, font=("Arial", 30), fg="gray")  # same way bg
        # info2.place(x=100, y=500)

        #function defined to exit from windowv section
        def exit_winv():
            if mbox.askokcancel("Exit", "Do you want to exit?", parent = windowv):
                windowv.destroy()
        windowv.protocol("WM_DELETE_WINDOW", exit_winv)

    # image on the main window
    pathv = "Images/image2.png"
    imgv = ImageTk.PhotoImage(Image.open(pathv))
    panelv = tk.Label(window1, image = imgv)
    panelv.place(x = 700, y = 260)# 720, 260

    Button(window1, text="DETECT  FROM  VIDEO ➡",command=video_option, cursor="hand2", font=("Calibri", 30), bg = "light blue", fg = "blue").place(x = 110, y = 300) #90, 300

    # function defined to exit from window1
    def exit_win1():
        if mbox.askokcancel("Exit", "Do you want to exit?"):
            window1.destroy()

    # created exit button
    Button(window1, text="❌ EXIT",command=exit_win1,  cursor="hand2", font=("Calibri", 25), bg = "red", fg = "blue").place(x = 440, y = 600)
    window1.protocol("WM_DELETE_WINDOW", exit_win1)
    window1.mainloop()