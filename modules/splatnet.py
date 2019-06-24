import logging
import time
import asyncio
import json
from datetime import datetime, timedelta
import requests
import discord
from discord.ext import commands


def setup(client):
    """Add the module to the bot."""
    client.add_cog(Splatnet(client))
    logging.info("%s Module Online.", Splatnet.__name__)


class Splatnet(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(case_insensitive=True)
    async def s2(self, ctx):

        if ctx.invoked_subcommand is not None:
            return

        async with ctx.typing():
            schedule = requests.get(
                "https://splatoon2.ink/data/schedules.json").json()

            grizzco_schedule = requests.get(
                "https://splatoon2.ink/data/coop-schedules.json").json()

            splatnet = requests.get(
                "https://splatoon2.ink/data/merchandises.json").json()

            data = {
                "regular": {
                    "mode":
                    "Turf War",
                    "maps": [
                        schedule["regular"][0]['stage_a']['name'],
                        schedule["regular"][0]['stage_b']['name']
                    ],
                    "time": {
                        "start":
                        datetime.fromtimestamp(
                            schedule["regular"][0]["start_time"]).ctime(),
                        "end":
                        datetime.fromtimestamp(
                            schedule["regular"][0]["end_time"]).ctime(),
                        "remaining":
                        datetime.fromtimestamp(
                            schedule["regular"][0]["end_time"]) -
                        datetime.fromtimestamp(
                            schedule["regular"][0]["start_time"])
                    }
                },
                "ranked": {
                    "mode":
                    schedule["gachi"][0]["rule"]["name"],
                    "maps": [
                        schedule["gachi"][0]['stage_a']['name'],
                        schedule["gachi"][0]['stage_b']['name']
                    ],
                    "time": {
                        "start":
                        datetime.fromtimestamp(
                            schedule["gachi"][0]["start_time"]).ctime(),
                        "end":
                        datetime.fromtimestamp(
                            schedule["gachi"][0]["end_time"]).ctime(),
                        "remaining":
                        datetime.fromtimestamp(
                            schedule["gachi"][0]["end_time"]) - datetime.now()
                    }
                },
                "league": {
                    "mode":
                    schedule["league"][0]["rule"]["name"],
                    "maps": [
                        schedule["league"][0]['stage_a']['name'],
                        schedule["league"][0]['stage_b']['name']
                    ],
                    "time": {
                        "start":
                        datetime.fromtimestamp(
                            schedule["league"][0]["start_time"]).ctime(),
                        "end":
                        datetime.fromtimestamp(
                            schedule["league"][0]["end_time"]).ctime(),
                        "remaining":
                        datetime.fromtimestamp(
                            schedule["league"][0]["end_time"]) -
                        datetime.now()
                    }
                },
                "grizzco": {
                    "mode":
                    "Salmon Run",
                    "map":
                    grizzco_schedule["details"][0]["stage"]["name"],
                    "weapons": [
                        grizzco_schedule["details"][0]["weapons"][0]["weapon"]
                        ["name"], grizzco_schedule["details"][0]["weapons"][1]
                        ["weapon"]["name"], grizzco_schedule["details"][0]
                        ["weapons"][2]["weapon"]["name"],
                        grizzco_schedule["details"][0]["weapons"][3]["weapon"]
                        ["name"]
                    ],
                    "time": {
                        "start":
                        datetime.fromtimestamp(grizzco_schedule["details"][0]
                                               ["start_time"]).ctime(),
                        "end":
                        datetime.fromtimestamp(grizzco_schedule["details"][0]
                                               ["end_time"]).ctime(),
                        "remaining":
                        datetime.fromtimestamp(
                            grizzco_schedule["details"][0]["end_time"]) -
                        datetime.now()
                    }
                }
            }

            turf_embed = discord.Embed(
                title=
                f'Current Turf War Rotation: {data["regular"]["time"]["start"]} - {data["regular"]["time"]["end"]}',
                color=discord.Color.from_rgb(199, 207, 32))
            turf_embed.add_field(
                name="Map Set:",
                value=
                f'{data["regular"]["maps"][0]}, {data["regular"]["maps"][1]}')
            turf_embed.set_thumbnail(
                url=
                "https://cdn.wikimg.net/en/splatoonwiki/images/4/4c/Mode_Icon_Regular_Battle_2.png"
            )
            turf_embed.add_field(
                name="Time Left:",
                value=f'{data["regular"]["time"]["remaining"]}')

            ranked_embed = discord.Embed(
                title=
                f'Current Ranked Battle Rotation: {data["ranked"]["time"]["start"]} - {data["ranked"]["time"]["end"]}',
                color=discord.Color.from_rgb(243, 48, 0))
            ranked_embed.add_field(name="Current Mode:",
                                   value=data["ranked"]["mode"])
            ranked_embed.add_field(
                name="Map Set:",
                value=
                f'{data["ranked"]["maps"][0]}, {data["ranked"]["maps"][1]}')
            ranked_embed.set_thumbnail(
                url=
                "https://cdn.wikimg.net/en/splatoonwiki/images/2/2c/Mode_Icon_Ranked_Battle_2.png"
            )
            ranked_embed.add_field(
                name="Time Left:",
                value=f'{data["ranked"]["time"]["remaining"]}')

            league_embed = discord.Embed(
                title=
                f'Current League Rotation: {data["league"]["time"]["start"]} - {data["league"]["time"]["end"]}',
                color=discord.Color.from_rgb(234, 0, 107))
            league_embed.add_field(name="Current Mode:",
                                   value=f'{data["league"]["mode"]}')
            league_embed.add_field(
                name="Map Set:",
                value=
                f'{data["league"]["maps"][0]}, {data["league"]["maps"][1]}')
            league_embed.set_thumbnail(
                url=
                "https://cdn.wikimg.net/en/splatoonwiki/images/9/9b/Symbol_LeagueF.png"
            )
            league_embed.add_field(
                name="Time Left:",
                value=f'{data["league"]["time"]["remaining"]}')

            salmon_embed = discord.Embed(
                title=f"ADVERTISEMENT: Grizzco Industries is hiring!",
                color=discord.Color.from_rgb(255, 51, 54))
            salmon_embed.add_field(
                name="Current Recruitment Drive Time Window:",
                value=
                f'From {data["grizzco"]["time"]["start"]}, to {data["grizzco"]["time"]["end"]}'
            )
            salmon_embed.add_field(name="Current Location:",
                                   value=f'{data["grizzco"]["map"]}')
            salmon_embed.add_field(
                name="Available Weapon Pool:",
                value=
                f'{data["grizzco"]["weapon"][0]}, {data["grizzco"]["weapon"][1]}, {data["grizzco"]["weapon"][2]}, and {data["grizzco"]["weapon"][3]}'
            )
            salmon_embed.set_thumbnail(
                url=
                "https://cdn.wikimg.net/en/splatoonwiki/images/b/bf/S2_Icon_Grizzco.png"
            )

            await ctx.send(embed=turf_embed)
            await ctx.send(embed=ranked_embed)
            await ctx.send(embed=league_embed)

            if time.time() >= data["grizzco"]["time"]["start"]:
                await ctx.send(embed=salmon_embed)
