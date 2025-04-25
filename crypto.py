import subprocess
from rich.console import Console
from rich.table import Table
import pyfiglet
import os
import sys

console = Console()

def fichier_existe(fichier):
    return os.path.isfile(fichier)

def afficher_menu():
    """Affiche le menu principal avec style ASCII et tableau"""
    title = pyfiglet.figlet_format("Outil de\nCryptographie")
    console.print(f"[bold cyan]{title}[/bold cyan]")

    table = Table(title="[italic bold]Menu Principal[/italic bold]", show_header=True, header_style="bold magenta")
    table.add_column("Option", justify="center", style="cyan", no_wrap=True)
    table.add_column("Description", style="bold yellow")

    options = [
        ("1", "Génération de clé privée (RSA)"),
        ("2", "Chiffrement d'une clé privée (AES/3DES)"),
        ("3", "Génération de clé publique (RSA)"),
        ("4", "Chiffrement de données (RSA/AES/3DES)"),
        ("5", "Déchiffrement de données (RSA/AES/3DES)"),
        ("6", "Calcul d'empreinte (MD5)"),
        ("7", "Signature d'empreinte (RSA)"),
        ("8", "Vérification de signature (RSA)"),
        ("99", "Quitter"),
    ]

    for opt, desc in options:
        table.add_row(opt, desc)

    console.print(table)

def executer_commande(cmd):
    """Exécute une commande shell et gère les erreurs"""
    try:
        subprocess.run(cmd, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Erreur OpenSSL : {e}[/red]")
    except FileNotFoundError:
        console.print("[red]Erreur : fichier introuvable.[/red]")

def gen_cle_pri():
    try:
        console.print("\n[bold yellow]Génération de clé privée[/bold yellow]")
        file_name = input("Nom de la clé privée : ").strip()

        if not file_name:
            console.print("[red]Nom invalide.[/red]")
            return

        # Construction de la commande OpenSSL
        cmd = f"openssl genpkey -algorithm RSA -out {file_name} -pkeyopt rsa_keygen_bits:2048"
        executer_commande(cmd)

        if fichier_existe(file_name):
            console.print(f"[green]{file_name} créé avec succès ![/green]")
        else:
            console.print(f"[red]Échec de la création de {file_name}.[/red]")

    except KeyboardInterrupt:
        console.print("\n[red]Opération annulée par l'utilisateur.[/red]")
    except Exception as e:
        console.print(f"[red]Une erreur est survenue : {e}[/red]")

def chif_cle():
    try:
        console.print("\n[bold yellow]Chiffrement de clé privée[/bold yellow]")
        
        file_in = input("Nom de la clé à chiffrer : ").strip()
        if not fichier_existe(file_in):
            console.print("[red]Fichier introuvable.[/red]")
            return

        file_out = input("Nom du clé chiffré en sortie : ").strip()
        if not file_out:
            console.print("[red]Nom de la clé invalide.[/red]")
            return

        algo = input("Algorithme (aes256, des3) : ").lower().strip()
        if algo not in ["aes256", "des3"]:
            console.print("[red]Algorithme non supporté. Utilisez aes256 ou des3.[/red]")
            return

        cmd = f"openssl pkey -in {file_in} -{algo} -out {file_out}"
        executer_commande(cmd)

        if fichier_existe(file_out):
            console.print("[green]Clé chiffrée avec succès![/green]")
        else:
            console.print("[red]Échec du chiffrement.[/red]")

    except KeyboardInterrupt:
        console.print("\n[red]Opération annulée par l'utilisateur.[/red]")
    except Exception as e:
        console.print(f"[red]Erreur inattendue : {e}[/red]")

def gen_cle_pub():
    try:
        console.print("\n[bold yellow]Génération de clé public[/bold yellow]")
        file_in = input("Entrer la clé privé : ").strip()

        if not fichier_existe(file_in):
            console.print("[red]Clé privée introuvable.[/red]")
            return
        
        file_out = input("Nom de la clé publique : ").strip()

        if not file_in:
            console.print("[red]Nom invalide.[/red]")
            return
        
        # Construction de la commande OpenSSL
        cmd = f"openssl pkey -in {file_in} -pubout -out {file_out}"
        executer_commande(cmd)

        if fichier_existe(file_in):
            console.print(f"[green]{file_in} créé avec succès![/green]")
        else:
            console.print(f"[red]Échec de la création du fichier {file_in}.[/red]")

    except KeyboardInterrupt:
        console.print("\n[red]Opération annulée par l'utilisateur.[/red]")
    except Exception as e:
        console.print(f"[red]Une erreur est survenue : {e}[/red]")

def chif_d():
    try:
        console.print("\n[bold yellow]Chiffrement de données[/bold yellow]")
        file_in = input("Etrer le fichier à chiffrer : ").strip()

        if not fichier_existe(file_in):
            console.print("[red]Fichier introuvable.[/red]")
            return
        
        file_out = input("Nom du fichier chiffré : ").strip()

        if not file_out:
            console.print("[red]Nom du fichier invalide.[/red]")
            return
        
        algo = input("algorithme de chiffrement (aes256, des3) ou clé de chiffrement (cle) : ").lower().strip()

        if algo == "cle":
            cle_priv = input("Etrer la clé privé pour le chiffrement : ")
            if not fichier_existe(cle_priv):
                return console.print("[red]Clé privé introuvable.[/red]")

            cmd = f"openssl pkeyutl -encrypt -in {file_in} -inkey {cle_priv} -out {file_out}"

        elif algo in ["aes256", "des3"]:
            if algo == "aes256":
                cmd = f"openssl enc -aes-256-cbc -pbkdf2 -in {file_in} -out {file_out}"
            elif algo == "des3":
                cmd = f"openssl enc -des-ede3-cbc -pbkdf2 -in {file_in} -out {file_out}"
        else:
            console.print("[red]Algorithme non supporté.[/red]")
            return

        executer_commande(cmd)
        console.print("[green]Données chiffrées avec succès![/green]")

    except KeyboardInterrupt:
        console.print("\n[red]Opération annulée par l'utilisateur.[/red]")
    except Exception as e:
        console.print(f"[red]Erreur inattendue : {e}[/red]") 

def dechif_d():
    try:
        console.print("\n[bold yellow]Déchiffrement de données[/bold yellow]")
        file_in = input("Entrer le fichier à déchiffré : ")
        if not fichier_existe(file_in):
            return console.print("[red]Fichier introuvable.[/red]")
        
        file_out = input("Nom du fichier déchiffré : ").strip()
        if not file_out:
            console.print("[red]Nom du fichier invalide.[/red]")
            return
        
        algo = input("algorithme de dechiffrement (aes256, des3) ou clé de dechiffrement (cle) : ").lower().strip()

        if algo == "cle":
            cle_priv = input("Entrer la clé privé pour le dechiffrement : ")
            if not fichier_existe(cle_priv):
                return console.print("[red]Clé privé introuvable.[/red]")

            cmd = f"openssl pkeyutl -decrypt -in {file_in} -inkey {cle_priv} -out {file_out}"

        elif algo in ["aes256", "des3"]:
            if algo == "aes256":
                cmd = f"openssl enc -d -aes-256-cbc -pbkdf2 -in {file_in} -out {file_out}"
            elif algo == "des3":
                cmd = f"openssl enc -d -des-ede3-cbc -pbkdf2 -in {file_in} -out {file_out}"
        else:
            console.print("[red]Algorithme non supporté.[/red]")
            return

        executer_commande(cmd)
        console.print("[green]Données déchiffrées avec succès![/green]")

    except KeyboardInterrupt:
        console.print("\n[red]Opération annulée par l'utilisateur.[/red]")
    except Exception as e:
        console.print(f"[red]Erreur inattendue : {e}[/red]") 

def cal_em():
    try:
        console.print("\n[bold yellow]Calcul d'empreinte[/bold yellow]")
        algo = input("Entrer une fonction de hashage (md5) : ").lower().strip()

        file_in = input("Entrer le fichier à hacher : ").strip()
        if not fichier_existe(file_in):
            return console.print("[red]Fichier introuvable.[/red]")
        
        empreinte = input("Etrer le nom de l'empreinte : ").strip()
        if not empreinte:
            console.print("[red]Nom de l'empreinte invalide.[/red]")
            return
        
        if algo in ["md5", "sha256"]:
            cmd = f"openssl dgst -{algo} -out {empreinte} {file_in}"

            executer_commande(cmd)
            console.print("[green]Empreinte générée avec succès![/green]")
        
        else:
            console.print("[green]Algorythme introuvable.[/green]")
            return

    except KeyboardInterrupt:
        console.print("\n[red]Opération annulée par l'utilisateur.[/red]")
    except Exception as e:
        console.print(f"[red]Erreur inattendue : {e}[/red]")

def sign_em():
    try:
        console.print("\n[bold yellow]Signature d'empreinte[/bold yellow]")
        file_in = input("Entrer l'empreinte à signer : ").strip()
        if not fichier_existe(file_in):
            return console.print("[red]Empreinte introuvable.[/red]")
        
        cle_pri = input("Entrer la clé privée : ").strip()
        if not fichier_existe(cle_pri):
            return console.print("[red]Clé privée introuvable.[/red]")
        
        sig_out = input("Etrer le nom de la signature : ").strip()
        if not sig_out:
            console.print("[red]Nom de la signature invalide.[/red]")
            return
        
        cmd = f"openssl pkeyutl -sign -in {file_in} -inkey {cle_pri} -out {sig_out}"
        
        executer_commande(cmd)
        console.print("[green]Signature créée avec succès![/green]")

    except KeyboardInterrupt:
        console.print("\n[red]Opération annulée par l'utilisateur.[/red]")
    except Exception as e:
        console.print(f"[red]Erreur inattendue : {e}[/red]")

def ver_sign():
    try:
        console.print("\n[bold yellow]Vérification de signature[/bold yellow]")
        file_out = input("Entrer le nom de l'empreinte : ").strip()
        if fichier_existe(file_out):
            console.print("[red]Nom d'empreinte déjà existante.[/red]")
            return
        elif not file_out:
            return console.print("[red]Nom de l'empreinte invalide.[/red]")
        
        signature = input("Entrer la signature : ").strip()
        if not fichier_existe(signature):
            return console.print("[red]Signature introuvable.[/red]")
        
        cle_pub = input("Entrer la clé publique : ").strip()
        if not fichier_existe(cle_pub):
            return console.print("[red]Clé publique introuvable.[/red]")

        cmd = f"openssl rsautl -verify -in {signature} -pubin -inkey {cle_pub} -out {file_out}"
        executer_commande(cmd)

        console.print(f"[green]{file_out} crée![/green]")

    except KeyboardInterrupt:
        console.print("\n[red]Opération annulée par l'utilisateur.[/red]")
    except Exception as e:
        console.print(f"[red]Erreur inattendue : {e}[/red]")

def main():
    try:
        while True:
            afficher_menu()
            try:
                choice = input("Choisir une option : ").strip()
            except (EOFError, KeyboardInterrupt):
                console.print("\n[red]Fermeture de l'application...[/red]")
                break

            match choice:
                case "1": gen_cle_pri()
                case "2": chif_cle()
                case "3": gen_cle_pub()
                case "4": chif_d()
                case "5": dechif_d()
                case "6": cal_em()
                case "7": sign_em()
                case "8": ver_sign()
                case "99": break
                case _: console.print("[red]Option invalide. Veuillez réessayer.[/red]")

    except Exception as e:
        console.print(f"[bold red]Erreur critique : {e}[/bold red]")
    finally:
        console.print("[bold blue]Merci d’avoir utilisé l’outil de cryptographie.[/bold blue]")

if __name__ == "__main__":
    main()
