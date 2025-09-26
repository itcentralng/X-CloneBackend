import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="Xbackenddb",
    user="postgres",
    password="Emmanuel",
    port="5432"
)


cur = conn.cursor()

try:
    cur.execute("""SELECT * FROM testsignupii""")

    values = cur.fetchall()
    for i in values:
        print(i)

        if "Emmanueltest1" in i and 12345 in i:
            print("Yes it's their")
        # elif "Emmanueltest1"in i  and 123 not in i:
        #     print("Wrong Password")
        elif "solomon" not in i and 12345 in i:
            print("Wrong Username")
        
        # else :
        #     print("their seems to be an error!")

    # cur.execute("""
    #             CREATE TABLE testpsycopg2(
    #                 id INT PRIMARY KEY,
    #                 name TEXT,
    #                 email TEXT,
    #                 password TEXT
    #             ) 
    #             """
    #             )
    
    # cur.execute("""
    #             INSERT INTO testpsycopg2 (id , name , email , password)
    #             VALUES ( 2 , 'testmeii' , 'testmeii@gmail.com' , 'testt' ),
    #                    ( 3 , 'testmeiii' , 'testmeiii@gmail.com' , 'testt' ),
    #                    ( 4 , 'testmeiv' , 'testmeiv@gmail.com' , 'testt' ),
    #                    ( 5 , 'testmev' , 'testmev@gmail.com' , 'testt' ),
    #                    ( 6 , 'testmevi' , 'testmevi@gmail.com' , 'testt' )
    #         """)
    
    
    # cur.execute("""
    #             SELECT * FROM testpsycopg2
    #         """)

except psycopg2.Error as e:
    print(f"Error while executing Reason: {e}")   

conn.commit() 
# --- To close any commiting 
cur.close();

# --- To close the connections
conn.close();