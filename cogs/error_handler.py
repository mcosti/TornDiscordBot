import sys
import traceback

from discord.ext import commands


class GenericErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        if hasattr(ctx.command, 'on_error'):
            return

        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Command not found')

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing argument')

        elif isinstance(error, commands.UserInputError):
            await ctx.send('There was a unknown problem with your command')

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.BadArgument):
            await ctx.send('Bad argument')
        else:
            await ctx.send('Unexpected error. Probably not your fault')
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            return

        return await ctx.send('Check usage with !help command')