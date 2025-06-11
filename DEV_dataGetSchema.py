import json
import os
import pickle
import xmltodict

import MyFramework.Data as Data

# Möglichkeiten, ein dict oder eine list zu speichern
# a) als JSON
# Eine sehr einfache Variante zum Speichern eines dict oder einer list.
# Diese Dateien können auch wieder leicht eingelesen werden.
# Die Datei ist sehr gut von Menschen lesbar.
# Die gesamte Konvertierung der Objekte wird von dem json-Module übernommen,
# sofern die Objekte json serializable sind.
# 
# Speichern:
#   with open("DEV.txt", "w") as f:
#       f.write(json.dumps(content_dict, indent=3))
# Einlesen:
#   f = open("DEV.json")
#       data = f.read()
#   theDict = json.loads(data)
# 
# b) als String
# Speichern ist kein Problem. Das erneute Einlesen ist nicht ohne weiteres möglich.
# Eine Option für eine angenehme Formatierung des Dateiinhalts fehlt.
# Hintergrund: Im Gegensatz zum Speichern über json.dumps() werden einfache anstelle doppelter Hochkommata verwendet.
# Die mir geläufige Funktion zum (re-)interpretieren des Dateiinhalts ist json.loads(). Diese erwartet die doppelten 
# Hochkommata.
# 
# Speichern:
#   with open("DEV.txt", "w") as f:
#       f.write(str(theDict))
# 
# c) Binär über pickel
# Kann ohne Probleme genutzt werden, um ein dict oder eine list zu speichern und wider
# erneut einzulesen.
# Not suitable for cross-language compatibility.
#
# Speichern:
#   with open('DEV.pkl', 'wb') as file:
#       pickle.dump(content, file)
# Einlesen:
#   with open('DEV.pkl', 'rb') as file:
#       data = pickle.load(file)
# 
# https://blog.finxter.com/5-best-ways-to-write-a-set-to-a-file-in-python/
# Method 1: Text File. Simple and human-readable. Not structured for complex data.
# Method 2: CSV Format. Good for simple data interchange and spreadsheet applications. Limited to flat data structures.
# Method 3: JSON Format. Excellent for data interchange. Human-readable and preserves data structure. Cannot directly serialize sets.
# Method 4: Pickle Format. Perfect for Python-specific applications where data structure and type retention are necessary. Not suitable for cross-language compatibility.
# Bonus Method 5: Using str. Quick and easy one-liner for saving a set’s representation. Offers little control over the output format and not suitable for processing.

contentForFile = {
# Text Type:	str
    "key01" : "value1",
# Numeric Types:	int, float, complex
    "key02" : 123,
    "key03" : 1.23,
    "key04" : str((3 + 7j)),
# Sequence Types:	list, tuple, range --> Not supported
    "key05" : [1, 2],
    "key06" : str(("TUPLE A", "TUPLE B")),

# Mapping Type:	dict
    "key07" : {
        "keyA" : "DICT valueA",
        "keyB" : "DICT valueB"
    },
# Set Types:	set, frozenset
    "key08" : str({"SET A", "SET B", "SET C"}),
    "key09" : str(frozenset([1,3,(3,5)])),
# Boolean Type:	bool
    "key10" : True,
    "key11" : False,
# Binary Types:	bytes, bytearray, memoryview --> Not supported
    "key12" : str(bytes('Python', 'utf-8')),
    "key13" : str(bytearray([2, 3, 5, 7])),
# None Type:	NoneType
    "key14" : None,
# XML
    # "xml": "&lt;mxGraphModel&gt;&lt;root&gt;&lt;mxCell id=\"0\"/&gt;&lt;mxCell id=\"1\" parent=\"0\"/&gt;&lt;object label=\"Table*\" name=\"DB Table\" id=\"2\"&gt;&lt;mxCell style=\"shape=table;startSize=20;container=1;collapsible=1;childLayout=tableLayout;fixedRows=1;rowLines=0;fontStyle=1;align=center;resizeLast=1;html=1;whiteSpace=wrap;\" vertex=\"1\" parent=\"1\"&gt;&lt;mxGeometry y=\"1.1368683772161603e-13\" width=\"280\" height=\"40\" as=\"geometry\"/&gt;&lt;/mxCell&gt;&lt;/object&gt;&lt;object label=\"\" name=\"DB Column\" id=\"3\"&gt;&lt;mxCell style=\"shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=none;collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;top=0;left=0;right=0;bottom=0;\" vertex=\"1\" parent=\"2\"&gt;&lt;mxGeometry y=\"20\" width=\"280\" height=\"20\" as=\"geometry\"/&gt;&lt;/mxCell&gt;&lt;/object&gt;&lt;mxCell id=\"4\" value=\"000 FK, PK N\" style=\"shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;fontStyle=0;overflow=hidden;whiteSpace=wrap;html=1;\" vertex=\"1\" parent=\"3\"&gt;&lt;mxGeometry width=\"80\" height=\"20\" as=\"geometry\"&gt;&lt;mxRectangle width=\"80\" height=\"20\" as=\"alternateBounds\"/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=\"5\" value=\"UniqueID*\" style=\"shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;align=left;spacingLeft=6;fontStyle=0;overflow=hidden;whiteSpace=wrap;html=1;\" vertex=\"1\" parent=\"3\"&gt;&lt;mxGeometry x=\"80\" width=\"200\" height=\"20\" as=\"geometry\"&gt;&lt;mxRectangle width=\"200\" height=\"20\" as=\"alternateBounds\"/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;",
}

contentDirect = {
    "dict1" : {
        "dict1.1" :
        {
            "key1.1" : "value1",
            "key1.2" : "value2",
        },
        "dict1.2" :
        {
            "key1.1" : "value1",
            "key1.2" : "value2",
        }
    },
    "dict2" : {
        "dict2.1" :
        {
            "key2.1" : "value1",
            "key2.2" : "value2",
        },
        "dict2.2" :
        {
            "key2.1" : "value1",
            "key2.2" : "value2",
        }
    }
}

# contentDirect = [
#         1,
#         2,
#         3
#     ]

with open("DEV.json", "w") as f:
    f.write(json.dumps(contentForFile, indent=3))
    
with open("DEV.txt", "w") as f:
    f.write(str(contentForFile))

# writing dictionary to a binary file
with open('DEV.pkl', 'wb') as file:
    pickle.dump(contentForFile, file)

# Reading dictionary from the binary file
with open('DEV.pkl', 'rb') as file:
    data = pickle.load(file)

f = open("MySQLiteDrawIOLibrary.xml")
# f = open("DEV.json")
data = f.read()

schemaTree = Data.getSchema(data)
# print(json.dumps(schemaTree, indent=3))
# Data.printSchema(schemaTree)
text = Data.printSchemaSimple(schemaTree)
print(text)
