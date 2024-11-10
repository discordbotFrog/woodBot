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
        # Set up required intents
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.synced = False  # Track if commands have been synced

    async def setup_hook(self):
        if not self.synced:  # Check if commands have been synced
            await self.tree.sync()  # Sync commands to all guilds
            self.synced = True

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        if not self.synced:  # Sync commands if they haven't been synced yet
            await self.tree.sync()
            self.synced = True
            print("Slash commands synced!")

client = AcreClient()

@client.tree.command(
    name="optimize",
    description="Calculate maximum possible fusions"
)
@app_commands.describe(
    timber="Amount of timber",
    tender="Amount of tender",
    abidos="Amount of abidos"
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

# Run the bot
print("Starting bot...")
client.run(bot_token)
