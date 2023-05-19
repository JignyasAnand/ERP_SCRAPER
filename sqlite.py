import json
import sqlite3


class SQLOBJ:
    def __init__(self):
        self.conn = sqlite3.connect("res.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("create table if not exists results (uid text, component text, cid text)")

    def insert(self,uid, obj, cid):
        dtext = json.dumps(obj)
        # print("Inside")
        # print(obj)
        self.cursor.execute("insert into results values (?,?,?)",(uid, dtext, cid))
        self.cursor.execute("commit")
    def delete(self, uid):
        self.cursor.execute("delete from results where uid=(?)", (uid,))
        self.cursor.execute("commit")

    def get(self, uid, cid):
        query = "select * from results where uid=? and cid=?"
        self.cursor.execute(query, (uid, cid))
        res=[]
        for row in self.cursor.fetchall():
            res.append(row[1])
        return res

if __name__ == '__main__':
    obj = SQLOBJ()
    obj.insert(123, {"name":"bye"}, 12)
    # obj.delete(123)
    res=obj.get("25cd2c68-70bc-4d0d-a124-2ceb686a477d", "internals")
    print(json)