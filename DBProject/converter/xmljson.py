import json
# from xml2json import *
# import xmltodict
import xmltodict
import dicttoxml
from xml.dom.minidom import parseString


"""json to xml"""
def json_xml(inputStr):
    jdata = json.loads(inputStr)
    xml = dicttoxml.dicttoxml(jdata, root=True, attr_type=False)
    return parseString(xml).toprettyxml()
    # xml = dicttoxml.dicttoxml(jdata, root=False, attr_type=False)
    # return parseString(xml).toprettyxml()


"""xml to json"""
def xml_json(inputStr):
    return json.dumps(xmltodict.parse(inputStr.encode("utf8")),indent=4)

    # p = optparse.OptionParser(
    #     description='Converts XML to JSON or the other way around.  Reads from standard input by default, or from file if given.',
    #     prog='xml2json',
    #     usage='%prog -t xml2json -o file.json [file]'
    # )
    # p.add_option('--type', '-t', help="'xml2json' or 'json2xml'", default="xml2json")
    # p.add_option('--out', '-o', help="Write to OUT instead of stdout", default='-o')
    # p.add_option(
    #     '--strip_text', action="store_true",
    #     dest="strip_text", help="Strip text for xml2json", default=1)
    # p.add_option(
    #     '--pretty', action="store_true",
    #     dest="pretty", help="Format JSON output so it is easier to read", default=1)
    # p.add_option(
    #     '--strip_namespace', action="store_true",
    #     dest="strip_ns", help="Strip namespace for xml2json", default=1)
    # p.add_option(
    #     '--strip_newlines', action="store_true",
    #     dest="strip_nl", help="Strip newlines for xml2json", default=1)
    # options, arguments = p.parse_args()
    # return xml2json(inputStr, options)
