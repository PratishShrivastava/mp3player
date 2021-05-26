import cx_Oracle
import traceback
conn=None
try:
    dns_tns=cx_Oracle.makedsn("localhost","1522",service_name="xe")
    conn=cx_Oracle.connect(user="System",password="Music",dsn=dns_tns)
    print("connected to db")
    print("version",conn.version)
    print("DB user: ",conn.username)
except cx_Oracle.DatabaseError:
    print(traceback.format_exc())
finally:
    if conn is not None:
        conn.close()
        print("disconected from db")