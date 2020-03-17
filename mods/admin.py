import importlib
import os


async def reload_all(bot, mods, ignore):
    # load all commands/cogs
    for file in os.listdir('./exts/'):
        if file.endswith('.py') and file not in ignore:
            ext = file.split('.')[0]
            await reload_load(ext, bot=bot)
            print(f"Loaded command: {ext}")
    # load all non-command functions
    for file in os.listdir('./mods/'):
        if file.endswith('.py') and file not in ignore:
            mod = file.split('.')[0]
            mods[mod] = await reload_load(mod, mods=mods)
            print(f"Loaded module: {mod}")
    return 'Reloaded all commands/extensions'


async def reload_load(modext, mods=None, bot=None):
    if mods:  # looking for a module
        if modext in mods:
            mod = await _reload_mod(mods[modext])
            st = f'Reloaded module: **{modext}**'
        else:  # if module is not loaded
            mod = await _load_mod(modext)  # tries to load module
            st = f'Loaded module: **{modext}**'
        return mod, st
    if bot:
        if f'exts.{modext}' in bot.extensions:
            st = await _reload_ext(bot, modext)
        else:
            st = await _load_ext(bot, modext)
        return st
    return 'Must provide either mod or bot'


async def _reload_ext(bot, ext):
    bot.reload_extension(f'exts.{ext}')
    return f'Reloaded extension: **{ext}**'


async def _reload_mod(mod):
    mod = importlib.reload(mod)
    return mod


async def _load_ext(bot, ext):
    bot.load_extension(f'exts.{ext}')
    return f'Loaded extension: **{ext}**'


async def _load_mod(mod):
    mod = importlib.import_module(f'mods.{mod}')
    return mod
