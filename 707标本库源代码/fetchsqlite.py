#coding=gb2312
from sqlite3 import connect



class Conn:
        def __init__(self, dbfile):
                self.dbfile = dbfile
        
        #连接上数据库文件，并且得到cursor
        def getCursor(self):
                conn = connect(self.dbfile)
                cur = conn.cursor()
                return cur

        def getTableInfo(self):
                cur = Conn.getCursor(self)
                cur.execute('select type, name from sqlite_master')
                allTableNames = [table[1] for table in cur.fetchall()]
                cur.close()
                return allTableNames[0]
        
        #以下方法的用法为：提供一个数据库的table名称，将得到这个table的列名称(表头)
        def getColumnNameWithinTable(self, tableName):
                query = 'select * from %s' % (tableName)
                cur = Conn.getCursor(self)
                cur.execute(query)
                column = [column[0] for column in cur.description]
                return column
                

        def search(self ,tableName, columnName, columnValue):
                cur = Conn.getCursor(self)
                query = 'select * from %s where %s= "%s" ' % (tableName, columnName, columnValue) 
                cur.execute(query)
                lists = cur.fetchall()
                header = Conn.getColumnNameWithinTable(self,tableName)
                self.show(lists, header)#show function is imported from somedefs module
                
        def show(self, lists, header):            
            for i in range(len(lists)):
                for j in range(len(header)):
                    print(header[j], ":%s\n" % lists[i][j])
                print("###########################\n")
        
        def getAllcolumnNames(self):
            alltablenames = Conn.getTableInfo(self)
            names = []
            for table in alltablenames:
                names += Conn.getColumnNameWithinTable(self, table)
            return list(set(names))
        
#if __name__ =='__main__':
 #       db = Conn(None)
  #      print(db.getTableInfo())



