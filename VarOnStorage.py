from random import randint,choices
from string import ascii_letters,digits
from pickle import dumps,loads
from os import getenv,remove
from time import sleep
class VariableCreator(object):
    variables={}
    tmp_dir=getenv("temp") or getenv("tmp")
    def createVar(self,var:str,data:list|dict|set|str)->None:
        assert isinstance(var,str)
        assert not isinstance(data,int)
        if var in self.variables:return None
        file=open("".join((self.tmp_dir,"\\",self.__createname(),".tmp")),"w+b" if (isinstance(data,list)|isinstance(data,dict)|isinstance(data, set)) else "w+")
        file.write(dumps(data) if isinstance(data,list)|isinstance(data,dict)|isinstance(data, set) else data)
        file.seek(0)
        self.variables[var]=(file,True if (isinstance(data,list)|isinstance(data,dict)|isinstance(data, set)) else False)
    def getVar(self,var:str)->list|dict|set|str|None:
        if not var in self.variables:return None
        data=self.variables.get(var)
        data[0].seek(0)
        return loads(data[0].read()) if data[1] else data[0].read()
    def changeValue(self,var:str,data:list|dict|set|str)->None:
        assert isinstance(var,str)
        assert not isinstance(data,int)
        if not var in self.variables:return self.createVar(var,data)
        file=self.variables.get(var)[0]
        name=file.name
        file.close()
        file=open(name,"w+b" if (isinstance(data,list)|isinstance(data,dict)|isinstance(data, set)) else "w+")
        file.write(dumps(data) if isinstance(data, list)|isinstance(data, dict)|isinstance(data, set) else data)
        file.seek(0)
        self.variables[var] = (file, True if (isinstance(data, list) | isinstance(data, dict)|isinstance(data, set)) else False)
    def removeVar(self,var)->None:
        if not var in self.variables:return None
        file=self.variables.get(var)[0]
        self.variables.pop(var)
        file.write("")
        file.close()
        remove(file.name)
    def clear(self,timeout:int=0):
        sleep(timeout)
        for key,value in self.variables:
            self.removeVar(key)
    def __createname(self)->str:
        return "".join(choices("".join((ascii_letters,str(digits))),k=randint(5,50)))