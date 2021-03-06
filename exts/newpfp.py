import discord
from discord.ext import commands

from mods import firestore, info, vars_, util
from mods.core import get_cat_link
from mods.core import change_avatar


@commands.command()
async def newpfp(ctx, arg='random'):
    if ctx.author.bot:
        return

    async with ctx.typing():

        uid = str(ctx.author.id)
        user_ = await firestore.get_user(uid)
        attachments = ctx.message.attachments
        embed = discord.Embed(title='Newpfp')
        if attachments and attachments[0].filename.lower().split('.')[-1] in ['png', 'jpg']:
            arg = attachments[0].url
        elif arg in ['last', '^', '_']:
            arg = (await firestore.get_command(uid, 'meow'))['_last']
        elif arg == 'random':
            arg = await get_cat_link()

        if user_['self']:
            # handle self-hosting here
            await firestore.update_command_field(uid, 'newpfp', 'link', arg)
            await util.flash_flag(uid, 'newpfp')
            embed.description = "I've told your slave to update your avatar"
            embed.colour = vars_.colour_success
            await ctx.send(embed=embed)
            return

        result, success = await change_avatar(user_, arg)
        if success:
            embed.colour = vars_.colour_success
        else:
            embed.colour = vars_.colour_error
        embed.description = result
        await ctx.send(embed=embed)


@newpfp.error
async def newpfp_error(ctx, err):
    e = discord.Embed(
        title="Newpfp",
        colour=vars_.colour_error,
        description=err
    ).set_footer(text=vars_.default_footer_text)
    await ctx.send(embed=e)


def setup(bot):
    info.Info(
        name='newpfp',
        brief='changes your avatar to a random cat',
        description='use `settings newpfp timer <minutes>` to set a timer',
        usage='`newpfp [last|^|_]`',
        category='Core',
        settings={
            'timer': 'automatically change your pfp every ... (minutes)',
            'enabled': 'none',
        },
        defaults={
            'timer': 0,  # off,
            'enabled': True,
        }
    ).export(vars_.info_)

    bot.add_command(newpfp)
