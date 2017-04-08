import psycopg2
import json
import collections
import sys

sys.setrecursionlimit(100000)

# Recursive function to construct hierarchy dictionary with indexes
def build_json_tree(curr_index):
    global sql_hier_parent, sql_hier_child
    if curr_index in sql_hier_parent:
        cursor.execute('SELECT * FROM Hierarchy WHERE parent_id = %d;' %curr_index)
        curr_hier = cursor.fetchall()
        for curr_parent, curr_child in curr_hier:
            if curr_index not in json_output_dict:
                if curr_index not in sql_hier_child:
                    json_output_dict[curr_parent] = {}
            if curr_child in sql_hier_parent:
                curr_value = {curr_child: {}}
                update_json_tree(json_output_dict,curr_parent,curr_value)
                build_json_tree(curr_child)
            else:
                curr_cont = sql_cont_text[sql_cont_index.index(curr_child)].strip()
                curr_value = {curr_child: curr_cont}
                update_json_tree(json_output_dict,curr_parent,curr_value)

#insert a new value into nested dictionary[key]
def update_json_tree(tree, key, value):
    """Return true if update, else false"""
    tree_value = tree.get(key, None)
    if tree_value is not None:
        tree_value.update(value)
    for branch in tree.values():
        if type(branch) == dict:
            result = update_json_tree(branch, key, value)
            if result is True:
                return True
    return False

#sort dictionary according to its key
def sort_nested_dict(d):
    new = collections.OrderedDict(sorted(d.items()))
    for k, v in d.iteritems():
        if type(v) == dict:
            v = collections.OrderedDict(sorted(sort_nested_dict(v).items()))
        new[k] = v
    return new

#insert attr to json as a element:content pair
def update_json_attr(d):
    try:
        cursor.execute('SELECT * FROM Attributes;')
        sql_attr_data = cursor.fetchall()
        for (k, attr, value) in sql_attr_data:
            update_json_tree(d, k, {attr: value})
        return d
    except:
        return d

#match the index in the dictionary into element text
def update_json_key(d):
    new = collections.OrderedDict({})
    for k, v in d.iteritems():
        if isinstance(k,int):
            if isinstance(v, dict):
                v = update_json_key(v)
            curr_elem_text = sql_elem_text[k-1]
            if curr_elem_text in new.keys():
                temp_v = new[curr_elem_text]
                if isinstance(temp_v,list):
                    temp_v.append(v)
                    new[curr_elem_text] = temp_v
                else:
                    new[curr_elem_text] = [temp_v,v]
            else:
                new[sql_elem_text[k-1]] = v
        else:
            new[k] = v
    return new

def db2json():
    global sql_hier_parent, sql_hier_child, cursor, json_output_dict, sql_cont_text, sql_cont_index, sql_elem_text
    # Set database connection
    conn = psycopg2.connect(host = "localhost",database="dbproject", user="postgres", password="123456")

    cursor = conn.cursor()

    # Query database table
    cursor.execute('SELECT * FROM Elements;')
    sql_elem_data  = cursor.fetchall()
    sql_elem_index = [sql_elem_row[0] for sql_elem_row in sql_elem_data]
    sql_elem_text  = [sql_elem_row[1].strip() for sql_elem_row in sql_elem_data]

    cursor.execute('SELECT * FROM Contents;')
    sql_cont_data  = cursor.fetchall()
    sql_cont_index = [sql_cont_row[0] for sql_cont_row in sql_cont_data]
    sql_cont_text  = [sql_cont_row[1].strip() for sql_cont_row in sql_cont_data]

    cursor.execute('SELECT * FROM Hierarchy;')
    sql_hier_data   = cursor.fetchall()
    sql_hier_child  = [sql_hier_row[1] for sql_hier_row in sql_hier_data]
    sql_hier_parent = [sql_hier_row[0] for sql_hier_row in sql_hier_data]

    json_output_dict = {}


    for sql_elem in sql_elem_data:
        json_output_index = sql_elem[0]
        json_output_key   = sql_elem[1].strip()
        if (json_output_index not in sql_hier_child):
            build_json_tree(json_output_index)

    for json_cont_index in sql_cont_index:
        if json_cont_index not in sql_hier_parent and json_cont_index not in sql_hier_child:
            json_output_dict[json_cont_index]=sql_cont_text[sql_cont_index.index(json_cont_index)]

    json_output_dict = sort_nested_dict(json_output_dict)
    json_output_dict = update_json_attr(json_output_dict)
    json_output_dict = update_json_key(json_output_dict)
    json_output = json.dumps(json_output_dict,indent=4)
    conn.close()
    return json_output
