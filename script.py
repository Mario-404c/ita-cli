from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint
import questionary
import requests
import re
from bs4 import BeautifulSoup
import subprocess

HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

def cerca():
    risultati = []
    link_risultati = []

    nome = input("Inserisci il nome dell'anime: ")
    nome = nome.replace(" ", "%20")
    ricerca = f"https://www.animesaturn.cx/animelist?search={nome}"
    risposta = requests.get(
        ricerca,
        headers=HEADERS
    )
    
    soup = BeautifulSoup(risposta.text, "html.parser")

    link = soup.find_all("a", href=True)
    for l in link:
        if "/anime/" in l["href"]:
            if l["href"].startswith("https://"):
                if(len(l.text.strip()) != 0 and len(l.text.strip()) < 100):
                    risultati.append(l.text.strip())
                    link_risultati.append(l["href"])
                
    return risultati, link_risultati

def seleziona_episodio(link):
    risultati = []
    link_risultati = []
    
    risposta = requests.get(
    link,
    headers=HEADERS
    )

    soup = BeautifulSoup(risposta.text, "html.parser")

    link = soup.find_all("a", href=True)
    for l in link:
        if "/ep/" in l["href"]:
            risultati.append(l.text.strip())
            link_risultati.append(l["href"])
    return risultati, link_risultati

def trova_link(link):
    
    risposta = requests.get(
    link,
    headers=HEADERS
    )

    soup = BeautifulSoup(risposta.text, "html.parser")

    link = soup.find_all("a", href=True)
    for l in link:
        if "Guarda lo streaming" in l.text:
            risultato = (l["href"])
            
    r = requests.get(risultato, headers=HEADERS)
    html = r.text

    match = re.search(r'https?://[^\s\'"<>]+\.mp4[^\s\'"<>]*', html)
    if match:
        return match.group(0)
    else:
        rprint("[bold red]Errore[/bold red]")
    
    

console = Console()

while True:
    console.print(Panel("[bold cyan]ita-ani-cli[/bold cyan]", border_style="cyan", title="v1.0"))

    s = questionary.select(
        "Cosa vuoi fare?",
        choices=["Guarda", "Scarica", "Impostazioni", "Esci"]
    ).ask()

    match s:
        case "Guarda":
            lista_anime = []
            link_anime = []
            lista_ep = []
            link_ep = []
            
            lista_anime, link_anime = cerca()
            
            if not lista_anime:
                rprint("[bold red]La ricerca non ha prodotto nessun risultato![/bold red]")
            else:
                scelta = questionary.select(
                        "Seleziona uno dei titoli disponibili:",
                        choices=lista_anime
                    ).ask()
                
                lista_ep, link_ep = seleziona_episodio(link_anime[lista_anime.index(scelta)]) #Link dell'anime in base allo stesso index della scelta per lista_anime
                
                scelta = questionary.select(
                        "Seleziona un episodio: ",
                        choices=lista_ep
                    ).ask()
                
                link = trova_link(link_ep[lista_ep.index(scelta)]) #Link dell'episodio in base allo stesso index della scelta per lista_ep
                
                scelta = questionary.select(
                        "Scegli un player: ",
                        choices=["mpv", "ffplay"]
                    ).ask()

                if(scelta == "mpv"):
                    subprocess.run(["mpv.exe", link])
                else:
                    subprocess.run(["ffplay", link])
            
        case "Scarica":
            rprint("Funzione non aggiunta")
        case "Esci":
            rprint("Arrivederci!")
            break
        case _:
            rprint("[bold red]Errore[/bold red]") 