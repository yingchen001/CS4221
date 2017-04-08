import psycopg2


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (

        """
        DROP TABLE IF EXISTS Contents;
        DROP TABLE IF EXISTS Attributes;
        DROP TABLE IF EXISTS Hierarchy;
        DROP TABLE IF EXISTS Elements;
        CREATE TABLE Elements (
            Element_ID INTEGER PRIMARY KEY,
            Element_Name VARCHAR(255) NOT NULL
        )
        """,
        """
        
        CREATE TABLE Hierarchy (
                Parent_ID INTEGER NOT NULL,
                Child_ID INTEGER NOT NULL,
                FOREIGN KEY (Child_ID) REFERENCES Elements(Element_ID)                
 
        )
        """,
        """

        CREATE TABLE Attributes (
                Element_ID INTEGER NOT NULL,
                Key VARCHAR(255) NOT NULL,
                Value VARCHAR(255) NOT NULL,
                FOREIGN KEY (Element_ID) REFERENCES Elements(Element_ID)              
        )
        """,
        """
        
        CREATE TABLE Contents (
                Element_ID INTEGER,
                Contents VARCHAR(255) NOT NULL,
                FOREIGN KEY (Element_ID) REFERENCES Elements(Element_ID)
        )
        """)
    conn = None
    try:
        # read the connection parameters
        conn = psycopg2.connect(host="localhost",database="xml2db", user="postgres", password="yu4231781")
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
 
 
if __name__ == '__main__':
    create_tables()