import os
from discord.ext import commands
import discord
from discord_slash import SlashCommand, SlashContext
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!")
slash = SlashCommand(bot, sync_commands=True)  # Enable slash commands


def calculate_max_fusions(timber, tender, abidos):
    # Validation for inputs and handling large numbers
    if not all(isinstance(x, int) for x in [timber, tender, abidos]):
        return "cant make any"
    
    TIMBER_PER_FUSION = 86
    TENDER_PER_FUSION = 45
    ABIDOS_PER_FUSION = 33
    TIMBER_TO_LUMBER = 80
    TENDER_TO_LUMBER = 80
    LUMBER_TO_ABIDOS = 10
    
    direct_fusions = min(timber // TIMBER_PER_FUSION, tender // TENDER_PER_FUSION, abidos // ABIDOS_PER_FUSION)
    timber -= direct_fusions * TIMBER_PER_FUSION
    tender -= direct_fusions * TENDER_PER_FUSION
    abidos -= direct_fusions * ABIDOS_PER_FUSION

    timber_conversions = timber // 100
    tender_conversions = tender // 50
    lumber_from_timber = timber_conversions * TIMBER_TO_LUMBER
    lumber_from_tender = tender_conversions * TENDER_TO_LUMBER

    total_lumber = lumber_from_timber + lumber_from_tender
    additional_abidos = (total_lumber // 100) * LUMBER_TO_ABIDOS
    total_abidos = abidos + additional_abidos

    additional_fusions = min(timber // TIMBER_PER_FUSION, tender // TENDER_PER_FUSION, total_abidos // ABIDOS_PER_FUSION)
    timber -= additional_fusions * TIMBER_PER_FUSION
    tender -= additional_fusions * TENDER_PER_FUSION
    total_abidos -= additional_fusions * ABIDOS_PER_FUSION

    max_fusions = direct_fusions + additional_fusions
    
    return {
        'max_fusions': max_fusions,
        'timber_to_convert': timber_conversions * 100,
        'tender_to_convert': tender_conversions * 50,
        'remaining_timber': timber,
        'remaining_tender': tender,
        'remaining_abidos': total_abidos,
        'lumber_powder_created': total_lumber,
        'new_abidos_from_conversion': additional_abidos
    }

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="Type /help for commands"))

@slash.slash(name="optimize", description="Calculate maximum possible fusions from given resources")
async def _optimize(ctx: SlashContext, timber: int, tender: int, abidos: int):
    result = calculate_max_fusions(timber, tender, abidos)
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

    **Remaining resources after conversions and fusions:**
    Timber: {result['remaining_timber']}
    Tender: {result['remaining_tender']}
    Abidos: {result['remaining_abidos']}
    """
    
    await ctx.send(response)

@slash.slash(name="rates", description="Display all conversion rates and requirements")
async def _rates(ctx: SlashContext):
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

@slash.slash(name="commands", description="List all available commands")
async def _commands(ctx: SlashContext):
    commands_list = """
    **Available Commands:**
    
    `/optimize <timber> <tender> <abidos>`
    • Calculates maximum possible fusions from your resources
    
    `/rates`
    • Shows all conversion rates and fusion requirements
    
    `/commands`
    • Shows this list of commands
    """
    await ctx.send(commands_list)

bot.run(bot_token)
