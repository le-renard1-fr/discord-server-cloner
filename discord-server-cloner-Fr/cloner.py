import discord
import asyncio
import random
import requests
import time
from colorama import Fore, init, Style


class Clone:
    @staticmethod
    async def roles_delete(guild_to: discord.Guild):
        for role in guild_to.roles:
            try:
                if role.name != "@everyone":
                    await role.delete()
                    print_delete(
                        f"Le rôle {Fore.YELLOW}{role.name}{Fore.BLUE} a été supprimé"
                    )
                    await asyncio.sleep(random.randint(0.15, 0.10))
            except discord.Forbidden:
                print_error(
                    f"Erreur lors de la suppression du rôle : {Fore.YELLOW}{role.name}{Fore.RED} Permissions insuffisantes.{Fore.RESET}"
                )

            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(
                        f"Trop de requêtes effectuées. Attente de 60 secondes. Détails : {e}"
                    )
                    await asyncio.sleep(60)

    @staticmethod
    async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
        roles = []
        role: discord.Role
        for role in guild_from.roles:
            if role.name != "@everyone":
                roles.append(role)
        roles = roles[::-1]
        for role in roles:
            try:
                await guild_to.create_role(name=role.name,
                                           permissions=role.permissions,
                                           colour=role.colour,
                                           hoist=role.hoist,
                                           mentionable=role.mentionable)
                print_add(
                    f"Le rôle {Fore.YELLOW}{role.name}{Fore.BLUE} a été créé")
                await asyncio.sleep(random.uniform(0.3, 0.6))
            except discord.Forbidden:
                print_error(
                    f"Erreur lors de la création du rôle : {Fore.YELLOW}{role.name}{Fore.RED} Permissions insuffisantes.{Fore.RESET}"
                )
                await asyncio.sleep(random.randint(0.20, 0.40))
            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(
                        f"Trop de requêtes effectuées. Attente de 60 secondes. Détails : {e}"
                    )
                    await asyncio.sleep(60)

    @staticmethod
    async def channels_delete(guild_to: discord.Guild):
        for channel in guild_to.channels:
            try:
                await channel.delete()
                print_delete(
                    f"La catégorie {Fore.YELLOW}{channel.name}{Fore.BLUE} a été supprimée"
                )
                await asyncio.sleep(0.20)
            except discord.Forbidden:
                print_error(
                    f"Erreur lors de la suppression de la catégorie : {Fore.YELLOW}{channel.name}{Fore.RED} Permissions insuffisantes.{Fore.RESET}"
                )
                await asyncio.sleep(random.randint(2, 3))
            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(
                        f"Trop de requêtes effectuées. Attente de 60 secondes. Détails : {e}"
                    )
                    await asyncio.sleep(60)
            except:
                print_error(
                    f"Impossible de supprimer le canal {Fore.YELLOW}{channel.name}{Fore.RED} Erreur non identifiée"
                )
                await asyncio.sleep(random.randint(9, 12))

    @staticmethod
    async def categories_create(guild_to: discord.Guild,
                                guild_from: discord.Guild):
        channels = guild_from.categories
        channel: discord.CategoryChannel
        new_channel: discord.CategoryChannel
        for channel in channels:
            try:
                overwrites_to = {}
                for key, value in channel.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                new_channel = await guild_to.create_category(
                    name=channel.name, overwrites=overwrites_to)
                await new_channel.edit(position=channel.position)
                print_add(
                    f"La catégorie {Fore.YELLOW}{channel.name}{Fore.BLUE} a été créée"
                )
                await asyncio.sleep(random.randint(1, 3))
            except discord.Forbidden:
                print_error(
                    f"Erreur lors de la création de la catégorie : {Fore.YELLOW}{channel.name}{Fore.RED} Permissions insuffisantes.{Fore.RESET}"
                )
                await asyncio.sleep(random.randint(2, 3))
            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(
                        f"Trop de requêtes effectuées. Attente de 60 secondes. Détails : {e}"
                    )
                    await asyncio.sleep(60)
            except:
                print_error(
                    f"Impossible de créer la catégorie {Fore.YELLOW}{channel.name}{Fore.RED} Erreur non identifiée"
                )
                await asyncio.sleep(random.randint(9, 12))

    @staticmethod
    async def channels_create(guild_to: discord.Guild,
                              guild_from: discord.Guild):
        channel_text: discord.TextChannel
        channel_voice: discord.VoiceChannel
        category = None
        for channel_text in guild_from.text_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_text.category.name:
                            break
                    except AttributeError:
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_text.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position,
                        topic=channel_text.topic,
                        slowmode_delay=channel_text.slowmode_delay,
                        nsfw=channel_text.nsfw)
                except:
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_add(
                    f"Le canal texte {Fore.YELLOW}{channel_text.name}{Fore.BLUE} a été créé"
                )
                await asyncio.sleep(0.59)
            except discord.Forbidden:
                print_error(
                    f"Erreur lors de la création du canal texte : {channel_text.name}"
                )
                await asyncio.sleep(random.randint(8, 10))
            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(
                        f"Trop de requêtes effectuées. Attente de 60 secondes. Détails : {e}"
                    )
                    await asyncio.sleep(60)
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_add(
                    f"Le canal {Fore.YELLOW}{channel_text.name}{Fore.BLUE} a été créé"
                )
            except:
                print_error(
                    f"Erreur lors de la création du canal texte : {channel_text.name}"
                )
                await asyncio.sleep(random.randint(9, 12))

        category = None
        for channel_voice in guild_from.voice_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_voice.category.name:
                            break
                    except AttributeError:
                        print_warning(
                            f"Le canal vocal {channel_voice.name} n'a pas de catégorie !"
                        )
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_voice.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position,
                        bitrate=channel_voice.bitrate,
                        user_limit=channel_voice.user_limit,
                    )
                except:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_add(
                    f"Le canal vocal {Fore.YELLOW}{channel_voice.name}{Fore.BLUE} a été créé"
                )
                await asyncio.sleep(0.48)
            except discord.Forbidden:
                print_error(
                    f"Erreur lors de la création du canal vocal : {channel_voice.name}"
                )
                await asyncio.sleep(random.randint(6, 7))
            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(
                        f"Trop de requêtes effectuées. Attente de 60 secondes. Détails : {e}"
                    )
                    await asyncio.sleep(60)
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_add(
                    f"Le canal vocal {Fore.YELLOW}{channel_voice.name}{Fore.BLUE} a été créé"
                )
            except:
                print_error(
                    f"Erreur lors de la création du canal vocal : {channel_voice.name}"
                )

    @staticmethod
    async def emojis_create(guild_to: discord.Guild,
                            guild_from: discord.Guild):
        emojis = guild_from.emojis
        if not emojis:
            print_warning("Aucun emoji trouvé.")
            return
        for emoji in guild_from.emojis:
            try:
                emoji_image = await emoji.url.read()
                await guild_to.create_custom_emoji(
                    name=emoji.name, image=emoji_image)
                print_add(f"L'emoji {Fore.YELLOW}{emoji.name}{Fore.BLUE} a été créé")
                await asyncio.sleep(0.15)
            except discord.Forbidden:
                print_error(
                    f"Erreur lors de la création de l'emoji : {Fore.YELLOW}{emoji.name}{Fore.RED} Permissions insuffisantes.{Fore.RESET}"
                )
                await asyncio.sleep(random.randint(3, 5))
            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(
                        f"Trop de requêtes effectuées. Attente de 60 secondes. Détails : {e}"
                    )
                    await asyncio.sleep(60)
            except:
                print_error(
                    f"Erreur non identifiée lors de la création de l'emoji {Fore.YELLOW}{emoji.name}{Fore.RED}."
                )
                await asyncio.sleep(random.randint(3, 5))

    @staticmethod
    async def stickers_create(guild_to: discord.Guild,
                              guild_from: discord.Guild):
        stickers = guild_from.stickers
        if not stickers:
            print_warning("Aucun sticker trouvé.")
            return
        for sticker in stickers:
            try:
                sticker_image = await sticker.asset.read()
                await guild_to.create_custom_sticker(
                    name=sticker.name, image=sticker_image,
                    description=sticker.description,
                    tags=sticker.tags)
                print_add(f"Le sticker {Fore.YELLOW}{sticker.name}{Fore.BLUE} a été créé")
                await asyncio.sleep(0.20)
            except discord.Forbidden:
                print_error(
                    f"Erreur lors de la création du sticker : {Fore.YELLOW}{sticker.name}{Fore.RED} Permissions insuffisantes.{Fore.RESET}"
                )
                await asyncio.sleep(random.randint(2, 3))
            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(
                        f"Trop de requêtes effectuées. Attente de 60 secondes. Détails : {e}"
                    )
                    await asyncio.sleep(60)
            except:
                print_error(
                    f"Erreur non identifiée lors de la création du sticker {Fore.YELLOW}{sticker.name}{Fore.RED}."
                )
                await asyncio.sleep(random.randint(3, 5))
