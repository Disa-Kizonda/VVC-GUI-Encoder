import os,tkinter
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from tkinter import Tk, Button, Canvas, Label, Entry, Spinbox, PhotoImage, NE, END, ttk

def SelectButton():
	global i,filename
	filename=str(fd.askopenfilename(title = "Select file",filetypes = (("Video","*.mp4 .ts .webm .mkv"),("All files","*.*"))))
	fs1.config(text=f'Size(Mb): {os.path.getsize(filename)/1048576:.2f}')
	os.system('ffmpeg_vvceasy.exe -y -i "'+filename+'" -vf thumbnail -frames:v 1 temp.jpg')
	imgone=Image.open('temp.jpg')
	imgone.thumbnail((180,200))
	i=ImageTk.PhotoImage(imgone)
	canvas.create_image(0, 0, anchor='nw', image=i)
	os.remove('temp.jpg')
	videoselect.delete(0,END)
	videoselect.insert(0,filename)
	saveto.delete(0,END)
	saveto.insert(0,filename+"_266.mp4")
def EncodeButton():
	global ii
	audn = '{: .0f}'.format(audioquality.get())
	os.system('ffmpeg_vvceasy.exe -y -i "'+filename+'" -q:a 0 -map a temp.wav')
	os.system('exhale.exe '+audv[int(audn)-1]+' temp.wav temp.m4a') 
	if passes.get() == "1 pass": 
		os.system('ffmpeg_vvceasy.exe -y -i "'+filename+'" -c:v vvc -b:v 0 -qp '+quality.get()+'  -preset '+preset.get()+' temp.266')
	if passes.get() == "2 pass": 
		os.system('ffmpeg_vvceasy.exe  -y -i "'+filename+'" -an -vcodec vvc -vvenc-params passes=2:pass=1:rcstatsfile=temp.json -preset '+preset.get()+' -b:v '+qualitytwo.get()+'k -f null NUL')
		os.system('ffmpeg_vvceasy.exe  -y -i "'+filename+'" -acodec copy -vcodec vvc -vvenc-params passes=2:pass=2:rcstatsfile=temp.json -preset '+preset.get()+' -b:v '+qualitytwo.get()+'k temp.266')
		os.remove('temp.json')
	if os.path.exists('temp.wav'):
		os.remove('temp.wav')
		os.system('mp4box.exe -add temp.266 -add temp.m4a -new "'+saveto.get()+'"')
		os.remove('temp.m4a')
	else:
		os.system("mp4box.exe -add temp.266 -new "+'"'+saveto.get()+'"')
	os.remove('temp.266')
	os.system('ffmpeg_vvceasy.exe -y -i "'+saveto.get()+'" -vf "thumbnail" -frames:v 1 temp.jpg')
	imgtwo=Image.open('temp.jpg')
	imthum=imgtwo
	imthum.thumbnail((512,512))	
	imthum.save("thumbnail.jpg")
	imgtwo.thumbnail((180,200))
	ii=ImageTk.PhotoImage(imgtwo)
	canvas.create_image(180, 0, anchor='nw', image=ii)
	os.system("mp4box.exe -add "+'"'+saveto.get()+'"'+" -add thumbnail.jpg -new "+'"'+saveto.get()+'"')
	os.remove("temp.jpg")
	os.remove("thumbnail.jpg")
	fs2.config(text=f'Size(Mb): {os.path.getsize(saveto.get())/1048576:.2f}')
def btnClickFunctiontwo():
	fn=os.path.basename(filename).rsplit('.',1)
	data = [("mp4","*.mp4")]
	saveto.delete(0,END)
	saveto.insert(0,str(fd.asksaveasfilename(filetypes=data,defaultextension=data,initialfile=fn[0]+".mp4_266")))
def audioQ(event):
	audn = '{: .0f}'.format(audioquality.get())
	audqual.configure(text='Quality (kb): '+audvn[int(audn)-1])
def btnOpenVid(): os.popen(videoselect.get())
def btnOpenVid2(): os.popen(saveto.get())
def on_canvas_click(event):open_window()
def open_window():
	frame = 0
	new_window = tkinter.Toplevel()
	new_window.geometry('1000x560')
	new_window.title('Comparison')
	canvas2 = Canvas(new_window, width=1000, height=500)
	canvas2.place(x=0, y=50)
	i = None
	i2 = None
	zoom=0
	def update_canvas():
		nonlocal frame, i, i2
		if i is not None:
			canvas2.delete(i)
		if i2 is not None:
			canvas2.delete(i2)
		def update_image(videoname, side):
			nonlocal i, i2,zoom
			os.system(f'ffmpeg_vvceasy.exe -y -i "{videoname}" -vf "select=eq(n\,{frame})" -frames:v 1 temp.jpg')
			image = Image.open('temp.jpg')
			image.thumbnail((500, 500))
			width, height = image.size
			widthoriginal=width
			if width+zoom>=widthoriginal:
				image = image.resize((width+zoom, height+zoom), Image.ANTIALIAS)	
				if side == "left":
					i = ImageTk.PhotoImage(image)
					canvas2.create_image(0, 0, anchor='nw', image=i)
				elif side == "right":
					i2 = ImageTk.PhotoImage(image)
					if width+zoom<=500:canvas2.create_image(width+zoom, 0, anchor='nw', image=i2)
					if width+zoom>=500:canvas2.create_image(500, 0, anchor='nw', image=i2)
			else:
				if side == "left":
					i = ImageTk.PhotoImage(image)
					canvas2.create_image(0, 0, anchor='nw', image=i)
				elif side == "right":
					i2 = ImageTk.PhotoImage(image)
					canvas2.create_image(width, 0, anchor='nw', image=i2)
				zoom=0
			os.remove('temp.jpg')
		update_image(videoselect.get(), "left")
		update_image(saveto.get(), "right")
	def update(act):
		nonlocal frame
		nonlocal zoom
		if act == "inc_f":
			frame += 1
		elif act == "dec_f":
			frame -= 1
			if frame < 0:
				frame = 0
		elif act == "inc_z":
			zoom += 15
		elif act == "dec_z":
			zoom -= 15
		update_canvas()
	b1 = Button(new_window, text='<--',command=lambda:update("dec_f"))
	b1.place(x=50, y=10)
	b2 = Button(new_window, text='-->',command=lambda:update("inc_f"))
	b2.place(x=150, y=10)
	b3 = Button(new_window, text='+',command=lambda:update("inc_z"))
	b3.place(x=250, y=10)
	b4 = Button(new_window, text='-',command=lambda:update("dec_z"))
	b4.place(x=300, y=10)
	update_canvas()
	new_window.mainloop()

audv=['a','b','1','c','2','d','3','e','f','4','g','5','6','7','8','9']
audvn=['50','62','64','74','80','86','96','98','110','112','122','128','144','160','176','192']
root=Tk()
root.geometry('500x350')
root.resizable(False, False)
root.configure(background='#F0F8FF')
root.title('VVC GUI Encoder')

Button(root,text='Encode',bg='#F0F8FF',font=('arial',12,'bold'),command=EncodeButton).place(x=409,y=308)
Button(root,text='Select',bg='#F0F8FF',font=('arial',12,'normal'),command=SelectButton).place(x=39,y=68)
Button(root,text='Select',bg='#F0F8FF',font=('arial',12,'normal'),command=btnClickFunctiontwo).place(x=39,y=278)
Button(root,text='Open',bg='#F0F8FF',font=('arial',7,'italic'),command=btnOpenVid).place(x=259,y=280)
Button(root,text='Open',bg='#F0F8FF',font=('arial',7,'italic'),command=btnOpenVid2).place(x=459,y=280)


Label(root,text='Select Video', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=9, y=8)
Label(root,text='Preset', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=9, y=118)
Label(root,text='1 pass / 2 pass', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=9, y=188)
Label(root,text='1 Pass', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=169, y=8)
Label(root,text='2 Pass', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=289, y=8)
Label(root,text='Audio Quality', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=379, y=8)
Label(root,text='Quality (1-63)', bg='#F0F8FF', font=('arial', 10, 'italic')).place(x=169, y=28)
Label(root,text='Quality (kb)', bg='#F0F8FF', font=('arial', 10, 'italic')).place(x=289, y=28)
Label(root,text='Save as:', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=39, y=248)

fs1=Label(root,text='Size(Mb): 0', bg='#F0F8FF', font=('arial', 10, 'italic'))
fs1.place(x=129, y=288)
fs2=Label(root,text='Size(Mb): 0', bg='#F0F8FF', font=('arial', 10, 'italic'))
fs2.place(x=310, y=288)

audqual=Label(root,text='Quality (kb): 96', bg='#F0F8FF', font=('arial', 10, 'italic'))
audqual.place(x=379, y=28)

videoselect=Entry(root)
videoselect.place(x=9,y=38)

saveto=Entry(root,width=65)
saveto.place(x=9,y=318)

preset=ttk.Combobox(root, values=['faster','fast','medium','slow','slower'],font=('arial',12,'normal'),width=6,state ="readonly")
preset.place(x=9,y=148)
preset.current(1)

audioquality=ttk.Scale(root, from_=1, to=16,command=audioQ)
audioquality.place(x=379,y=48)
audioquality.set(8)

passes=ttk.Combobox(root,values=['1 pass', '2 pass'],font=('arial',12,'normal'),width=6,state="readonly")
passes.place(x=9,y=218)
passes.current(0)

quality=Spinbox(root,from_=1,to=63,font=('arial',10,'italic'),bg='#F0F8FF',width=10)
quality.place(x=169,y=48)
quality.insert(0,3)

qualitytwo=Entry(root,width=10)
qualitytwo.place(x=289,y=48)
qualitytwo.insert(0,500)

canvas=Canvas(root,width=360,height=200)
canvas.place(x=129,y=78)
canvas.bind('<Button-3>', on_canvas_click)

root.mainloop()