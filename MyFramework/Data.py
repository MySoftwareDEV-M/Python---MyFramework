import ast
import html
import inspect
import json
import xmltodict

def addListToDict(aDict : dict, key : str, value):
    """
    Erzeugt ein key-value-Paar, wenn zu dem Key noch keines besteht. Der value wird in eine Liste eingefügt.
    Wenn bereits ein key-value-Paar besteht, wird der value der Liste angehangen.

    Args:
        aDict (dict): Das Dictionary, in dem das key-value-Paar zeugt oder ergänzt werden soll
        key (str): Key zu der Liste, die erzeugt oder ergänzt werden soll
        value (beliebig): Value, der in der Liste hinzugefügt werden soll
    """    
    try:
        theList = aDict[key]
        theList.append(value)
        aDict[key] = theList
    except:
        aDict[key] = [value]

def copyArguments(sourceDict : dict) -> dict:
    """
    Creates a Dictionary which contains all the Arguments, the keys starting wird "@",
    within the sourceDict.
    Args:
        sourceDict (dict): Dictionary to be copied.

    Returns:
        dict: Dictionary, only containing the key value pairs whies keys start with "@"
    """    
    result = {}
    for key in sourceDict.keys():
        if(key[0] == "@"):
            result[key] = sourceDict[key]

    return result

def printNice(content, highlighting = "", addFileInfo = True):
    """
    Gibt den content über json.dumps() mit einem indent = 3 aus.
    Args:
        content (): Content, der über json.dumps() ausgegeben werden kann.
    """

    currentFrame = inspect.currentframe()
    # a list of al the frames / calles, that lead to the call of this function
    callingFrame = inspect.getouterframes(currentFrame, 2)
    # we are interessted in the function that called the announce...() functions
    try:
        frameInfo = callingFrame[1]
        func = "> " + frameInfo.function + "()"
    except:
        frameInfo = callingFrame[1]
        func = ""

    filename = str(frameInfo.filename).split("\\")
    filename = filename[len(filename)-1]
    
    if(highlighting != ""):
        fileInfo = ""
        if(addFileInfo):
            fileInfo = " (" + filename + func + " in line = " + str(frameInfo.lineno) + ")"
            
        print("######################################################################")
        print(highlighting + fileInfo + " ==>")
        print(json.dumps(content, indent = 3))
        print("<== " + highlighting)
        print("######################################################################")
    else:
        print(json.dumps(content, indent = 3))

def str2xml(data : str) -> tuple:
    content = (None, None)
    try:
        content = ("direct", xmltodict.parse(data))
    except:
        try:
            data = html.unescape(data)
            content = ("escaped", xmltodict.parse(data))
        except:
            pass
    return content

def str2dictOrList(data : str) -> dict:
    content = None
    try:
        content = json.loads(data)
    except:
        pass
    return content

def str_doLiteralEval(data : str) -> set:
    content = None
    try:
        content = ast.literal_eval(data)
    except:
        pass
    return content

def getSchema(data) -> list:
    """
    When dealing with data, esspecially when provided by others, understanding the structure of the data is important.

    This function determines the structure of the data and returns it as a nested list.


    """
    # To understand this function, it is devided into two sections, the first handles strings, the other one
    # handles all other data types.
    # 
    # The special focus on string originates from the fact that strings might be contain other data structure,
    # which needs to be converted first.
    # 
    # ---------------------------------------------------------------------------------------------
    # SECTION STRING
    # If data is a string, ...
    if(type(data) == str):
        # ... a) check whether the content can be converted into a json object (which can be a dict or list) ...
        content = str2dictOrList(data)
        if(content != None):
            if(type(content) == dict):
                return ("STR->DICT", None, getSchema(content))
            
            if(type(content) == list):
                return ("STR->LIST", None, getSchema(content))
        
        # ... b) try to eval content is a literal directly ...
        content = str_doLiteralEval(data)
        if(content != None):
            if(type(content) == set):
                return ("STR->SET", None, getSchema(content))
                
            if(type(content) == bytes):
                return ("STR->BYTES", None, getSchema(content))
        
        # ... c) check if content might be a frozenset ...
        if(data.startswith("frozenset(") and data.endswith(")")):
            data = data[10:]
            data = data[0:-1]
            content = str_doLiteralEval(data)
            if(content != None):
                return ("STR->FROZENSET", None, getSchema(content))
        
        # ... d) check if content might be a bytearray ...
        if(data.startswith("bytearray(") and data.endswith(")")):
            data = data[10:]
            data = data[0:-1]
            content = str_doLiteralEval(data)
            if(content != None):
                return ("STR->BYTEARRAY", None, getSchema(content))
        
        # ... e) check if content might be a tuple ...
        if(data.startswith("(") and data.endswith(")")):
            data = data[1:]
            data = data[0:-1]
            content = str_doLiteralEval(data)
            if(content != None):
                return ("STR->TUPLE", None, getSchema(content))

        # ... f) check if content might be xml ...
        content = str2xml(data)
        if(content[0] != None):
            if(content[0] == "direct"):
                return ("STR->XML", None, getSchema(content[1]))
            else:
                return ("STR->XML (escaped)", None, getSchema(content[1]))

        # ... g) if it is none of the above types, just return the string schema.
        return ("STR", None, data)
    
    # ---------------------------------------------------------------------------------------------
    # SECTION NO STRINGS
    # If data is an integer, ...
    if(type(data) == int):
        # ... just return the integer schema 
        return ("INT", None, data)

    # If data is a float, ...
    if(type(data) == float):
        # ... just return the float schema 
        return ("FLOAT", None, data)

    # If data is a complex number, ...
    if(type(data) == complex):
        # ... just return the float schema 
        return ("COMPLEX", None, str(data))

    # If data is a boolean, ...
    if(type(data) == bool):
        # ... just return the float schema 
        return ("BOOL", None, str(data))

    # If data is a bytearray, ...
    if(type(data) == bytearray):
        # ... just return the float schema 
        return ("BYTE ARRAY", None, str(data))

    # If data is a bytes, ...
    if(type(data) == bytes):
        # ... just return the float schema 
        return ("BYTES", None, str(data))

    # If data is a None, ...
    if(data == None):
        # ... just return the float schema 
        return ("NONE", None, str(data))
    
    # If data is a list, ...
    if(type(data) == list):
        # ... determine the schema for each element ...
        listSchemes = []
        for element in data:
            result = getSchema(element)
            listSchemes.append(("ELEMENT", None, result))
        # ... and return all these schemes
        return ("LIST", None, listSchemes)
    
    # If data is a dict, ...
    if(type(data) == dict):
        # ... determine the schema for each key value pair ...
        keySchemes = []
        keys = list(data.keys())
        for key in keys:
            result = getSchema(data[key])
            keySchemes.append(("KEY", key, result))
        # ... and return all these schemes
        return ("DICT", None, keySchemes)
        
    # If data is a set, ...
    if(type(data) == set):
        # ... determine the schema for each element ...
        setSchemes = []
        for element in data:
            result = getSchema(element)
            setSchemes.append(("ELEMENT", None, result))
        # ... and return all these schemes
        return ("SET", None, setSchemes)
        
    # If data is a frozenset, ...
    if(type(data) == frozenset):
        # ... determine the schema for each element ...
        setSchemes = []
        for element in data:
            result = getSchema(element)
            setSchemes.append(("ELEMENT", None, result))
        # ... and return all these schemes
        return ("FROZEN SET", None, setSchemes)
        
    # If data is a tuple, ...
    if(type(data) == tuple):
        # ... determine the schema for each element ...
        tupleSchemes = []
        for element in data:
            result = getSchema(element)
            tupleSchemes.append(("ELEMENT", None, result))
        # ... and return all these schemes
        return ("TUPLE", None, tupleSchemes)

    # If we made it this far, we missed something.
    return ("NOT IMPLEMENTED: " + str(type(data)), None, None)

def printSchema(schema, indent = 0):
    tmp = ".." * indent
    if(schema[0] == "KEY"):
        print(tmp + str(schema[0] + ": " + str(schema[1])))
    else:
        print(tmp + str(schema[0]))

    if(type(schema[2]) == list):
        for element in schema[2]:
            printSchema(element, indent+1)
        
    if(type(schema[2]) == tuple):
        printSchema(schema[2], indent+1)

def printSchemaSimple(schema, indent = "") -> str:
    outputText = ""
    indentAddition = ".."

    schema0 = schema[0]
    schema2 = schema[2]
    if(schema0 == "KEY"):
        outputText += (indent + str(schema[0] + ": " + str(schema[1])) + "\n")
        indent = indent.replace(".", " ")
        indentAddition = "  "
        
    elif(schema0.startswith("STR->")):
        outputText += (indent + str(schema[0]) + " > " + str(schema2[0]) + "\n")
        schema = schema[2]
        
        if(schema2[0] == "DICT"):
            indentAddition = "."
            indent = indent.replace(".", " ")
            indent += "|"
        if(schema2[0] == "LIST"):
            indentAddition = "."
            indent = indent.replace(".", " ")
            indent += ":"

    else:
        outputText += (indent + str(schema[0]) + "\n")
        if(schema[0] == "DICT"):
            indentAddition = "."
            indent = indent.replace(".", " ")
            indent += "|"
        elif(schema[0] == "LIST"):
            indentAddition = "."
            indent = indent.replace(".", " ")
            indent += ":"

    if(type(schema[2]) == list):
        simpleElements = ""
        outputText__ = ""
        for element in schema[2]:
            if(element[0] == "KEY"):
                if( (element[2][0]) == "INT"):
                    simpleElements += str(element[1]) + ": " + str(element[2][2]) + ", "
                    continue

                if( (element[2][0]) == "FLOAT"):
                    simpleElements += str(element[1]) + ": " + str(element[2][2]) + ", "
                    continue

                if( (element[2][0]) == "COMPLEX"):
                    simpleElements += str(element[1]) + ": " + str(element[2][2]) + ", "
                    continue

                if( (element[2][0]) == "BOOL"):
                    simpleElements += str(element[1]) + ": " + str(element[2][2]) + ", "
                    continue

                if( (element[2][0]) == "NONE"):
                    simpleElements += str(element[1]) + ": None, "
                    continue

                elif( (element[2][0]) == "STR"):
                    tmp = str(element[2][2])
                    if(len(tmp) > 10):
                        tmp = tmp[0:10] + "..."
                    simpleElements += str(element[1]) + ": \"" + tmp + "\", "
                    continue

                elif( (element[2][0]) == "BYTE ARRAY"):
                    tmp = str(element[2][2])
                    if(len(tmp) > 10):
                        tmp = tmp[0:10] + "..."
                    simpleElements += str(element[1]) + ": \"" + tmp + "\", "
                    continue

                elif( (element[2][0]) == "BYTES"):
                    tmp = str(element[2][2])
                    if(len(tmp) > 10):
                        tmp = tmp[0:10] + "..."
                    simpleElements += str(element[1]) + ": \"" + tmp + "\", "
                    continue
    
            outputText__ += printSchemaSimple(element, indent + indentAddition)
        if(simpleElements != ""):
            outputText += (indent + ".." + simpleElements + "\n")
        outputText += outputText__
        
    if(type(schema[2]) == tuple):
        outputText += printSchemaSimple(schema[2], indent + indentAddition)

    return outputText
