import discord
import asyncio
from discord.ext import commands
import firebase_admin

class Say(commands.Cog):

  def __init__(self,client):

    self.client = client
  db = firebase_admin.firestore.Client()

  


def setup(client):
  client.add_cog(Say(client))
  print("say is online :)")
