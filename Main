import discord
import time
import datetime

global LastSave
LastSave=0
TOKEN = "XD"
GUILD = "MIKO"
Users =[]

Plik=input("czy chcesz wczytać dane z pliku? jeśli tak podaj nazwę, inaczej wypisz 0")
client = discord.Client(intents=discord.Intents.all())

class User():
    def __init__(self, ID, discord_ID, name, points):
        self.ID=ID
        self.discord_ID=discord_ID
        self.name=name
        self.points=points
def GiveUserPoints(user,Points):
    UserID=0
    for x in range(len(Users)):
        if(int(Users[x].discord_ID)==int(user.id)):
            UserID=x
    Users[UserID].points+=Points


def SaveUsersArray(nazwa):
    global LastSave
    LastSave = time.time()
    f = open(nazwa+".txt", 'w')
    for x in Users:
        f.write(str(x.ID) +";"+str(x.discord_ID)+";" + x.name + ";" + str(x.points) + "\n")

@client.event # Obsługa zdarzenia połączenia z serwerem Discord
async def on_ready():
    print('Zalogowano jako {0.user}'.format(client))
    if(Plik=="0"):
        print("XD")
        for x in client.guilds:
            if(x.name==GUILD):
                print(x.name)
                serwer=x
                break
        UsersTemp=serwer.members
        i=0
        for x in UsersTemp:
            Users.append(User(i,x.id,x.name,0))
            i+=1
        teraz = str(datetime.datetime.now())
        teraz=teraz.replace(':', "-")
        SaveUsersArray("Users"+str(teraz))
    else:
        f=open(Plik,'r')
        UsersTemp=f.readlines()
        for x in UsersTemp:
            id,id_dc,name,points=x.split(';')
            points=int(points)
            id=int(id)
            Users.append(User(id,id_dc,name,points))
        for x in client.guilds:
            if(x.name==GUILD):
                print(x.name)
                serwer=x
                break
        UsersTemp = serwer.members
        i=Users[-1].ID+1
        for x in UsersTemp:
            CzyIstnieje=0
            for y in Users:
                if(int(y.discord_ID)==int(x.id)):
                    print(y.discord_ID,x.id)
                    CzyIstnieje=1
                    break

            if(not(CzyIstnieje)):
                Users.append(User(i,x.id,x.name,0))
                i+=1
        teraz = str(datetime.datetime.now())
        teraz = teraz.replace(':', "-")
        SaveUsersArray("Users" + str(teraz))
    #for x in Users:
    #    print(x.ID, x.discord_ID, x.name)

@client.event
async def on_reaction_add(reaction,user):   # Obsługa zdarzenia dodania reakcji do wiadomości
    wiad=reaction.message
    Wysylajacy=wiad.author
    Liczba_reakcji=0
    if(user!=Wysylajacy):
        OtherReactions = wiad.reactions
        for x in OtherReactions:
            users = [user async for user in x.users()]
            for y in users:
                if y == user:
                    Liczba_reakcji+=1

        if(Liczba_reakcji==1):
            if(("#Zadanie" in wiad.content) or ("#zadanie" in wiad.content)):
                GiveUserPoints(Wysylajacy,800)
                print("dodano 20 pkt:" ,str(Wysylajacy))
            elif(("#Materiał" in wiad.content) or ("#Material" in wiad.content)):
                GiveUserPoints(Wysylajacy, 2400)
                print("dodano 60 pkt:", str(Wysylajacy))
            elif (("#Solve" in wiad.content) or ("#Rozwiązanie" in wiad.content) or  ("#Rozwiazanie" in wiad.content)):
                GiveUserPoints(Wysylajacy, 800)
                print("dodano 20 pkt:", str(Wysylajacy))
            elif (("#Mem" in wiad.content) or ("#Meme" in wiad.content)):
                GiveUserPoints(Wysylajacy, 200)
                print("dodano 5 pkt:", str(Wysylajacy))

@client.event
async def on_reaction_remove(reaction,user):   # Obsługa zdarzenia dodania reakcji do wiadomości
    wiad=reaction.message
    Wysylajacy=wiad.author
    Liczba_reakcji=0
    if (user != Wysylajacy):
        OtherReactions = wiad.reactions
        for x in OtherReactions:
            users = [user async for user in x.users()]
            for x in users:
                if(x==user):
                    Liczba_reakcji+=1

        if(Liczba_reakcji==0):
            if(("#Zadanie" in wiad.content) or ("#zadanie" in wiad.content)):
                GiveUserPoints(Wysylajacy,-800)
            elif (("#Materiał" in wiad.content) or ("#Material" in wiad.content)):
                GiveUserPoints(Wysylajacy, -2400)
                print("dodano 60 pkt:", str(Wysylajacy))
            elif (("#Solve" in wiad.content) or ("#Rozwiązanie" in wiad.content) or ("#Rozwiazanie" in wiad.content)):
                GiveUserPoints(Wysylajacy, -800)
                print("dodano 20 pkt:", str(Wysylajacy))
            elif (("#Mem" in wiad.content) or ("#Meme" in wiad.content)):
                GiveUserPoints(Wysylajacy, -200)
                print("dodano 5 pkt:", str(Wysylajacy))
@client.event
async def on_member_join(member): #obsługa dołączenia nowego członka
    i = Users[-1].ID + 1
    Users.append(User(i,member.id,member.name,0))
    print("dodane", member.name)

@client.event
async def on_message(message): #robienie save'a
    if(message.content=="!ZAPISZ"):
        if (int(message.author.id) == 439425264901160961):
            teraz = str(datetime.datetime.now())
            teraz = teraz.replace(':', "-")
            SaveUsersArray("Users" + str(teraz))
    elif(message.content=="!MyPoints"):
        for x in Users:
            if(int(x.discord_ID)==int(message.author.id)):
                r1=str(x.name)+" "+str(x.points)
                await message.channel.send(r1)
    elif(message.content=="!check"):
        if(int(message.author.id)==439425264901160961):
            for x in Users:
                r1 = str(x.ID) + " " + str(x.name) + " " + str(x.points)
                await message.channel.send(r1)
    if(LastSave-time.time()>3600):
        SaveUsersArray()
    GiveUserPoints(message.author,1)

client.run(TOKEN)

