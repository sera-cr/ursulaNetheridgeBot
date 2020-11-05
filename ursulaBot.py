# ursulaBot.py
import os
import random
from asyncio import sleep
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='-!',
                   description='Ursula Netheridge, Guardiana del Umbral de la Torre de ébano, asistente de la '
                               'VII Jornada de Rol Inf. Uma a tu disposición para ayudarte en lo que necesites',
                   intents=intents)
bot.remove_command('help')


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    guilds = '\n - '.join([g.name for g in bot.guilds])
    members = '\n - '.join([member.name for member in guild.members])
    print(
        f'{bot.user.name} se ha conectado a Discord!\n'
        f'Se ha conectado a los siguientes servidores:\n {guilds}\n'
        f'Miembros del Servidor:\n - {members}'
    )
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='-!ayuda'))


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'*Tras un largo camino entre la niebla, esta empieza a disiparse, una enorme estructura permanece ante ti.'
        f' Una puerta doble de ébano de grandes dimensiones se situa en tu campo de visión. Decides abrir las puertas. '
        f' Detrás de estas, un recibidor de granito de dimensiones ciclópeas.'
        f' La niebla cubre la visión completamente del suelo, y una figura se te acerca...*\n'
        f'*"Saludos Caminante de la Bruma. Soy Ursula Netheridge, Guardiana del Umbral de la Torre de Ébano.'
        f' Y te guiaré por tu estancia en el interior. Acompáñame, y veremos también cúal es tu camino...."*'
    )
    await member.create_dm()
    await member.dm_channel.send(
        f'¡Bienvenido a la VII Jornada de Rol Inf. Uma! Soy la asistente del evento y te ayudaré en proporcionarte'
        f' la información sobre este.'
        f'Esta jornada se realizará completamente online en este servidor.'
        f'Se te proporcionarán roles según tu partida y tus funciones dentro del servidor lo más rápido posible,'
        f' para que puedas comunicarte con el resto de asistentes del evento, además de tus compañeros de partida y '
        f'el Director de Juego de esta.\n'
        f'Por favor, lee el mensaje en el tablón de bienvenida del servidor. Se respetuoso, y si tienes alguna duda, '
        f'sugerencia, etc.'
        f' no dudes en preguntar al Staff, o incluso a mi con el comando -!ayuda y quizá tenga la respuesta a tus '
        f'preguntas.\n'
        f' Y ahora, ¡entra dentro de la Torre de Ébano (VII Jornada de Rol Inf. Uma) y disfruta de las jornadas! '
        f':dash: :dash: '
    )
    member_join_quotes = [
        f'¡{member.mention} ha cruzado la niebla y se encuentra con nosotros! :crossed_swords:.',
        f'{member.mention} ha llegado a la Torre de Ébano. :shield:.',
        f'Bienvenido a la Torre de Ébano, {member.mention} :crossed_swords:.',
        f'Un nuevo Caminante de la Bruma se une a nuestro encuentro, {member.mention} :shield:.',
        f'La niebla trae a un nuevo miembro, {member.mention} :dash:.',
        f'{member.mention}, te doy la bienvenida a la Torre de Ébano. :dash:.',
        f'¡Caminantes de la Bruma!¡Un nuevo miembro se une a la Torre de Ébano! {member.mention}',
        f'Os presento a un nuevo Caminante de la Bruma, {member.mention} :dash:.'
    ]
    server = bot.guilds[0]
    channel = discord.utils.get(server.channels, name='general')
    async with channel.typing():
        await sleep(0.30)
        response = random.choice(member_join_quotes)
        await channel.send(response)

    guild = discord.utils.get(bot.guilds, name=GUILD)
    role = discord.utils.get(guild.roles, name='Caminante de la bruma')
    await discord.Member.add_roles(member, role)


@bot.command(name='saludar')
async def saludar(ctx):
    greetings_quotes = [
        f'{ctx.message.author.mention} Saludos.',
        f'{ctx.message.author.mention} ¿Qué tal?',
        f'{ctx.message.author.mention} ¿Cómo va el día?',
        f'{ctx.message.author.mention} ¿Necesitas algo?',
        f'{ctx.message.author.mention} ¿Todo bien?',
        f'{ctx.message.author.mention} Espero que disfrutes de tu estancia aquí'
    ]
    response = random.choice(greetings_quotes)
    await ctx.send(response)


@bot.command(name='ayuda')
async def ayuda(ctx):
    embed = discord.Embed(color=discord.Color.dark_gray(), timestamp=ctx.message.created_at)

    embed.set_author(name='¿Qué deseas, Caminante?')
    embed.add_field(name='-!saludar',
                    value='Me saludas.', inline=False)
    embed.add_field(name='-!fecha',
                    value='La fecha del evento y las partidas.', inline=False)
    embed.add_field(name='-!masters',
                    value='La lista de todos los masters y sus partidas.', inline=False)
    embed.add_field(name='-!sinopsis',
                    value='La carpeta con las sinopsis de las partidas.', inline=False)
    embed.add_field(name='-!duracion',
                    value='La duración e inicio de las partidas.', inline=False)

    await ctx.send(embed=embed)


@bot.command(name='fecha')
async def fecha(ctx):
    response = f'{ctx.message.author.mention} La VII Jornada de Rol Inf. Uma ' \
               f'se realizará el Jueves 5 y Viernes 6 de Noviembre. \n' \
               f'Las partidas son:\n' \
               f'    - Jueves 5: Hijo Rata - NSD20\n' \
               f'    - Jueves 5: Dead Girls Tell no Tales - FATE\n' \
               f'    - Jueves 5: Una Cuestión de Honor - Shadowshot Narrativo\n' \
               f'    - Viernes 6: Huellas Inmutables - Offworlders\n' \
               f'    - Viernes 6: Un Sendero Blanco - 1800: El Ocaso de la Humanidad\n' \
               f'    - Viernes 6: El Cumpleaños de la Emperatriz - Anima\n'

    await ctx.send(response)


@bot.command(name='masters')
async def masters(ctx):
    shafledome_id = '<@256834615661166602>'
    mogu_id = '<@137194784040157184>'
    elsyor_id = '<@478513560855773185>'
    david_id = '<@209928730582188043>'
    koboldID = '<@277469785418235906>'
    bardolimo_id = '<@365901196122390529>'
    response = f'{ctx.message.author.mention} Los masters son los siguientes:\n' \
               f'    Hijo Rata - NSD20: {bardolimo_id}\n' \
               f'    Dead Girls Tell no Tales - FATE: {koboldID}\n' \
               f'    Una Cuestión de Honor - Shadowshot Narrativo: {mogu_id}\n' \
               f'    Huellas Inmutables - Offworlders: {elsyor_id}\n' \
               f'    Un Sendero Blanco - 1800: El Ocaso de la Narrativa: {shafledome_id}\n' \
               f'    El Cumpleaños de la Emperatriz: Anima: {david_id}\n'

    await ctx.send(response)


@bot.command(name='sinopsis')
async def sinopsis(ctx):
    response = f'{ctx.message.author.mention} En esta carpeta se encuentran todas las sinopsis:\n' \
               f'http://u.uma.es/Hv/ \n' \
               f'    Hijo Rata - NSD20 (terror): http://u.uma.es/J0/ \n' \
               f'    Dead Girls Tell no Tales - Fate (misterio/investigación): http://u.uma.es/J1/ \n' \
               f'    Una Cuestión de Honor - Shadowshot narrativo (japón feudal): http://u.uma.es/J2/ \n' \
               f'    Huellas Inmutables - Offworlders (ciencia ficción/western): http://u.uma.es/J3/ \n' \
               f'    Un Sendero Blanco - 1800: El Ocaso de la Humanidad (fantasía oscura/steampunk):' \
               f' http://u.uma.es/J4/\n' \
               f'    El Cumpleaños de la Emperatriz - Anima (fantasía): http://u.uma.es/J5/ \n'
    await ctx.send(response)


@bot.command(name='duracion')
async def duracion(ctx):
    response = f'{ctx.message.author.mention} Las partidas comienzan a las 16:30 y terminan a las 20:30, ' \
               f'pero debido a que en esta jornada se realizan en el servidor, pueden llegar a extenderse más ' \
               f'de la hora. Luego la duración es mínima de 4h.'

    await ctx.send(response)


bot.run(TOKEN)
