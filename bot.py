#-----------------------------------------

import discord
import json
import os
from discord.ext import commands
import asyncio
from itertools import cycle

#-----------------------------------------
TOKEN = 'NTU0MDc4NDY4MDA3MDAyMTIy.D2XZUQ.HlI5HIMALT0o-YAb1sxfdWYmBmI'
#-----------------------------------------

client = commands.Bot(command_prefix = '?')
client.remove_command('help')
os.chdir(r'/home/arslan/Arslan/Discord BOT/')


players = {}
queues = {}

def check_queues(id):
	if queues[id] != []:
		player - queues[id].pop(0)
		player[id] = player
		player.start()
		
		
		

status = ['THIS BOT IS DANK', 'USE ?HELP', 'YEAH NA']

async def change_status():
	await client.wait_until_ready()
	msgs = cycle(status)
	
	while not client.is_closed:
		current_status = next(msgs)
		await client.change_presence(game=discord.Game(name=current_status))
		await asyncio.sleep(5)
	
	
	
#-----------------------------------------
#BOT STATUS
@client.event
async def on_ready():
	#await client.change_presence(game=discord.Game(name='Matthew is a Homo'))
	print('Bot is ready.')
	
#-----------------------------------------
#TERMINAL MSG SEND
@client.event
async def on_message(message):
	print('A user has sent a message.')
	await client.process_commands(message) 
	
#-----------------------------------------
#AUTO ROLE COMMAND
@client.event
async def on_member_join(member):
	role = discord.utils.get(member.server.roles, name='Members')
	await client.add_roles(member, role)
	
#-----------------------------------------

@client.command()
async def ping(): 
	await client.say('Pong!')
	
#-----------------------------------------
#ECHO COMMAND
@client.command()
async def echo(*args):
	output = ''
	for word in args:
		output += word
		output += ' '
	await client.say(output)
	
#-----------------------------------------	
#CLEAR COMMAND
@client.command(pass_context=True)
async def clear(ctx, amount=10):
	channel = ctx.message.channel
	messages = []
	async for message in client.logs_from(channel, limit=int(amount)):
		messages.append(message)
	await client.delete_messages(messages)
	await client.say('Messages deleted')
	
#-----------------------------------------	
@client.command()
async def displayembed():
	embed = discord.Embed(
		title = 'Title',
		description = 'This is a description.',
		colour = discord.Colour.purple()
		
	)
	
	embed.set_footer(text='This is a footer.')
	embed.set_image(url='https://cdn.discordapp.com/attachments/544087334245629953/553820285191716876/image0.jpg')
	embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/544087334245629953/553820285191716876/image0.jpg')
	embed.set_author(name='Author Name', 
	icon_url='https://cdn.discordapp.com/attachments/544087334245629953/553820285191716876/image0.jpg')
	embed.add_field(name='Field Name', value='Field Value', inline=False) 
	embed.add_field(name='Field Name', value='Field Value', inline=True) 
	embed.add_field(name='Field Name', value='Field Value', inline=True) 
	
	await client.say(embed=embed)

#-----------------------------------------
@client.command(pass_context=True)
async def help(ctx):
	author = ctx.message.author
	
	embed = discord.Embed(
		colour = discord.Colour.orange()
		
	)
	
	embed.set_author(name='Help')
	embed.add_field(name='?ping', value='Returns Pong!', inline=False)
	embed.add_field(name='?clear', value='Clears a message!', inline=False)
	embed.add_field(name='?echo', value='Repeats msg!', inline=False)
	
	await client.send_message(author, embed=embed)

#-----------------------------------------
@client.event
async def on_reaction_add(reaction, user):
	channel = reaction.message.channel
	await client.send_message(channel, '{} had added {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))
	
@client.event	
async def on_reaction_add(reaction, user):
	channel = reaction.message.channel
	await client.send_message(channel, '{} had added {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))

#-----------------------------------------
@client.command(pass_context=True)
async def join(ctx):
	channel = ctx.message.author.voice.voice_channel
	await client.join_voice_channel(channel)
	
@client.command(pass_context=True)
async def leave(ctx):
	server = ctx.message.server
	voice_client = client.voice_client_in(server)
	await voice_client.disconnect()	

#-----------------------------------------

@client.command(pass_context=True)
async def play(ctx, url):
	server = ctx.message.server
	voice_client = client.voice_client_in(server)
	player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
	players[server.id] = player
	player.start()

#-----------------------------------------
@client.command(pass_context=True)
async def pause(ctx):
	id = ctx.message.server.id
	players[id].pause()
	
@client.command(pass_context=True)
async def stop(ctx):
	id = ctx.message.server.id
	players[id].stop()	

@client.command(pass_context=True)
async def resume(ctx):
	id = ctx.message.server.id
	players[id].resume()
	
#-----------------------------------------
@client.command(pass_context=True)
async def queue(ctx, url):
	server = ctx.message.server
	voice_client = client.voice_client_in(server)
	player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
	
	if server.id in queues:
		queues[server.id].append(player)
	else:
		queues[server.id] = [player]
	await client.say('Video queued.')
#-----------------------------------------

@client.event
async def on_member_join(member):
	with open('users.json', 'r') as f:
		users = json.load(f)
		
	await update_data(users, member)
	
	with open('users.json', 'w') as f:
		json.dump(users, f)
		
	
@client.event 
async def on_message(message):
	with open('users.json', 'r') as f:
		users = json.load(f)
		
	await update_data(users, message.author)
	await add_experience(users, message.author, 5)
	await level_up(users, message.author, message.channel)
	
	with open('users.json', 'w') as f:
		json.dump(users, f)
	
async def update_data(users, user):
	if not user.id in users:
		users[user.id] = {}
		users[user.id]['experience'] = 0
		users[user.id]['level'] = 1
		
async def add_experience(users, user, exp):
	users[user.id]['experience'] += exp
	
async def level_up(users, user, channel):
	experience = users[user.id]['experience']
	lvl_start = users[user.id]['level']
	lvl_end = int(experience ** (1/4))
	
	if lvl_start < lvl_end:
		await client.send_message(channel, '{} has leveled up to level {}'.format(user.mention,lvl_end))
		users[user.id]['level'] = lvl_end
	
#-----------------------------------------
client.loop.create_task(change_status())
client.run(TOKEN)














'''
@client.event
async def on_message(message):
	channel = message.channel
	if message.content.startswith('!What do you call black people?'):	
		await client.send_message(channel, 'Niggers!')
	
	channel = message.channel
	if message.content.startswith('!Is the bot working?'):	
		await client.send_message(channel, 'Yes!')
	
	
	
	if message.content.startswith('!echo'):
		msg = message.content.split()
		output = ''
		for word in msg[1:]:
			output += word 
			output += ' '
		await client.send_message(channel,output)
'''

