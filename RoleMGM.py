import discord
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True  # Enables message-based commands

bot = commands.Bot(command_prefix="!", intents=intents)

# Priority role-to-tag mapping
role_tags = {
    "administrator": "[ADM]",
    "developer": "[DEV]",
    "honored": "[HON]",
    "member": "[MEM]",
    "bots": "[BOT]"  
}



@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

# Function to apply tag logic to a member
async def apply_tag(member):
    base_name = member.nick or member.name
    tag = ""

    # Determine tag
    if member.bot:
        tag = "[BOT]"
    else:
        for role_name, tag_value in role_tags.items():
            if any(role.name.lower() == role_name for role in member.roles):
                tag = tag_value
                break

    # Strip old tag
    for old_tag in list(role_tags.values()) + ["[BOT]"]:
        if base_name.startswith(old_tag):
            base_name = base_name[len(old_tag):].strip()

    new_nick = f"{tag} {base_name}" if tag else base_name

    try:
        if member.nick != new_nick:
            await member.edit(nick=new_nick)
            print(f"Updated {member.name} to {new_nick}")
    except discord.Forbidden:
        print(f"Can't change nickname for {member.name}")
    except discord.HTTPException as e:
        print(f"HTTP error for {member.name}: {e}")

# Manual command to update all members
@bot.command()
@commands.has_permissions(administrator=True)
async def updateall(ctx):
    await ctx.send("🔄 Updating all member nicknames...")

    for member in ctx.guild.members:
        await apply_tag(member)  # 👈 This is your line!

    await ctx.send("✅ Update complete!")

keep_alive()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))

