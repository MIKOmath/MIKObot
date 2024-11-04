class ClassMeet():
    def __init__(self):
        self.type = 0
        self.type_str= "OM - Początujący"
        self.date = "2024-12-31"
        self.time = "20:00-21:30"
        self.host = "Filip Manijak"
        self.description = "Super koło"
    def load_from_discord(self,type,date,time,host,description):
        self.type = int(type)
        self.date = date
        self.time = time
        self.host = host
        self.description = description
        if self.type == 0:
            self.type_str = "OM - Początujący"
        if self.type == 1:
            self.type_str = "OM - Średna"
        if self.type == 2:
            self.type_str = "OM - Finał++"
        if self.type == 3:
            self.type_str = "OAI"
        if self.type == 4:
            self.type_str = "OF"
        if self.type == 5:
            self.type_str = "OI"


def user_class_match(type,user_roles):
    for role in user_roles:
        if role.name=='Średnia' and type==0:
            return True
        if role.name == 'Średnia' and type==1:
            return True
        if role.name == 'finał++' and type==2:
            return True
        if role.name == 'AI' and type==3:
            return True
        if role.name == 'Fizyka' and type==4:
            return True
        if role.name == 'Informatyka' and type==5:
            return True
    return False