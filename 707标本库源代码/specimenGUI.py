#coding= gb2312
#这个module里面有两个variables是global的，他们是：db和table
from sqlite3 import connect
from tkinter import *
from fetchsqlite import Conn
from tkinter import ttk
from tkinter.messagebox import *
from rooms import *
from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename, asksaveasfilename  
import os, sys
import csv, glob
    
class SpecimenGUI(Frame, Conn):
    
    def __init__(self, parent = None, dbfile = None):
        Frame.__init__(self, parent)       
        Conn.__init__(self, dbfile)
        self.master.title("表格文件搜索")
        #image = PhotoImage(file = 'search.gif')
        #self.tk.call('wm','iconphoto', self.master._w, image)
        self.master.geometry("402x220+30+30")
        self.master.config(bg="beige")
        self.master.resizable(width= False, height= False)#this makes the window unresizable    
        self.initUI()
        
        self.dbfile = dbfile#如果不提供sqlite3数据库文件，默认为None
        global db, table #让这两个variables成为global
        if self.dbfile ==None:
            table = None# 如果没有提供sqlite3数据库文件，那table也将成为None
            db=None #db也将成为None,这样在下面的SelectConditions类中， getFieldsName得到的是个空字符
        else:#如果self.dblife不是None，也就是说提供了sqlite3数据库文件，则：
            self.db = Conn(self.dbfile)# 增加一个属性.db
            self.table = Conn.getTableInfo(self)           
            db = self.db
            table = '%s' % self.table  #取得表头名称， scope为global       
        self.automateLoadDbfile()#次序很重要，只能放这里。当程序启动时自动加载数据库
        
    def initUI(self):
        top = Menu(self.master)
        self.master.config(menu = top)
        file = Menu(top)
        file.add_command(label = "Unload..", command = self.unloadDbfile, underline = 0)
        file.add_command(label = 'Import..', command = self.askImportCondition, underline = 0)
        file.add_command(label = 'Load..', command = self.automateLoadDbfile, underline = 0)
        top.add_cascade(label = '文件', menu = file)
       
        
        BX = 50
        BY = BX 
        CEIL= 40            #显示按钮的宽度和高度 
        FONT= ('bold', 9)          
        TEXT = ["位置信息","搜索样本","更新数据", "退出"]
        COMMAND = [self.location, self.anotherWindow, self.notdone,self.master.destroy]
        COLOR = ["cyan4"]*4
        
        for i in range(len(TEXT)):
            widgets = Button(self.master, command = COMMAND[i])
            widgets.place( x = 20 + i *100 , y = CEIL, width = BX, height = BY)
            
            widgets.config(text = TEXT[i], bg = COLOR[i], font = FONT,relief = RAISED, bd= 2)
        
        markbutton = Button(self.master, text = "by 张伟")
        markbutton.place( x = 0, y = 110, width = 402, height= 30)
        markbutton.config( bg= 'snow',relief = SUNKEN, bd = 2)
    
    def location(self):
        top = Toplevel(self)
        RoomsButton(top).mainloop()
    
    def notdone(self):
        showerror('错误', '相关功能还没有植入！')
        
    def askImportCondition(self):
        questions =["导入文件的分隔符："," 导入后保存的文件名："]
        top = Toplevel(self)
        askimport = CollectInformation(top, question = questions)
        top.wait_window()# 必须得说，这是一个非常神奇的恐怖的存在！！！！！！！！！！！！！
        answerlist = askimport.getAnswer()
        #输入的文件名称增加到属性
        #加了一个后缀名,用来作为特别的一个marker,以便自动加载
        if type(answerlist)==type([]):
            self.dbname = answerlist[1]+".MedBioSoft"
        #print(answerlist)
        if answerlist:#如果answerlist不是None,就导入所需要的文件(txt, csv)
            self.fileImport(dbname = self.dbname, delimiter = answerlist[0])
    #下面这个方法：提供导入 ##文件的分隔符##和 ##创建的数据库名称##，将导入的文件，创建为sqlite3数据库文件            
    def fileImport(self, dbname, delimiter='\t'):
        filename = askopenfilename()
        if (delimiter =='Tab') | (delimiter =='tab'):
            delimiter = '\t'
        if len(filename)!=0:
            #连接数据库，如果不存在就在先途径下创建一个数据库，名为：dbname.MedBioSoft
            conn = connect(dbname)
            curs= conn.cursor()
            file = open(filename, "r")#读取要导入sqlite3的文件
            file.seek(0)#确保读取的光标回到第一行
            header = (file.readline().rstrip()).split(delimiter)#文件第一行作为header，去掉最后的\n，及分隔符成为一个list
            file.close()
            file = csv.reader(open(filename, 'r'), delimiter=delimiter)
            filename = os.path.basename(filename)
            tablename = (filename.split('.'))[0]#把要导入的文件去掉后缀名如.txt，把留下的作为table名称
            #以下为了让格式符合Python3中调用sqlite3的命令，进行了字符串的一系列方法调用
            condition = '%s TEXT,'* len(header)
            condition = condition[0:len(condition)-1]#去掉最后的一个逗号
            # 创建数据库的fields及type的语句,为了符合一般情况，均进行了 string 的 formatting
            allcondition = condition % tuple(header)
            query_create = 'CREATE TABLE %s (id INTEGER PRIMARY KEY, %s)' % (tablename, allcondition)
            
            question_mark = "?," * len(header)
            question_mark = question_mark[0: len(question_mark)-1]
            # 把数据插入数据库中的语句，为了符合一般情况，均进行了 string 的 formatting
            query_insert = 'INSERT INTO %s %s VALUES (%s)' % (tablename, tuple(header),question_mark )
            curs.execute(query_create)    
            # 把读数据的光标移到第二行，因为表头不需要读进去：0为第一行，1为第二行。别忘了0作为第一个index
            for row in file:
                to_db=[]
                for i in range(len(header)):                    
                    to_db.append(row[i])
                curs.execute(query_insert, to_db)
            conn.commit()#提交到数据，这时候还是连在数据库文件上的#这时候再工作目录中生成的
            #数据库文件里面就有了数据
            conn.close()
            self.loadDbfile()#将生成的数据库文件加载到程序
        
    def loadDbfile(self):
        global db, table
        db = Conn(self.dbname)
        table =Conn.getTableInfo(db) 
        table = '%s' % table 
    
    
    #虽然导入文件进程序后，创建了数据库文件到硬盘上，但是在退出程序后，
    #再打开程序，创建的数据库文件没有自动加载进来，为了避免每次都要导入数据
    #创建一个方法：打开程序后自动加载进前一次创建的数据库文件
    def automateLoadDbfile(self):
        dbfilelist= glob.glob('*.medbiosoft')
        #print(dbfilelist)
        if len(dbfilelist) !=0:#检查是否存在创建好的含特别标识的数据库文件
            self.dbname = dbfilelist[0]
            self.loadDbfile()
 
    #有了自动加载文件的功能，同时也要有手动unload数据库文件的功能
    def unloadDbfile(self):
        self.dbname = None
        global db, table
        db = None
        table=None
    
       
    def getTable(self):
       
        cur = Conn.getCursor(self)
        cur.execute('select type, name from sqlite_master')
        allTableNames = [table[1] for table in cur.fetchall()]
        cur.close()
        self.textInsert(str(allTableNames))
        
    
        
    def textInsert(self, content):
        self.text.delete('1.0', END)
        self.text.insert('1.0', content)
        
    def clear(self):
        self.text.delete('1.0', END)
     
    #点击"搜索条件"按钮时，弹出另一个窗口    
    def anotherWindow(self):
        frame =Toplevel(self)
        SelectConditions(frame).mainloop()




class SelectConditions(Frame):   
    def __init__(self, parent=None, text = None, txt = 'here ', count =0):
        Frame.__init__(self, parent)
        self.pw = PanedWindow(self.master, orient = VERTICAL)
        self.bottom = Text(self.pw)
        self.up= Frame(self.pw)
        self.pw.add(self.bottom)
        self.pw.add(self.up)
        self.pw.pack(side = BOTTOM, fill =BOTH, expand = YES)
        self.pw.update_idletasks()
        self.pw.proxy_place(*self.pw.sash_coord(0))
        self.pw.proxy_forget()
        
        #self.master.bind('<Left>', self.on_down)
        #self.master.bind('<Right>', self.on_up)
        #self.master.bind('<Return>', self.on_return) 
        self.selectboxlogic = ttk.Combobox(self.up)
        self.selectbox2 = ttk.Combobox(self.up)
        self.entry2 = Entry(self.up)
        
        self.count = count
        self.pack(side = TOP)
        self.setFieldsName()
        self.initUI()
    
    def on_down(self, ev):
        x,y = self.pw.proxy_coord()
        self.pw.proxy_place(x, y-1)

    def on_up(self,ev):
        x,y = self.pw.proxy_coord()
        self.pw.proxy_place(x, y+1)
    
    def on_return(self, ev):
        self.pw.sash_place(0, *self.pw.proxy_coord())
        self.pw.proxy_forget()
       
        
    def initUI(self):
        self.master.geometry("600x400+20+20")
        self.master.resizable( width=0, height= 0)
        TEXT = ["搜索", "清除屏幕", "保存为", "更新数据"]
        COMMAND=[self.searchResult, self.clearScreen, self.save,self.notdone ]
        for i in range(len(TEXT)):
            button = Button(self.up, text = TEXT[i], command = COMMAND[i])
            button.config(font = ('helvetical', 10), relief = RAISED, bd = 2)
            button.place(x = 70+i*140, y = 5, width = 60, height =40)
        
        self.addEntry()
        self.addPlusButton()
        self.addminusButton()
        self.addSelectBox()
        self.setSelectBoxValue()
        
        self.text = Text(self.bottom, relief = SUNKEN)
        self.sbar = Scrollbar(self.text)
        
        self.sbar.config(command = self.text.yview)
        self.text.config(yscrollcommand= self.sbar.set)
        self.sbar.pack(side = RIGHT, expand = NO, fill = Y)
        self.text.pack(side = LEFT, expand = YES, fill = BOTH)
        
        
      
   
    def addSelectBox(self):
        
        fieldvar = StringVar()       
        self.selectbox = ttk.Combobox(self.up, textvariable = fieldvar)
        self.selectbox.place(x = 10, y = 50, width = 200, height = 20)        
        # 这里面显示的是 搜索满足的条件值
    def addEntry(self):
        
        self.entry = Entry(self.up)
        self.entry.place(x = 220, y = 50, width = 200, height = 20)
            
    def addPlusButton(self):
        buttonadd = Button(self.up, text = "+", command = self.searchPlus)
        buttonadd.place( x = 422, y = 50, width = 20, height = 20)
        self.buttonadd = buttonadd
        
        #点击“+”按钮后 可选菜单和输入框复制
    def searchPlus(self):
        self.count +=1
        addY = 60*self.count
        
        
        self.selectboxlogic.place( x = 10, y = 50+ 30, width = 50, height = 20)
        self.selectboxlogic['value']=['AND','OR']
        
       
        self.selectbox2.place( x = 10, y = 50+addY, width = 200, height =20)
        self.selectbox2['value'] = self.fieldsname
        
        
        self.entry2.place(x = 220, y = 50+addY, width = 200, height = 20)
        

    def addminusButton(self):
        buttonminus = Button(self.up, text = "-", command = self.searchMinus)
        buttonminus.place(x = 450, y = 50, width = 20, height = 20)
        self.buttonminus= buttonminus
        
    def searchMinus(self):
        self.count -= 1
        
        self.selectbox2.destroy()
        self.entry2.destroy()
        self.selectboxlogic.destroy()
        self.selectboxlogic = ttk.Combobox(self.up)
        self.selectbox2 = ttk.Combobox(self.up)
        self.entry2 = Entry(self.up)

    def setSelectBoxValue(self):
        self.selectbox['value']= self.fieldsname
        
        
    
    def setFieldsName(self):
        if db ==None:
            self.fieldsname = ''
        else:            
            self.fieldsname = db.getColumnNameWithinTable(table)
        
    def getSelectBoxValue(self):
        return (self.selectbox.get())
    
    def getSelectBoxlogicValue(self):
        
        return self.selectboxlogic.get()
        
    def getSelectBox2Value(self):
        
        return self.selectbox2.get()
        
    
    def getEntryValue(self):
        ent = self.entry.get()
        return (ent)
    
    def getEntry2Value(self): 
        return self.entry2.get()
    
    #保存文件
    def save(self):
        filename = asksaveasfilename(defaultextension="TXT")
        if len(filename)!=0:
            file = open(filename, 'w')
            file.write( self.text.get('1.0', END))
            file.close()
            
    def searchResult(self):               
            columnName = self.getSelectBoxValue()
            columnValue = self.getEntryValue()
            columnName2 = self.getSelectBox2Value()
            columnValue2 = self.getEntry2Value()
            logicvalues = self.getSelectBoxlogicValue()
            if len(columnName)==0:
                showerror("错误！", " 请至少输入一个搜索条件！")
            elif columnName not in self.fieldsname:
                showwarning("提示", "不存在这一列名")
            else:
                cur = db.getCursor() 
            
                if (len(columnValue2) !=0 ) & (len(logicvalues) !=0) & (len(columnName2)!=0):
                    query = 'select * from %s where %s = "%s" %s %s = "%s"' %(table, columnName, columnValue, logicvalues.lower(), columnName2, columnValue2)
                else:
                    query = 'select * from %s where %s = "%s"' % (table,columnName, columnValue)
                
                cur.execute(query)
            
                value = cur.fetchall()
                if len(value) != 0:
                    self.textInsert(self.formatting(self.fieldsname, value))
                else:
                    self.textInsert("没有搜索到您要找的内容，请更改条件后再次搜索！")
                                
    def formatting(self, header, lists):
        string = ''
        count = 1
        for item in lists:
            newlists = list(zip(header,item))
            for newitem in newlists:
                string += (str(count)+'%s:   %s\n'+ '-' *98 + '\n') % newitem
            count +=1
            string += "#"*98+"\n"
        return string
             
    def textInsert(self, content):
        self.clearScreen()
        self.text.insert('1.0', content)
        
    def clearScreen(self):
        self.text.delete('1.0', END)
            
    def notdone(self):
        showerror('错误', '相关功能还没有植入！') 




class CollectInformation(Frame):
    def __init__(self, parent = None, question=['Q1', 'Q2', 'Q3']):
        Frame.__init__(self, parent)
        self.question = question
        
        self.pack()
        self.toAddEntry()
        self.toAddButtons()
        
    def toAddEntry(self):
        self.ent = []#准备把Entry object 放进list中
        for i in range(len(self.question)):
            row = Frame(self)
            row.pack(side =TOP, fill = X)
            lab = Label(row, width = 20, text = self.question[i])
            ent =Entry(row)
            lab.pack(side = LEFT)
            ent.pack(side = RIGHT, expand = YES, fill = X)  
            self.ent.append(ent)#把Entry object 放进list中
            
            
    def toAddButtons(self):
        TEXT = ["确定", "取消"]
        COMMAND = [self.sure, self.master.destroy]
        for i in range(len(TEXT)):
            Button(self, text = TEXT[i], command = COMMAND[i]).pack(side = LEFT)
    #sure为点击确定按钮后的一系列事件       
    def sure(self):
        self.answer= []#点击确定按钮后，赋予一个answer值:一个空的list
        for i in self.ent:
            if len(i.get()) !=0:#在逐个对entry里的内容检查不是空字符后，放进self.answer的list中
                self.answer.append(i.get())
            else:#只要里面有一个是空字符，显示错误对话框
                showerror("Error!", "条件不能为空")
                self.answer = None
                break#退出循环
        self.master.destroy()#最后让弹出的窗口消失， self.answer 留下
    #这个方法为获取answer这个属性。
    def getAnswer(self):
        if hasattr(self, 'answer'):
            return self.answer
        return None
        
       
        
root = Tk()        
SpecimenGUI(root).mainloop()
      
       
