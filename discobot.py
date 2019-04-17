import discord
import asyncio
from datetime import datetime
from config import TOKEN

# Client ID 567157490765266944

# 523328 permissions

# https://discordapp.com/api/oauth2/authorize?client_id=567157490765266944&permissions=523328&scope=bot

''' list of waifus to claim ''' 
waifus = ['akeno himejima', 'rias gremory', 'riven', 'ciri', 'shinoa hiragi', 'ringo noyamano', 'mikuru asahina', 'aria shichijou', 'cynthia', 'skyla', 'chika fujiwara', 'jibril', 'pharah', 'blair', 'utaha kasumigaoka', 'rydia', 'yui', 'cia', 'ai shindou', 'shizuku ninomiya', 'mitty', 'a2', '2b', '9s', 'mirai kuriyama', 'kaede azusagawa', 'shiro', 'kanna kamui', 'taiga aisaka', 'sagiri izumi', 'illyasviel von einzbern (kaleid)', 'izuna hatsuse', 'zero two', 'sakura matou', 'chiho sasaki', 'asuna', 'frey (machine-doll)']

''' list of users with access to commands '''
users = ['220296856800854018', '175858990855487489', '141997543365017600', '95043633278885888',
         '200481198525513728', '567153956900569109']

''' INSTANTIATE CLIENT '''
client = discord.Client()

''' CAN I CLAIM???? global variable '''
claimable = True

''' background task that just '''
async def my_background_task():
    await client.wait_until_ready()

    time = datetime.now()

    global claimable
    
    ''' reset claim every 3 hours at xx:37:00 '''
    if (((time.hour-5) % 24) in [0, 3, 6, 9, 12, 15, 18, 21]) and (time.minute == 37) and (time.second == 0):
        claimable = True

@client.event
async def on_ready():
    print('Logged on as', client.user)
    
# Channel IDs

# testmudae 567154106528170006
# testmudae.general 567154106528170012

# eyedentity server 205903858604572672
# waifu channel 564189777398726666
# waifu-claimer 566856249937756161

@client.event
async def on_message(message):
    ''' don't respond to ourselves '''
    if message.author == client.user:
        return

    global claimable
    global users
    global waifus
    
    ''' if mudamaid 25 in this channel sees waifu in waifu list, claim '''
    if message.author.name:# == 'Mudamaid 25':
        if message.channel.id == '564189777398726666' or message.channel.id == '567154106528170012' or message.channel.id == '566856249937756161':
           
            await asyncio.sleep(2)
            
            print(("Channel: {} \n" +
                  "Message author disc id: {} \n" +
                  "Message content: {} \n" +
                  "Message type: {} \n" +
                  "Message reactions: {} \n" +
                  "Message embeds: {} \n" +
                  "\n").format(message.channel,
                                message.author,
                                message.content,
                                message.type,
                                message.reactions,
                                message.embeds))
                        
            if claimable:
                if message.embeds:
                    if len(message.reactions) < 2:
                        if message.reactions:
                            if message.embeds[0]['author']['name'].lower() in waifus:
                                #print('hello'+str(message.reactions[0].emoji)+'\n')
                                await client.add_reaction(message, message.reactions[0].emoji)
                                claimable = False

    ''' ping pong '''
    if message.content == 'ping':
        await client.send_message(message.channel, content='pong')
    ''' echo for trade '''
    if message.author.id in users and message.content.startswith("~echo"):
        await client.send_message(message.channel, message.content[5:])

    ''' react for messages '''
    if message.author.id in users and message.content.startswith("~react"):
        target_message_id = message.content[6:]
        target_message = client.get_message(message.channel, target_message_id)
        print(target_message.content)
        if target_message.embeds:
            if len(target_message.reactions) < 2:
                if target_message.reactions:
                    await client.add_reaction(target_message, target_message.reactions[0].emoji)

    ''' display list '''
    if message.author.id == '220296856800854018' and message.content.startswith("~list"):
        await client.send_message(message.channel, content=str(waifus))

    ''' add to waifulist '''
    if message.author.id == '220296856800854018' and message.content.startswith("~add"):
        waifus.append(message.content[4:].lower())

    ''' remove from waifulist '''
    if message.author.id == '220296856800854018' and message.content.startswith('`remove'):
        if message.content[7:].lower() in waifus:
            waifus.remove(message.content[7:])

client.loop.create_task(my_background_task())

client.run(TOKEN)
