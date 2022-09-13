import tkinter as tk
import os, cv2
from PIL import Image,  ImageTk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import Tk, Button, Canvas, Label, Entry, Spinbox, PhotoImage, NE, END
global fps
global height
global width
global i,ii,fin,fn,ext,filename
def btnClickFunctionone():
	global fps
	global height
	global width
	global i,fin,fn,ext,filename
	filename = str(fd.askopenfilename(title = "Select file",filetypes = (("Video","*.mp4 .ts .webm .mkv"),("All files","*.*"))))
	fn,ext = os.path.basename(filename).split('.')
	fin='"'+filename+'"'
	os.system('ffmpeg_vvceasy.exe -y -i '+fin+' -vf thumbnail -frames:v 1  '+fin+'.jpg')
	imgone=Image.open(filename+'.jpg')
	wpercent = (150/float(imgone.size[0]))
	hsize = int((float(imgone.size[1])*float(wpercent)))
	i=ImageTk.PhotoImage(imgone.resize((150,hsize)))
	canvas.create_image(0, 0, anchor='nw', image=i)
	os.remove(filename+'.jpg')
	videoselect.delete(0,END)
	videoselect.insert(0,filename)
	saveto.delete(0,END)
	saveto.insert(0,filename+"_266.mp4")
	fps= int(cv2.VideoCapture(filename).get(cv2.CAP_PROP_FPS))
	height = int(cv2.VideoCapture(filename).get(cv2.CAP_PROP_FRAME_HEIGHT))
	width = int(cv2.VideoCapture(filename).get(cv2.CAP_PROP_FRAME_WIDTH))
def btnClickFunction():
	global ii
	prst=preset.get()
	pss=passes.get()
	os.system("ffmpeg_vvceasy.exe -i "+fin+" -q:a 0 -map a "+fn+"."+ext+".wav")
	os.system("exhale.exe c "+fn+"."+ext+".wav "+fn+"."+ext+".m4a") 
	os.system("ffmpeg_vvceasy.exe -y -i "+fin+" -pix_fmt yuv420p -strict -1 "+fin+".Y4M")
	if pss == "1 pass": 
		os.system("vvencapp.exe --preset "+prst+" -i "+fin+".Y4M -s "+str(width)+"x"+str(height)+" -r "+str(fps)+"  -q "+quality.get()+" -o "+fin+".266")
	if pss == "2 pass": 
		os.system("vvencapp.exe --preset "+prst+" -i "+fin+".Y4M -s "+str(width)+"x"+str(height)+" -r "+str(fps)+" --qpa 1  -p 2 -b "+qualitytwo.get()+"k -o "+fin+".266")
	os.system("mp4box.exe -add "+fin+".266:fmt=VVC -add "+fn+"."+ext+".m4a -new "+fin+"_266.mp4")
	os.remove(filename+".266")
	os.system("ffmpeg_vvceasy.exe -y -i "+fin+"_266.mp4 -vf 'thumbnail' -frames:v 1  "+fin+"_266.jpg")
	os.system("mp4box.exe -add "+fin+"_266.mp4 -add "+fin+"_266.jpg -new "+fin+"_266.mp4")
	imgtwo=Image.open(filename+'_266.jpg')
	wpercent = (150/float(imgtwo.size[0]))
	hsize = int((float(imgtwo.size[1])*float(wpercent)))
	ii=ImageTk.PhotoImage(imgtwo.resize((150,hsize)))
	canvas2.create_image(0, 0, anchor='nw', image=ii)
	os.remove(filename+"_266.jpg")
	os.remove(filename+".Y4M")
	os.remove(fn+"."+ext+".wav")
	os.remove(fn+"."+ext+".m4a")
def btnClickFunctiontwo():
	print('clicked')
root = Tk()
root.geometry('500x350')
root.configure(background='#F0F8FF')
root.title('VVC GUI Encoder')

Button(root,text='Encode',bg='#F0F8FF',font=('arial',12,'bold'),command=btnClickFunction).place(x=409,y=308)
Button(root,text='Select',bg='#F0F8FF',font=('arial',12,'normal'),command=btnClickFunctionone).place(x=39,y=68)
Button(root,text='Select',bg='#F0F8FF',font=('arial',12,'normal'),command=btnClickFunctiontwo).place(x=39,y=278)

Label(root,text='Select Video', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=9, y=8)
Label(root,text='Preset', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=9, y=118)
Label(root,text='1 pass / 2 pass', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=9, y=188)
Label(root,text='1 Pass', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=169, y=8)
Label(root,text='2 Pass', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=329, y=8)
Label(root,text='Quality (1-63)', bg='#F0F8FF', font=('arial', 10, 'italic')).place(x=169, y=38)
Label(root,text='Quality (kb)', bg='#F0F8FF', font=('arial', 10, 'italic')).place(x=329, y=38)
Label(root,text='Save as:', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=39, y=248)

videoselect=Entry(root)
videoselect.place(x=9,y=38)

preset=ttk.Combobox(root, values=['faster', 'fast', 'medium', 'slow', 'slower'],font=('arial',12,'normal'),width=10,state ="readonly")
preset.place(x=9,y=148)
preset.current(1)

passes=ttk.Combobox(root,values=['1 pass', '2 pass'],font=('arial',12,'normal'),width=10,state="readonly")
passes.place(x=9,y=218)
passes.current(0)

quality=Spinbox(root,from_=1,to=63,font=('arial',10,'italic'),bg='#F0F8FF',width=10)
quality.place(x=169,y=58)
quality.insert(0,3)

qualitytwo=Entry(root)
qualitytwo.place(x=329,y=58)
qualitytwo.insert(0,500)

canvas=tk.Canvas(root,width=150,height=200)
canvas.place(x=159,y=88)

canvas2=tk.Canvas(root,width=150,height=200)
canvas2.place(x=329,y=88)

saveto=Entry(root,width=65)
saveto.place(x=9,y=318)

root.mainloop()