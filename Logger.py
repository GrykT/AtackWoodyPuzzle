from os import path,getcwd,linesep

class Logger:
    def __init__(self, log_filepath = f"{getcwd()}\\log.txt"):
        self.log_filepath = log_filepath

    def write(self, content):
        with open(self.log_filepath, mode="a" , encoding="shift-jis") as w:
            if(type(content) is str):
                w.write(str(content))
                w.write(linesep)
            
            if(type(content) is list):
                for l in content:
                    w.writelines(str(l))
                    w.write(linesep)