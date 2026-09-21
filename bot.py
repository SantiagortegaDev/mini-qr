import traceback
import dotenv
import discord
from discord.ext import commands
from qr_utils import qr_ascii_half_block

dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")
    await bot.tree.sync()



class Qr_modal(discord.ui.Modal):
    def __init__(self, qrcode: str):
        super().__init__(title='Your QR Code')
        self.qrcode = qrcode
        self.add_item(discord.ui.TextDisplay(content=f"```\n{qrcode}\n```"))

    async def on_submit(self):
        return

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message("sorry, the computer it's not computing", ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)


@bot.tree.command(name='qr', description='Generate a simple QR code')
async def qr_command(interaction: discord.Interaction, contenido: str):
    ascii_qr = qr_ascii_half_block(contenido)
    await interaction.response.send_modal(Qr_modal(qrcode=ascii_qr))


@bot.command(name="qr")
async def qr_command(ctx, *, contenido: str):
    ascii_qr = qr_ascii_half_block(contenido)
    await ctx.send(f"```\n{ascii_qr}\n```")


bot.run(dotenv.get("DISCORD_TOKEN"))