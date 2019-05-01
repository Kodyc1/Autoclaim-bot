from config import TOKEN
from datetime import datetime
from pathlib import Path
import ast
import asyncio
import discord # 0.16.12
import logging 
import pickle

# Client ID 567157490765266944

# 523328 permissions

# https://discordapp.com/api/oauth2/authorize?client_id=567157490765266944&permissions=523328&scope=bot

# Channel IDs

# testmudae 567154106528170006
# testmudae.general 567154106528170012

# eyedentity server 205903858604572672
# waifu channel 564189777398726666
# waifu-claimer 566856249937756161



#################
### CONSTANTS ###
#################

''' base list of waifus to claim ''' 
waifus = ['akeno himejima', 'rias gremory', 'riven', 'ciri', 'shinoa hiragi',
          'ringo noyamano', 'mikuru asahina', 'aria shichijou', 'cynthia', 
          'skyla', 'chika fujiwara', 'jibril', 'pharah', 'blair', 'utaha kasumigaoka', 
          'rydia', 'yui', 'cia', 'ai shindou', 'shizuku ninomiya', 'mitty', 
          'a2', '2b', '9s', 'mirai kuriyama', 'kaede azusagawa', 'shiro', 'kanna kamui', 
          'taiga aisaka', 'sagiri izumi', 'illyasviel von einzbern (kaleid)', 
          'izuna hatsuse', 'zero two', 'sakura matou', 'chiho sasaki', 'asuna', 'frey (machine-doll)',
          'shura kirigakure']

''' list of users with access to commands '''
users = ['220296856800854018', '200481198525513728', '567153956900569109']

''' INSTANTIATE CLIENT '''
client = discord.Client()

''' Claimable global variable '''
claimable = True



#######################
### Background Loop ###
#######################

async def my_background_task():
    ''' Background task that just resets claimable every 3 hours
    '''
    await client.wait_until_ready()

    time = datetime.now()

    global claimable
    
    ''' reset claim every 3 hours at xx:37:00 '''
    if ((time.hour in [2, 5, 8, 11, 14, 17, 20, 23]) and (time.minute == 37) and (time.second == 0)):
        claimable = True
        logging.info('Claim reset at {}:{}:{}'.format(time.hour, time.minute, time.second))

@client.event
async def on_ready():
    print('Logged on as', client.user)


########################
### Helper functions ###
########################
    
def read_pickle(server_pickle, server):
    pickle_in = open(server + '.pickle', "rb")
    waifulist = pickle.load(pickle_in)
    pickle_in.close()
    return waifulist

def write_pickle(server_pickle, server, data):
    pickle_out = open(server + '.pickle', "wb")
    pickle.dump(data, pickle_out)
    pickle_out.close()


#######################
###    ON MESSAGE   ###
#######################

@client.event
async def on_message(message):
    ''' don't respond to ourselves '''
    if message.author == client.user:
        return

    global claimable
    global users
    global waifus

    server_pickle = Path(message.server.name + '.pickle')


    #########################
    ### Claim and Logging ###
    #########################
    
    if message.author.name:
        if (message.channel.id == '564189777398726666' or 
            message.channel.id == '567154106528170012' or 
            message.channel.id == '566856249937756161'):
           
            await asyncio.sleep(1)
            
            # TODO: LOG DATA IN PROGRESS
            logdata = ("Server - Channel: {} - {} \n" +
                  "Message author disc id: {} \n" +
                  "Message content: {} \n" +
                  "Message type: {} \n" +
                  "Message reactions: {} \n" +
                  "Message embeds: {} \n" +
                  "\n").format(message.server,
                               message.channel,
                               message.author,
                               message.content,
                               message.type,
                               message.reactions,
                               message.embeds))
            print(logdata)
            f = open("logs.txt", "a+")
            f.write(logdata)

            if message.embeds and message.reactions and len(message.reactions) < 2:
                    
                waifulist = read_pickle(server_pickle, message.server.name)
                    
                if message.embeds[0]['author']['name'].lower() in waifulist:

                    await client.add_reaction(message, message.reactions[0].emoji)
                        
                    

    ''' play ping pong '''
    if message.content == 'ping':
        await client.send_message(message.channel, content='pong')
        


    ####################
    ##### COMMANDS #####
    ####################

    ''' ~echo for trade '''
    if message.author.id in users and message.content.startswith("~echo"):

        await client.send_message(message.channel, message.content[5:])


    ''' ~react <target_message_ID> '''
    if message.author.id in users and message.content.startswith("~react"):

        target_message_id = message.content[6:]
        
        target_message = await client.get_message(message.channel, target_message_id)

        if target_message.embeds and target_message.reactions:

            await client.add_reaction(target_message, target_message.reactions[0].emoji)


    ''' ~list to display wishlist '''
    if (message.content == "~list") and (message.author.id in users):
        # if pickle already exists, read from it and display it
        if server_pickle.exists():            
            waifulist = read_pickle(server_pickle, message.server.name)
            await client.send_message(message.channel, content=str(waifulist))
            
        # else write the base list to a server.pickle and display it
        else:
            await client.send_message(message.channel, content="Creating base list")
            write_pickle(server_pickle, message.server.name, waifus)
            await client.send_message(message.channel, content=str(waifus))


    ''' ~set [] waifulist '''
    if (message.content.startswith("~set") and (message.author.id in users)):
        if server_pickle.exists():
            waifulist = ast.literal_eval(message.content[4:].strip())

            if isinstance(waifulist, list):

                write_pickle(server_pickle, message.server.name, waifulist)

                await client.add_reaction(message, '\u2705')

            else:
                await client.send_message(message.channel, content='Must set a list')
            

    ''' ~add <waifu> adds a waifu to waifulist '''
    if (message.content.startswith("~add") and (message.author.id in users)):
        if server_pickle.exists():
            waifulist = read_pickle(server_pickle, message.server.name)

            waifulist.append(message.content[4:].strip())

            write_pickle(server_pickle, message.server.name, waifulist)
            
            await client.add_reaction(message, '\u2705')
            
        else:
            await client.send_message(message.channel,
                                      content='Claim list does not exist yet. Create a base list with **~list**')


    ''' `remove <waifu> removes a waifu from waifulist '''
    if (message.content.startswith('`remove') and (message.author.id in users)):
        if server_pickle.exists():
            waifulist = read_pickle(server_pickle, message.server.name)
        
            waifu = message.content[7:].lower().strip()

            if (waifu) in waifulist:
                waifulist.remove(waifu)

            write_pickle(server_pickle, message.server.name, waifulist)

            await client.add_reaction(message, '\u2705')
            
        else:
            await client.send_message(message.channel,
                                      content='Claim list does not exist yet. Create a base list with **~list**')


    ''' ~claim  if claimable, return True, else return False '''
    if ((message.author.id in users) and (message.content == '~claim')):
        #await client.add_reaction(message,'\u2705')
        if claimable:
            await client.send_message(message.channel, content=str(claimable))


client.loop.create_task(my_background_task())

client.run(TOKEN)
