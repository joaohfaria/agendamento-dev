
import sqlite3; 
db = sqlite3.connect('database.db'); 
print(db.execute("SELECT sql FROM sqlite_master WHERE name='servicos'").fetchone()[0])