#coding=gb2312
from sqlite3 import connect
import os
import csv


def fileimport(filename,dbname,delimiter='\t'):
        #filename = askopenfilename()
        if len(filename)!=0:
            Conn = connect(dbname)#连接数据库，如果不存在就创建一个数据库，名为：'db.db'
            curs= Conn.cursor()
            file = open(filename, "r")#读取要导入sqlite3的文件
            file.seek(0)#确保读取的光标回到第一行
            header = (file.readline().rstrip()).split(delimiter)#文件第一行作为header，去掉最后的\n，及分隔符成为一个list
            file.close()
            file = csv.reader(open(filename, 'r'), delimiter=delimiter)
            filename = os.path.basename(filename)
            tablename = (filename.split('.'))[0]#把要导入的文件去掉后缀名如.txt，把留下的作为table名称
            #以下为了让格式符合Python3中调用sqlite3的命令，进行了字符串的一系列方法调用
            condition = '%s CHAR,'* len(header)
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
            Conn.commit()
            Conn.close()
            
