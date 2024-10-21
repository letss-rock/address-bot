moimport discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the bot token from the environment variable
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Set up intents
intents = discord.Intents.default()
intents.messages = True  # Enable message intents
intents.message_content = True  # Explicitly enable message content intent
intents.guilds = True  # To access guild information
intents.members = True  # To manage members and roles

# Create bot instance with a command prefix
bot = commands.Bot(command_prefix='?', intents=intents)

# Dictionary to store user addresses
user_addresses = {}


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('Bot is ready to respond!')


@bot.event
async def on_member_join(member):
    # Automatically assign a house or flat to new members
    print(f"New member joined: {member.name}")

    # Randomly choose house or flat
    home_type = random.choice(['house', 'flat'])

    # Generate random house/flat numbers and types
    house_types = ['Single Storey', 'Double Decker', 'Bungalow']
    flat_types = ['1BHK', '2BHK', 'Penthouse']

    if home_type == 'house':
        selected_house_type = random.choice(house_types)
        house_number = random.randint(1, 100)
        address = f"{selected_house_type} House {house_number}, Martian Way"
        role_name = f"{selected_house_type} House {house_number}"
    else:
        selected_flat_type = random.choice(flat_types)
        flat_number = random.randint(1, 20)
        address = f"{selected_flat_type} Flat {flat_number}, Martian Way"
        role_name = f"{selected_flat_type} Flat {flat_number}"

    # Check if the role already exists
    role = discord.utils.get(member.guild.roles, name=role_name)
    if not role:
        # Create a new role if it doesn't exist
        role = await member.guild.create_role(name=role_name)

    # Assign the role to the new member
    await member.add_roles(role)

    # Store the user's address
    user_addresses[member.id] = {
        "role_name": role_name,
        "address": address,
    }

    # Send a welcome message in the specified channel
    channel = bot.get_channel(
        1297052143269969920)  # Replace with your channel ID
    if channel:
        await channel.send(
            f"Welcome to the server, {member.mention}! You have been assigned:\n- Address: {address}\n- Role: {role_name}"
        )
    else:
        print("Channel not found.")


@bot.command()
async def choosehome(ctx):
    """Allocate a unique home address to the user."""
    if ctx.author.id in user_addresses:
        await ctx.send(
            f"You already have a home allocated: {user_addresses[ctx.author.id]['address']}. Use `?viewaddress` to check it."
        )
        return

    # Randomly choose house or flat
    home_type = random.choice(['house', 'flat'])

    # Generate random house/flat numbers and types
    house_types = ['Single Storey', 'Double Decker', 'Bungalow']
    flat_types = ['1BHK', '2BHK', 'Penthouse']

    if home_type == 'house':
        selected_house_type = random.choice(house_types)
        house_number = random.randint(1, 100)
        address = f"{selected_house_type} House {house_number}, Martian Way"
        role_name = f"{selected_house_type} House {house_number}"
    else:
        selected_flat_type = random.choice(flat_types)
        flat_number = random.randint(1, 20)
        address = f"{selected_flat_type} Flat {flat_number}, Martian Way"
        role_name = f"{selected_flat_type} Flat {flat_number}"

    # Check if the role already exists
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        # Create a new role if it doesn't exist
        role = await ctx.guild.create_role(name=role_name)

    # Assign the role to the user
    await ctx.author.add_roles(role)

    # Store the user's address
    user_addresses[ctx.author.id] = {
        "role_name": role_name,
        "address": address,
    }

    await ctx.send(
        f"You have been allocated:\n- Address: {address}\n- Role: {role_name}")


@bot.command()
async def viewaddress(ctx):
    """View the user's allocated address."""
    user_info = user_addresses.get(ctx.author.id)
    if user_info:
        await ctx.send(
            f"Your assigned address is:\n- Address: {user_info['address']}\n- Role: {user_info['role_name']}"
        )
    else:
        await ctx.send(
            "You haven't chosen a home yet. Use `?choosehome` to get one!")


@bot.command()
@commands.has_role(
    'Admin')  # Only users with the 'Admin' role can use this command
@commands.has_permissions(
    administrator=True)  # And users with 'Administrator' permission
async def setaddress(ctx, member: discord.Member, *, address: str):
    """Manually assign a specific address to a user."""
    role_name = address.split(',')[0]  # Role name is derived from the address

    # Check if the role already exists
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        # Create a new role if it doesn't exist
        role = await ctx.guild.create_role(name=role_name)

    # Assign the role to the specified member
    await member.add_roles(role)

    # Manually store the address for the user
    user_addresses[member.id] = {
        "role_name": role_name,
        "address": address,
        "manual": True  # Manually assigned
    }

    await ctx.send(
        f"Manually assigned {member.mention} the following address:\n- Address: {address}\n- Role: {role_name}"
    )


@bot.command()
async def changeaddress(ctx, *, new_address: str):
    """Change the user's allocated address."""
    if ctx.author.id in user_addresses:
        user_addresses[ctx.author.id]['address'] = new_address
        await ctx.send(f"Your address has been updated to: {new_address}")
    else:
        await ctx.send(
            "You haven't chosen a home yet. Use `?choosehome` to get one!")


@bot.command()
async def ping(ctx):
    """Ping command to test bot response."""
    await ctx.send("Pong!")


# Run the bot
bot.run(TOKEN)
