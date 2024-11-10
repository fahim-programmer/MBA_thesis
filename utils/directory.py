import os

def folder(foldername:str):
    out = ""
    try:
        os.mkdir(foldername)
        out = out + " Folder Created"
    except Exception:
        out = out + " Failed to Create " + foldername
    return out