import tkinter as tk
import os
from PIL import Image,  ImageTk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import Tk, Button, Canvas, Label, Entry, Spinbox, PhotoImage, NE, END
def SelectButton():
	global fps,height,width,i,filename
	filename=str(fd.askopenfilename(title = "Select file",filetypes = (("Video","*.mp4 .ts .webm .mkv"),("All files","*.*"))))
	fs1.config(text = 'Size(Mb): '+str(round(os.path.getsize(filename)/1048576,2)))
	os.system('ffmpeg_vvceasy.exe -y -i "'+filename+'" -vf thumbnail -frames:v 1 temp.jpg')
	imgone=Image.open('temp.jpg')
	if imgone.size[0] >= imgone.size[1]:
		wpercent=180/imgone.size[0]
		hsize=int(imgone.size[1]*wpercent)
		i=ImageTk.PhotoImage(imgone.resize((180,hsize)))
	else:
		wpercent=200/imgone.size[1]
		wsize=int(imgone.size[0]*wpercent)
		i=ImageTk.PhotoImage(imgone.resize((wsize,200)))
	canvas.create_image(0, 0, anchor='nw', image=i)
	os.remove('temp.jpg')
	videoselect.delete(0,END)
	videoselect.insert(0,filename)
	saveto.delete(0,END)
	saveto.insert(0,filename+"_266.mp4")
def EncodeButton():
	global ii
	os.system('ffmpeg_vvceasy.exe -i "'+filename+'" -q:a 0 -map a temp.wav')
	os.system('exhale.exe c temp.wav temp.m4a') 
	if passes.get() == "1 pass": 
		os.system('ffmpeg_vvceasy.exe -y -i "'+filename+'" -pix_fmt yuv420p -f yuv4mpegpipe - | vvencapp.exe --y4m -i - --preset '+preset.get()+' -q '+quality.get()+' -o temp.266')
	if passes.get() == "2 pass": 
		os.system('ffmpeg_vvceasy.exe -y -i "'+filename+'" -pix_fmt yuv420p temp.y4m')
		os.system('vvencapp.exe --y4m -i temp.y4m --preset '+preset.get()+' --qpa 1 -p 2 -b '+qualitytwo.get()+'k -o temp.266')
		os.remove('temp.y4m')
	if os.path.exists('temp.wav'):
		os.remove('temp.wav')
		os.system('mp4box.exe -add temp.266:fmt=VVC -add temp.m4a -new "'+saveto.get()+'"')
		os.remove('temp.m4a')
	else:
		os.system("mp4box.exe -add temp.266:fmt=VVC -new "+'"'+saveto.get()+'"')
	os.remove('temp.266')
	os.system('ffmpeg_vvceasy.exe -y -i "'+saveto.get()+'" -vf "thumbnail" -frames:v 1 temp.jpg')
	os.system("mp4box.exe -add "+'"'+saveto.get()+'"'+" -add temp.jpg -new "+'"'+saveto.get()+'"')
	imgtwo=Image.open('temp.jpg')
	if imgtwo.size[0] >= imgtwo.size[1]:
		wpercent=180/imgtwo.size[0]
		hsize=int(imgtwo.size[1]*wpercent)
		ii=ImageTk.PhotoImage(imgtwo.resize((180,hsize)))
	else:
		wpercent=200/imgtwo.size[1]
		wsize=int(imgtwo.size[0]*wpercent)
		ii=ImageTk.PhotoImage(imgtwo.resize((wsize,200)))
	canvas.create_image(180, 0, anchor='nw', image=ii)
	os.remove("temp.jpg")
	fs2.config(text = 'Size(Mb): '+str(round(os.path.getsize(saveto.get())/1048576,2)))
def btnClickFunctiontwo():
	fn=os.path.basename(filename).rsplit('.',1)
	data = [("mp4","*.mp4")]
	saveto.delete(0,END)
	saveto.insert(0,str(fd.asksaveasfilename(filetypes=data,defaultextension=data,initialfile=fn[0]+".mp4_266")))
root=Tk()
root.geometry('500x350')
root.configure(background='#F0F8FF')
root.title('VVC GUI Encoder')

Button(root,text='Encode',bg='#F0F8FF',font=('arial',12,'bold'),command=EncodeButton).place(x=409,y=308)
Button(root,text='Select',bg='#F0F8FF',font=('arial',12,'normal'),command=SelectButton).place(x=39,y=68)
Button(root,text='Select',bg='#F0F8FF',font=('arial',12,'normal'),command=btnClickFunctiontwo).place(x=39,y=278)

Label(root,text='Select Video', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=9, y=8)
Label(root,text='Preset', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=9, y=118)
Label(root,text='1 pass / 2 pass', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=9, y=188)
Label(root,text='1 Pass', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=169, y=8)
Label(root,text='2 Pass', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=329, y=8)
Label(root,text='Quality (1-63)', bg='#F0F8FF', font=('arial', 10, 'italic')).place(x=169, y=28)
Label(root,text='Quality (kb)', bg='#F0F8FF', font=('arial', 10, 'italic')).place(x=329, y=28)
Label(root,text='Save as:', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=39, y=248)

fs1=Label(root,text='Size(Mb):', bg='#F0F8FF', font=('arial', 10, 'italic'))
fs1.place(x=129, y=288)
fs2=Label(root,text='Size(Mb):', bg='#F0F8FF', font=('arial', 10, 'italic'))
fs2.place(x=310, y=288)

videoselect=Entry(root)
videoselect.place(x=9,y=38)

saveto=Entry(root,width=65)
saveto.place(x=9,y=318)

preset=ttk.Combobox(root, values=['faster','fast','medium','slow','slower'],font=('arial',12,'normal'),width=6,state ="readonly")
preset.place(x=9,y=148)
preset.current(1)

passes=ttk.Combobox(root,values=['1 pass', '2 pass'],font=('arial',12,'normal'),width=6,state="readonly")
passes.place(x=9,y=218)
passes.current(0)

quality=Spinbox(root,from_=1,to=63,font=('arial',10,'italic'),bg='#F0F8FF',width=10)
quality.place(x=169,y=48)
quality.insert(0,3)

qualitytwo=Entry(root)
qualitytwo.place(x=329,y=48)
qualitytwo.insert(0,500)

canvas=tk.Canvas(root,width=360,height=200)
canvas.place(x=129,y=78)

root.mainloop()