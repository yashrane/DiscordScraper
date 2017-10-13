import discord
import asyncio
import csv

client = discord.Client()

authorized_users = ['insert user ids here']


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
	
	
#All data should be anonymous: Never store the user id or nickname
#TODO: csv file with message information 
#TODO: csv file for user information(roles, time of joining, introduction info)
#TODO: check to see if we can get old archived data automatically using the bot

def get_logs():
	NUM_LIMIT = 1000
	CHANNEL_ID = "insert channel id here"
	SERVER_ID = "insert server id here"
	print(client.servers[0])
	
	#client.logs_from()








@client.event
async def on_message(message):
	if message.content.startswith('!test'):
		get_logs()
		counter = 0
		tmp = await client.send_message(message.channel, 'Calculating messages...')
		async for log in client.logs_from(message.channel, limit=100):
			if log.author == message.author:
				counter += 1

				await client.edit_message(tmp, 'You have {} messages.'.format(counter))
				
	elif message.content.startswith('!stop') and message.author.id in authorized_users:
		await client.logout()
		csvfile.close()
	else:
		roles = [r.name for r in message.author.roles[1:]]
		
		messageInfo = (roles, str(message.timestamp), message.channel.name, message.clean_content )#NOTE: @here and @everyone mentions include the unicode zero width space for whatever reason
		print (messageInfo)
		csvwriter.writerow(messageInfo)
		
csvfile = open("messages.csv", 'a')
csvwriter = csv.writer(csvfile)
print("Opened messages.csv to append")
 
client.run('insert bot id here')		
		
		
		
		
# Sample Introductions:


# Oppen_heimer - 07/22/2017
# 1)Oppen_heimer#0725
# 2) UCSB/2nd/CS
# 3) idk, ask guy fieri
# 4) yashtritch?
# 5) never bringing the bot back <---- you sure about that?

# HuntDucks - 07/26/2017
# huntducks #3238
# ucsb/2017/cs
# was in server before
# reddit

		#all on seperate lines
# DJ Megatron - 09/18/2017
# 1) DJ Megatron #0596
# 2) UCSB 3rd year Biology
# 3) I'm with koolkbraza
# 4) reddit moderators told me to come		
		

#NOTE: we only need messages from July 18, 2017 and onwards		

#introduction is a string which should contain a single introduction
#multiline introductions should be combined before being put into this function
def parseIntroduction(introduction):	

	return ""