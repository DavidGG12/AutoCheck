import sqlite3

class InitDataBase:
    def __init__(self):
        self._con = sqlite3.connect('AutoCheck.db')
        self._cur = self._con.cursor()

    def getConnection(self) -> sqlite3.Connection:
        return self._con

    def getCursor(self) -> sqlite3.Cursor:
        return self._cur
    
    def creatingTable(self) -> None:
        self._cur.execute('''CREATE TABLE ExecuteProcess (NumberOfExecutions text)''')
        self._cur.execute("INSERT INTO ExecuteProcess VALUES('0')")
        self._con.commit()

    def deletingTable(self) -> None:
        try:
            self._cur.execute("DROP TABLE ExecuteProcess")
        except Exception as ex:
            raise ValueError(ex)

    def updExecuteProcess(self, data: str) -> str:
        try:
            self._cur.execute("UPDATE ExecuteProcess SET NumberOfExecutions = ? WHERE NumberOfExecutions = '0'", data)
            return "Row updated"
        except Exception as ex:
            return f"There was an unexpected error while executing update: {ex}"
        
    def slExecuteProcess(self):
        try:
            for x in self._cur.execute("SELECT * FROM ExecuteProcess"):
                print(x)
        except Exception as ex:
            return f"There was an unexpected error while executing select: {ex}"

    def closeConnection(self) -> None:
        self._con.close()

lol = InitDataBase()
# lol.deletingTable()
# lol.creatingTable()
lol.slExecuteProcess()
lol.updExecuteProcess("1")
lol.slExecuteProcess() 
lol.closeConnection()

