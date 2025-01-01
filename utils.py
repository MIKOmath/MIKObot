


class ClassMeet:
    """
    class that stores Class Meets events
    load_from_discord - changes class variables to data fetched from discord
    load_from_api - changes class variables to data fetched from API
    change_type_str - changes type_str value to value corresponding to type.
    """
    def __init__(self):
        self.id = None
        self.type = 0
        self.type_str= "OM - Początujący"
        self.date = "2024-12-31"
        self.time = "20:00-21:30"
        self.host = "Filip Manijak"
        self.description = "Super koło"
        self.theme = "Przykladowe koło"
        self.started=0
        self.finished=0
        self.difficulty=1
        self.special_guest=""
    def load_from_discord(self,typ,date,time,host,description,theme,
                          difficulty=1,special_guest=""):
        self.type = int(typ)
        self.date = date
        self.time = time
        self.host = host
        self.description = description
        self.change_type_str()
        self.theme = theme
        self.difficulty = difficulty
        self.special_guest = special_guest
    def change_type_str(self):
        if self.type == 0:
            self.type_str = "OM - Początujący"
        if self.type == 1:
            self.type_str = "OM - Średnia"
        if self.type == 2:
            self.type_str = "OM - Finał++"
        if self.type == 3:
            self.type_str = "OAI"
        if self.type == 4:
            self.type_str = "OF"
        if self.type == 5:
            self.type_str = "OI"
    def load_from_api(self, kolo_json):
        h1,m1,s1 = kolo_json["time"].split(':')
        h2, m2, s2 = kolo_json["duration"].split(':')
        s3= int(s1)+int(s2)
        if s3>=60:
            m1=int(m1)+1
            s3=s3-60
        m3 = int(m1)+int(m2)
        if m3>60:
            h1=int(h1)+1
            m3=m3-60
        if m3<10:
            m3='0'+str(m3)
        h3=(int(h1)+int(h2))%24
        if h3<10:
            h3='0'+str(h3)
        self.time = f"{h1}:{str(m1)}-{h3}:{str(m3)}"
        self.date = kolo_json["date"]
        try:
            self.type = int(kolo_json["group"])
        except:
            self.type = 0
        self.change_type_str()
        self.id = kolo_json['id']
        self.description = kolo_json["description"]
        self.theme = kolo_json["theme"]
        self.type = kolo_json["group"]

        self.started = int(kolo_json["started"])
        self.finished = int(kolo_json["finished"])
        self.difficulty = int(kolo_json['difficulty'])
        self.special_guest= kolo_json['special_guest']

def user_class_match(typ,user_roles):
    for role in user_roles:
        if role.name=='Początkująca' and typ==0:
            return True
        if role.name == 'Średnia' and typ==1:
            return True
        if role.name == 'finał++' and typ==2:
            return True
        if role.name == 'AI' and typ==3:
            return True
        if role.name == 'Fizyka' and typ==4:
            return True
        if role.name == 'Informatyka' and typ==5:
            return True
    return False
class Group:
    def __init__(self):
        self.name = "OM Średnia"
        self.lead = "Koło przygotowywujące do II etapu OM"
        self.description = "Fajna Grupa"
        self.discord_role_id=0
        self.default_difficulty=2
    def load_from_json(self,json_group):
        self.name = json_group['name']
        self.lead = json_group['lead']
        self.description = json_group['description']
        self.discord_role_id = json_group['discord_role_id']
        self.default_difficulty=json_group['default_difficulty']