###########################################  Database SQLite ##################################

#Importing Sqlite module 
# import sqlite3

# #Creating Database and Connect 
# db = sqlite3.connect("app.db")

# # Setting up the cursor 

# cr = db.cursor()

# # Creating Rows and Columns using cursor 
# cr.execute("CREATE TABLE if not exists users (user_id INTEGER , name TEXT)")
# cr.execute("CREATE TABLE if not exists skills (name TEXT , progress INTEGER , user_id INTEGER)")

# # Inserting Data 

# # names = ["Ahmed" , "Islam", "Zain" , "Ehab" , "Mamdouh" , "Kamal" , "Sameh"]
# # # Looping to extract name and its index from the above list
# # for index,name in enumerate(names) :
# #     cr.execute(f"INSERT INTO USERS(user_id, name) values({index + 1}, '{name}')")

# # Fetch Data 
# cr.execute("select * from users ")



# # Saving Changes 
# db.commit()
# # Close Database 
# db.close()

############################## End of learn and Test Part ##############################################################

# importing Libs 
import sqlite3

names = ["Ahmed" , "Islam"]

def close_connection_to_database(db):
    if(db):
        # Closing connection to database 
        db.commit()
        db.close()
        print("Connection to Database is closed")


def connect_to_database():
    err = -1
    try:
        # Create Connection to database
        db = sqlite3.connect("app.db")
        return db
    except sqlite3 as  err:
        print(f"Error Reading Data {err}")
        return err
 

def get_all_data(db):
    if(db == -1):
        pass
    else:
        print("Connected to Database Succefully")
    # Setting Up Cursur 
    cr = db.cursor()
    for index,name in enumerate(names) :
        cr.execute(f"INSERT INTO USERS(user_id, name) values({index + 1}, '{name}')")
    # Update Data  
    cr.execute("UPDATE users set name = 'Gamal' WHERE user_id =1")

    # Deleting Rows 
    cr.execute("DELETE FROM skills ")
    # Fetch Data from Database
    cr.execute("SELECT * FROM users")
    # Assign Data to variable ' List of tuples '
    result = cr.fetchall()
    # Number of Rows 
    print(f"Number of Rows in Database = {len(result)}")
    # Showing Data 
    for row in result :
        # print(f"UserID => {row[0]}   Name => {row[1]}")
        print(f"UserID => {row[0]}",end=",")
        print(f"Name => {row[1]}")

    
   

db = connect_to_database()
get_all_data(db)
close_connection_to_database(db)

