import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('DISCORD_TOKEN')

# Initial resources as per the logic
initial_resources = {
    'timber': 57670,
    'tender': 22041,
    'abidos': 10033
}

def calculate_max_fusions(timber, tender, abidos):
    """
    Calculate maximum possible fusions using an iterative approach.
    Returns dictionary with number of fusions and optimal conversion amounts.
    """
    # Resources needed per fusion
    TIMBER_PER_FUSION = 86
    TENDER_PER_FUSION = 45
    ABIDOS_PER_FUSION = 33
    
    # Conversion rates
    TIMBER_TO_LUMBER = 80  # from 100 timber
    TENDER_TO_LUMBER = 80  # from 50 tender
    LUMBER_TO_ABIDOS = 10  # from 100 lumber powder
    
    best_result = {
        'max_fusions': 0,
        'timber_to_convert': 0,
        'tender_to_convert': 0,
        'remaining_timber': timber,
        'remaining_tender': tender,
        'remaining_abidos': abidos
    }
    
    # Calculate maximum possible lumber powder from each resource
    max_timber_conversions = timber // 100
    max_tender_conversions = tender // 50
    
    # Try different combinations of conversions
    for timber_conversions in range(max_timber_conversions + 1):
        remaining_timber = timber - (timber_conversions * 100)
        lumber_from_timber = timber_conversions * TIMBER_TO_LUMBER
        
        for tender_conversions in range(max_tender_conversions + 1):
            remaining_tender = tender - (tender_conversions * 50)
            lumber_from_tender = tender_conversions * TENDER_TO_LUMBER
            
            # Calculate total lumber and resulting abidos
            total_lumber = lumber_from_timber + lumber_from_tender
            new_abidos = (total_lumber // 100) * LUMBER_TO_ABIDOS
            total_abidos = abidos + new_abidos
            
            # Calculate how many fusions are possible with these resources
            possible_fusions_timber = remaining_timber // TIMBER_PER_FUSION
            possible_fusions_tender = remaining_tender // TENDER_PER_FUSION
            possible_fusions_abidos = total_abidos // ABIDOS_PER_FUSION
            
            # The actual number of fusions is limited by the most constrained resource
            fusions = min(possible_fusions_timber, possible_fusions_tender, possible_fusions_abidos)
            
            if fusions > best_result['max_fusions']:
                # Calculate final remaining resources after fusions
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
            
            # Optimization: If we can't make any fusions with these conversions,
            # and we've already found a better solution, skip remaining tender conversions
            if fusions == 0 and best_result['max_fusions'] > 0:
                break
                
        # Similar optimization for timber loop
        if best_result['max_fusions'] > 0 and remaining_timber < TIMBER_PER_FUSION:
            break
    
    return best_result

# Set up the bot (discord.py v2.0 or higher required for slash commands)
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="Type /help for commands"))

    # Syncing slash commands with Discord
    await bot.tree.sync()
    print("Slash commands synced!")

# Slash command for /optimize
@bot.tree.command(name="optimize", description="Optimize resources for maximum fusions")
async def optimize(interaction: discord.Interaction, timber: int, tender: int, abidos: int):
    """Calculate maximum possible fusions from given resources"""
    
    print(f"Received /optimize command with timber={timber}, tender={tender}, abidos={abidos}")
    
    # Validate resource inputs
    if timber < 0 or tender < 0 or abidos < 0:
        await interaction.response.send_message("Negative values can't be used.")
        return
    if timber > 100000 or tender > 100000 or abidos > 100000:
        await interaction.response.send_message("Input values can't be greater than 100,000.")
        return
    
    # Use the new logic to calculate the result
    result = calculate_max_fusions(timber, tender, abidos)

    if result['max_fusions'] == 0:
        await interaction.response.send_message("Cannot make any fusions with the current resources.")
        return

    # Send the results back to Discord
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
    
    await interaction.response.send_message(response)

# Slash command for /rates
@bot.tree.command(name="rates", description="Show all conversion rates and fusion requirements")
async def rates(interaction: discord.Interaction):
    """Display all conversion rates and requirements"""
    rates_info = """
    **Conversion Rates:**
    • 100 Timber → 80 Lumber Powder
    • 50 Tender → 80 Lumber Powder
    • 100 Lumber Powder → 10 Abidos

    **Fusion Requirements:**
    Each fusion needs:
    • 86 Timber
    • 45 Tender
    • 33 Abidos
    """
    await interaction.response.send_message(rates_info)

# Slash command for /commands
@bot.tree.command(name="commands", description="List all available commands")
async def commands(interaction: discord.Interaction):
    """List all available commands"""
    commands_list = """
    **Available Commands:**
    
    `/optimize <timber> <tender> <abidos>`
    • Calculates maximum possible fusions from your resources
    • Example: `/optimize 1000 500 100`
    
    `/rates`
    • Shows all conversion rates and fusion requirements
    
    `/commands`
    • Shows this list of commands
    
    """
    await interaction.response.send_message(commands_list)

# Error handling for slash commands
@bot.event
async def on_application_command_error(interaction: discord.Interaction, error: Exception):
    print(f"Error occurred: {str(error)}")
    if isinstance(error, app_commands.MissingRequiredArgument):
        await interaction.response.send_message("Missing required argument. Please provide the necessary parameters.")
    elif isinstance(error, app_commands.CommandInvokeError):
        await interaction.response.send_message("An error occurred while processing your command.")
    else:
        await interaction.response.send_message("An error occurred. Please try again.")

# Run the bot with your token
bot.run(bot_token)
