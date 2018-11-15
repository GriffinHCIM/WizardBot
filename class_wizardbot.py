import asyncio
import discord # https://github.com/Rapptz/discord.py
import re
import urllib.request
import urllib
import logging
import json

from discord.ext import commands

class WizardBot:
    ## Common items

    channel_dir = {}

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
        bot.loop.create_task(self.list_servers())

    ## Helper Functions

    async def list_servers(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed:
            for server in self.bot.servers:
                for channel in server.channels:
                  self.channel_dir[channel.name] = channel
            await asyncio.sleep(600)

    async def ehp_worker(self, ctx, skillname = "Overall"):
        splitmsg = ctx.message.content.split(" ", 1)

        if (len(splitmsg) == 2):
          cml_url = 'https://www.crystalmathlabs.com/tracker/api.php?type=trackehp&player=' + splitmsg[1]
          cml_url = cml_url.replace(" ", "%20")
          print(cml_url)

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

    def hsstring2dict(hs_string):
        if hs_string == '':
            return dict()

        spit_hs_string = hs_string.split()
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

        return {'overall':overall_dict,
                'attack':attack_dict,
                'defence':defence_dict,
                'strength':strength_dict,
                'hitpoints':hitpoints_dict,
                'range':range_dict,
                'prayer':prayer_dict,
                'magic':magic_dict,
                'cooking':cooking_dict,
                'woodcutting':woodcutting_dict,
                'fletching':fletching_dict,
                'fishing':fishing_dict,
                'firemaking':firemaking_dict,
                'crafting':crafting_dict,
                'smithing':smithing_dict,
                'mining':mining_dict,
                'herblore':herblore_dict,
                'agility':agility_dict,
                'thieving':thieving_dict,
                'slayer':slayer_dict,
                'farming':farming_dict,
                'runcrafting':runecrafting_dict,
                'hunter':hunter_dict,
                'construction':construction_dict}

    def retrieve_hiscore_string(username, scoreboard='regular'):
        scoreboard_type = ''

        if scoreboard in scoreboard_types:
            scoreboard_type = scoreboard_types[scoreboard]
        else:
            raise Error('Scoreboard not a valid type')

        url = "http://services.runescape.com/m=" + scoreboard_type + "/index_lite.ws?player=" + str(username)
        try:
            info = urllib.urlopen(url).read()
            return info
        except urllib.HTTPError as e:
            print(e)
            #raise Error('User not found')

    def get_player_levels(args):
        hs_string = retrieve_hiscore_string(args['username'], args['scoreboard'])
        hs_dict = hsstring2dict(hs_string)
        print(args['username'])
        tuple_list = []
        for subd in hs_dict:
            #print "\t" + subd + " : " + hs_dict[subd]['level'] + " " + hs_dict[subd]['rank']
            tuple_list += [(subd, int(hs_dict[subd]['level']), hs_dict[subd]['experience'], hs_dict[subd]['rank'])]

        Overall = ""
        tuple_list =  reversed(sorted(tuple_list, key=lambda x: int(x[2])))
        for skillrank in tuple_list:
            (skill, level, experience, rank) = skillrank
            if (skill == "overall"):
                Overall = "" + skill.ljust(13) + "\t" + str(level) + "\t" + rank + "\t{:,}".format(int(experience))
            if (skill != "overall"):
                if (level == 99):
                    print("" + skill.ljust(13) + "\t" + str(level) + "\t" + rank + "\t{:,}".format(int(experience)))
                else:
                    print("" + skill.ljust(13) + "\t" + str(level) + "\t" + rank)

        print(Overall)
        print("combat: " + str(int(combat_level(hs_dict))))

    ## Discord Commands

    @commands.command(name="kick-summary", pass_context=True, no_pm=True)
    async def kicksummary(self, ctx, *, kick_limit : int = 100):
        """ Summary of latest in #kick-log
        Optional paramter: int - size of messages to read, defaults to 100
        """
        regex = "(?i)(username):(\s\S+|\S+)"
        counter = 0
        tmp = await self.bot.send_message(ctx.message.channel, 'Calculating messages...')

        kicked_people = {}
        async for log in self.bot.logs_from(self.channel_dir["kick-log"], limit=kick_limit):
            if re.search(regex, log.content):
              match = re.search(regex, log.content)
              kicked_people[match.group(2).strip()] = kicked_people.get(match.group(2).strip(), 0) + 1

        msg = "The following people have been kicked recently:\n"
        for person in kicked_people:
          msg += str(person) + " has been kicked " + str(kicked_people[person]) + " times\n"

        await self.bot.edit_message(tmp, msg)

    @commands.command(pass_context=True, no_pm=True)
    async def hello(self, ctx):
        """ Simple command for testing if the bot is online """
        msg = 'Hello {0.author.mention}'.format(ctx.message)
        await self.bot.send_message(ctx.message.channel, msg)

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
        await self.ehp_worker(ctx, "fletching")

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

    bot.run(DISCORD_TOKEN)

if __name__ == '__main__':
    start_bot()
