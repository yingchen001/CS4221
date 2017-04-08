import json
import psycopg2
from collections import OrderedDict
# from Create_Table import create_tables

def printjson(dl,json_parent_index,json_parent):
    global json_index

    if isinstance(dl, dict):
        for json_key in dl.keys():
            json_index += 1
            # print (json_index,json_key)
            Elem_json_list.append((json_index,json_key))

            if json_parent:
                # print(json_parent_index,json_index)
                Hier_json_list.append((json_parent_index,json_index))
            if isinstance(dl[json_key],dict):
                printjson(dl[json_key],json_index,json_parent=1)
            elif isinstance(dl[json_key], list):
                for json_list_elem in dl[json_key]:
                    printjson(json_list_elem,json_index,json_parent=1)
            else:
                # print (json_index, dl[json_key])
                Cont_json_list.append((json_index, dl[json_key]))

def json2db(json_data):


    jdata = json.loads(json_data,object_pairs_hook=OrderedDict)

    global json_index,json_parent_index,json_parent
    json_index = 0
    json_parent_index = 1
    json_parent = 0
    global Elem_json_list,Hier_json_list,Cont_json_list
    Elem_json_list,Hier_json_list,Cont_json_list=[],[],[]
    printjson(jdata,json_parent_index,json_parent)
    # print(Elem_json_list,Hier_json_list,Cont_json_list)

    # Elem_json_id,Child_json_id=[],[]
    # Elem_json_id=[row[0] for row in Elem_json_list]
    # Child_json_id=[row[1] for row in Hier_json_list]
    # Unconn_node_id=set(Elem_json_id)-set(Child_json_id)
    # if len(Unconn_node_id)!=1:
    #     Elem_json_list = [(elem[0] + 1, elem[1]) for elem in Elem_json_list]
    #     Elem_json_list.insert(0, (1,'root'))
    #     Hier_json_list = [(hier[0] + 1, hier[1]+1) for hier in Hier_json_list]
    #     for unconn in sorted(Unconn_node_id, reverse=True):
    #         Hier_json_list.insert(0, (1,unconn+1))
    #     Cont_json_list = [(cont[0] + 1, cont[1]) for cont in Cont_json_list]


    #To obtain sql code
    json2db_sql=("""
DROP TABLE IF EXISTS Contents;
DROP TABLE IF EXISTS Attributes;
DROP TABLE IF EXISTS Hierarchy;
DROP TABLE IF EXISTS Elements;
CREATE TABLE Elements (
    Element_ID INTEGER PRIMARY KEY,
    Element_Name VARCHAR(255) NOT NULL
);
CREATE TABLE Hierarchy (
        Parent_ID INTEGER NOT NULL,
        Child_ID INTEGER NOT NULL,
        FOREIGN KEY (Child_ID) REFERENCES Elements(Element_ID)                
);
CREATE TABLE Contents (
        Element_ID INTEGER,
        Contents VARCHAR(255) NOT NULL,
        FOREIGN KEY (Element_ID) REFERENCES Elements(Element_ID)
);\n""")


    for Elem_json_each in Elem_json_list:
        json2db_sql+=("INSERT INTO Elements (Element_ID,Element_Name) VALUES ("+str(Elem_json_each[0]))
        json2db_sql+=(","+str(Elem_json_each[1])+");\n")

    for Hier_json_each in Hier_json_list:
        json2db_sql+=("INSERT INTO Hierarchy (Parent_ID,Child_ID) VALUES "+str(Hier_json_each[0]))
        json2db_sql+=(","+str(Hier_json_each[0])+");\n")

    for Cont_json_each in Cont_json_list:
        json2db_sql+=("INSERT INTO Contents (Element_ID,Contents) VALUES "+str(Cont_json_each[0]))
        json2db_sql+=(","+str(Cont_json_each[0])+");\n")

# #Create json tables
#     create_tables()

    sql1 = "INSERT INTO Elements (Element_ID,Element_Name) VALUES (%s, %s);"
    sql2 = "INSERT INTO Hierarchy (Parent_ID,Child_ID) VALUES (%s, %s);"
    sql3 = "INSERT INTO Contents (Element_ID,Contents) VALUES (%s, %s);"
#Connect postgresql and insert values into tables
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(host="localhost",database="dbproject", user="postgres", password="123456")
        cur = conn.cursor()
        cur.executemany(sql1,Elem_json_list)
        cur.executemany(sql2,Hier_json_list)
        cur.executemany(sql3,Cont_json_list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return json2db_sql