"Please modify connection to database before running"
import sys
from xml.etree import ElementTree
from xml.dom import minidom
import psycopg2
from psycopg2 import connect
from xml.etree.ElementTree import Element, SubElement, Comment

sys.setrecursionlimit(100000)

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

def build_tree(Elem):
    global index_number, rows_hierarchy
    children_number= 0
    for row in rows_hierarchy:       
        if row[0] == index_number:
            children_number=1
            Elem=SubElement(Elem,str(row[1]))
            index_number=row[1]
            rows_hierarchy.remove(row)
            build_tree(Elem)                 
    if children_number==0:
        parent_map = {}
        "find the parent and continue"
        for p in root.iter():
            for c in p:
                parent_map[c] = [p]
                if c==Elem:
                    index_number=int(p.tag)
                    build_tree(p)

def db2xml():
    global index_number, rows_hierarchy, root                                
    conn = None
    try:
        "build connection"
        conn = psycopg2.connect(dbname='dbproject', user='postgres', host = 'localhost', password='123456')
        cur = conn.cursor()
        cur.execute("SELECT * FROM elements")
        rows_tag = cur.fetchall()        
        cur.execute("SELECT * FROM hierarchy")
        rows_hierarchy= cur.fetchall()
        cur.execute("SELECT * FROM contents")
        rows_content= cur.fetchall()
        cur.execute("SELECT * FROM attributes")
        rows_attribute= cur.fetchall()       

        #insert root if not having one
        Elem_db_id,Child_db_id=[],[]
        Elem_db_id=[row[0] for row in rows_tag]
        Child_db_id=[row[1] for row in rows_hierarchy]
        Unconn_node_id=set(Elem_db_id)-set(Child_db_id)
        if len(Unconn_node_id)!=1:
            rows_tag = [(elem[0] + 1, elem[1]) for elem in rows_tag]
            rows_tag.insert(0, (1,'root'))
            rows_hierarchy = [(hier[0] + 1, hier[1]+1) for hier in rows_hierarchy]
            for unconn in sorted(Unconn_node_id, reverse=True):
                rows_hierarchy.insert(0, (1,unconn+1))
            rows_content = [(cont[0] + 1, cont[1]) for cont in rows_content]
            rows_attribute = [(attr[0] + 1, attr[1],attr[2]) for attr in rows_attribute]
        # print(rows_hierarchy)
        # print(rows_tag,rows_hierarchy,rows_content,rows_attribute)
        root= Element (str(rows_tag[0][0]))
        index_number=1
        build_tree(root)
        "modify the element tree's content,attribute and tag"
        for row in rows_content:
            for q in root.iter():
                if int(q.tag)==row[0]:
                        q.text=row[1]
        for row in rows_attribute:
            for q in root.iter():
                if int(q.tag)==row[0]:
                    q.set(row[1], row[2])
        for q in root.iter():
            q.tag= rows_tag[int(q.tag)-1][1]
        cur.close()
        return prettify(root)
            
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
