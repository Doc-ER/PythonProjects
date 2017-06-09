#coding=gb2312
'''
Created on 2013-5-1

@author: zhangwei
'''
from tkinter import *   
    
class RoomsButton(Frame):
   
    
    def __init__(self, parent=None, roomNum = 0, count=0, addY=0):
        Frame.__init__(self, parent)
        self.roomNum = roomNum
        self.addY=addY
        self.count = count
        self.master.title("低温储存室")
        self.master.geometry("500x300+10+10")
        Label(self.master, text="="*200).place(x = 0, y=52)
        self.pack(expand = YES, fill = BOTH)
        self.initUI()
        
    def initUI(self):
        TEXTS = ["建造", "删除"]
        COMMAND= [self.createRoom, self.deleteRoom]
        for i in range(2):
            buttons = Button(self.master, text = TEXTS[i], command= COMMAND[i])
            buttons.config(font = ('bold', 10))
            buttons.place(x = 20+i*100, y = 1, width = 50, height = 50)
         
    def createRoom(self):       
        self.roomNum +=100
        self.count +=1
        button =Button(self.master, text = '储藏室%s' % self.count, relief=RIDGE)
        if (self.count) % 5 ==0:
            self.addY +=100
            self.roomNum=100
        button.place(x = -70+self.roomNum, y = 70+ self.addY, width =100, height=100)
            
        
        
    def deleteRoom(self):
        pass
    
 
class ThemeButton(Button):# imagefile为图片的文件名称，让按钮的图像变成这个个图。
    def __init__(self, parent, imagefile):
        Button.__init__(self, parent = None)
        self.pack()
        self.image = PhotoImage(file = imagefile)         
        self.config(image = self.image, command = self.destroy)
        
        
        
#if __name__ == '__main__':
 #   win = Tk()
  #  win.title('root')
   # win2 = Toplevel(win)
    
    
    
    
   # db = ThemeButton(win2, 'closedRef.gif')
    
    #db.place(x = 30, y = 50)
    
    
    
    

        
        
