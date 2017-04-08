import xml.etree.ElementTree as ET
import psycopg2
# from Create_Table import create_tables
# element table->hier table->attribute table->content table


def dfs_xml(elem):
    global xml_index
    xml_root_index = xml_index
    if elem.getchildren():
        for child in elem.getchildren():
            xml_index = xml_index + 1
            Elem_xml_list.append((xml_index,child.tag))
            Hier_xml_list.append((xml_root_index,xml_index))
            # print(xml_root_index, xml_index)
            # print (xml_index,child.tag)
            if child.attrib:
                for xml_key, xml_value in child.attrib.items():
                    #print (xml_index,key,value)
                    Attri_xml_list.append((xml_index,xml_key,xml_value))
            xml_text=child.text

            if xml_text is not None: 
                xml_text=xml_text.strip(' \t\n\r')
                if xml_text:
                    Cont_xml_list.append((xml_index,xml_text))
            dfs_xml(child)

def xml2db(xml):
    root = ET.fromstring(xml)
    # root = tree.getroot()
    global xml_index
    xml_index=1
    global Elem_xml_list,Hier_xml_list,Attri_xml_list,Cont_xml_list
    Elem_xml_list,Hier_xml_list,Attri_xml_list,Cont_xml_list=[],[],[],[]
    Elem_xml_list.append((xml_index,root.tag))
    #print (xml_index,root.tag)
    if root.attrib:
        for xml_key, xml_value in root.attrib.items():
            #print (xml_index,xml_key,xml_value)
            Attri_xml_list.append((xml_index,xml_key,xml_value))
    xml_text=root.text.strip(' \t\n\r')
    if xml_text:
        # print (xml_index,xml_text)
        Cont_xml_list.append((xml_index,xml_text))
    dfs_xml(root)

    # print(Elem_xml_list,Hier_xml_list,Attri_xml_list,Cont_xml_list)
    

   

#To obtain sql code
    xml2db_sql=("""
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
CREATE TABLE Attributes (
        Element_ID INTEGER NOT NULL,
        Key VARCHAR(255) NOT NULL,
        Value VARCHAR(255) NOT NULL,
        FOREIGN KEY (Element_ID) REFERENCES Elements(Element_ID)              
);
CREATE TABLE Contents (
        Element_ID INTEGER,
        Contents VARCHAR(255) NOT NULL,
        FOREIGN KEY (Element_ID) REFERENCES Elements(Element_ID)
);\n""")


    for Elem_xml_each in Elem_xml_list:
        xml2db_sql+=("INSERT INTO Elements (Element_ID,Element_Name) VALUES "+str(Elem_xml_each))
        xml2db_sql+=(";\n")

    for Hier_xml_each in Hier_xml_list:
        xml2db_sql+=("INSERT INTO Hierarchy (Parent_ID,Child_ID) VALUES "+str(Hier_xml_each))
        xml2db_sql+=(";\n")

    for Attri_xml_each in Attri_xml_list:
        xml2db_sql+=("INSERT INTO Attributes (Element_ID,Key,Value) VALUES "+str(Attri_xml_each))
        xml2db_sql+=(";\n")

    for Cont_xml_each in Cont_xml_list:
        xml2db_sql+=("INSERT INTO Contents (Element_ID,Contents) VALUES "+str(Cont_xml_each))
        xml2db_sql+=(";\n")
# #Create Table
#     create_tables()
#Connect to postgresql and insert values into tables.
    xml_elem_sql = "INSERT INTO Elements (Element_ID,Element_Name) VALUES (%s, %s);"
    xml_hier_sql = "INSERT INTO Hierarchy (Parent_ID,Child_ID) VALUES (%s, %s);"
    xml_attri_sql = "INSERT INTO Attributes (Element_ID,Key,Value) VALUES (%s, %s, %s);"
    xml_cont_sql = "INSERT INTO Contents (Element_ID,Contents) VALUES (%s, %s);"
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(host="localhost",database="dbproject", user="postgres", password="123456")
        cur = conn.cursor()
        cur.executemany(xml_elem_sql,Elem_xml_list)
        cur.executemany(xml_hier_sql,Hier_xml_list)
        cur.executemany(xml_attri_sql,Attri_xml_list)
        cur.executemany(xml_cont_sql,Cont_xml_list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return xml2db_sql


