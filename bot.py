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
bot = commands.Bot(command_prefix="!qr!", intents=None)


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
async def qr_command(interaction: discord.Interaction, contenido: str, invert_colors: bool):
    ascii_qr = qr_ascii_half_block(contenido, invert_colors)
    await interaction.response.send_modal(Qr_modal(qrcode=ascii_qr))


@bot.command(name="qr")
async def qr_command(ctx, *, contenido: str):
    ascii_qr = qr_ascii_half_block(contenido)
    await ctx.send(f"```\n{ascii_qr}\n```")


bot.run(os.getenv("DISCORD_TOKEN"))
