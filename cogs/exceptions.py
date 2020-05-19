from discord.ext import commands


class UserNotAuthenticated(commands.CommandError):
    """Current discord user is not authenticated"""
    msg = "Your discord account is not linked to any torn account. Use !help to see how to signup"
