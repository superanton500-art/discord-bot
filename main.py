import discord
import dotenv
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()    
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='s!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server.')
    await member.send(f'Welcome to the server, {member.name}, if you have any questions, feel free to open a ticket!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "fuck" in message.content.lower():
        await message.delete()
        await message.channel.send(f'{message.author.mention}, please refrain from using inappropriate language.')

    if any(role.name == "muted" for role in message.author.roles):
        await message.delete()
    
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}!')

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title=question, description=question, color=0x00ff00)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction('👍')
    await poll_message.add_reaction('👎')

@bot.command()
async def add_role(ctx, member: discord.Member, *, role=None):
    if ctx.author.guild_permissions.manage_roles:
        try:
            if role is not None:
                role_obj = discord.utils.get(ctx.guild.roles, name=role)
                if role_obj is not None:
                    # Check role hierarchy
                    if role_obj >= ctx.guild.me.top_role:
                        await ctx.send(f'{ctx.author.mention}, I cannot assign roles equal to or higher than my highest role.')
                        return
                    await member.add_roles(role_obj)
                    await ctx.send(f'{member.mention} has been given the role {role_obj.name}.')
                else:
                    await ctx.send(f'{ctx.author.mention}, the role "{role}" does not exist.')
            else:
                staff_role = discord.utils.get(ctx.guild.roles, name="staff")
                if staff_role is not None:
                    # Check role hierarchy
                    if staff_role >= ctx.guild.me.top_role:
                        await ctx.send(f'{ctx.author.mention}, I cannot assign the role (role hierarchy issue).')
                        return
                    await member.add_roles(staff_role)
                    await ctx.send(f'{member.mention} has been given the role {staff_role.name}.')
                else:
                    await ctx.send(f'{ctx.author.mention}, the role does not exist.')
        except discord.Forbidden:
            await ctx.send(f'{ctx.author.mention}, I do not have permission to assign roles.')
        except Exception as e:
            await ctx.send(f'{ctx.author.mention}, an error occurred: {e}')
    else:
        await ctx.send(f'{ctx.author.mention}, you do not have permission to assign roles.')

@bot.command()
async def remove_role(ctx, member: discord.Member, *, role=None):
    if ctx.author.guild_permissions.manage_roles:
        try:
            if role is not None:
                role_obj = discord.utils.get(ctx.guild.roles, name=role)
                if role_obj is not None:
                    # Check role hierarchy
                    if role_obj >= ctx.guild.me.top_role:
                        await ctx.send(f'{ctx.author.mention}, I cannot remove roles equal to or higher than my highest role.')
                        return
                    await member.remove_roles(role_obj)
                    await ctx.send(f'{member.mention} has been removed from the role {role_obj.name}.')
                else:
                    await ctx.send(f'{ctx.author.mention}, the role "{role}" does not exist.')
            else:
                staff_role = discord.utils.get(ctx.guild.roles, name="staff")
                if staff_role is not None:
                    # Check role hierarchy
                    if staff_role >= ctx.guild.me.top_role:
                        await ctx.send(f'{ctx.author.mention}, I cannot remove the staff role (role hierarchy issue).')
                        return
                    await member.remove_roles(staff_role)
                    await ctx.send(f'{member.mention} has been fired from the server.')
                else:
                    await ctx.send(f'{ctx.author.mention}, the "staff" role does not exist.')
        except discord.Forbidden:
            await ctx.send(f'{ctx.author.mention}, I do not have permission to remove roles.')
        except Exception as e:
            await ctx.send(f'{ctx.author.mention}, an error occurred: {e}')
    else:
        await ctx.send(f'{ctx.author.mention}, you do not have permission to remove roles.')

@bot.command()
async def warn(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.manage_messages:
        try:
            warning_3_role = discord.utils.get(ctx.guild.roles, name="warning 3")
            warning_2_role = discord.utils.get(ctx.guild.roles, name="warning 2")
            warning_1_role = discord.utils.get(ctx.guild.roles, name="warning 1")
            muted_role = discord.utils.get(ctx.guild.roles, name="muted")
            
            await ctx.send(f'{member.mention} has been warned. Reason: {reason if reason else "No reason provided"}')
            
            # Check if member has warning 3 role
            if warning_3_role and warning_3_role in member.roles:
                if muted_role is not None:
                    if muted_role >= ctx.guild.me.top_role:
                        await ctx.send(f'{ctx.author.mention}, I cannot assign the Muted role (role hierarchy issue).')
                        return
                    await member.add_roles(muted_role)
                    await ctx.send(f'{member.mention} already has 3 warnings and has been muted.')
            # Check if member has warning 2 role
            elif warning_2_role and warning_2_role in member.roles:
                if warning_3_role is not None:
                    if warning_3_role >= ctx.guild.me.top_role:
                        await ctx.send(f'{ctx.author.mention}, I cannot assign the Warning 3 role (role hierarchy issue).')
                        return
                    await member.add_roles(warning_3_role)
                    await ctx.send(f'{member.mention} has received their 3rd warning.')
            # Check if member has warning 1 role
            elif warning_1_role and warning_1_role in member.roles:
                if warning_2_role is not None:
                    if warning_2_role >= ctx.guild.me.top_role:
                        await ctx.send(f'{ctx.author.mention}, I cannot assign the Warning 2 role (role hierarchy issue).')
                        return
                    await member.add_roles(warning_2_role)
                    await ctx.send(f'{member.mention} has received their 2nd warning.')
            # First warning
            else:
                if warning_1_role is not None:
                    if warning_1_role >= ctx.guild.me.top_role:
                        await ctx.send(f'{ctx.author.mention}, I cannot assign the Warning 1 role (role hierarchy issue).')
                        return
                    await member.add_roles(warning_1_role)
                    await ctx.send(f'{member.mention} has received their 1st warning.')
                else:
                    await ctx.send(f'{ctx.author.mention}, the "Warning 1" role does not exist.')
        except discord.Forbidden:
            await ctx.send(f'{ctx.author.mention}, I do not have permission to warn members.')
        except Exception as e:
            await ctx.send(f'{ctx.author.mention}, an error occurred: {e}')
    try:        await member.send(f'You have been warned in {ctx.guild.name}. Reason: {reason if reason else "No reason provided"}')
    except discord.Forbidden:
        pass  # User has DMs closed or blocked the bot
    else:
        await ctx.send(f'{ctx.author.mention}, you do not have permission to warn members.')


@bot.command()
async def unmute(ctx, member: discord.Member):
    if ctx.author.guild_permissions.manage_roles:
        muted_role = discord.utils.get(ctx.guild.roles, name="muted")
        if muted_role is not None:
            # Check role hierarchy
            if muted_role >= ctx.guild.me.top_role:
                await ctx.send(f'{ctx.author.mention}, I cannot remove the Muted role (role hierarchy issue).')
                return
            await member.remove_roles(muted_role)
            await ctx.send(f'{member.mention} has been unmuted.')
        else:
            await ctx.send(f'{ctx.author.mention}, the "Muted" role does not exist.')
    else:
        await ctx.send(f'{ctx.author.mention}, you do not have permission to unmute members.')


@bot.command()
async def mute(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.manage_roles:
        muted_role = discord.utils.get(ctx.guild.roles, name="muted")
        if muted_role is not None:
            # Check role hierarchy
            if muted_role >= ctx.guild.me.top_role:
                await ctx.send(f'{ctx.author.mention}, I cannot assign the Muted role (role hierarchy issue).')
                return
            await member.add_roles(muted_role)
            await ctx.send(f'{member.mention} has been muted. Reason: {reason}')
        else:
            await ctx.send(f'{ctx.author.mention}, the "Muted" role does not exist.')
    else:
        await ctx.send(f'{ctx.author.mention}, you do not have permission to mute members.')

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.kick_members:
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} has been kicked from the server.')
    else:
        await ctx.send(f'{ctx.author.mention}, you do not have permission to kick members.')

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.ban_members:
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has been banned from the server.')
    else:
        await ctx.send(f'{ctx.author.mention}, you do not have permission to ban members.')


bot.run(token, log_handler=handler, log_level=logging.DEBUG)