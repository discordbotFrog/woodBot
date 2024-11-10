import os
import discord
from discord import app_commands
from dotenv import load_dotenv
from decimal import Decimal, InvalidOperation
import math

load_dotenv()
bot_token = os.getenv('DISCORD_TOKEN')

def calculate_max_fusions(timber: str, tender: str, abidos: str) -> dict:
    try:
        # Convert string inputs to integers
        timber = int(Decimal(timber))
        tender = int(Decimal(tender))
        abidos = int(Decimal(abidos))
        
        # Early validation
        if any(x < 0 for x in [timber, tender, abidos]):
            return "cant make any"
            
        # Constants
        TIMBER_PER_FUSION = 86
        TENDER_PER_FUSION = 45
        ABIDOS_PER_FUSION = 33
        
        if timber < TIMBER_PER_FUSION or tender < TENDER_PER_FUSION or abidos < ABIDOS_PER_FUSION:
            return "cant make any"
            
        # Optimized calculation using math instead of loops
        max_direct_fusions = min(
            timber // TIMBER_PER_FUSION,
            tender // TENDER_PER_FUSION,
            abidos // ABIDOS_PER_FUSION
        )
        
        # Calculate maximum possible lumber from conversions
        max_timber_lumber = (timber // 100) * 80  # 100 timber -> 80 lumber
        max_tender_lumber = (tender // 50) * 80   # 50 tender -> 80 lumber
        
        # Calculate maximum abidos from lumber conversion
        max_new_abidos = ((max_timber_lumber + max_tender_lumber) // 100) * 10
        
        # Calculate how many fusions possible with converted resources
        total_abidos = abidos + max_new_abidos
        max_converted_fusions = min(
            (timber - (max_timber_lumber // 80 * 100)) // TIMBER_PER_FUSION,
            (tender - (max_tender_lumber // 80 * 50)) // TENDER_PER_FUSION,
            total_abidos // ABIDOS_PER_FUSION
        )
        
        # Use the better of the two approaches
        if max_direct_fusions >= max_converted_fusions:
            return {
                'max_fusions': max_direct_fusions,
                'timber_to_convert': 0,
                'tender_to_convert': 0,
                'remaining_timber': timber - (max_direct_fusions * TIMBER_PER_FUSION),
                'remaining_tender': tender - (max_direct_fusions * TENDER_PER_FUSION),
                'remaining_abidos': abidos - (max_direct_fusions * ABIDOS_PER_FUSION),
                'lumber_powder_created': 0,
                'new_abidos_from_conversion': 0
            }
        else:
            timber_to_convert = (max_timber_lumber // 80 * 100)
            tender_to_convert = (max_tender_lumber // 80 * 50)
            return {
                'max_fusions': max_converted_fusions,
                'timber_to_convert': timber_to_convert,
                'tender_to_convert': tender_to_convert,
                'remaining_timber': timber - timber_to_convert - (max_converted_fusions * TIMBER_PER_FUSION),
                'remaining_tender': tender - tender_to_convert - (max_converted_fusions * TENDER_PER_FUSION),
                'remaining_abidos': total_abidos - (max_converted_fusions * ABIDOS_PER_FUSION),
                'lumber_powder_created': max_timber_lumber + max_tender_lumber,
                'new_abidos_from_conversion': max_new_abidos
            }
            
    except (InvalidOperation, ValueError, OverflowError):
        return "cant make any"

class Client(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = Client()

@client.tree.command(
    name="optimize",
    description="Calculate optimal resource conversion and fusion amounts"
)
@app_commands.describe(
    timber="Amount of timber",
    tender="Amount of tender",
    abidos="Amount of abidos"
)
async def optimize(
    interaction: discord.Interaction,
    timber: str,
    tender: str,
    abidos: str
):
    await interaction.response.defer()  # Defer the response to prevent timeout
    
    try:
        result = calculate_max_fusions(timber, tender, abidos)
        
        if isinstance(result, str):
            await interaction.followup.send(result)
            return
            
        response = f"""
        **Resource Optimization Results:**
        Maximum possible fusions: {result['max_fusions']:,}

        **Optimal conversion strategy:**
        Convert {result['timber_to_convert']:,} timber to lumber powder
        Convert {result['tender_to_convert']:,} tender to lumber powder

        **Conversion details:**
        Lumber powder created: {result['lumber_powder_created']:,}
        New abidos from conversion: {result['new_abidos_from_conversion']:,}

        **Remaining resources after ALL conversions and fusions:**
        Timber: {result['remaining_timber']:,}
        Tender: {result['remaining_tender']:,}
        Abidos: {result['remaining_abidos']:,}

        **Verification:**
        Resources used in fusions:
        Timber used: {result['max_fusions'] * 86:,}
        Tender used: {result['max_fusions'] * 45:,}
        Abidos used: {result['max_fusions'] * 33:,}
        """
        
        await interaction.followup.send(response)
        
    except Exception as e:
        await interaction.followup.send("cant make any")

client.run(bot_token)
