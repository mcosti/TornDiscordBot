import inspect
from tabulate import tabulate
from discord.ext import commands
import discord
from cogs.exceptions import UserNotAuthenticated
from fb.models import User, Credentials
from fb.torn.TornAPI import TornAPI
from fb.torn.exceptions import TornException
from fb.torn.models import TornData
from fb.database import Database, UserAlreadyExistsException

db = Database()


def get_user(ctx):
    discord_id = ctx.author.id
    user = Database.get_user_by_discord(discord_id)

    return user


class UserCog(commands.Cog, name='User'):
    def __init__(self, bot):
        self.bot = bot

    @commands.dm_only()
    @commands.command(name='signup', help='Usage: !signup 12345678 (Torn API KEY)')
    async def signup(self, ctx, torn_key):
        user = get_user(ctx)
        if user:
            await ctx.send('You can only have one torn account linked to one discord account')
            return await ctx.send('Use !delete_account to remove your torn account from our database')

        try:
            torn_resp = TornAPI.fetch_for_key(torn_key)
        except TornException as e:
            return await ctx.send(e)

        torn_data = TornData.from_data(torn_resp)
        credentials = Credentials(torn_key=torn_key, discord_id=ctx.author.id)
        user = User.create_new_user(torn_data=torn_data, credentials=credentials)
        try:
            Database.save_new_user(user)
        except UserAlreadyExistsException as e:
            await ctx.send("Your account already exists. I will link your new discord account to this torn account")
            user = Database.get_user(torn_data.player_id)
            discord_user = self.bot.get_user(user.credentials.discord_id)
            user.transfer_user(ctx.author.id)
            await discord_user.send(
                "Your key was transferred to another discord account. If you are not aware of this, change your API key"
            )

        await ctx.send(f"Welcome, {torn_data.name}!")
        await ctx.send("Use !settings to check your settings")

    @commands.dm_only()
    @commands.command(name='settings', help='Get your current settings')
    async def get_settings(self, ctx):
        user = get_user(ctx)
        if not user:
            return await ctx.send(UserNotAuthenticated.msg)

        embed = discord.Embed(title="Your settings")
        for key, value in user.settings.__dict__.items():
            embed.add_field(name=key, value=value, inline=True)

        return await ctx.send(embed=embed)

    @commands.dm_only()
    @commands.command(name='set', help='Change settings. Example: !set enable_global 0')
    async def change_setting(self, ctx, key, value):
        user = get_user(ctx)
        if not user:
            return await ctx.send(UserNotAuthenticated.msg)

        try:
            getattr(user.settings, key)
        except AttributeError:
            return await ctx.send("Invalid setting. Check !settings for all available settings")

        if value not in ['0', '1']:
            return await ctx.send(f"Invalid value {value}. The value can only be 0 or 1")

        new_value = bool(int(value))
        setattr(user.settings, key, new_value)
        Database.save_user(user, save_settings=True)
        return await ctx.send(f'New value for {key}: {new_value}')

    @commands.dm_only()
    @commands.command(name='delete_account', help='Delete all data in our database related to you')
    async def delete(self, ctx, confirm=''):
        user = get_user(ctx)
        if not user:
            return await ctx.send(UserNotAuthenticated.msg)

        confirm = (confirm.lower() == 'confirm')

        if not confirm:
            return await ctx.send(
                "This command deletes all data related to you. \n '!delete_account confirm' to confirm deletion"
            )

        db.delete_user(user)

        return await ctx.send("User deleted. We will miss you!")





