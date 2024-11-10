import os
from discord import app_commands
import discord
from dotenv import load_dotenv
from typing import Optional
from decimal import Decimal, InvalidOperation

load_dotenv()
bot_token = os.getenv('DISCORD_TOKEN')

def calculate_max_fusions(timber: str, tender: str, abidos: str) -> dict:
    try:
        # Convert string inputs to Decimal for arbitrary-precision arithmetic
        timber_dec = Decimal(timber)
        tender_dec = Decimal(tender)
        abidos_dec = Decimal(abidos)
        
        # Check for negative values or non-whole numbers
        if any(not x.is_integer() or x < 0 for x in [timber_dec, tender_dec, abidos_dec]):
            return "cant make any"
        
        # Convert to integers for processing
        timber = int(timber_dec)
        tender = int(tender_dec)
        abidos = int(abidos_dec)
        
        # Constants for resource requirements
        TIMBER_PER_FUSION = 86
        TENDER_PER_FUSION = 45
        ABIDOS_PER_FUSION = 33
        
        # Check if inputs meet minimum requirements
        if timber < TIMBER_PER_FUSION or tender < TENDER_PER_FUSION or abidos < ABIDOS_PER_FUSION:
            return "cant make any"
        
        # Constants for conversion rates
        TIMBER_TO_LUMBER = 80
        TENDER_TO_LUMBER = 80
        LUMBER_TO_ABIDOS = 10
        
        best_result = {
            'max_fusions': 0,
            'timber_to_convert': 0,
            'tender_to_convert': 0,
            'remaining_timber': timber,
            'remaining_tender': tender,
            'remaining_abidos': abidos
        }
        
        # Calculate maximum possible conversions based on input values
        max_timber_conversions = timber // 100
        max_tender_conversions = tender // 50
        
        for timber_conversions in range(min(max_timber_conversions + 1, 1000000)):  # Add reasonable limit
            remaining_timber = Decimal(timber - (timber_conversions * 100))
            lumber_from_timber = Decimal(timber_conversions * TIMBER_TO_LUMBER)
            
            for tender_conversions in range(min(max_tender_conversions + 1, 1000000)):  # Add reasonable limit
                remaining_tender = Decimal(tender - (tender_conversions * 50))
                lumber_from_tender = Decimal(tender_conversions * TENDER_TO_LUMBER)
                
                total_lumber = lumber_from_timber + lumber_from_tender
                new_abidos = Decimal((total_lumber // 100) * LUMBER_TO_ABIDOS)
                total_abidos = Decimal(abidos) + new_abidos
                
                possible_fusions_timber = remaining_timber // TIMBER_PER_FUSION
                possible_fusions_tender = remaining_tender // TENDER_PER_FUSION
                possible_fusions_abidos = total_abidos // ABIDOS_PER_FUSION
                
                fusions = int(min(possible_fusions_timber, possible_fusions_tender, possible_fusions_abidos))
                
                if fusions > best_result['max_fusions']:
                    final_remaining_timber = int(remaining_timber - (fusions * TIMBER_PER_FUSION))
                    final_remaining_tender = int(remaining_tender - (fusions * TENDER_PER_FUSION))
                    final_remaining_abidos = int(total_abidos - (fusions * ABIDOS_PER_FUSION))
                    
                    best_result = {
                        'max_fusions': fusions,
                        'timber_to_convert': timber_conversions * 100,
                        'tender_to_convert': tender_conversions * 50,
                        'remaining_timber': final_remaining_timber,
                        'remaining_tender': final_remaining_tender,
                        'remaining_abidos': final_remaining_abidos,
                        'lumber_powder_created': int(total_lumber),
                        'new_abidos_from_conversion': int(new_abidos)
                    }
                
                if fusions == 0 and best_result['max_fusions'] > 0:
                    break
                    
            if best_result['max_fusions'] > 0 and remaining_timber < TIMBER_PER_FUSION:
                break
        
        return best_result
        
    except (InvalidOperation, ValueError, OverflowError):
        return "cant make any"

class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = Client()

@client.tree.command(name="optimize", description="Optimize resource conversion and fusion")
async def optimize(
    interaction: discord.Interaction,
    timber: str,
    tender: str,
    abidos: str
):
    try:
        result = calculate_max_fusions(timber, tender, abidos)
        
        if isinstance(result, str):
            await interaction.response.send_message(result)
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
        
        await interaction.response.send_message(response)
        
    except Exception as e:
        await interaction.response.send_message("cant make any")

client.run(bot_token)
