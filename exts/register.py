from discord.ext import commands
from mods import token
from mods import firestore


class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def register(self, ctx):
        if ctx.author.bot:
            return -1

        user = ctx.author
        if token.token_exists(user.id):
            await ctx.send('You\'re already registered, dming you your token')
            user_token = firestore.get_user_token(user.id)
            await user.send(f'Here\'s your token again, don\'t lose it this time! ```{user_token}```\n'
                            f'Did you want to revoke or regenerate your token? Use revoke & refresh')
            # TODO user react to delete message
        else:
            def dm_reply(m):
                return m.guild is None and m.author == user

            await user.send('Hello! Please reply with either the required information or with `self` to self-host\n'
                            'Please start with your token:')
            resp = await self.bot.wait_for('message', timeout=30.0, check=dm_reply)
            if resp.content == 'self':
                custom_token = token.create_custom_token(str(ctx.author.id)).decode('utf-8')
                await user.send('Alright, head here and follow the instructions to get started: '
                                'https://repl.it/@kenhtsun/BraincellBot-Client'
                                'Your unique token is ```{custom_token}```. Keep this token safe!')
                firestore.add_user(user.id, self_hosting=True, token=custom_token)
            else:
                token_ = resp
                await user.send('Now enter your discord email, or react to skip')
                email = await self.bot.wait_for('message', timeout=30.0, check=dm_reply)
                await user.send('And finally your password...')
                pwd = await self.bot.wait_for('message', timeout=30.0, check=dm_reply)
                firestore.add_user(user.id, self_hosting=False, token=token_, email=email, pwd=pwd)
                await user.send('That\'s it! The bot can now change your status and avatar. The default prefix is `b!`')


def setup(bot):
    bot.add_cog(Register(bot))
