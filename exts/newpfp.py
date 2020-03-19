from discord.ext import commands

from mods import firestore, info, vars_
from mods.core import get_cat_link
from mods.core import change_avatar


@commands.command()
async def newpfp(ctx, arg='random'):
    if ctx.author.bot:
        return

    async with ctx.typing():

        uid = str(ctx.author.id)
        user_ = await firestore.get_user(uid)
        if arg in ['last', '^', '_']:
            arg = (await firestore.get_command(uid, 'meow'))['_last']

        if user_['self']:
            # handle self-hosting here
            await firestore.update_command(uid, 'newpfp', 'link_', await get_cat_link())
            await ctx.send("I told your client to update your avatar")
            return

        result = await _new_avatar(ctx, user_, arg)
        await ctx.send(result)


@newpfp.error
async def newpfp_error(ctx, err):
    await ctx.send(err)


async def _new_avatar(ctx, user_: dict, arg):
    if arg[-3:] in ['jpg', 'png']:
        img_link = arg
    elif len(ctx.message.attachments) == 1:
        img_link = ctx.message.attachments[0].url
    elif arg == 'random':
        img_link = await get_cat_link()
    else:
        result = 'Are you sure you called the command correctly?'
        return result
    # print(img_link)
    result = await change_avatar(user_, img_link)
    return result


def setup(bot):
    info.Info(
        name='newpfp',
        brief='changes your avatar to a random cat',
        description='use `settings newpfp timer <minutes>` to set a timer',
        usage='`newpfp [last|^|_]`',
        settings={
            'timer': int,
            'enabled': None,
        },
        defaults={
            'timer': 0,  # off,
            'enabled': True,
        }
    ).export(vars_.info_)

    bot.add_command(newpfp)
