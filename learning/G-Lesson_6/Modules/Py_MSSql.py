import sys
import pandas as pd
import pyodbc
import numpy as np
from pandas.api.types import is_string_dtype
from pandas.api.types import is_datetime64_any_dtype
from pandas.api.types import is_numeric_dtype

class Py_MSSql:

    def __init__(self,server = "XXX", database = "YYY", host_port = "HOST_XXX"):

        self.df = None
        self.columnNameLst = None          
        self.columnAndTypesStr = None
        self.server = server
        self.database = database
        self.conn_host_port = host_port
        self.conn_encoding = "UTF-8"
        self.conn_nencoding = "UTF-8"
        self.conn = None
        self.max_varchar_len_sql = 8000
        self.__connect()

    def __connect(self):                
        try: 
            self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+self.server+';DATABASE='+self.database+';')#, nencoding = self.con_nencoding)
            #return self.conn

        except Exception as e:
            print(str(e)) 
            raise    

    def close(self):
        try:
            self.conn.close()            

        except Exception as e:
            print(str(e))
            raise            

    def get_conn(self):
        return self.conn

    def execute_query(self, query, commit = False):    
        try:
            cur = self.conn.cursor()            
            cur.execute(query)
                
            if commit:
                cur.execute("commit")
            cur.close()
            return True

        except Exception as e:
            print("QUERY failed: ", e )  
            raise           

    def __get_column_types(self):
        try:
            # convert array of columns names to list
            self.columnNameLst = list(self.df.columns.values) 
            columnAndTypesLst = []
            for colName in self.columnNameLst:
                if is_numeric_dtype(self.df[colName]):
                    columnAndTypesLst.append(colName + ' NUMERIC(18,10)')
                elif is_datetime64_any_dtype(self.df[colName]):
                    columnAndTypesLst.append(colName + ' DATETIME2')                               
                elif is_string_dtype(self.df[colName]):                                  
                    colLen = self.df[colName].str.len().max()                   
                    colLen = int(colLen*2 if colLen < self.max_varchar_len_sql/2  else self.max_varchar_len_sql)   
                    columnAndTypesLst.append(colName + ' VARCHAR('+str(colLen)+')')

            self.columnAndTypesStr = ", ".join(columnAndTypesLst)
            return True

        except Exception as e:
            print(str(e))
            raise           
            

    def create_tbl_from_df(self, df, tbl_trgt):
        try:
            self.df = df
            if self.__get_column_types():
                cur = self.conn.cursor() 
                create_query = "CREATE TABLE " + tbl_trgt + " (" + self.columnAndTypesStr + ")"           
                print(create_query)
                cur.execute(create_query)               
                cur.execute('commit')     
                cur.close()                 

            else:
                print("problem in __get_column_types() ")   
                #ARIEL FIX: raise Exception           

        #except cx_Oracle.DatabaseError as e:
        except Exception as e:
            print("table creation failed: ", e )
            raise       

    def insert_into_tbl_from_df(self, df, tbl_trgt):
        try:
            # df.where: if value is not NaN leave it, else: replace with None to enable INSERTING NULL to DB, otherwise it will fail
            # (another elegant working option: df = df.replace({pd.np.nan: None}))
            self.df = df.where(pd.notnull(df), None)
            self.columnNameLst = list(self.df.columns.values)
            columnNames = ", ".join(self.columnNameLst)   

            # extract list of tuples because it's the 2nd argument of cur.executemany           
            list_of_tuples = list(self.df.itertuples(index=False, name=None))                                  
            values_quotm = "?,"*len(self.columnNameLst)    
            print(values_quotm,len(columnNames))        
            insrt_query = "INSERT INTO " + tbl_trgt + " ("+ columnNames +") VALUES("+values_quotm[:-1]+")"     
            print ("INSERT QUERY:"+insrt_query)

            # the cursor is for the sql execute
            cur = self.conn.cursor()     
            cur.fast_executemany = True       
            cur.executemany(insrt_query, list_of_tuples)
            self.conn.commit()
            cur.close()
            return True

        except Exception as e:
            print("table insertion failed: ", e )
            raise                       


    def drop_table_if_exist(self, tbl, schema="dbo"):
        try:               
            cur = self.conn.cursor()                       
            drop_query = "IF OBJECT_ID('"+schema+"."+tbl+"', 'U') IS NOT NULL DROP TABLE "+schema+"."+tbl  
            print (drop_query)                        
            cur.execute(drop_query)  
            self.conn.commit()         
            cur.close()                      

        except Exception as e:
            print("drop table failed: ", e )
            raise            

    def read_sql_query(self,sql_query):         
        try:
            df = pd.read_sql_query(sql_query, self.conn)
            return df
        except Exception as e:
            print("read_sql_query failed: ", e )
            raise   
         
