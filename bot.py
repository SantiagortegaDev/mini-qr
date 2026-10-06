import traceback
import os
import discord
from discord.ext import commands
from qr_utils import qr_ascii_half_block
import dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

dotenv.load_dotenv()

# i don't use the prefix because it's only slash commands but i don't know what i'm doing man
# edit: i discover i can put None and it doesn't show again the warning for the message intent permision
bot = commands.Bot(command_prefix=None, intents=None)

class apicontainer(discord.ui.LayoutView):    
    container1 = discord.ui.Container(
        discord.ui.TextDisplay(content="# Mini QR API"),
        discord.ui.Separator(visible=True, spacing=discord.SeparatorSpacing.small),
        discord.ui.TextDisplay(content="## - Status\n**GET** `https://miniqr.alwaysdata.net/api`\n```ansi\n\u001b[0;2m{ \u001b[0;32m\"status\" \u001b[0m: \u001b[0;33m\"ok\"\u001b[0m ,\n\u001b[0;32m  \"name\"\u001b[0m :\u001b[0;33m \"Mini Qr\" \u001b[0m,\n\u001b[0;32m\u001b[0;32m  \"creator\"\u001b[0m\u001b[0;32m\u001b[0m : \u001b[0;33m\"@santiagortega\"\u001b[0m }\u001b[0m\n```"),
        discord.ui.Separator(visible=True, spacing=discord.SeparatorSpacing.small),
        discord.ui.TextDisplay(content="## - Generate QR\n**GET** `https://miniqr.alwaysdata.net/api/v1/qr?content=hello!`\n(Response in plain text)\n```ansi\n                         \n  █▀▀▀▀▀█ █▀ ▄█ █▀▀▀▀▀█  \n  █ ███ █ ▄▀█ ▄ █ ███ █  \n  █ ▀▀▀ █  █    █ ▀▀▀ █  \n  ▀▀▀▀▀▀▀ █ ▀ ▀ ▀▀▀▀▀▀▀  \n  █▄▀▀▄▀▀▀▄▄█ ▄ ▀▄ █▄▀█  \n  ▄▄▀█▀▄▀ █▀▄ ██▀▀▀▄ █▀  \n  ▀▀  ▀▀▀▀▄ █▀ █  ▀ ▄ ▀  \n  █▀▀▀▀▀█ █▀▄▄▄██ ▀▄▄ ▄  \n  █ ███ █ ▄█▄▀ ▄▀  ███▀  \n  █ ▀▀▀ █ ▀█▀█▄▀▄█▄ ▀ ▄  \n  ▀▀▀▀▀▀▀ ▀ ▀▀▀  ▀  ▀    \n```\n- **content**: str *\n- **invert**: bool = False\n- **raw**: bool = False (it return the qr in a json response)\n- **long**: bool = False (it bypass the discord bot character limit)"),
    )



@bot.event
async def on_ready():
    info = Text()
    info.append(f"Name: ", style="dim")
    info.append(f"{bot.user}\n", style="bold white")
    info.append(f"ID: ", style="dim")
    info.append(f"{bot.user.id}\n", style="bold white")
    info.append(f"Servers: ", style="dim")
    info.append(f"{len(bot.guilds)}\n", style="bold white")
    info.append(f"Ping: ", style="dim")
    info.append(f"{round(bot.latency * 1000)}ms", style="bold white")

    console.print(
        Panel(
            info,
            title="[bold white]Bot Online![/bold white]",
            border_style="white",
            expand=False,
        )
    )
    # if you don't try the bot here is what it shows, it's beautiful but i know no one is going to see except you :)

    #2026-09-26 22:41:55 INFO     discord.client logging in using static token
    #2026-09-26 22:41:57 INFO     discord.gateway Shard ID None has connected to Gateway (Session ID: fcf7a3e9d568296758a1918fe435f2a0).
    #╭────── Bot Online! ──────╮
    #│ Name: Mini Qr#0262      │
    #│ ID: 1550911077712142336 │
    #│ Servers: 1              │
    #│ Ping: 146ms             │
    #╰─────────────────────────╯

    # it has colors so if you can run it to see it


    await bot.tree.sync()


class Qr_modal(discord.ui.Modal):
    def __init__(self, qrcode: str):
        super().__init__(title='Your QR Code')
        self.qrcode = qrcode
        self.add_item(discord.ui.TextDisplay(content=f"```\n{qrcode}\n```"))

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message("sorry, the computer it's not computing", ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)


@bot.tree.command(name='qr', description='Generate a simple QR code')
async def qr_command(interaction: discord.Interaction, contenido: str, invert_colors: bool = False):
    ascii_qr = qr_ascii_half_block(contenido, invert_colors)
    await interaction.response.send_modal(Qr_modal(qrcode=ascii_qr))

@bot.tree.command(name='api', description='See how to generate a QR code with our api')
async def api_command(interaction: discord.Interaction):
    await interaction.response.send_message(view=apicontainer())

try:
 bot.run(os.getenv("DISCORD_TOKEN"))
except discord.errors.LoginFailure:
    info = Text()
    info.append(f"Bot token invalid: ", style="bold red")
    info.append(f"Improper token has been passed.\n\n", style="black")
    info.append(f"Check the discord developers panel and the .env file", style="bold white")
    console.print(
            Panel(
                info,
                title="[bold red]Bot Error[/bold red]",
                border_style="red",
                expand=False,
            )
        )
    #new error message!
    #$ python bot.py
    #2026-10-05 21:42:42 INFO     discord.client logging in using static token
    #╭───────────────────── Bot Error ──────────────────────╮
    #│ Bot token invalid: Improper token has been passed.   │
    #│                                                      │
    #│ Check the discord developers panel and the .env file │
    #╰──────────────────────────────────────────────────────╯
    #it looks better in terminal with the colors
