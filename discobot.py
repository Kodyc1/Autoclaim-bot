from config import TOKEN
from datetime import datetime
import asyncio
import discord
import logging 
import pickle

# Client ID 567157490765266944

# 523328 permissions

# https://discordapp.com/api/oauth2/authorize?client_id=567157490765266944&permissions=523328&scope=bot

''' list of waifus to claim ''' 
waifus = ['akeno himejima', 'rias gremory', 'riven', 'ciri', 'shinoa hiragi',
          'ringo noyamano', 'mikuru asahina', 'aria shichijou', 'cynthia', 
          'skyla', 'chika fujiwara', 'jibril', 'pharah', 'blair', 'utaha kasumigaoka', 
          'rydia', 'yui', 'cia', 'ai shindou', 'shizuku ninomiya', 'mitty', 
          'a2', '2b', '9s', 'mirai kuriyama', 'kaede azusagawa', 'shiro', 'kanna kamui', 
          'taiga aisaka', 'sagiri izumi', 'illyasviel von einzbern (kaleid)', 
          'izuna hatsuse', 'zero two', 'sakura matou', 'chiho sasaki', 'asuna', 'frey (machine-doll)',
          'shura kirigakure']

''' list of users with access to commands '''
users = ['220296856800854018', '175858990855487489',
         '141997543365017600', '95043633278885888',
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
        logging.info('Claim reset at {}:{}:{}'.format(time.hour, time.minute, time.second))

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
        if (message.channel.id == '564189777398726666' or 
            message.channel.id == '567154106528170012' or 
            message.channel.id == '566856249937756161'):
           
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

    ''' react to target message IDs '''
    if message.author.id in users and message.content.startswith("~react"):
        target_message_id = message.content[6:]
        target_message = await client.get_message(message.channel, target_message_id)
        if target_message.embeds:
            if target_message.reactions:
                await client.add_reaction(target_message, target_message.reactions[0].emoji)


    ''' display list '''
    if message.author.id == '220296856800854018' and message.content.startswith("~list"):
        pickle_in = open("waifu.pickle", "rb")
        waifulist = pickle.load(pickle_in)
        pickle_in.close()
        await client.send_message(message.channel, content=str(waifulist))

    ''' add to waifulist '''
    if message.author.id == '220296856800854018' and message.content.startswith("~add"):
        pickle_in = open("waifu.pickle", "rb")
        waifulist = pickle.load(pickle_in)
        waifulist.append(message.content[4:].lower())
        pickle_in.close()
        
        pickle_out=open("waifu.pickle", "wb")
        pickle.dump(waifulist, pickle_out)
        pickle_out.close()

    ''' remove from waifulist '''
    if message.author.id == '220296856800854018' and message.content.startswith('!!remove'):
        pickle_in = open("waifu.pickle", "rb")
        waifulist = pickle.load(pickle_in)
        if (message.content[8:].lower()) in waifulist:
            print('i should technically be removing message.content[8:]')
            waifulist.remove(message.content[7:])
        pickle_in.close()
        
        pickle_out=open("waifu.pickle", "wb")
        pickle.dump(waifulist, pickle_out)
        pickle_out.close()

client.loop.create_task(my_background_task())

client.run(TOKEN)
