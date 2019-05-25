"""Core file holding the Prismarine Bot."""
import os
import logging
import json
from itertools import cycle
import discord
from discord.ext import commands, tasks


with open("config.json", "r") as infile:
    try:
        CONFIG = json.load(infile)
        _ = CONFIG["token"]
        _ = CONFIG["owner"]

    except (KeyError, FileNotFoundError):
        raise EnvironmentError(
            "Your config.json file is either missing, or incomplete. Check your config.json and ensure it has the keys 'token' and 'owner'"
        )

STATUS = cycle(["with my creator!", "with life, the universe, and everything.",
                "with my ROBOT ARMY!", "with a rubber ducky :)"])

CLIENT = commands.Bot(
    command_prefix="-",
    status=discord.Status.online,
)

logging.basicConfig(
    level=logging.INFO, format="%(name)s - %(levelname)s - %(asctime)s - %(message)s"
)

# --- Client Events


@CLIENT.event
async def on_ready():
    """What happens whem the bot is ready."""
    logging.basicConfig(
        level=logging.INFO, format="%(name)s - %(levelname)s - %(asctime)s - %(message)s"
    )
    stat_change.start()
    logging.info("Log successfuly launched. Project Prismarine is online.")


# --- Bot Commands

@CLIENT.command()
async def credits(ctx):
    """Credits the people who have contributed to the bot."""
    embed = discord.Embed(
        title="The Credits",
        description="""This command exists to commemorate and properly credit those who have assisted, inspired, or otherwise contributed to the creation of Project Prismarine.

    @.MO#0401 - For initially inspiring me to learn Python and persue Computer Science and programming in a serious manner.

    @Ikaheishi#0003 - For reviewing Project Prismarine's code and general assistance in my code endeavors.
    @TruePikachu#1985 - For aiding me in fixing several commands and showing me just how much of a newbie I am at Python.

    @DuckyQuack#7707 - For his massive assistance in improving the backend of Project Prismarine and making a multitide of improvements in the bot.

    To all of these people, I only have one thing to say.

    Thank you.
    """,
        color=discord.Color.gold(),
    )
    embed.set_author(name="Unit 10008-RSP", icon_url=CLIENT.user.avatar_url)
    embed.set_footer(text=f"Solidarity, Dr. Prismarine Bluefall.")
    await ctx.send(embed=embed)

# --- Misc. Code


@tasks.loop(seconds=30)
async def stat_change():
    """Changes the status of the bot every few seconds."""
    await CLIENT.change_presence(activity=discord.Game(next(STATUS)))

for filename in os.listdir('./modules'):
    if filename.endswith(".py"):
        CLIENT.load_extension(f"modules.{filename[:-3]}")

CLIENT.run(CONFIG["token"])
