from os import system
import psutil
import os
from pypresence import Presence
import time
import sys
import discord
import subprocess
import json
from rich.table import Table
from rich.console import Console
from rich.style import Style
from rich.panel import Panel as RichPanel
from rich.text import Text
import asyncio
import colorama
from colorama import Fore, init, Style
import platform
import inquirer
from cloner import Clone

version = '0.3'
clones = {'Clones_tests_effectues': 0}
version_python = sys.version.split()[0]

console = Console()


def nettoyer_tout():
    system('cls')
    print(f"""{Style.BRIGHT}{Fore.RED}
           __                                                   
          /  |                                                  
  _______ $$ |  ______   _______    ______   __    __   ______  
 /       |$$ | /      \ /       \  /      \ /  |  /  | /      \ 
/$$$$$$$/ $$ |/$$$$$$  |$$$$$$$  |/$$$$$$  |$$ |  $$ |/$$$$$$  |
$$ |      $$ |$$ |  $$ |$$ |  $$ |$$    $$ |$$ |  $$ |$$ |  $$/ 
$$ \_____ $$ |$$ \__$$ |$$ |  $$ |$$$$$$$$/ $$ \__$$ |$$ |      
$$       |$$ |$$    $$/ $$ |  $$ |$$       |$$    $$/ $$ |      
 $$$$$$$/ $$/  $$$$$$/  $$/   $$/  $$$$$$$/  $$$$$$/  $$/       
{Style.RESET_ALL}{Fore.WHITE}{Fore.RESET}""")


client = discord.Client()
if os == "Windows":
    system("cls")
else:
    print(chr(27) + "[2J")
    nettoyer_tout()
while True:
    token = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Entrez votre jeton pour continuer{Style.RESET_ALL}{Fore.RESET}\n >'
    )
    serveur_source_id = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Entrez l\'ID du serveur que vous souhaitez cloner{Style.RESET_ALL}{Fore.RESET}\n >'
    )
    serveur_destination_id = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Entrez l\'ID du serveur de destination pour coller le serveur cloné{Style.RESET_ALL}{Fore.RESET}\n>'
    )
    nettoyer_tout()
    print(f'{Style.BRIGHT}{Fore.GREEN}Les valeurs saisies sont :')
    print(
        f'{Style.BRIGHT}{Fore.GREEN}Votre jeton : {Fore.YELLOW}{token}{Style.RESET_ALL}{Fore.RESET}'
    )
    print(
        f'{Style.BRIGHT}{Fore.GREEN}ID du serveur à cloner : {Fore.YELLOW}{serveur_source_id}{Style.RESET_ALL}{Fore.RESET}'
    )
    print(
        f'{Style.BRIGHT}{Fore.GREEN}ID du serveur de destination : {Fore.YELLOW}{serveur_destination_id}{Style.RESET_ALL}{Fore.RESET}'
    )
    confirmation = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Les valeurs sont-elles correctes ? {Fore.YELLOW}(O/N){Style.RESET_ALL}{Fore.RESET}\n >'
    )
    if confirmation.upper() == 'O':
        if not serveur_source_id.isnumeric():
            nettoyer_tout()
            print(
                f'{Style.BRIGHT}{Fore.RED}L\'ID du serveur à cloner ne doit contenir que des chiffres.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        if not serveur_destination_id.isnumeric():
            nettoyer_tout()
            print(
                f'{Style.BRIGHT}{Fore.RED}L\'ID du serveur de destination doit contenir que des chiffres.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        if not token.strip() or not serveur_source_id.strip() or not serveur_destination_id.strip():
            nettoyer_tout()
            print(
                f'{Style.BRIGHT}{Fore.RED}Un ou plusieurs champs sont vides.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        if len(token.strip()) < 3 or len(serveur_source_id.strip()) < 3 or len(
                serveur_destination_id.strip()) < 3:
            nettoyer_tout()
            print(
                f'{Style.BRIGHT}{Fore.RED}Un ou plusieurs champs contiennent moins de 3 caractères.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        break

    elif confirmation.upper() == 'N':
        nettoyer_tout()
else:
    nettoyer_tout()
    print(
        f'{Style.BRIGHT}{Fore.RED}Option invalide. Veuillez entrer O ou N.{Style.RESET_ALL}{Fore.RESET}'
    )
input_serveur_source_id = serveur_source_id
input_serveur_destination_id = serveur_destination_id
token = token
nettoyer_tout()


@client.event
async def on_ready():
    try:
        heure_de_debut = time.time()
        global clones
        tableau = Table(title="Versions", style="bold magenta")
        tableau.add_column("Composant")
        tableau.add_column("Version")
        tableau.add_row("Cloner", str(version), style="cyan")
        tableau.add_row("Discord.py", str(discord.__version__), style="cyan")
        tableau.add_row("Python", str(version_python), style="cyan")
        console.print(RichPanel(tableau, width=47))
        console.print(
            RichPanel(f" Authentification réussie",
                      style="bold green",
                      width=47))
        console.print(
            RichPanel(
                f" Bonjour, {client.user.name} ! Démarrage du Cloner...",
                style="bold blue",
                width=47))
        print(f"\n")
        questions = [
            inquirer.List(
                'cloner_emojis',
                message="\033[35mSouhaitez-vous cloner les emojis ?\033[0m",
                choices=['\033[32mOui\033[0m', '\033[31mNon\033[0m'],
            ),
        ]
        reponses = inquirer.prompt(questions)
        serveur_source = client.get_guild(int(input_serveur_source_id))
        serveur_destination = client.get_guild(int(input_serveur_destination_id))
        await Clone.guild_edit(serveur_destination, serveur_source)
        await Clone.channels_delete(serveur_destination)
        await Clone.roles_create(serveur_destination, serveur_source)
        await Clone.categories_create(serveur_destination, serveur_source)
        await Clone.channels_create(serveur_destination, serveur_source)
        heure_de_fin = time.time()
        duree = heure_de_fin - heure_de_debut
        duree_str = time.strftime("%M:%S", time.gmtime(duree))
        if reponses['cloner_emojis'] == '\033[32mOui\033[0m':
            print(
                f"{Style.BRIGHT}{Fore.YELLOW}Clonage des emojis en cours. Cela peut prendre un moment."
            )
            await asyncio.sleep(20)
            await Clone.emojis_create(serveur_destination, serveur_source)
            print(
                f"{Style.BRIGHT}{Fore.BLUE}Le serveur a été cloné avec succès en {Fore.YELLOW}{duree_str}{Style.RESET_ALL}"
            )
            print(
                f"{Style.BRIGHT}{Fore.BLUE}Pour plus d'infos, rejoignez notre serveur Discord : {Fore.YELLOW}https://discord.gg/encoders{Style.RESET_ALL}"
            )
            clones['Clones_tests_effectues'] += 1
            with open('saves.json', 'w') as f:
                json.dump(clones, f)
            print(
                f"{Style.BRIGHT}{Fore.BLUE}Fin du processus et fermeture de la session pour le compte {Fore.YELLOW}{client.user}"
            )
            await client.close()  # ferme le programme
    except discord.LoginFailure:
        print(
            "Impossible de s'authentifier au compte. Vérifiez si le jeton est correct."
        )
    except discord.Forbidden:
        print("Impossible de cloner en raison de permissions insuffisantes.")
    except discord.HTTPException:
        print("Une erreur est survenue lors de la communication avec l'API de Discord.")
    except discord.NotFound:
        print(
            "Impossible de trouver un des éléments à copier (canaux, catégories, etc.)."
        )
    except Exception as e:
        print(Fore.RED + "Une erreur est survenue :", e)


try:
    client.run(token, bot=False)
except discord.LoginFailure:
    print(Fore.RED + "Le jeton saisi est invalide")
    print(
        Fore.YELLOW +
        "\n\nLe programme va redémarrer dans 10 secondes. Si vous ne voulez pas attendre, actualisez la page et recommencez."
    )
    print(Style.RESET_ALL)
    time.sleep(10)
    subprocess.Popen(["python", __file__])
    print(Fore.RED + "Redémarrage...")
