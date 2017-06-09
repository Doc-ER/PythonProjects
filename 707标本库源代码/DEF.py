#coding=gb2312
from sqlite3 import connect
import os
import csv


def fileimport(filename,dbname,delimiter='\t'):
        #filename = askopenfilename()
        if len(filename)!=0:
            Conn = connect(dbname)#�������ݿ⣬��������ھʹ���һ�����ݿ⣬��Ϊ��'db.db'
            curs= Conn.cursor()
            file = open(filename, "r")#��ȡҪ����sqlite3���ļ�
            file.seek(0)#ȷ����ȡ�Ĺ��ص���һ��
            header = (file.readline().rstrip()).split(delimiter)#�ļ���һ����Ϊheader��ȥ������\n�����ָ�����Ϊһ��list
            file.close()
            file = csv.reader(open(filename, 'r'), delimiter=delimiter)
            filename = os.path.basename(filename)
            tablename = (filename.split('.'))[0]#��Ҫ������ļ�ȥ����׺����.txt�������µ���Ϊtable����
            #����Ϊ���ø�ʽ����Python3�е���sqlite3������������ַ�����һϵ�з�������
            condition = '%s CHAR,'* len(header)
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
            Conn.commit()
            Conn.close()
            
