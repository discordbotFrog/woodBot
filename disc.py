import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('DISCORD_TOKEN')

MAX_RESOURCE_VALUE = 100000  # Maximum allowable value for resources
MIN_RESOURCE_VALUE = 0

def calculate_max_fusions(timber, tender, abidos):
    # Constants for resource requirements
    TIMBER_PER_FUSION = 86
    TENDER_PER_FUSION = 45
    ABIDOS_PER_FUSION = 33
    
    # Check if inputs meet minimum requirements
    if timber < TIMBER_PER_FUSION or tender < TENDER_PER_FUSION or abidos < ABIDOS_PER_FUSION:
        return "Minimum requirements not met"

    # Here, you would proceed with the calculation of fusions and return the result
    # Assuming result is a dictionary with the necessary fields
    result = {
        "max_fusions": min(timber // TIMBER_PER_FUSION, tender // TENDER_PER_FUSION, abidos // ABIDOS_PER_FUSION),
        "timber_to_convert": timber % TIMBER_PER_FUSION,
        "tender_to_convert": tender % TENDER_PER_FUSION,
        "lumber_powder_created": 0,  # Placeholder for your calculation logic
        "new_abidos_from_conversion": 0,  # Placeholder
        "remaining_timber": timber % TIMBER_PER_FUSION,
        "remaining_tender": tender % TENDER_PER_FUSION,
        "remaining_abidos": abidos - (result["max_fusions"] * ABIDOS_PER_FUSION),
    }
    return result

def validate_resources(*args):
    """Validate resource inputs"""
    for value in args:
        if not isinstance(value, int):
            return "All inputs must be integers"
        if value < MIN_RESOURCE_VALUE:
            return "Negative values cannot be used"
        if value > MAX_RESOURCE_VALUE:
            return f"Input values must be less than {MAX_RESOURCE_VALUE}"

# Set up the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="Type /help for commands"))

    # Syncing slash commands
    await bot.tree.sync()
    print("Slash commands synced!")

# Slash command for /optimize
@bot.tree.command(name="optimize", description="Optimize resources for maximum fusions")
async def optimize(interaction: discord.Interaction, timber: int, tender: int, abidos: int):
    """Calculate maximum possible fusions from given resources"""
    
    # Validate resource inputs
    validation_result = validate_resources(timber, tender, abidos)
    if validation_result:
        await interaction.response.send_message(validation_result)
        return

    result = calculate_max_fusions(timber, tender, abidos)

    # Check if result is an error message
    if isinstance(result, str):
        await interaction.response.send_message(result)
        return

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
    
    `/help`
    • Shows detailed help for all commands
    """
    await interaction.response.send_message(commands_list)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, (commands.errors.MissingRequiredArgument, 
                         commands.errors.BadArgument, 
                         commands.errors.MissingPermissions,
                         commands.errors.CommandInvokeError)):
        await ctx.send("An error occurred. Please try again.")
    else:
        # Log other errors but still give user-friendly message
        print(f"Error: {str(error)}")
        await ctx.send("An error occurred. Please try again.")

# Run the bot with your token
bot.run(bot_token)
