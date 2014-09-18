import wx
import wx.media
import os
import pyaudio 
import os.path
import wave, struct
import numpy

global file1,file2,file3
chunk = 1024
global flag1,flag2,flag3
global a1,ts1,ts,a12,a13,ts12,ts13,ts2,ts3
global m1,m2,m3,mo1,mo2,mo3,r1,r2,r3
a1 = 2
a12 = 2
a13 = 2
ts1 = 0
ts12 = 0
ts13 = 0
ts = 2
ts2 = 2
ts3 = 2
r1 = 0
r2 = 0
r3 = 0
mo1 = 0
mo2 = 0
mo3 = 0
m1 = 0
m2 = 0
m3 = 0
#global par
#par = []


class SoundFile:
      def  __init__(self, signal):
	      self.file = wave.open('result1.wav', 'wb')		#the signal will be written in result.wav file
	      self.signal = signal
	      self.sr = 44100
      def write(self):
	self.file.setparams((1, 2, self.sr, 44100*4, 'NONE', 'noncompressed'))
	self.file.writeframes(self.signal)
	self.file.close()

# function for writing the sound file
def makesignal(signal):
	ssignal = ''
	for i in range(len(signal)):
	        ssignal += wave.struct.pack('h',signal[i]) # transform to binary
	f = SoundFile(ssignal)
	f.write()
	print 'file written'

def digitize(waveFile):
	signal3 = []
	par = waveFile.getparams()
	length = waveFile.getnframes()
	for i in range(0,length):
	    waveData = waveFile.readframes(1)
	    data = struct.unpack("<h", waveData)
	    signal3.append(int(data[0])%32768)
	return signal3


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,title = "Media Player",size=(950,600))

	self.panel = wx.Panel(self)
	self.player1 = wx.media.MediaCtrl(self.panel)
	self.player2 = wx.media.MediaCtrl(self.panel)
	self.player3 = wx.media.MediaCtrl(self.panel)
	self.player4 = wx.media.MediaCtrl(self.panel)
	self.player5 = wx.media.MediaCtrl(self.panel)

	font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
	font.SetPointSize(9)
	self.currentVolume1 = 50
	self.currentVolume2 = 50
	self.currentVolume3 = 50
	self.currentVolume4 = 50
	self.currentVolume5 = 50

	

	self.panel.SetBackgroundColour((200,200,200))

	imageFile1 = "dsaa_play.jpg"
	image1 = wx.Image(imageFile1, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

	imageFile2 = "dsaa_pause.jpg"
	image2 = wx.Image(imageFile2, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

	imageFile3 = "dsaa_stop.jpg"
	image3 = wx.Image(imageFile3, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

	self.st1 = wx.StaticText(self.panel, label="Wave Mixer", style=wx.ALIGN_CENTRE,pos=(400,10))

	# File 1
	wx.StaticBox(self.panel, label='Wave 1:', pos=(5, 30), size=(300, 450))

	self.cbtn1 = wx.Button(self.panel, label='Select File', pos=(20, 50))
	self.cbtn1.Bind(wx.EVT_BUTTON,self.loadFile)
	
	self.bt1 = wx.Button(self.panel, label='New File', pos=(60, 440))
	self.bt1.Bind(wx.EVT_BUTTON,self.playFile1)

	self.bt4 = wx.Button(self.panel, label='Record', pos=(420, 540))
	self.bt4.Bind(wx.EVT_BUTTON,self.record1)

	self.bt = wx.Button(self.panel, label='Play Record', pos=(520, 540))
	self.bt.Bind(wx.EVT_BUTTON,self.playrecord)

	self.filename1 = wx.StaticText(self.panel,wx.ID_ANY,pos=(150,60),label="Name:")

	self.txt1 = wx.StaticText(self.panel, label='Amplitude', pos=(20, 110))
	self.txt2 = wx.StaticText(self.panel, label='Time Shift', pos=(20, 160)) 
	self.txt3 = wx.StaticText(self.panel, label='Time Scaling', pos=(20, 210))

	self.sld1 = wx.Slider(self.panel, value=2, minValue=0, maxValue=5, pos=(20, 120), 
			size=(250, -1), style=wx.SL_LABELS)
	self.sld1.Bind(wx.EVT_SLIDER,self.onslider1)

	self.sld2 = wx.Slider(self.panel, value=0, minValue=-100, maxValue=100, pos=(20, 170), 
			size=(250, -1), style=wx.wx.SL_LABELS)
	self.sld2.Bind(wx.EVT_SLIDER,self.onslider2)

	self.sld3 = wx.Slider(self.panel, value=2, minValue=0, maxValue=7, pos=(20, 220), 
			size=(250, -1), style=wx.SL_LABELS)
	self.sld3.Bind(wx.EVT_SLIDER,self.onslider3)



	self.cb1 = wx.CheckBox(self.panel, label='Time Reversal', pos=(20, 260))
	self.cb1.Bind(wx.EVT_CHECKBOX, self.OnChecked1)
	self.cb2 = wx.CheckBox(self.panel, label='Select for Modulation', pos=(20, 290))
	self.cb2.Bind(wx.EVT_CHECKBOX, self.OnChecked2)
	self.cb3 = wx.CheckBox(self.panel, label='Select for Mixing', pos=(20, 320))
	self.cb3.Bind(wx.EVT_CHECKBOX, self.OnChecked3)

	self.button1 = wx.BitmapButton(self.panel, id=-1, bitmap=image1,                       #play
			pos=(20, 370), size = (image1.GetWidth()/3, image1.GetHeight()/3))
	self.button1.Bind(wx.EVT_LEFT_DOWN,self.playFile11)

	


	self.button4 = wx.BitmapButton(self.panel, id=-1, bitmap=image2, 			#pause
			pos=(60, 370), size = (image2.GetWidth()/3, image2.GetHeight()/2.5))
	self.button4.Bind(wx.EVT_LEFT_DOWN,self.pauseFile1)


	slider1 = wx.Slider(self.panel, -1, 0, 0, 0, size=wx.Size(150, -1),pos=(100,380))
        self.slider1 = slider1
        self.Bind(wx.EVT_SLIDER, self.Seek1, slider1)

	# create volume control
        self.volumeCtrl1 = wx.Slider(self.panel,pos=(240,310),style=wx.SL_VERTICAL,size=(-1,100))
        self.volumeCtrl1.SetRange(0, 100)
        self.volumeCtrl1.SetValue(self.currentVolume1)
        self.volumeCtrl1.Bind(wx.EVT_SLIDER, self.on_set_volume1)
        

	self.button7 = wx.BitmapButton(self.panel, id=-1, bitmap=image3,			#stop
			pos=(260, 370), size = (image3.GetWidth()/3, image3.GetHeight()/2.5))
	self.button7.Bind(wx.EVT_LEFT_DOWN,self.stopFile1)

	
        self.length1 = wx.StaticText(self.panel,wx.ID_ANY,pos=(20,420),label="Time:")
        self.pos1 = wx.StaticText(self.panel,wx.ID_ANY,pos=(150,420),label="Position:")



	# File 2
	wx.StaticBox(self.panel, label='Wave 2:', pos=(305, 30), size=(300, 450))

	self.cbtn2 = wx.Button(self.panel, label='Select File', pos=(340, 50))
	self.cbtn2.Bind(wx.EVT_BUTTON,self.loadFile2)
	
	self.bt2 = wx.Button(self.panel, label='New File', pos=(360, 440))
	self.bt2.Bind(wx.EVT_BUTTON,self.playFile2)

	#self.bt5 = wx.Button(self.panel, label='Record', pos=(460, 440))
	#self.bt5.Bind(wx.EVT_BUTTON,self.record2)

	self.filename2 = wx.StaticText(self.panel,wx.ID_ANY,pos=(480,60),label="Name:")


	self.txt4 = wx.StaticText(self.panel, label='Amplitude', pos=(340, 110))
	self.txt5 = wx.StaticText(self.panel, label='Time Shift', pos=(340, 160)) 
	self.txt6 = wx.StaticText(self.panel, label='Time Scaling', pos=(340, 210))

	self.sld4 = wx.Slider(self.panel, value=2, minValue=0, maxValue=5, pos=(340, 120), 
			size=(250, -1), style=wx.SL_LABELS)
	self.sld4.Bind(wx.EVT_SLIDER,self.onslider4)
	

	self.sld5 = wx.Slider(self.panel, value=0, minValue=-100, maxValue=100, pos=(340, 170), 
			size=(250, -1), style=wx.SL_LABELS)
	self.sld5.Bind(wx.EVT_SLIDER,self.onslider5)

	self.sld6 = wx.Slider(self.panel, value=2, minValue=0, maxValue=7, pos=(340, 220), 
			size=(250, -1), style=wx.SL_LABELS)
	self.sld6.Bind(wx.EVT_SLIDER,self.onslider6)


	self.cb4 = wx.CheckBox(self.panel, label='Time Reversal', pos=(340, 260))
	self.cb4.Bind(wx.EVT_CHECKBOX, self.OnChecked4)
	self.cb5 = wx.CheckBox(self.panel, label='Select for Modulation', pos=(340, 290))
	self.cb5.Bind(wx.EVT_CHECKBOX, self.OnChecked5)
	self.cb6 = wx.CheckBox(self.panel, label='Select for Mixing', pos=(340, 320))	
	self.cb6.Bind(wx.EVT_CHECKBOX, self.OnChecked6)

	self.button2 = wx.BitmapButton(self.panel, id=-1, bitmap=image1,          #play
			pos=(320, 370), size = (image1.GetWidth()/3, image1.GetHeight()/3))
	self.button2.Bind(wx.EVT_LEFT_DOWN,self.playFile12)

	self.button5 = wx.BitmapButton(self.panel, id=-1, bitmap=image2,            #pause
			pos=(360, 370), size = (image2.GetWidth()/3, image2.GetHeight()/2.5))
	self.button5.Bind(wx.EVT_LEFT_DOWN,self.pauseFile2)
	
	self.slider2 = wx.Slider(self.panel,wx.ID_ANY,pos=(400,380),size = (150,-1))
        self.slider2.Bind(wx.EVT_SLIDER,self.Seek2)

	self.volumeCtrl2 = wx.Slider(self.panel,pos=(540,310),style=wx.SL_VERTICAL,size=(-1,100))
        self.volumeCtrl2.SetRange(0, 100)
        self.volumeCtrl2.SetValue(self.currentVolume2)
        self.volumeCtrl2.Bind(wx.EVT_SLIDER, self.on_set_volume2)

	self.button8 = wx.BitmapButton(self.panel, id=-1, bitmap=image3,
			pos=(560, 370), size = (image3.GetWidth()/3, image3.GetHeight()/2.5))
	self.button8.Bind(wx.EVT_LEFT_DOWN,self.stopFile2)


	self.length2 = wx.StaticText(self.panel,wx.ID_ANY,pos=(340,420),label="Time:")
        self.pos2 = wx.StaticText(self.panel,wx.ID_ANY,pos=(470,420),label="Position:")



	# File 3
	wx.StaticBox(self.panel, label='Wave 3:', pos=(615, 30), size=(300, 450))

	self.cbtn3 = wx.Button(self.panel, label='Select File', pos=(660, 50))
	self.cbtn3.Bind(wx.EVT_BUTTON,self.loadFile3)

	self.bt3 = wx.Button(self.panel, label='New File', pos=(660, 440))
	self.bt3.Bind(wx.EVT_BUTTON,self.playFile3)


	#self.bt6 = wx.Button(self.panel, label='Record', pos=(750, 440))
	#self.bt6.Bind(wx.EVT_BUTTON,self.record3)


	self.filename3 = wx.StaticText(self.panel,wx.ID_ANY,pos=(780,60),label="Name:")


	self.txt7 = wx.StaticText(self.panel, label='Amplitude', pos=(660, 110))
	self.txt8 = wx.StaticText(self.panel, label='Time Shift', pos=(660, 160)) 
	self.txt9 = wx.StaticText(self.panel, label='Time Scaling', pos=(660, 210))

	self.sld7 = wx.Slider(self.panel, value=2, minValue=0, maxValue=5, pos=(660, 120), 
			size=(250, -1), style=wx.SL_LABELS)
	self.sld7.Bind(wx.EVT_SLIDER,self.onslider7)

	self.sld8 = wx.Slider(self.panel, value=0, minValue=-100, maxValue=100, pos=(660, 170), 
			size=(250, -1), style=wx.SL_LABELS)
	self.sld8.Bind(wx.EVT_SLIDER,self.onslider8)

	self.sld9 = wx.Slider(self.panel, value=2, minValue=0, maxValue=7, pos=(660, 220), 
			size=(250, -1), style=wx.SL_LABELS)
	self.sld9.Bind(wx.EVT_SLIDER,self.onslider9)


	self.cb7 = wx.CheckBox(self.panel, label='Time Reversal', pos=(660, 260))
	self.cb7.Bind(wx.EVT_CHECKBOX, self.OnChecked7)
	self.cb8 = wx.CheckBox(self.panel, label='Select for Modulation', pos=(660, 290))
	self.cb8.Bind(wx.EVT_CHECKBOX, self.OnChecked8)
	self.cb9 = wx.CheckBox(self.panel, label='Select for Mixing', pos=(660, 320))	
	self.cb9.Bind(wx.EVT_CHECKBOX, self.OnChecked9)

	self.button3 = wx.BitmapButton(self.panel, id=-1, bitmap=image1,           #play
			pos=(630, 370), size = (image1.GetWidth()/3, image1.GetHeight()/3))
	self.button3.Bind(wx.EVT_LEFT_DOWN,self.playFile13)

	self.button6 = wx.BitmapButton(self.panel, id=-1, bitmap=image2,                #pause
			pos=(670, 370), size = (image2.GetWidth()/3, image2.GetHeight()/2.5))
	self.button6.Bind(wx.EVT_LEFT_DOWN,self.pauseFile3)


	self.slider3 = wx.Slider(self.panel,wx.ID_ANY,pos=(710,380),size = (150,-1))
        self.slider3.Bind(wx.EVT_SLIDER,self.Seek3)

	self.volumeCtrl3 = wx.Slider(self.panel,pos=(850,310),style=wx.SL_VERTICAL,size=(-1,100))
        self.volumeCtrl3.SetRange(0, 100)
        self.volumeCtrl3.SetValue(self.currentVolume3)
        self.volumeCtrl3.Bind(wx.EVT_SLIDER, self.on_set_volume3)

	self.button9 = wx.BitmapButton(self.panel, id=-1, bitmap=image3,
			pos=(870, 370), size = (image3.GetWidth()/3, image3.GetHeight()/2.5))
	self.button9.Bind(wx.EVT_LEFT_DOWN,self.stopFile3)

	self.length3 = wx.StaticText(self.panel,wx.ID_ANY,pos=(660,420),label="Time:")
        self.pos3 = wx.StaticText(self.panel,wx.ID_ANY,pos=(790,420),label="Position:")


	##### Modulation

	self.button2 = wx.BitmapButton(self.panel, id=-1, bitmap=image1,          #play
			pos=(130, 500), size = (image1.GetWidth()/3, image1.GetHeight()/3))
	self.button2.Bind(wx.EVT_LEFT_DOWN,self.playFile4)

	self.button5 = wx.BitmapButton(self.panel, id=-1, bitmap=image2,            #pause
			pos=(170, 500), size = (image2.GetWidth()/3, image2.GetHeight()/2.5))
	self.button5.Bind(wx.EVT_LEFT_DOWN,self.pauseFile4)
	
	self.slider4 = wx.Slider(self.panel,wx.ID_ANY,pos=(210,510),size = (150,-1))
        self.slider4.Bind(wx.EVT_SLIDER,self.Seek4)

	self.volumeCtrl4 = wx.Slider(self.panel,pos=(350,440),style=wx.SL_VERTICAL,size=(-1,100))
        self.volumeCtrl4.SetRange(0, 100)
        self.volumeCtrl4.SetValue(self.currentVolume4)
        self.volumeCtrl4.Bind(wx.EVT_SLIDER, self.on_set_volume4)

	self.button8 = wx.BitmapButton(self.panel, id=-1, bitmap=image3,
			pos=(370, 500), size = (image3.GetWidth()/3, image3.GetHeight()/2.5))
	self.button8.Bind(wx.EVT_LEFT_DOWN,self.stopFile4)

	self.txt10 = wx.StaticText(self.panel, label='Modulation and Play', pos=(190, 570))


	self.length4 = wx.StaticText(self.panel,wx.ID_ANY,pos=(170,550),label="Time:")
        self.pos4 = wx.StaticText(self.panel,wx.ID_ANY,pos=(280,550),label="Position:")
	


	###### Mix


	self.button2 = wx.BitmapButton(self.panel, id=-1, bitmap=image1,          #play
			pos=(620, 500), size = (image1.GetWidth()/3, image1.GetHeight()/3))
	self.button2.Bind(wx.EVT_LEFT_DOWN,self.playFile5)

	self.button5 = wx.BitmapButton(self.panel, id=-1, bitmap=image2,            #pause
			pos=(660, 500), size = (image2.GetWidth()/3, image2.GetHeight()/2.5))
	self.button5.Bind(wx.EVT_LEFT_DOWN,self.pauseFile5)
	
	self.slider5 = wx.Slider(self.panel,wx.ID_ANY,pos=(700,510),size = (150,-1))
        self.slider5.Bind(wx.EVT_SLIDER,self.Seek5)


	

	self.volumeCtrl5 = wx.Slider(self.panel,pos=(840,440),style=wx.SL_VERTICAL,size=(-1,100))
        self.volumeCtrl5.SetRange(0, 100)
        self.volumeCtrl5.SetValue(self.currentVolume5)
        self.volumeCtrl5.Bind(wx.EVT_SLIDER, self.on_set_volume5)

	self.button8 = wx.BitmapButton(self.panel, id=-1, bitmap=image3,
			pos=(860, 500), size = (image3.GetWidth()/3, image3.GetHeight()/2.5))
	self.button8.Bind(wx.EVT_LEFT_DOWN,self.stopFile5)

	self.txt10 = wx.StaticText(self.panel, label='Mix and Play', pos=(720, 570))

	self.length5 = wx.StaticText(self.panel,wx.ID_ANY,pos=(720,550),label="Time:")
        self.pos5 = wx.StaticText(self.panel,wx.ID_ANY,pos=(840,550),label="Position:")
	
        
       
        self.timer1 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer1,self.timer1)
        self.timer1.Start(100)

	self.timer2 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer2,self.timer2)
        self.timer2.Start(100)

	self.timer3 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer3,self.timer3)
        self.timer3.Start(100)

	self.timer4 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer4,self.timer4)
        self.timer4.Start(100)

	self.timer5 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer5,self.timer5)
        self.timer5.Start(100)

        
        #self.panel.SetInitialSize()
        #self.SetInitialSize()
	self.Show()

    def playrecord(self,e):
	chunk = 1024  

	f = wave.open("record1.wav","r")  
	p = pyaudio.PyAudio()   
	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
		                channels = f.getnchannels(),  
				                rate = f.getframerate(),  
						                output = True)  
	data = f.readframes(chunk)    
	while data != '': 
		 
	    	stream.write(data)  
	    	data = f.readframes(chunk)  
	stream.stop_stream()  
	stream.close()   
	p.terminate()  

    
    def record1(self,e):
	chunk = 1024     #chunk of data 
	form= pyaudio.paInt16 
	channels = 1 
	framerate = 16000
	seconds = 5  
	p = pyaudio.PyAudio() 
	s= p.open(format=form,channels=channels,rate=framerate,input=True,frames_per_buffer=chunk)  
	fr = [] 
	for i in range(0, int(framerate / chunk * seconds)): 
		d = s.read(chunk) 
		fr.append(d)  
	s.stop_stream() 
	s.close() 
	p.terminate() 
	w1 = wave.open("record1.wav", 'wb') 
	w1.setnchannels(channels) 
	w1.setsampwidth(p.get_sample_size(form)) 
	w1.setframerate(framerate) 
	w1.writeframes(b''.join(fr)) 
	w1.close()


    def onslider1(self,e):
	    obj = e.GetEventObject()
	    global a1
	    a1 = obj.GetValue()
	    #print a1
	   
    def onslider2(self,e):
	obj = e.GetEventObject()
	global ts1
	ts1 = obj.GetValue()
	

    def onslider3(self,e):
    	obj = e.GetEventObject()
	global ts
	ts = obj.GetValue()

    def onslider4(self,e):
	    obj = e.GetEventObject()
	    global a12
	    a12 = obj.GetValue()
	    #print a1
	   
    def onslider5(self,e):
	obj = e.GetEventObject()
	global ts12
	ts12 = obj.GetValue()
	

    def onslider6(self,e):
    	obj = e.GetEventObject()
	global ts
	ts2 = obj.GetValue()

    def onslider7(self,e):
	    obj = e.GetEventObject()
	    global a13
	    a13 = obj.GetValue()
	    #print a1
	   
    def onslider8(self,e):
	obj = e.GetEventObject()
	global ts13
	ts13 = obj.GetValue()
	

    def onslider9(self,e):
    	obj = e.GetEventObject()
	global ts3
	ts3= obj.GetValue()
	

    def OnChecked1(self,e):
	s = e.GetEventObject()
	global r1
	r1 = s.GetValue()

    def OnChecked2(self,e):
	s = e.GetEventObject()
	global mo1
	mo1 = s.GetValue()

    def OnChecked3(self,e):
	s = e.GetEventObject()
	global m1
	m1 = s.GetValue()
	

    def OnChecked4(self,e):
	s = e.GetEventObject()
	global r2
	r2 = s.GetValue()
	

    def OnChecked5(self,e):
	s = e.GetEventObject()
	global mo2
	mo2 = s.GetValue()
	

    def OnChecked6(self,e):
	s = e.GetEventObject()
	global m2
	m2 = s.GetValue()

    def OnChecked7(self,e):
	s = e.GetEventObject()
	global r3
	r3 = s.GetValue()
	

    def OnChecked8(self,e):
	s = e.GetEventObject()
	global mo3
	mo3 = s.GetValue()
	

    def OnChecked9(self,e):
	s = e.GetEventObject()
	global m3
	m3 = s.GetValue()

    def playFile5(self,event):
	global m1,m2,m3
	global file1,file2,file3
	l1 = -1
	l2 = -1
	l3 = -1
	if (mo1 or mo2 or mo3):
		if m1:
			f1 = wave.open(file1, 'rb')
			p1 = f1.getparams()
			g1 = p1[3] # number of frames
			s1 = f1.readframes(g1)
			f1.close()
			s1 = numpy.fromstring(s1, numpy.int16)
			l1 = len(s1)
		if m2:
			f2 = wave.open(file2, 'rb')
			p2 = f2.getparams()
			g2 = p2[3] # number of frames
			s2 = f2.readframes(g2)
			f2.close()
			s2 = numpy.fromstring(s2, numpy.int16)
			l2 = len(s2)
		if m3:
			f3 = wave.open(file3, 'rb')
			p3 = f3.getparams()
			g3 = p3[3] # number of frames
			s3 = f3.readframes(g3)
			f3.close()
			s3 = numpy.fromstring(s3, numpy.int16)
			l3 = len(s3)

		mix = []	
	
		l = max(l1,l2,l3)
		for i in range(0,l):
			mix.append(0)
		print l1
		for i in range(0,l):
			if m1 and i<l1:
				mix[i] += s1[i]
			if m2 and i<l2:
				mix[i] += s2[i]
			if m3 and i<l3:
				mix[i] += s3[i]
	
		mix = struct.pack('h'*len(mix), *tuple(mix))  
		if l == l1:
			f = wave.open("mixer.wav",'wb')
			f.setparams(p1)
			f.writeframes(mix)
			f.close()
		elif l==l2:
			f = wave.open("mixer.wav",'wb')
			f.setparams(p2)
			f.writeframes(mix)
			f.close()
		elif l==l3:
			f = wave.open("mixer.wav",'wb')
			f.setparams(p3)
			f.writeframes(mix)
			f.close()

		chunk = 1024  

		f = wave.open("mixer.wav","r")  
		p = pyaudio.PyAudio()   
		stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
			                channels = f.getnchannels(),  
				                rate = f.getframerate(),  
						                output = True)  
		data = f.readframes(chunk)    
		while data != '': 
		 
	    		stream.write(data)  
	    		data = f.readframes(chunk)  
		stream.stop_stream()  
		stream.close()   
		p.terminate()  			
	




        #self.player5.Play()
        	self.slider5.SetRange(0, self.player5.Length())
        	self.length5.SetLabel('length: %d seconds' % (self.player5.Length()/1000))
        #self.info_name.SetLabel("Name: %s" % (os.path.split(self.path3\5)[1]))
        #self.panel.SetInitialSize()
        #self.SetInitialSize()

    def playFile11(self,event):
        self.player1.Play()
        self.slider1.SetRange(0, self.player1.Length())
        self.length1.SetLabel('length: %d seconds' % (self.player1.Length()/1000))

    def playFile12(self,event):
        self.player2.Play()
        self.slider2.SetRange(0, self.player2.Length())
        self.length2.SetLabel('length: %d seconds' % (self.player2.Length()/1000))

    def playFile13(self,event):
        self.player3.Play()
        self.slider3.SetRange(0, self.player3.Length())
        self.length3.SetLabel('length: %d seconds' % (self.player3.Length()/1000))
	

    def playFile1(self,event):
	global file1
   	f = wave.open(file1, 'rb')
	p = f.getparams()
	g = p[3] # number of frames
	s = f.readframes(g)
	f.close()
	ar1 = []
	ar2 = []
	ar3 = []
	#ar1 = digitize(f)
	#length = len(ar1)
	#print length
	j=0
	global a1
	global ts
	global ts1
	global r1
	print ts1
 
	s = numpy.fromstring(s, numpy.int16) * a1
        s = struct.pack('h'*len(s), *tuple(s))
	
	f = wave.open("result1.wav",'wb')
	f.setparams(p)
	f.writeframes(s)
	f.close()
	
	# time shift	
	d1 = ts1/100
	f = wave.open("result1.wav",'rb')
	p = f.getparams()
	g = p[3] # number of frames
	s = f.readframes(g)
	f.close()
	s = numpy.fromstring(s, numpy.int16)
	
	if d1>=0:
		#print '*'
		l1 = 16000 * d1
		l2 = int(l1)
		for i in range(0,l2):
			ar2.append(0)
		for i in range (0,len(s)):
			ar2.append(s[i])
		
	if d1<0:
		l1 = 16000*(-d1)
		l2 = int(l1)
		for i in range (l2,len(s)):
			ar2.append(s[i])
	ar2 = struct.pack('h'*len(ar2), *tuple(ar2))

	f = wave.open("result1.wav",'wb')
	f.setparams(p)
	f.writeframes(ar2)
	f.close()

	
	## Time Scaling
	
	f = wave.open("result1.wav",'rb')
	p = f.getparams()
	g = p[3] # number of frames
	s = f.readframes(g)
	f.close()
	s = numpy.fromstring(s, numpy.int16)
	print ts
	if ts ==0:
		q = 0
	if ts ==1:
		q = 1/2
	if ts == 1:
		q = 1/4
	if ts == 2:
		q = 1/8
	if ts == 3:
		q = 1
	if ts == 4:
		q = 2
	if ts == 5:
		q = 4
	if ts == 6:
		q = 6
	if ts == 7:
		q = 8
	if q<1 and q!=0:
		tt = 1/q
		t = int(tt)
	#	print t
		t1 = 0
		t2 = 0
		j=0
		for i in range(0,len(s)):
			ar3.append(s[t1])
			t2+=1
			if t2==t:
				t2=0
				t1 += t
		print ar3
	elif q>=1:
		ts11 = int(q)
		for i in range(0,len(s)):
			if(i%ts11==0):
	#			print i
				ar3.append(s[i])
				j+=1
		
	elif q==0:
		for i in range(0,len(s)):
			ar3.append(s[0])

	ar3 = struct.pack('h'*len(ar3), *ar3)
	f = wave.open("result1.wav",'wb')
	f.setparams(p)
	f.writeframes(ar3)
	f.close()
	
	#time reversal
	if r1:

		f = wave.open("result1.wav",'rb')
		p = f.getparams()
		g = p[3] # number of frames
		s = f.readframes(g)
		f.close()
		s = numpy.fromstring(s, numpy.int16)

		ar=[]
		for i in range(0,len(s)):
			ar.append(s[len(s)-i-1])
	
		ar = struct.pack('h'*len(ar), *tuple(ar))
		f = wave.open("result1.wav",'wb')
		f.setparams(p)
		f.writeframes(ar)
		f.close()
	else:
		f = wave.open("result1.wav",'wb')
		f.setparams(p)
		f.writeframes(ar3)
		f.close()

	chunk = 1024  

	f = wave.open("result1.wav","r")  
	p = pyaudio.PyAudio()   
	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
		                channels = f.getnchannels(),  
				                rate = f.getframerate(),  
						                output = True)  
	data = f.readframes(chunk)    
	while data != '': 
		 
	    	stream.write(data)  
	    	data = f.readframes(chunk)  
	stream.stop_stream()  
	stream.close()   
	p.terminate()  



	
        #self.player1.Play()
        #self.slider1.SetRange(0, self.player1.Length())
        #self.length1.SetLabel('length: %d seconds' % (self.player1.Length()/1000))
        
        #self.panel.SetInitialSize()
        #self.SetInitialSize()     


    def playFile2(self,event):
	global file2
   	f = wave.open(file2, 'rb')
	p = f.getparams()
	g = p[3] # number of frames
	s = f.readframes(g)
	f.close()
	ar1 = []
	ar2 = []
	ar3 = []
	#ar1 = digitize(f)
	#length = len(ar1)
	#print length
	j=0
	global a12
	global ts2
	global ts12
	global r2
	print ts12
 
	s = numpy.fromstring(s, numpy.int16) * a12
        s = struct.pack('h'*len(s), *tuple(s))
	
	f = wave.open("result2.wav",'wb')
	f.setparams(p)
	f.writeframes(s)
	f.close()
	
	# time shift	
	d2 = ts12/100
	f = wave.open("result2.wav",'rb')
	p = f.getparams()
	g = p[3] # number of frames
	s = f.readframes(g)
	f.close()
	s = numpy.fromstring(s, numpy.int16)
	
	if d2>=0:
		#print '*'
		l1 = 16000 * d2
		l2 = int(l1)
		for i in range(0,l2):
			ar2.append(0)
		for i in range (0,len(s)):
			ar2.append(s[i])
		
	if d2<0:
		l1 = 16000*(-d2)
		l2 = int(l1)
		for i in range (l2,len(s)):
			ar2.append(s[i])
	ar2 = struct.pack('h'*len(ar2), *tuple(ar2))

	f = wave.open("result2.wav",'wb')
	f.setparams(p)
	f.writeframes(ar2)
	f.close()

	
	## Time Scaling
	
	f = wave.open("result2.wav",'rb')
	p = f.getparams()
	g = p[3] # number of frames
	s = f.readframes(g)
	f.close()
	s = numpy.fromstring(s, numpy.int16)
	print ts2
	
	if ts2<1 and ts2!=0:
		tt = 1/ts2
		t = int(tt)
	#	print t
		t1 = 0
		t2 = 0
		j=0
		for i in range(0,len(s)):
			ar3.append(s[t1])
			t2+=1
			if t2==t:
				t2=0
				t1 += t
		print ar3
	elif ts2>=1:
		ts11 = int(ts2)
		for i in range(0,len(s)):
			if(i%ts11==0):
	#			print i
				ar3.append(s[i])
				j+=1
		
	elif ts2==0:
		for i in range(0,len(s)):
			ar3.append(s[0])

	ar3 = struct.pack('h'*len(ar3), *ar3)
	f = wave.open("result2.wav",'wb')
	f.setparams(p)
	f.writeframes(ar3)
	f.close()
	
	#time reversal
	if r2:

		f = wave.open("result2.wav",'rb')
		p = f.getparams()
		g = p[3] # number of frames
		s = f.readframes(g)
		f.close()
		s = numpy.fromstring(s, numpy.int16)

		ar=[]
		for i in range(0,len(s)):
			ar.append(s[len(s)-i-1])
	
		ar = struct.pack('h'*len(ar), *tuple(ar))
		f = wave.open("result2.wav",'wb')
		f.setparams(p)
		f.writeframes(ar)
		f.close()
	else:
		f = wave.open("result2.wav",'wb')
		f.setparams(p)
		f.writeframes(ar3)
		f.close()

	chunk = 1024  

	f = wave.open("result2.wav","r")  
	p = pyaudio.PyAudio()   
	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
		                channels = f.getnchannels(),  
				                rate = f.getframerate(),  
						                output = True)  
	data = f.readframes(chunk)    
	while data != '': 
		 
	    	stream.write(data)  
	    	data = f.readframes(chunk)  
	stream.stop_stream()  
	stream.close()   
	p.terminate()  



	
        #self.player1.Play()
        self.slider2.SetRange(0, self.player2.Length())
        self.length2.SetLabel('length: %d seconds' % (self.player2.Length()/1000))
        
        #self.panel.SetInitialSize()
        #self.SetInitialSize()     


    def playFile3(self,event):
	global file3
	
   	f = wave.open(file3, 'rb')
	p = f.getparams()
	g = p[3] # number of frames
	s = f.readframes(g)
	f.close()
	ar1 = []
	ar2 = []
	ar3 = []
	#ar1 = digitize(f)
	length = len(ar1)
	#print length
	j=0
	global a13
	global ts3
	global ts13
	global r3

	print a13
	s = numpy.fromstring(s, numpy.int16) * a13
        s = struct.pack('h'*len(s), *s)

	f = wave.open("result3.wav",'wb')
	f.setparams(p)
	f.writeframes(s)
	f.close()	
	# time shift	
	
	f = wave.open("result3.wav",'rb')
	p = f.getparams()
	g = p[3] # number of frames
	s = f.readframes(g)
	f.close()
	s = numpy.fromstring(s, numpy.int16)
	d3 = ts13/100
	if d3>=0:
		#print '*'
		l1 = 16000 * d3
		l2 = int(l1)
		for i in range(0,l2):
			ar2.append(0)
		for i in range (0,len(s)):
			ar2.append(s[i])
		
	if d3<0:
		l1 = 16000*(-d3)
		l2 = int(l1)
		for i in range (l2,len(s)):
			ar2.append(s[i])
	ar2 = struct.pack('h'*len(ar2), *ar2)

	f = wave.open("result3.wav",'wb')
	f.setparams(p)
	f.writeframes(ar2)
	f.close()

	## Time scaling

	if ts3 ==0:
		q = 0
	if ts3 ==1:
		q = 1/2
	if ts3 == 1:
		q = 1/4
	if ts3 == 2:
		q = 1/8
	if ts3 == 3:
		q = 1
	if ts3 == 4:
		q = 2
	if ts3 == 5:
		q = 4
	if ts3 == 6:
		q = 6
	if ts3 == 7:
		q = 8
	if q<1 and q!=0:
		tt = 1/q
		t = int(tt)
	#	print t
		t1 = 0
		t2 = 0
		j=0
		for i in range(0,len(s)):
			ar3.append(s[t1])
			t2+=1
			if t2==t:
				t2=0
				t1 += t
		print ar3
	elif q>=1:
		ts11 = int(q)
		for i in range(0,len(s)):
			if(i%ts11==0):
	#			print i
				ar3.append(s[i])
				j+=1
		
	elif q==0:
		for i in range(0,len(s)):
			ar3.append(s[0])

	ar3 = struct.pack('h'*len(ar3), *ar3)
	f = wave.open("result3.wav",'wb')
	f.setparams(p)
	f.writeframes(ar3)
	f.close()

	#time reversal
	if r3:		
		f = wave.open("result3.wav",'rb')
		p = f.getparams()
		g = p[3] # number of frames
		s = f.readframes(g)
		f.close()
		s = numpy.fromstring(s, numpy.int16)

		ar=[]
		for i in range(0,len(s)):
			ar.append(s[len(s)-i-1])
	
		ar = struct.pack('h'*len(ar), *tuple(ar))
		f = wave.open("result3.wav",'wb')
		f.setparams(p)
		f.writeframes(ar)
		f.close()
	else:
		f = wave.open("result3.wav",'wb')
		f.setparams(p)
		f.writeframes(ar3)
		f.close()
		
	chunk = 1024  

	f = wave.open("result3.wav","r")  
	p = pyaudio.PyAudio()   
	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
		                channels = f.getnchannels(),  
				                rate = f.getframerate(),  
						                output = True)  
	data = f.readframes(chunk)    
	while data != '': 
		 
	    	stream.write(data)  
	    	data = f.readframes(chunk)  
	stream.stop_stream()  
	stream.close()   
	p.terminate()  


        #self.player3.Play()
        self.slider3.SetRange(0, self.player3.Length())
        self.length3.SetLabel('length: %d seconds' % (self.player3.Length()/1000))




    def digitize(waveFile):
	signal3 = []
	length = waveFile.getnframes()
	for i in range(0,length):
	    waveData = waveFile.readframes(1)
	    data = struct.unpack("<h", waveData)
	    signal3.append(int(data[0])%32768)
	return signal3

 

	
    def onTimer1(self,event):
        current1 = self.player1.Tell()
        self.pos1.SetLabel("Pos: %i seconds" % (int(current1)/1000))
        self.slider1.SetValue(current1)

    def onTimer2(self,event):
        current2 = self.player2.Tell()
        self.pos2.SetLabel("Pos: %i seconds" % (int(current2)/1000))
        self.slider2.SetValue(current2)

    def onTimer3(self,event):
        current3 = self.player3.Tell()
        self.pos3.SetLabel("Pos: %i seconds" % (int(current3)/1000))
        self.slider3.SetValue(current3)

    def onTimer4(self,event):
        current4 = self.player4.Tell()
        self.pos4.SetLabel("Pos: %i seconds" % (int(current4)/1000))
        self.slider4.SetValue(current4)

    def onTimer5(self,event):
        current5 = self.player5.Tell()
        self.pos5.SetLabel("Pos: %i seconds" % (int(current5)/1000))
        self.slider5.SetValue(current5)


    def Seek1(self, evt):
        offset = self.slider1.GetValue()
        self.player1.Seek(offset)


    def Seek2(self,event):
       
        self.player2.Seek(self.slider2.GetValue())

    def Seek3(self,event):
       
        self.player3.Seek(self.slider3.GetValue())

    def Seek4(self,event):
       
        self.player4.Seek(self.slider4.GetValue())

    def Seek5(self,event):
       
        self.player5.Seek(self.slider5.GetValue())
      
        
    def loadFile(self,event):
        
        msg1 = wx.FileDialog(self, message = "Open a media file",
                               style = wx.OPEN,
                               wildcard = "*.wav;")
        if msg1.ShowModal() == wx.ID_OK:
            path1 = msg1.GetPath()
            self.path1 = path1
	    self.filename1.SetLabel("Name: %s" % (os.path.split(self.path1)[1]))
	    global file1
	    file1 = path1
	    file11 = path1
	    file13 = path1
            
            if not self.player1.Load(path1):
                wx.MessageBox("Unable to load this file, it is in the wrong format")

    #def loadResult(self,e):
	#msg1 = File

    def loadFile2(self,event):
        
        msg2 = wx.FileDialog(self, message = "Open a media file",
                               style = wx.OPEN,
                               wildcard = "*.wav;")
        if msg2.ShowModal() == wx.ID_OK:
            path2 = msg2.GetPath()
            self.path2 = path2
	    self.filename2.SetLabel("Name: %s" % (os.path.split(self.path2)[1]))
	    global file2
	    file2 = path2
	    file22 = path2
            file23 = path2
	    
            
            if not self.player2.Load(path2):
                wx.MessageBox("Unable to load this file, it is in the wrong format")

    def loadFile3(self,event):
        
        msg3 = wx.FileDialog(self, message = "Open a media file",
                               style = wx.OPEN,
                               wildcard = "*.wav;")
        if msg3.ShowModal() == wx.ID_OK:
            path3 = msg3.GetPath()
            self.path3 = path3
	    self.filename3.SetLabel("Name: %s" % (os.path.split(self.path3)[1]))
	    global file3
	    file3=path3
            
            if not self.player3.Load(path3):
                wx.MessageBox("Unable to load this file, it is in the wrong format")
              
                
    def playFile4(self,event):
	global mo1,mo2,mo3
	global file1,file2,file3
	a = []
	l1 = 99999
	l2 = 99999
	l3 = 99999
	if(mo1 or mo2 or mo3):
		if mo1:
			f1 = wave.open(file1, 'rb')
			p1 = f1.getparams()
			g1 = p1[3] # number of frames
			s1 = f1.readframes(g1)
			f1.close()
			s1 = numpy.fromstring(s1, numpy.int16)
			l1 = len(s1)
			a.append(1)
		if mo2:
			f2 = wave.open(file2, 'rb')
			p2 = f2.getparams()
			g2 = p2[3] # number of frames
			s2 = f2.readframes(g2)
			f2.close()
			s2 = numpy.fromstring(s2, numpy.int16)
			l2 = len(s2)
			a.append(2)
		if mo3:	
			f3 = wave.open(file3, 'rb')
			p3 = f3.getparams()
			g3 = p3[3] # number of frames
			s3 = f3.readframes(g3)
			f3.close()
			s3 = numpy.fromstring(s3, numpy.int16)
			l3 = len(s3)
			a.append(3)
	
		mod = []
		l=999999
		for i in range(0,len(a)):
			if a[i]==1:
				l = min(l,l1)
			if a[i]==2:
				l = min(l,l2)
			if a[i]==3:
				l = min(l,l3)
		
		for i in range(0,l):
			mod.append(1)
		print l1
		for i in range(0,l):
			if mo1 and i<l1:
				mod[i] *= s1[i]
				mod[i] = mod[i]%32768
			if mo2 and i<l2:
				mod[i] *= s2[i]
				mod[i] = mod[i]%32768
			if mo3 and i<l3:
				mod[i] *= s3[i]
				mod[i] = mod[i]%32768
	#print mod

		mod = struct.pack('h'*len(mod), *tuple(mod))
  	
		if l == l1 and mo1:
			f = wave.open("modulation.wav",'wb')
			f.setparams(p1)
			f.writeframes(mod)
			f.close()
		elif l==l2 and mo2:
			f = wave.open("modulation.wav",'wb')
			f.setparams(p2)
			f.writeframes(mod)
			f.close()
		elif l==l3 and mo3:
			f = wave.open("modulation.wav",'wb')
			f.setparams(p3)
			f.writeframes(mod)
			f.close()

		chunk = 1024  

		f = wave.open("modulation.wav","r")  
		p = pyaudio.PyAudio()   
		stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
		                channels = f.getnchannels(),  
				                rate = f.getframerate(),  
						                output = True)  
		data = f.readframes(chunk)    
		while data != '': 
		 
	    		stream.write(data)  
	    		data = f.readframes(chunk)  
		stream.stop_stream()  
		stream.close()   
		p.terminate()  			
	




        #self.player4.Play()
        	self.slider4.SetRange(0, self.player4.Length())
        	self.length4.SetLabel('length: %d seconds' % (self.player4.Length()/1000))
        #self.info_name.SetLabel("Name: %s" % (os.path.split(self.path3\5)[1]))
        #self.panel.SetInitialSize()
        #self.SetInitialSize()                
                




   
        
    def pauseFile1(self,event):
        self.player1.Pause()

    def pauseFile2(self,event):
        self.player2.Pause()

    def pauseFile3(self,event):
        self.player3.Pause()

    def pauseFile4(self,event):
        self.player4.Pause()

    def pauseFile5(self,event):
        self.player5.Pause()
        
    def stopFile1(self,event):
        self.player1.Stop()

    def stopFile2(self,event):
        self.player2.Stop()

    def stopFile3(self,event):
        self.player3.Stop()

    def stopFile4(self,event):
        self.player4.Stop()

    def stopFile5(self,event):
        self.player5.Stop()

    def on_set_volume1(self, event):
        """
        Sets the volume of the music player
        """
        self.currentVolume1 = self.volumeCtrl1.GetValue()
        self.player1.SetVolume(self.currentVolume1)

    def on_set_volume2(self, event):
        """
        Sets the volume of the music player
        """
        self.currentVolume2 = self.volumeCtrl2.GetValue()
        self.player2.SetVolume(self.currentVolume2)

    def on_set_volume3(self, event):
        """
        Sets the volume of the music player
        """
        self.currentVolume3 = self.volumeCtrl3.GetValue()
        self.player3.SetVolume(self.currentVolume3)

    def on_set_volume4(self, event):
        """
        Sets the volume of the music player
        """
        self.currentVolume4 = self.volumeCtrl4.GetValue()
        self.player4.SetVolume(self.currentVolume4)

    def on_set_volume5(self, event):
        """
        Sets the volume of the music player
        """
        self.currentVolume5 = self.volumeCtrl5.GetValue()
        self.player5.SetVolume( self.currentVolume5)
    
        
app = wx.App(False)
frame = MainFrame()
app.MainLoop()
