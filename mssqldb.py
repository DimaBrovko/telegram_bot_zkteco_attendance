import pypyodbc
from config import SQLServer,Database, login_db,passwrd_db

connection = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'Server= ' + SQLServer + ';'
                              'Database=' + Database + ';'
                              'uid='+ login_db +';'
                              'pwd='+ passwrd_db +';'
                              )

cursor = connection.cursor()

SQLQuery = ("""
            SELECT DISTINCT TOP(1) pin, time, Name, CONVERT(varchar, time, 8) AS hhmmss, CONVERT(varchar, time, 4) AS day
            FROM dbo.acc_monitor_log 
            INNER JOIN dbo.USERINFO 
                ON dbo.acc_monitor_log.pin = dbo.USERINFO.Badgenumber
            WHERE time >= ? AND Name= ?
            ORDER BY hhmmss
            ;
            """)

def last_attendance_BO(massage_list):
    name2 = str(massage_list[0])
    day_time = massage_list[1]
    params = [day_time, name2]
    cursor.execute(SQLQuery, params)
    results = cursor.fetchall()
    last_coming=[]
    for row in results:
        last_coming.append({
            'pin': row[0],
            'hhmmss': row[3],
            'Name': row[2],
            'day': row[4]
        })
    return last_coming

#connection.close()