import os
from discord.ext import commands
import discord
from dotenv import load_dotenv
load_dotenv()

bot_token = os.getenv('DISCORD_TOKEN')

def calculate_max_fusions(timber, tender, abidos):
    # Check for invalid inputs
    if not all(isinstance(x, int) for x in [timber, tender, abidos]):
        return "invalid input, please make sure to input all 3 timbers"
    
    # Check for negative values
    if any(x < 0 for x in [timber, tender, abidos]):
        return "negative value cant be used"
    
    # Constants for resource requirements
    TIMBER_PER_FUSION = 86
    TENDER_PER_FUSION = 45
    ABIDOS_PER_FUSION = 33
    
    # Check if inputs meet minimum requirements
    if timber < TIMBER_PER_FUSION or tender < TENDER_PER_FUSION or abidos < ABIDOS_PER_FUSION:
        return "cant make any"
    
    # Rest of the calculation function remains the same...
    # [Previous calculation code here]

# Set up the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
intents.message_content = True

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="Type !help for commands"))

@bot.command(name='optimize')
async def optimize(ctx, *, args=None):
    """Calculate maximum possible fusions from given resources
    Usage: !optimize <timber> <tender> <abidos>
    Example: !optimize 1000 500 100"""
    
    if args is None:
        await ctx.send("cant make any")
        return
        
    try:
        # Split the args and convert to integers
        values = args.split()
        if len(values) != 3:
            await ctx.send("cant make any")
            return
            
        timber, tender, abidos = map(int, values)
        result = calculate_max_fusions(timber, tender, abidos)
        
        # Check if result is the error message
        if isinstance(result, str):
            await ctx.send(result)
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
        
        await ctx.send(response)
        
    except (ValueError, TypeError):
        await ctx.send("cant make any")

@bot.command(name='rates')
async def rates(ctx):
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
    await ctx.send(rates_info)

@bot.command(name='commands')
async def commands(ctx):
    """List all available commands"""
    commands_list = """
    **Available Commands:**
    
    `!optimize <timber> <tender> <abidos>`
    • Calculates maximum possible fusions from your resources
    • Example: `!optimize 1000 500 100`
    
    `!rates`
    • Shows all conversion rates and fusion requirements
    
    `!commands`
    • Shows this list of commands
    
    `!help`
    • Shows detailed help for all commands
    """
    await ctx.send(commands_list)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, (commands.errors.MissingRequiredArgument, 
                         commands.errors.BadArgument, 
                         commands.errors.MissingPermissions,
                         commands.errors.CommandInvokeError)):
        await ctx.send("cant make any")
    else:
        # Log other errors but still give user-friendly message
        print(f"Error: {str(error)}")
        await ctx.send("cant make any")

# Run the bot with your token
bot.run(bot_token)
