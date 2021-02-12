import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials, firestore

class Events(commands.Cog):

  def __init__(self,client):
    db = firestore.client()
    self.client = client


def setup(client):
  client.add_cog(Events(client))
  print("event is online")
# will be deleted soon