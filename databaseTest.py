import mysql.connector


#database initialization
db = mysql.connector.connect(host="localhost",user="root",password="",database="sensornetwork")
print(db)
myCursor = db.cursor()

print('step 1') 
#print(myCursor.execute("SHOW DATABASES"))
#print('step 2') 
#print(myCursor.execute("USE sensornetwork"))
#print('step 3') 
myCursor.execute("SELECT * FROM sensor_node_1_tb")
output = myCursor.fetchall()

print(tuple(range(1,5+1)))