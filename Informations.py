from enum import Flag, auto, Enum
import datetime
import inspect

class Informations:
    """
    Diese Klasse dient dazu, Hinweise, die während der Ausführung einer Anwendung erfasst werden sollen, ...
    <li> ... zentral zu speichern und für anschließende Aufrufe bereitzustellen. Diese Informationen können entsprechend weiterführender Anwendungsfälle angezeigt, gespeichert oder analysiert werden.
    <li> ... über einheitliche und leicht zugängliche Funktionen direkt im Terminal auszugeben.

    Je nach Wahl der `Framework.Informations.Informations.Verbosity` werden die Informationen im Terminal ausgegeben.

    Je nachdem welcher der announce-Funktionen genutzt wird, werden die Informationen automatisch typisiert. (Beispielsweise `Framework.Informations.Informations.announceInfo`)
    """
    class Verbosity(Enum):
        """
        Definiert, wie umfangreich Ausgaben gestaltet werden sollen.
        <li> NoPrint: Keine Ausgabe
        <li> PrintSimple: Ausgabe in einer Zeile
        <li> PrintBulky: Ausgabe mit einer auffälligen Hervorhebung.

        (Siehe auch `Framework.Informations.Informations`)
        """        
        NoPrint             =  0
        PrintSimple         =  1
        PrintBulky          =  2

    class Types(Flag):
        """
        Typen, um Informationen zu typisieren. Die Wahl und Interpretation dieser Typen liegt vollständig beim Anwender. Informationen, die dieser Klasse übergeben werden, werden unabhängig vom Typ einheitlich behandelt.

        (Siehe auch `Framework.Informations.Informations`)
        """    
        DEBUG   = 1
        INFO    = 2
        WARN    = 4
        ERROR   = 8

    class Entry(dict):
        """
        Die übergebenen Informationen werden in den Entries mit entsprechenden Metainformationen erfasst und gespeichert. Diese sind über `Framework.Informations.entries` abrufbar.
        """
        __textColumnWidth = 70

        def __init__(self, type, file : str, func : str, line : str, text : str):
            dateTime = datetime.datetime.now()
            self["type"] = type
            self["file"] = file
            self["func"] = func
            self["line"] = line
            self["text"] = text
            self["date"] = dateTime.date()
            self["time"] = dateTime.time().replace(microsecond=0)
        
        def __typeToString(self, type, oneLength = True) -> str:
            tmp = str(type)
            tmp = "[" + tmp[6:] + "]"
            if( oneLength and len(tmp) == 6):
                tmp = tmp + " "
            return tmp
        
        def printSimple(self, printDateTime):
            """
            Gibt einen Entry in einer Zeile im Terminal aus.
            """            
            if(self["func"] == "<module>"):
                func = ""
            else:
                func = "-> " + self["func"] + "()"
            
            theString = self.__typeToString(self["type"])
            theString += " > " + self["file"] + func + " in line " + self["line"]
            if(printDateTime):
                theString += " on " + str(self["date"]) + " at " + str(self["time"])
            theString += "\n\"" + self["text"] + "\""
            print(theString)

        def printBulky(self, printDateTime):
            """
            Gibt einen Entry in mehreren Zeilen im Terminal aus.
            """
            separationLine = self.__textColumnWidth * "-"

            if(self["func"] == "<module>"):
                func = ""
            else:
                func = "-> " + self["func"] + "()"
            text = self["text"]

            print(separationLine)
            print("| " + self.__typeToString(self["type"]) )
            print("| " + self["file"] + func + " in line " + self["line"])
            if(printDateTime):
                print("| On " + str(self["date"]) + " at " + str(self["time"]))
            while(len(text)):
                tmp = text[0:self.__textColumnWidth]
                print("| " + tmp)
                text = text[self.__textColumnWidth:]
            print(separationLine)

    ###############################################################################################
    # class variables
    _entries                = list[Entry]()
    __printAnnouncements    = Verbosity.PrintSimple
    __typesToPrint          = Types.DEBUG | Types.INFO | Types.WARN | Types.ERROR
    __printDateTime         = True

    ###############################################################################################
    # private functions
    #----------------------------------------------------------------------------------------------
    def _appendInfo(self, type : Types, text : str):
        # inspect provides informations on the execution of a program
        # current frame is referencing the frame of this function (def announceError(self, text : str))
        currentFrame = inspect.currentframe()
        # a list of al the frames / calles, that lead to the call of this function
        callingFrame = inspect.getouterframes(currentFrame, 2)
        # we are interessted in the function that called the announce...() functions
        for frame in callingFrame:
            if not "Informations.py" in frame.filename:
                break
        frameInfo = frame

        filename = str(frameInfo.filename).split("\\")
        filename = filename[len(filename)-1]

        entry = Informations.Entry(file=filename, func=frameInfo.function, line=str(frameInfo.lineno), type=type, text=text)
        self._entries.append(entry)

        if not type in self.__typesToPrint:
            return
        
        if(self.__printAnnouncements == Informations.Verbosity.PrintSimple):
            entry.printSimple(self.__printDateTime)
        elif(self.__printAnnouncements == Informations.Verbosity.PrintBulky):
            entry.printBulky(self.__printDateTime)
   
    #----------------------------------------------------------------------------------------------
    def __init__(self, verbosity : Verbosity = None, types : Types = None, dateTime = None):
        """
        Um die Default-Einstellungen zu ändern, wird empfohlen, eine Instanz von Informations einmalig aufzurufen und die Verbosity und die Types einmalig zu setzen. Diese Wahl gilt dann für die gesamte Anwendung.
        
        <li> verbosity (Informations.Verbosity, optional) Standardmäßg ist PrintSimple gesetzt.
        <li> types (Informations.Types, optional)   Standardmäßig werden alle Typen ausgegeben.
        """
        if(verbosity != None):
            self.__printAnnouncements = verbosity
        if(types != None):
            self.__typesToPrint = types
        if(dateTime != None):
            self.__printDateTime = dateTime

    #----------------------------------------------------------------------------------------------
    # Framework modules are create as singleton, so the very same instance
    # can be called from anywhere
    def __new__(cls, verbosity : Verbosity = None, types : Types = None, dateTime : bool = None):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Informations, cls).__new__(cls)
        return cls.instance

    ###############################################################################################
    # Public functions

###################################################################################################
# Public global functions / Helper functions
#--------------------------------------------------------------------------------------------------
def announceInfo(text : str):
    """
    Globale Funktion, um eine Information vom Typ INFO zu erfassen.
    """    
    infos = Informations()
    infos._appendInfo(Informations.Types.INFO, text)

#--------------------------------------------------------------------------------------------------
def announceWarning(text : str):
    """
    Globale Funktion, um eine Information vom Typ WARN zu erfassen.
    """    
    infos = Informations()
    infos._appendInfo(Informations.Types.WARN, text)

#--------------------------------------------------------------------------------------------------
def announceError(text : str):
    """
    Globale Funktion, um eine Information vom Typ ERROR zu erfassen.
    """    
    infos = Informations()
    infos._appendInfo(Informations.Types.ERROR, text)

#--------------------------------------------------------------------------------------------------
def announceDebug(text : str):
    """
    Globale Funktion, um eine Information vom Typ DEBUG zu erfassen.
    """    
    infos = Informations()
    infos._appendInfo(Informations.Types.DEBUG, text)

#----------------------------------------------------------------------------------------------
def printEntries(types : Informations.Types = Informations.Types.DEBUG | Informations.Types.INFO | Informations.Types.WARN | Informations.Types.ERROR):
    """
    Globale Funktion, um alle Information mit den ausgewählten Typen im Terminal auszugeben.
    """    
    infos = Informations()
    for entry in infos._entries:
        if(entry["type"] in types):
            entry.printSimple()

#----------------------------------------------------------------------------------------------
def entries(types : Informations.Types = Informations.Types.DEBUG | Informations.Types.INFO | Informations.Types.WARN | Informations.Types.ERROR) -> list[Informations.Entry]:
    """
    Globale Funktion, um alle Information mit den ausgewählten Typen zurückzugeben.
    """ 
    infos = Informations()
    output = []
    for entry in infos._entries:
        if(entry["type"] in types):
            output.append(entry)
    return output
