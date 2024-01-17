import sqlite3


#/************************************ Commit and Close Function *************************************************/#
def save_and_close_connection_to_database(db):
    if(db):
        db.commit()
        db.close()
        print("Connection to Database is closed")
#/********************************************************************************************************/#

#/************************************ Connect Function *************************************************/#
def connect_to_database():
    err = -1
    try:
        db = sqlite3.connect("app.db")
        cr = db.cursor()
        return db,cr
    except sqlite3 as  err:
        print(f"Error Reading Data {err}")
        return err
#/********************************************************************************************************/#

#/************************************ Display Function *************************************************/#
def show_skills(db,cr):
    cr.execute(f"SELECT * FROM skills where user_id = '{uID}'")
    result = cr.fetchall()
    if( len(result) <= 0):
        print("You have no skills ")
    else:
        print(f"Number of Rows : {len(result)}")
        print("*** Showing Skills with Progress *** ")
        for row in result:
            print(f"Skill Name : {row[0]} , Progress : {row[1]}")

    save_and_close_connection_to_database(db)
#/********************************************************************************************************/#


#/************************************ Add Function *************************************************/#
def add_skill(db,cr):

    skill_name = input("Write skill_name : ").strip().capitalize() 
    cr.execute(f"SELECT name from skills where name = '{skill_name}' and  user_id = '{uID}'")
    sk_names = cr.fetchall()

    if len(sk_names) > 0:
        print("This Skill name already exist")
        y_n =input("Do you want to update it or not please Enter y for Yes of n for No (y/n) ?")
        if(y_n == 'y'):
            progress = input("Write new skill_progress : ").strip()
            cr.execute(f"UPDATE skills set progress = '{progress}' where name = '{skill_name}' AND  user_id = '{uID}'")
            print("Skill Updated successfully ")
        elif(y_n == 'n'):
            pass
        else:
            print("Invalid Input quiting ... ")
        save_and_close_connection_to_database(db)
    else:
        progress = input("Write skill_progress : ").strip()
        cr.execute(f"INSERT INTO skills(name,progress,user_id) values('{skill_name}' , '{progress}' , '{uID}')")
        print("Skill Added successfully ")
        save_and_close_connection_to_database(db)
#/********************************************************************************************************/#


#/************************************ Delete Function *************************************************/#
def del_skill(db,cr):
    skill_name = input("Write skill_name : ").strip().capitalize()
    cr.execute(f"DELETE FROM SKILLS where name = '{skill_name}' AND user_id = '{uID}'") 
    save_and_close_connection_to_database(db)
#/********************************************************************************************************/#

#/************************************ Update Function *************************************************/#
def update_skills(db,cr):
    skill_name = input("Write skill_name : ").strip().capitalize()
    progress = input("Write new skill_progress : ").strip()
    cr.execute(f"UPDATE skills set progress = '{progress}' where name = '{skill_name}' AND  user_id = '{uID}'")
    print("Skill Updated successfully ")
    save_and_close_connection_to_database(db)
#/********************************************************************************************************/#


#/************************************ Authintication Function *************************************************/#
def Auth_fn(cr):
    id = input("Please Enter Your ID : ")
    cr.execute("SELECT DISTINCT user_id FROM skills")
    IDs = cr.fetchall()
    list_ids = [item[0] for item in IDs]
    print(list_ids)

    if(int(id) in list_ids):
        return True,id
    else:
        return False,id



#/********************************************************************************************************/#


############### Apllication #############
print("***************** Welcome To Database System *******************")
db,cr = connect_to_database()
auth,uID = Auth_fn(cr)
if(auth == True):
    print("You Enterd Exist Id so Welcome . . . ")
    msg = """
Choose one of the following :
************************************
*    (s) => show all skills        *
*    (a) => add new skills         *
*    (d) => delete a skill         *
*    (u) => update skill progress  * 
*    (q) => Quit the Application   * 
************************************
Your Choice : """

    user_input = input(msg).strip().lower()
    input_options = ['s' ,'a' ,'d', 'u','q']

    # checking if the command in command options or not 
    if user_input in input_options:
        print(f"command found {user_input}")
        if(user_input == 's'):
            show_skills(db,cr)
        elif(user_input == 'a'):
            add_skill(db,cr)
        elif(user_input == 'd'):
            del_skill(db,cr)
        elif(user_input == 'u'):
            update_skills(db,cr)
        else:
            pass

    else:
        print(f"sorry this command \"{user_input}\" not found in command options ")
else:
    print("You Enterd not Exist Id so you won't be able to Enter to th system Thank you ! Quiting ...")