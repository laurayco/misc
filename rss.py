import xml.etree.ElementTree as ET

def element_value(el,default):
    return el.text + el.tail if el else ""

class Item:
    def __init__(self):
        pass

class RSS:
    def __init__(self,title,description,link,language,copyright,editor,master,version,items):
        self.title = title
        self.description = description
        self.link = link
        self.language = language
        self.copyright = copyright
        self.editor = editor
        self.webmaster = master
        self.version = version
        self.items = items
    @classmethod
    def create(cls,data):
        tree = ET.fromstring(data)
        return {
            "0.91": cls.parse_91,
            "0.90": cls.parse_90,
            "2.0": cls.parse_20
        }[tree.get("version","2.0")](tree)
    @classmethod
    def parse_91(cls,tree):
        version = tree.get("version","0.91")
        title = element_value(tree.find("title"),"unknown")
        description = element_value(tree.find("description"),"unknown")
        language = element_value(tree.find("language"),"en-us")
        copyright = element_value(tree.find("copyright"),"unknown")
        editor = element_value(tree.find("managingEditor"),"unknown")
        master = element_value(tree.find("webMaster"),"unknown")
        items = map(cls.parse_item,tree.iter("item"))
        return cls(title,description,"",language,copyright,editor,master,version,list(items))
    @classmethod
    def parse_90(cls,tree):
        version = tree.get("version","0.90")
        title = element_value(tree.find("title"),"unknown")
        description = element_value(tree.find("description"),"unknown")
        language = element_value(tree.find("language"),"en-us")
        copyright = element_value(tree.find("copyright"),"unknown")
        editor = element_value(tree.find("managingEditor"),"unknown")
        master = element_value(tree.find("webMaster"),"unknown")
        items = map(cls.parse_item,tree.iter("item"))
        return cls(title,description,"",language,copyright,editor,master,version,list(items))
    @classmethod
    def parse_20(cls,tree):
        version = tree.get("version","2.0")
        title = element_value(tree.find("title"),"unknown")
        description = element_value(tree.find("description"),"unknown")
        language = element_value(tree.find("language"),"en-us")
        copyright = element_value(tree.find("copyright"),"unknown")
        editor = element_value(tree.find("managingEditor"),"unknown")
        master = element_value(tree.find("webMaster"),"unknown")
        items = map(cls.parse_item,tree.iter("item"))
        return cls(title,description,"",language,copyright,editor,master,version,list(items))
    @classmethod
    def parse_item(cls,node,version="2.0"):
        return Item()
