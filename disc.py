import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv('DISCORD_TOKEN')

def calculate_max_fusions(timber: int, tender: int, abidos: int) -> dict:
    # Constants
    TIMBER_PER_FUSION = 86
    TENDER_PER_FUSION = 45
    ABIDOS_PER_FUSION = 33
    
    # Calculate direct fusions possible
    max_fusions = min(
        timber // TIMBER_PER_FUSION,
        tender // TENDER_PER_FUSION,
        abidos // ABIDOS_PER_FUSION
    )
    
    return {
        'max_fusions': max_fusions,
        'timber_to_convert': 0,
        'tender_to_convert': 0,
        'remaining_timber': timber - (max_fusions * TIMBER_PER_FUSION),
        'remaining_tender': tender - (max_fusions * TENDER_PER_FUSION),
        'remaining_abidos': abidos - (max_fusions * ABIDOS_PER_FUSION),
        'lumber_powder_created': 0,
        'new_abidos_from_conversion': 0
    }

class AcreClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = AcreClient()

@client.tree.command(
    name="optimize",
    description="Calculate maximum possible fusions"
)
async def optimize(
    interaction: discord.Interaction,
    timber: int,
    tender: int,
    abidos: int
):
    try:
        result = calculate_max_fusions(timber, tender, abidos)
        
        response = f"""Maximum possible fusions: {result['max_fusions']}
Remaining resources:
Timber: {result['remaining_timber']}
Tender: {result['remaining_tender']}
Abidos: {result['remaining_abidos']}"""
        
        await interaction.response.send_message(response)
        
    except Exception as e:
        await interaction.response.send_message("cant make any")

client.run(bot_token)
