import os
from discord.ext import commands
import discord

bot_token = os.getenv('DISCORD_TOKEN')

# Resource optimization function
def calculate_max_fusions(timber, tender, abidos):
    TIMBER_PER_FUSION = 86
    TENDER_PER_FUSION = 45
    ABIDOS_PER_FUSION = 33
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
    
    max_timber_conversions = timber // 100
    max_tender_conversions = tender // 50
    
    for timber_conversions in range(max_timber_conversions + 1):
        remaining_timber = timber - (timber_conversions * 100)
        lumber_from_timber = timber_conversions * TIMBER_TO_LUMBER
        
        for tender_conversions in range(max_tender_conversions + 1):
            remaining_tender = tender - (tender_conversions * 50)
            lumber_from_tender = tender_conversions * TENDER_TO_LUMBER
            
            total_lumber = lumber_from_timber + lumber_from_tender
            new_abidos = (total_lumber // 100) * LUMBER_TO_ABIDOS
            total_abidos = abidos + new_abidos
            
            possible_fusions_timber = remaining_timber // TIMBER_PER_FUSION
            possible_fusions_tender = remaining_tender // TENDER_PER_FUSION
            possible_fusions_abidos = total_abidos // ABIDOS_PER_FUSION
            
            fusions = min(possible_fusions_timber, possible_fusions_tender, possible_fusions_abidos)
            
            if fusions > best_result['max_fusions']:
                final_remaining_timber = remaining_timber - (fusions * TIMBER_PER_FUSION)
                final_remaining_tender = remaining_tender - (fusions * TENDER_PER_FUSION)
                final_remaining_abidos = total_abidos - (fusions * ABIDOS_PER_FUSION)
                
                best_result = {
                    'max_fusions': fusions,
                    'timber_to_convert': timber_conversions * 100,
                    'tender_to_convert': tender_conversions * 50,
                    'remaining_timber': final_remaining_timber,
                    'remaining_tender': final_remaining_tender,
                    'remaining_abidos': final_remaining_abidos,
                    'lumber_powder_created': total_lumber,
                    'new_abidos_from_conversion': new_abidos
                }
            
            if fusions == 0 and best_result['max_fusions'] > 0:
                break
                
        if best_result['max_fusions'] > 0 and remaining_timber < TIMBER_PER_FUSION:
            break
    
    return best_result

# Set up the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
intents.message_content = True

# Command to run the fusion calculation
@bot.command()
async def optimize(ctx, timber: int, tender: int, abidos: int):
    result = calculate_max_fusions(timber, tender, abidos)

    response = f"""
    **Resource Optimization Results:**
    Maximum possible fusions: {result['max_fusions']}

    **Optimal conversion strategy:**
    Convert {result['timber_to_convert']} timber to lumber powder
    Convert {result['tender_to_convert']} tender to lumber powder

    **Conversion details:**
    Lumber powder created: {result['lumber_powder_created']}
    New abidos from conversion: {result['new_abidos_from_conversion']}

    **Remaining resources after ALL conversions and fusions:**
    Timber: {result['remaining_timber']}
    Tender: {result['remaining_tender']}
    Abidos: {result['remaining_abidos']}

    **Verification:**
    Resources used in fusions:
    Timber used: {result['max_fusions'] * 86}
    Tender used: {result['max_fusions'] * 45}
    Abidos used: {result['max_fusions'] * 33}
    """
    
    await ctx.send(response)

# Run the bot with your token
bot.run(bot_token)
