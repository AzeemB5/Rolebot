import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Priority tag mapping
role_tags = {
    "administrator": "[ADM]",
    "developer": "[DEV]",
    "honored": "[HON]",
    "member": "[MEM]"
}

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.event
async def on_member_update(before, after):
    current_nick = after.nick or after.name
    tag_to_apply = ""

    # Always tag bots first
    if after.bot:
        tag_to_apply = "[BOT]"
    else:
        for role_name, tag in role_tags.items():
            if any(role.name.lower() == role_name for role in after.roles):
                tag_to_apply = tag
                break

    # Remove any existing role tag from nickname
    all_possible_tags = list(role_tags.values()) + ["[BOT]"]
    for tag in all_possible_tags:
        if current_nick.startswith(tag):
            current_nick = current_nick[len(tag):].strip()

    # Apply the new tag if needed
    new_nick = f"{tag_to_apply} {current_nick}" if tag_to_apply else current_nick

    try:
        if after.nick != new_nick:
            await after.edit(nick=new_nick)
            print(f"Nickname updated to: {new_nick}")
    except discord.Forbidden:
        print(f"No permission to update nickname for {after.name}")
    except discord.HTTPException as e:
        print(f"Failed to update nickname: {e}")

bot.run("MTM5MTUxODg0OTQzNzkyNTUzNw.GuRQpu.PQOyfDYDuKsosY6Wzt05_isBhd2Aqu8I1K2_ZA")
