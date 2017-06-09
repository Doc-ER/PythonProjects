#coding= gb2312
#���module����������variables��global�ģ������ǣ�db��table
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
        self.master.title("����ļ�����")
        #image = PhotoImage(file = 'search.gif')
        #self.tk.call('wm','iconphoto', self.master._w, image)
        self.master.geometry("402x220+30+30")
        self.master.config(bg="beige")
        self.master.resizable(width= False, height= False)#this makes the window unresizable    
        self.initUI()
        
        self.dbfile = dbfile#������ṩsqlite3���ݿ��ļ���Ĭ��ΪNone
        global db, table #��������variables��Ϊglobal
        if self.dbfile ==None:
            table = None# ���û���ṩsqlite3���ݿ��ļ�����tableҲ����ΪNone
            db=None #dbҲ����ΪNone,�����������SelectConditions���У� getFieldsName�õ����Ǹ����ַ�
        else:#���self.dblife����None��Ҳ����˵�ṩ��sqlite3���ݿ��ļ�����
            self.db = Conn(self.dbfile)# ����һ������.db
            self.table = Conn.getTableInfo(self)           
            db = self.db
            table = '%s' % self.table  #ȡ�ñ�ͷ���ƣ� scopeΪglobal       
        self.automateLoadDbfile()#�������Ҫ��ֻ�ܷ��������������ʱ�Զ��������ݿ�
        
    def initUI(self):
        top = Menu(self.master)
        self.master.config(menu = top)
        file = Menu(top)
        file.add_command(label = "Unload..", command = self.unloadDbfile, underline = 0)
        file.add_command(label = 'Import..', command = self.askImportCondition, underline = 0)
        file.add_command(label = 'Load..', command = self.automateLoadDbfile, underline = 0)
        top.add_cascade(label = '�ļ�', menu = file)
       
        
        BX = 50
        BY = BX 
        CEIL= 40            #��ʾ��ť�Ŀ�Ⱥ͸߶� 
        FONT= ('bold', 9)          
        TEXT = ["λ����Ϣ","��������","��������", "�˳�"]
        COMMAND = [self.location, self.anotherWindow, self.notdone,self.master.destroy]
        COLOR = ["cyan4"]*4
        
        for i in range(len(TEXT)):
            widgets = Button(self.master, command = COMMAND[i])
            widgets.place( x = 20 + i *100 , y = CEIL, width = BX, height = BY)
            
            widgets.config(text = TEXT[i], bg = COLOR[i], font = FONT,relief = RAISED, bd= 2)
        
        markbutton = Button(self.master, text = "by ��ΰ")
        markbutton.place( x = 0, y = 110, width = 402, height= 30)
        markbutton.config( bg= 'snow',relief = SUNKEN, bd = 2)
    
    def location(self):
        top = Toplevel(self)
        RoomsButton(top).mainloop()
    
    def notdone(self):
        showerror('����', '��ع��ܻ�û��ֲ�룡')
        
    def askImportCondition(self):
        questions =["�����ļ��ķָ�����"," ����󱣴���ļ�����"]
        top = Toplevel(self)
        askimport = CollectInformation(top, question = questions)
        top.wait_window()# �����˵������һ���ǳ�����Ŀֲ��Ĵ��ڣ�������������������������
        answerlist = askimport.getAnswer()
        #������ļ��������ӵ�����
        #����һ����׺��,������Ϊ�ر��һ��marker,�Ա��Զ�����
        if type(answerlist)==type([]):
            self.dbname = answerlist[1]+".MedBioSoft"
        #print(answerlist)
        if answerlist:#���answerlist����None,�͵�������Ҫ���ļ�(txt, csv)
            self.fileImport(dbname = self.dbname, delimiter = answerlist[0])
    #��������������ṩ���� ##�ļ��ķָ���##�� ##���������ݿ�����##����������ļ�������Ϊsqlite3���ݿ��ļ�            
    def fileImport(self, dbname, delimiter='\t'):
        filename = askopenfilename()
        if (delimiter =='Tab') | (delimiter =='tab'):
            delimiter = '\t'
        if len(filename)!=0:
            #�������ݿ⣬��������ھ�����;���´���һ�����ݿ⣬��Ϊ��dbname.MedBioSoft
            conn = connect(dbname)
            curs= conn.cursor()
            file = open(filename, "r")#��ȡҪ����sqlite3���ļ�
            file.seek(0)#ȷ����ȡ�Ĺ��ص���һ��
            header = (file.readline().rstrip()).split(delimiter)#�ļ���һ����Ϊheader��ȥ������\n�����ָ�����Ϊһ��list
            file.close()
            file = csv.reader(open(filename, 'r'), delimiter=delimiter)
            filename = os.path.basename(filename)
            tablename = (filename.split('.'))[0]#��Ҫ������ļ�ȥ����׺����.txt�������µ���Ϊtable����
            #����Ϊ���ø�ʽ����Python3�е���sqlite3������������ַ�����һϵ�з�������
            condition = '%s TEXT,'* len(header)
            condition = condition[0:len(condition)-1]#ȥ������һ������
            # �������ݿ��fields��type�����,Ϊ�˷���һ��������������� string �� formatting
            allcondition = condition % tuple(header)
            query_create = 'CREATE TABLE %s (id INTEGER PRIMARY KEY, %s)' % (tablename, allcondition)
            
            question_mark = "?," * len(header)
            question_mark = question_mark[0: len(question_mark)-1]
            # �����ݲ������ݿ��е���䣬Ϊ�˷���һ��������������� string �� formatting
            query_insert = 'INSERT INTO %s %s VALUES (%s)' % (tablename, tuple(header),question_mark )
            curs.execute(query_create)    
            # �Ѷ����ݵĹ���Ƶ��ڶ��У���Ϊ��ͷ����Ҫ����ȥ��0Ϊ��һ�У�1Ϊ�ڶ��С�������0��Ϊ��һ��index
            for row in file:
                to_db=[]
                for i in range(len(header)):                    
                    to_db.append(row[i])
                curs.execute(query_insert, to_db)
            conn.commit()#�ύ�����ݣ���ʱ�����������ݿ��ļ��ϵ�#��ʱ���ٹ���Ŀ¼�����ɵ�
            #���ݿ��ļ��������������
            conn.close()
            self.loadDbfile()#�����ɵ����ݿ��ļ����ص�����
        
    def loadDbfile(self):
        global db, table
        db = Conn(self.dbname)
        table =Conn.getTableInfo(db) 
        table = '%s' % table 
    
    
    #��Ȼ�����ļ�������󣬴��������ݿ��ļ���Ӳ���ϣ��������˳������
    #�ٴ򿪳��򣬴��������ݿ��ļ�û���Զ����ؽ�����Ϊ�˱���ÿ�ζ�Ҫ��������
    #����һ���������򿪳�����Զ����ؽ�ǰһ�δ��������ݿ��ļ�
    def automateLoadDbfile(self):
        dbfilelist= glob.glob('*.medbiosoft')
        #print(dbfilelist)
        if len(dbfilelist) !=0:#����Ƿ���ڴ����õĺ��ر��ʶ�����ݿ��ļ�
            self.dbname = dbfilelist[0]
            self.loadDbfile()
 
    #�����Զ������ļ��Ĺ��ܣ�ͬʱҲҪ���ֶ�unload���ݿ��ļ��Ĺ���
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
     
    #���"��������"��ťʱ��������һ������    
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
        TEXT = ["����", "�����Ļ", "����Ϊ", "��������"]
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
        # ��������ʾ���� �������������ֵ
    def addEntry(self):
        
        self.entry = Entry(self.up)
        self.entry.place(x = 220, y = 50, width = 200, height = 20)
            
    def addPlusButton(self):
        buttonadd = Button(self.up, text = "+", command = self.searchPlus)
        buttonadd.place( x = 422, y = 50, width = 20, height = 20)
        self.buttonadd = buttonadd
        
        #�����+����ť�� ��ѡ�˵����������
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
    
    #�����ļ�
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
                showerror("����", " ����������һ������������")
            elif columnName not in self.fieldsname:
                showwarning("��ʾ", "��������һ����")
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
                    self.textInsert("û����������Ҫ�ҵ����ݣ�������������ٴ�������")
                                
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
        showerror('����', '��ع��ܻ�û��ֲ�룡') 




class CollectInformation(Frame):
    def __init__(self, parent = None, question=['Q1', 'Q2', 'Q3']):
        Frame.__init__(self, parent)
        self.question = question
        
        self.pack()
        self.toAddEntry()
        self.toAddButtons()
        
    def toAddEntry(self):
        self.ent = []#׼����Entry object �Ž�list��
        for i in range(len(self.question)):
            row = Frame(self)
            row.pack(side =TOP, fill = X)
            lab = Label(row, width = 20, text = self.question[i])
            ent =Entry(row)
            lab.pack(side = LEFT)
            ent.pack(side = RIGHT, expand = YES, fill = X)  
            self.ent.append(ent)#��Entry object �Ž�list��
            
            
    def toAddButtons(self):
        TEXT = ["ȷ��", "ȡ��"]
        COMMAND = [self.sure, self.master.destroy]
        for i in range(len(TEXT)):
            Button(self, text = TEXT[i], command = COMMAND[i]).pack(side = LEFT)
    #sureΪ���ȷ����ť���һϵ���¼�       
    def sure(self):
        self.answer= []#���ȷ����ť�󣬸���һ��answerֵ:һ���յ�list
        for i in self.ent:
            if len(i.get()) !=0:#�������entry������ݼ�鲻�ǿ��ַ��󣬷Ž�self.answer��list��
                self.answer.append(i.get())
            else:#ֻҪ������һ���ǿ��ַ�����ʾ����Ի���
                showerror("Error!", "��������Ϊ��")
                self.answer = None
                break#�˳�ѭ��
        self.master.destroy()#����õ����Ĵ�����ʧ�� self.answer ����
    #�������Ϊ��ȡanswer������ԡ�
    def getAnswer(self):
        if hasattr(self, 'answer'):
            return self.answer
        return None
        
       
        
root = Tk()        
SpecimenGUI(root).mainloop()
      
       
