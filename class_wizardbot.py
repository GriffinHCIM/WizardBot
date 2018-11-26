import asyncio
import discord # https://github.com/Rapptz/discord.py
import feedparser # pip3 install feedparser
import re
import urllib.request
import urllib
import logging
import json
import time
import os

from bot_memory import bot_memory
from discord.ext import commands

class WizardBot:
    ## Common items

    scoreboard_types = {
        'regular':'hiscore_oldschool',
        'normal':'hiscore_oldschool',
        'ironman':'hiscore_oldschool_ironman',
        'iron':'hiscore_oldschool_ironman',
        'btw':'hiscore_oldschool_ironman',
        'hardcore':'hiscore_oldschool_hardcore_ironman',
        'hc':'hiscore_oldschool_hardcore_ironman',
        'ultimate':'hiscore_oldschool_ultimate',
        'ult':'hiscore_oldschool_ultimate',
        'deadman':'hiscore_oldschool_deadman',
        'dmm':'hiscore_oldschool_deadman',
        'seasonal':'hiscore_oldschool_seasonal'
        }

    skill_to_number = {
        "Overall":0,
        "Attack":1,
        "Defence":2,
        "Strength":3,
        "Hitpoints":4,
        "Ranged":5,
        "Prayer":6,
        "Magic":7,
        "Cooking":8,
        "Woodcutting":9,
        "Fletching":10,
        "Fishing":11,
        "Firemaking":12,
        "Crafting":13,
        "Smithing":14,
        "Mining":15,
        "Herblore":16,
        "Agility":17,
        "Theiving":18,
        "Slayer":19,
        "Farming":20,
        "Runecrafting":21,
        "Hunter":22,
        "Construction":23
        }

    ## Init

    def __init__(self, bot):
        self.bot = bot
        #bot.loop.create_task(self.message_manager())

    async def message_manager(self):
        while (True):
            for directory in [f.path for f in os.scandir("memory/") if f.is_dir() ]:
                #print (directory)
                memory = bot_memory(directory)
                reminders = memory.get_reminders()
                for reminder in reminders["memory"]:
                    if (int(reminder["epoch"]) < time.time()):
                        print ("time to send out:" + reminder["user"] + " " + reminder["message"])
                        channel = discord.Object(id=reminder["user"])
                        await self.bot.send_message(channel, reminder["message"])

                #print (memory.get_reminders())
            #print ("testing")
            await asyncio.sleep(60)

    ## Helper Functions

    async def ehp_worker(self, ctx, skillname = "Overall"):
        splitmsg = ctx.message.content.split(" ", 1)

        if (len(splitmsg) == 2):
          cml_url = 'https://www.crystalmathlabs.com/tracker/api.php?type=trackehp&player=' + splitmsg[1]
          cml_url = cml_url.replace(" ", "%20")

          tmp = await self.bot.send_message(ctx.message.channel, "Checking with cml...")
          request = urllib.request.Request(cml_url, headers={'User-Agent': 'Mozilla/5.0'})

          try:
              result = urllib.request.urlopen(request)
              mystr = result.read().decode("utf-8").strip().split()

              skillnumber = self.skill_to_number[skillname] + 1

              Skill = mystr[skillnumber].split(",")

              exp = Skill[0]
              ehp = Skill[4]

              msg = str(splitmsg[1]) + " gained " + "{:,d}".format(int(exp)) + " " + skillname + " exp and " + str(ehp) +" ehp"
              await self.bot.edit_message(tmp, msg)

          except urllib.error.HTTPError as err:
              await self.bot.edit_message(tmp, "CML doesn't want to talk to me at the moment. They responded with code {}".format(err.code))

    def hsstring2dict(self, hs_string):
        if hs_string == '':
            return dict()

        #spit_hs_string = hs_string.split()
        spit_hs_string = hs_string
        
        split_raw_stats = []

        for raw_stats in spit_hs_string:
            split_raw_stats += [raw_stats.split(',')]

        overall_dict = {'rank':split_raw_stats[0][0], 'level':split_raw_stats[0][1], 'experience':split_raw_stats[0][2]}
        attack_dict = {'rank':split_raw_stats[1][0], 'level':split_raw_stats[1][1], 'experience':split_raw_stats[1][2]}
        defence_dict = {'rank':split_raw_stats[2][0], 'level':split_raw_stats[2][1], 'experience':split_raw_stats[2][2]}
        strength_dict = {'rank':split_raw_stats[3][0], 'level':split_raw_stats[3][1], 'experience':split_raw_stats[3][2]}
        hitpoints_dict = {'rank':split_raw_stats[4][0], 'level':split_raw_stats[4][1], 'experience':split_raw_stats[4][2]}
        range_dict = {'rank':split_raw_stats[5][0], 'level':split_raw_stats[5][1], 'experience':split_raw_stats[5][2]}
        prayer_dict = {'rank':split_raw_stats[6][0], 'level':split_raw_stats[6][1], 'experience':split_raw_stats[6][2]}
        magic_dict = {'rank':split_raw_stats[7][0], 'level':split_raw_stats[7][1], 'experience':split_raw_stats[7][2]}
        cooking_dict = {'rank':split_raw_stats[8][0], 'level':split_raw_stats[8][1], 'experience':split_raw_stats[8][2]}
        woodcutting_dict = {'rank':split_raw_stats[9][0], 'level':split_raw_stats[9][1], 'experience':split_raw_stats[9][2]}
        fletching_dict = {'rank':split_raw_stats[10][0], 'level':split_raw_stats[10][1], 'experience':split_raw_stats[10][2]}
        fishing_dict = {'rank':split_raw_stats[11][0], 'level':split_raw_stats[11][1], 'experience':split_raw_stats[11][2]}
        firemaking_dict = {'rank':split_raw_stats[12][0], 'level':split_raw_stats[12][1], 'experience':split_raw_stats[12][2]}
        crafting_dict = {'rank':split_raw_stats[13][0], 'level':split_raw_stats[13][1], 'experience':split_raw_stats[13][2]}
        smithing_dict = {'rank':split_raw_stats[14][0], 'level':split_raw_stats[14][1], 'experience':split_raw_stats[14][2]}
        mining_dict = {'rank':split_raw_stats[15][0], 'level':split_raw_stats[15][1], 'experience':split_raw_stats[15][2]}
        herblore_dict = {'rank':split_raw_stats[16][0], 'level':split_raw_stats[16][1], 'experience':split_raw_stats[16][2]}
        agility_dict = {'rank':split_raw_stats[17][0], 'level':split_raw_stats[17][1], 'experience':split_raw_stats[17][2]}
        thieving_dict = {'rank':split_raw_stats[18][0], 'level':split_raw_stats[18][1], 'experience':split_raw_stats[18][2]}
        slayer_dict = {'rank':split_raw_stats[19][0], 'level':split_raw_stats[19][1], 'experience':split_raw_stats[19][2]}
        farming_dict = {'rank':split_raw_stats[20][0], 'level':split_raw_stats[20][1], 'experience':split_raw_stats[20][2]}
        runecrafting_dict = {'rank':split_raw_stats[21][0], 'level':split_raw_stats[21][1], 'experience':split_raw_stats[21][2]}
        hunter_dict = {'rank':split_raw_stats[22][0], 'level':split_raw_stats[22][1], 'experience':split_raw_stats[22][2]}
        construction_dict = {'rank':split_raw_stats[23][0], 'level':split_raw_stats[23][1], 'experience':split_raw_stats[23][2]}

        return {'Overall':overall_dict,
                'Attack':attack_dict,
                'Defence':defence_dict,
                'Strength':strength_dict,
                'Hitpoints':hitpoints_dict,
                'Range':range_dict,
                'Prayer':prayer_dict,
                'Magic':magic_dict,
                'Cooking':cooking_dict,
                'Woodcutting':woodcutting_dict,
                'Fletching':fletching_dict,
                'Fishing':fishing_dict,
                'Firemaking':firemaking_dict,
                'Crafting':crafting_dict,
                'Smithing':smithing_dict,
                'Mining':mining_dict,
                'Herblore':herblore_dict,
                'Agility':agility_dict,
                'Thieving':thieving_dict,
                'Slayer':slayer_dict,
                'Farming':farming_dict,
                'Runcrafting':runecrafting_dict,
                'Hunter':hunter_dict,
                'Construction':construction_dict}

    def retrieve_hiscore_string(self, username, scoreboard='regular'):
        scoreboard_type = ''

        if scoreboard in self.scoreboard_types:
            scoreboard_type = self.scoreboard_types[scoreboard]
        else:
            raise Error('Scoreboard not a valid type')

        url = "http://services.runescape.com/m=" + scoreboard_type + "/index_lite.ws?player=" + str(username)
        try:
            #info = urllib.urlopen(url).read()
            request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            result = urllib.request.urlopen(request)
            info = result.read().decode("utf-8").strip().split()
            return info
        except:
            print(e)
            #raise Error('User not found')

    def get_player_levels(self, args):
        hs_string = self.retrieve_hiscore_string(args['username'], args['scoreboard'])
        hs_dict = self.hsstring2dict(hs_string)
        #print(args['username'])
        tuple_list = []
        for subd in hs_dict:
            #print "\t" + subd + " : " + hs_dict[subd]['level'] + " " + hs_dict[subd]['rank']
            tuple_list += [(subd, int(hs_dict[subd]['level']), hs_dict[subd]['experience'], hs_dict[subd]['rank'])]

        
        msg = ""
        Overall = ""
        for skillrank in tuple_list:
            (skill, level, experience, rank) = skillrank
            if (skill == "Overall"):
                Overall = "" + skill.ljust(13) + ": \t" + str(level) + "\t" + rank + "\t{:,}".format(int(experience)) + "\n"
            if (skill != "Overall"):
                msg += "" + skill.ljust(13) + ": \t" + str(level) + "\t Rank: " + rank + "\t Exp: {:,}".format(int(experience)) + "\n"

        return msg + Overall

    ## Discord Commands
    @commands.command(name="reminder", pass_context=True)
    async def reminder(self, ctx, timer : int, *usermsg):
        if (timer >= 60*60*24*365):
            await self.bot.send_message(ctx.message.channel, "No reminders longer then 1 year please")
            return

        if (timer <= 60*10):
            await self.bot.send_message(ctx.message.channel, "No reminders less then 10 mins please")
            return 

        split_message = ctx.message.content.split(" ",2)
        epoch_time = int(time.time())
        reminder_time = epoch_time + timer
        msg = "Ok I'll make a note about that and remind you later about it.\nI've send you the following message in " + str(reminder_time) + ":\n" + split_message[2]   
        
        
        memory_path = "memory/PMs"
        if ctx.message.server:
            memory_path = "memory/" + ctx.message.server.name
        
        memory = bot_memory(memory_path)

        print (ctx.message.author)
        memory.update_reminders([{"epoch":reminder_time, "user":str(ctx.message.author.id), "message":split_message[2]}])
        #print (timer)
        #print (usermsg)
        await self.bot.send_message(ctx.message.channel, msg)


    @commands.command(name="kick-summary", pass_context=True, no_pm=True)
    async def kicksummary(self, ctx, *, kick_limit : int = 100):
        """ Summary of latest in #kick-log
        Optional paramter: int - size of messages to read, defaults to 100
        """
        regex = "(?i)(username):(\s\S+|\S+)"
        counter = 0
        tmp = await self.bot.send_message(ctx.message.channel, 'Calculating messages...')

        channel_dir = {}
        for channel in ctx.message.server.channels:
            channel_dir[channel.name] = channel
        
        kicked_people = {}
        async for log in self.bot.logs_from(channel_dir["kick-log"], limit=kick_limit):
            if re.search(regex, log.content):
              match = re.search(regex, log.content)
              kicked_people[match.group(2).strip()] = kicked_people.get(match.group(2).strip(), 0) + 1

        msg = "The following people have been kicked recently:\n"
        for person in kicked_people:
          msg += str(person) + " has been kicked " + str(kicked_people[person]) + " times\n"

        await self.bot.edit_message(tmp, msg)

    @commands.command(pass_context=True)
    async def rank(self, ctx):
        """ Displays the overall rank of the username provided """
        splitmsg = ctx.message.content.split(" ", 1)
        username = splitmsg[1].replace(" ", "%20")
        msg = self.get_player_levels({"username":username, "scoreboard":"ironman"})
        embed = discord.Embed(title="Stats for: " + splitmsg[1], description=msg)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(name="rank-hcim", pass_context=True)
    async def rankhcim(self, ctx):
        """ Displays the overall rank of the username provided """
        splitmsg = ctx.message.content.split(" ", 1)
        username = splitmsg[1].replace(" ", "%20")
        msg = self.get_player_levels({"username":username, "scoreboard":"hardcore"})
        embed = discord.Embed(title="Stats for: " + splitmsg[1], description=msg)
        await self.bot.send_message(ctx.message.channel, embed=embed)
    
    @commands.command(name="rank-uim", pass_context=True)
    async def rankulti(self, ctx):
        """ Displays the overall rank of the username provided """
        splitmsg = ctx.message.content.split(" ", 1)
        username = splitmsg[1].replace(" ", "%20")
        msg = self.get_player_levels({"username":username, "scoreboard":"ultimate"})
        embed = discord.Embed(title="Stats for: " + splitmsg[1], description=msg)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    async def hello(self, ctx):
        """ Simple command for testing if the bot is online """
        msg = 'Hello {0.author.mention}'.format(ctx.message)
        await self.bot.send_message(ctx.message.channel, msg)

    @commands.command(pass_context=True, no_pm=True)
    async def raidrules(self, ctx):
        """ Displays the rules for Ironscape raids """
        embed = discord.Embed(title="Raids Info", description="Please click [HERE](https://www.reddit.com/r/ironscape/comments/9qqabg/raid_cc_rules_and_info/) for all of our rules and information about Raiding within Raid CC, if you have any further queries or would like to get in touch with a member of the raid cc staff, please use the @Raids Staff role. if you are a learner please use the @Raids Teacher role to find help.")
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    async def cc(self, ctx):
        """Displays the cc information """
        msg = 'https://i.imgur.com/tfWfHiT.png'
        await self.bot.send_message(ctx.message.channel, msg)
   
    @commands.command(pass_context=True, no_pm=True)
    async def reddit(self, ctx):
        """Displays the reddit information """
        msg = 'Ironscapes Reddit: https://www.reddit.com/r/ironscape/'
        await self.bot.send_message(ctx.message.channel, msg)
    
    @commands.command(pass_context=True, no_pm=True)
    async def twitter(self, ctx):
        """Displays the twitter information """
        msg = 'Ironscapes Twitter: https://twitter.com/IronmanCC'
        await self.bot.send_message(ctx.message.channel, msg)

    @commands.command(pass_context=True, no_pm=True)
    async def news(self, ctx):
        """Displays the latest news post about OldSchoolRS """
        rss_url = "http://services.runescape.com/m=news/latest_news.rss?oldschool=true"
        rss_parser = feedparser.parse(rss_url)
        embed = discord.Embed(title=rss_parser["feed"]["title"], description=rss_parser["feed"]["description"], url="http://services.runescape.com/m=news/archive?oldschool=1", color=0x00ff00)
        embed.add_field(name=rss_parser.entries[0].title,  value=str(rss_parser.entries[0].description)+" [Click Here]({0})".format(rss_parser.entries[0].link), inline=False)
        embed.add_field(name=rss_parser.entries[1].title,  value=str(rss_parser.entries[1].description)+" [Click Here]({0})".format(rss_parser.entries[1].link), inline=False)
        embed.add_field(name=rss_parser.entries[2].title,  value=str(rss_parser.entries[2].description)+" [Click Here]({0})".format(rss_parser.entries[2].link), inline=False)
        embed.set_thumbnail(url=rss_parser.entries[0]["links"][0]["href"])
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    async def wiki(self, ctx):
        """Tries to link to the relevant wiki article """
        splitmsg = ctx.message.content.split(" ", 1)
        SearchTopic = splitmsg[1].replace(" ","%20")
        embed = discord.Embed(title="Here is what I found on OSRSWiki", description="This is what OSRSWiki has to say about {1}".format(SearchTopic, splitmsg[1]), color=0x00ff00)
        embed.url = "https://oldschool.runescape.wiki/w/Special:Search?search={0}".format(SearchTopic)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    async def ehp(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest overall ehp given a username """
        await self.ehp_worker(ctx)

    @commands.command(name="ehp-attack", pass_context=True, no_pm=True)
    async def ehp_attack(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest attack ehp given a username """
        await self.ehp_worker(ctx, "Attack")

    @commands.command(name="ehp-defence", pass_context=True, no_pm=True)
    async def ehp_defence(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest defence ehp given a username """
        await self.ehp_worker(ctx, "Defence")

    @commands.command(name="ehp-strength", pass_context=True, no_pm=True)
    async def ehp_strength(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest strength ehp given a username """
        await self.ehp_worker(ctx, "Strength")

    @commands.command(name="ehp-hitpoints", pass_context=True, no_pm=True)
    async def ehp_hitpoints(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest hitpoints ehp given a username """
        await self.ehp_worker(ctx, "Hitpoints")

    @commands.command(name="ehp-ranged", pass_context=True, no_pm=True)
    async def ehp_ranged(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest ranged ehp given a username """
        await self.ehp_worker(ctx, "Ranged")

    @commands.command(name="ehp-prayer", pass_context=True, no_pm=True)
    async def ehp_prayer(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest prayer ehp given a username """
        await self.ehp_worker(ctx, "Prayer")

    @commands.command(name="ehp-magic", pass_context=True, no_pm=True)
    async def ehp_magic(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest magic ehp given a username """
        await self.ehp_worker(ctx, "Magic")

    @commands.command(name="ehp-cooking", pass_context=True, no_pm=True)
    async def ehp_cooking(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest cooking ehp given a username """
        await self.ehp_worker(ctx, "Cooking")

    @commands.command(name="ehp-woodcutting", pass_context=True, no_pm=True)
    async def ehp_woodcutting(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest woodcutting ehp given a username """
        await self.ehp_worker(ctx, "Woodcutting")

    @commands.command(name="ehp-fletching", pass_context=True, no_pm=True)
    async def ehp_fletching(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest fletching ehp given a username """
        await self.ehp_worker(ctx, "Fletching")

    @commands.command(name="ehp-fishing", pass_context=True, no_pm=True)
    async def ehp_fishing(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest fishing ehp given a username """
        await self.ehp_worker(ctx, "Fishing")

    @commands.command(name="ehp-firemaking", pass_context=True, no_pm=True)
    async def ehp_firemaking(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest firemaking ehp given a username """
        await self.ehp_worker(ctx, "Firemaking")

    @commands.command(name="ehp-crafting", pass_context=True, no_pm=True)
    async def ehp_crafting(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest crafting ehp given a username """
        await self.ehp_worker(ctx, "Crafting")

    @commands.command(name="ehp-smithing", pass_context=True, no_pm=True)
    async def ehp_smithing(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest smithing ehp given a username """
        await self.ehp_worker(ctx, "Smithing")

    @commands.command(name="ehp-mining", pass_context=True, no_pm=True)
    async def ehp_mining(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest mining ehp given a username """
        await self.ehp_worker(ctx, "Mining")

    @commands.command(name="ehp-herblore", pass_context=True, no_pm=True)
    async def ehp_herblore(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest herblore ehp given a username """
        await self.ehp_worker(ctx, "Herblore")

    @commands.command(name="ehp-agility", pass_context=True, no_pm=True)
    async def ehp_agility(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest agility ehp given a username """
        await self.ehp_worker(ctx, "Agility")

    @commands.command(name="ehp-theiving", pass_context=True, no_pm=True)
    async def ehp_theiving(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest theiving ehp given a username """
        await self.ehp_worker(ctx, "Theiving")

    @commands.command(name="ehp-slayer", pass_context=True, no_pm=True)
    async def ehp_slayer(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest slayer ehp given a username """
        await self.ehp_worker(ctx, "Slayer")

    @commands.command(name="ehp-farming", pass_context=True, no_pm=True)
    async def ehp_farming(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest farming ehp given a username """
        await self.ehp_worker(ctx, "Farming")

    @commands.command(name="ehp-runecrafting", pass_context=True, no_pm=True)
    async def ehp_runecrafting(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest runecrafting ehp given a username """
        await self.ehp_worker(ctx, "Runecrafting")

    @commands.command(name="ehp-hunter", pass_context=True, no_pm=True)
    async def ehp_hunter(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest hunter ehp given a username """
        await self.ehp_worker(ctx, "Hunter")

    @commands.command(name="ehp-construction", pass_context=True, no_pm=True)
    async def ehp_construction(self, ctx):
        """ ehp command uses crystalmathlabs api and gets the latest construction ehp given a username """
        await self.ehp_worker(ctx, "Construction")



async def message_manager(bot):
    while (True):

        await asyncio.sleep(60)
        for directory in [f.path for f in os.scandir("memory/") if f.is_dir() ]:
                #print (directory)
            memory = bot_memory(directory)
            reminders = memory.get_reminders()
            for reminder in reminders["memory"]:
                if (int(reminder["epoch"]) < time.time()):
                    print ("time to send out:" + reminder["user"] + " " + reminder["message"])
                    channel = discord.Object(id=reminder["user"])
                    await bot.send_message(channel, reminder["message"])

                #print (memory.get_reminders())
            #print ("testing")



def start_bot():
    with open('config.json', 'r') as f:
      array = json.load(f)
    DISCORD_TOKEN = array['DISCORD_TOKEN']
    VERSION = array['VERSION']
    bot = commands.Bot(command_prefix=commands.when_mentioned_or('?'), description='A bot for Ironscape', version=VERSION)
    bot.add_cog(WizardBot(bot))

    @bot.event
    async def on_ready():
        print('\nLogged in as:\n{0} (ID: {0.id}) on the follow servers:'.format(bot.user))
        for server in bot.servers:
            print("\t{0}".format(server.name))

    #bot.loop.create_task(message_manager(bot))

    bot.run(DISCORD_TOKEN)

if __name__ == '__main__':
    start_bot()
