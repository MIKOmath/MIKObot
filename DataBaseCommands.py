from contextlib import nullcontext
from utils import *
from supabase import create_client, Client

from utils import ClassMeet

SupabaseClient = 0
def connect_database():
    # Step 1: Set up Supabase credentials (replace with your actual Supabase URL and API key)
    SUPABASE_URL = "https://dbqakvurmeklbgyueptx.supabase.co"
    SUPABASE_KEY = open('databasekey.txt').readline()
    # Step 2: Create a Supabase client
    global SupabaseClient
    SupabaseClient = create_client(SUPABASE_URL, SUPABASE_KEY)

def sync_members(members):
    #in: list of discord.member class
    #Task: Add/remove members from db


    # Function to insert a new record into the 'messages' table
    def insert_message(content: str):
        response = SupabaseClient.table('messages').insert({'content': content, 'chuj2':2137}).execute()
        print(response)

    # Function to fetch messages from the 'messages' table
    def fetch_messages():
        response = SupabaseClient.table('messages').select('*').execute()
        print(response)
    pass
def add_class(kolo: ClassMeet):
    #Add_kolo to database
    pass

def get_class(time=14, role='all'):
    #wybieramy koła z bazy danych dla roli i w czasie mniejszym niż time dni.
    kolo1 = ClassMeet()
    kolo2= ClassMeet()
    kolo1.load_from_discord(type='1',date='2024-12-12',time='20:00-22:00',host="Fimpro",description="XD")
    kolo2.load_from_discord(type='2',date='2024-12-14',time='20:33-22:00',host="Fimpro222",description="XD222")
    return [kolo1,kolo2]

def add_point(member, points):
    #in discord.member class, int number
    #Task add (points) points to given member
    pass
def add_member(member):
    pass
    #in discord.member class
    #task add new member to database
def remove_member(member):
    pass
    #in discord.member class
    #task remove member from database