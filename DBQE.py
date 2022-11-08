import sqlite3
#create DB and table events
def create_db():
    conn=sqlite3.connect("QE.db")
    cur=conn.cursor()
    sql_create_tables="""
    CREATE TABLE events ( 
        StartDate DATETIME NOT NULL,
        EndDate DATETIME,  
        Name CHAR(255) NOT NULL, 
        Location CHAR(255),
        PRIMARY KEY (StartDate,Name)
        );"""
    cur.execute(sql_create_tables)
    sql_create_index="""CREATE UNIQUE INDEX idx_date
    ON events (StartDate);"""
    cur.execute(sql_create_index)
    conn.close()

#commit to db, event as tuple, return event id
def commit_to_db(event):
    try:
        conn=sqlite3.connect("QE.db")
        cur=conn.cursor()
        cur.execute("""
        INSERT INTO events (StartDate,EndDate,Name,Location)
        VALUES(?,?,?,?);""",
        event)
        conn.commit()
        id=cur.lastrowid
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

#get events from db as list
def get_all_db():
    conn=sqlite3.connect("QE.db")
    cur=conn.cursor()
    events=[]
    for row in cur.execute("""SELECT rowid,* FROM events"""):
        events.append(row)
    conn.close()
    return events

def get_next_x_db(date,x):
    conn=sqlite3.connect("QE.db")
    cur=conn.cursor()
    events=[]
    for row in cur.execute("""SELECT rowid,* FROM events WHERE EndDate>=? ORDER BY StartDate ASC LIMIT ?;""",(date,x)):
        events.append(row)
    conn.close()
    print("DB closed")
    print(date)
    return events

#delete event from DB based on id
def delete_from_db(id):
    try :
        conn=sqlite3.connect("QE.db")
        cur=conn.cursor()
        cur.execute("""
        DELETE FROM events WHERE rowid=?;""",(id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False

#update event in DB based on id
def update_db(event):
    try :
        conn=sqlite3.connect("QE.db")
        cur=conn.cursor()
        cur.execute("""
        UPDATE events SET StartDate=?,EndDate=?,Name=?,Location=? WHERE rowid=?;""",event)
        conn.commit()
        conn.close()
        return True
    except:
        return False