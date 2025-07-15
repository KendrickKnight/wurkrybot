import json

def syncData(fileName ,cmd=True ,inputData=None):
    # if cmd == true, then load the data
    # if cmd != true, than save the data
    
    try:
        filePath = f"data/{fileName}.json"
        with open(filePath,"r") as d:
            dataBase = json.load(d)
    except Exception as e:
        print(e)

    if cmd:
        return dataBase
    elif not cmd:
        with open(filePath, "w") as od:
            json.dump(inputData,od, indent=4)