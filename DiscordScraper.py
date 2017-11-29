import discord
import asyncio
import csv
import re
from datetime import datetime
from datetime import timedelta

client = discord.Client()


admin_ids = ['INSERT ADMIN ID HERE']	#currently, it only works with one admin id.
									#It will be changed in the future to support messaging multiple people
	

#parses an introduction message
#returns a tuple with scraped info
def parseIntroduction(introduction):
	clean_intro = removeTrailingWhitespace(introduction)
	pattern = re.compile(r'2.(.+)[,\/-](.+)[,\/-](.+)\s3.(.+)\s4.(.+)')
	result = pattern.search(clean_intro)
	if result is not None:
		return result.groups()

#helper function for parseIntroduction
#removes any consecutive whitespace characters and replaces them with a new line		
def removeTrailingWhitespace(text):
	pattern = re.compile(r'([ ]+)\s')
	return str(pattern.sub('\n', text))
	
#logs a message from all channels except those in the blacklist
def logMessage(message, introduction):

	#logs data to introduction.csv if it comes from the introduction channel
	if message.channel.id == introduction:
		#intro_data = parseIntroduction(message.clean_content)
		#if intro_data is not None:
		
		#parsing code has been removed so that the code will not crash anymore
		print(intro_data)
		intro_file.writerow(intro_data)
			
	#logs data from all other channels to messages.csv
	else:
		roles = [r.name for r in message.author.roles[1:]]		
		messageInfo = (roles, str(message.timestamp), message.channel.name, message.clean_content )#NOTE: @here and @everyone mentions include the unicode zero width space for whatever reason
		print (messageInfo)
		csvwriter.writerow(messageInfo)

#messages people in the admin_ids list with the specified message, then closes the client	
async def messageAdmins(message):
	admins = []
	for id in admin_ids:
		a = await client.get_user_info(id)
		admins.append(a)
		
	for admin in admins:
		await client.send_message(admin, message)	

		
#on startup
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	await client.change_presence(status=discord.Status.invisible) 

#when a message is sent or received
@client.event
async def on_message(message):

	if message.timestamp - last_reminder > timedelta(days=1):
		last_reminder = message.timestamp
		await messageAdmins("The bot is still up! - " + str(last_reminder))
	try:
		if type(message.author) == discord.Member:
			logMessage(message, 'INSERT INTRODUCTION CHANNEL ID HERE')
	except:
		print('There was an error somewhere.\n Message id: ' + message.id)
#		await messageAdmins('There was an error somewhere.\n Message id: ' + message.id)
	
		
		

#opens files to be written to
intro_file = open('introductions.csv', 'a')
intro_writer = csv.writer(intro_file)
print('opened introductions.csv to append')

message_file = open("messages.csv", 'a')
csvwriter = csv.writer(message_file)
print("Opened messages.csv to append")
last_reminder = datetime.now()
 
client.run('INSERT BOT ID HERE')		


