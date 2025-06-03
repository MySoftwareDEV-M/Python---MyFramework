import inspect
import json
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