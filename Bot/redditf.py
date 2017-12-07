import praw, json

def get_reddit(credfile='DataBase/cred.json'):
    with open(credfile) as json_data:
        cred = json.load(json_data)

    reddit = praw.Reddit(client_id=cred['client_id'],
                         client_secret=cred['client_secret'],
                         password=cred['password'],
                         user_agent=cred['user_agent'],
                         username=cred['username']
                         )
    return reddit

def inString(List, String):
    for word in List:
        if word.lower() in String:
            return (True, word)
    return (False, None)

def isValid(comment):
    """
    Check if the given comment is valid to reply
    """
    if not (comment.id in Database["Comments"]):
        """
        The given comment was not in the database
        Initialize the comment i.e flag the comment as alread replied
        this prevents the bot from futher responding to the comment
        """
        AuthorId = comment.author.id 
        Database["Comments"].append(comment.id)

        if AuthorId not in Database["Users"]:
            Database["Users"][AuthorId] = [0]
            UserBase[AuthorId] = comment.author.name

        with open("DataBase/Database.json", 'w') as Dtb:
            json.dump(Database, Dtb)

        with open("DataBase/Userbase.json", 'w') as Dtb:
            json.dump(UserBase, Dtb)
        return True
    else:
        return False

def GetHugs(AuthorId):
    return Database["Users"][AuthorId][0]

def IncrementHugs(AuthorId):
    Database["Users"][AuthorId][0] += 1
    
    with open("DataBase/Database.json","w") as Dtb:
        json.dump(Database, Dtb)

def DecrementHugs(AuthorId):
    Database["Users"][AuthorId][0] -= 1
    with open("DataBase/Database.json","w") as Dtb:
        json.dump(Database, Dtb)

def WriteLog(log):
    with open("DataBase/LogFile.txt","a") as LogFile:
        LogFile.write(log)
        
class Message(object):

    def __init__(self, filename="DataBase/MessageFile.txt"):
        self.file = open(filename, "r")
        self.body = self.file.read()

    def GetBody(self):
        return self.body

    def GetMessage(self, index):
        index = index-1
        body = self.body
        message = body.split("$$$")
        message = [msg for msg in message if len(msg) > 2]
        return message[index]

M = Message()

with open("DataBase/Database.json", "r") as DatabaseFile:
    Database = json.load(DatabaseFile)

with open("DataBase/Userbase.json", "r") as DatabaseFile:
    UserBase = json.load(DatabaseFile)
