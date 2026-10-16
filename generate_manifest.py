"""
Génère manifest.json pour le launcher (v7).

Dossier attendu (à côté de ce script) :
    pack/mods/      -> les .jar des mods
    pack/config/    -> (optionnel) les fichiers de config à imposer aux joueurs

Utilisation : py generate_manifest.py, puis envoie manifest.json et pack/ sur GitHub.
"""
import hashlib
import json
import os
from urllib.parse import quote

# --- Fichiers du pack --------------------------------------------------------
PACK_DIR = "pack"
BASE_URL = "https://raw.githubusercontent.com/Bombureuh/ChillCraft/main/pack"   # sans slash final

# --- Jeu ---------------------------------------------------------------------
MINECRAFT_VERSION = "1.20.1"     # à adapter à ton serveur
LOADER = "forge"                 # "forge", "fabric", "neoforge", "quilt" ou "" (vanilla)
LOADER_VERSION = ""              # vide = dernière version ; mieux vaut fixer celle du serveur

# --- Serveur (modifiable à tout moment sans recréer l'.exe) -------------------
SERVER_NAME = "ChillCraft"
SERVER_IP = "mc304.boxtoplay.com:26840"   # à remplacer par l'adresse réelle, ex. "play.monserveur.fr:25565"

# --- Thème (modifiable à tout moment sans recréer l'.exe) ---------------------
THEME = {
    "launcher_name": "CHILL CRAFT MC",
    "tagline": "Bienvenue sur le serveur",
    "icon": "⛏",
    "bg": "#1e1e1f",
    "panel": "#242425",
    "card": "#313233",
    "accent": "#3c8527",          # vert du bouton JOUER
    "accent_hover": "#4a9e33",
    "text": "#ffffff",
    "muted": "#a0a1a3",
    # Envoie scene_mc.webp et logo_mc.png à la racine de ton dépôt GitHub.
    "background_image": "https://raw.githubusercontent.com/Bombureuh/ChillCraft/main/scene_mc.webp",
    "logo_image": "https://raw.githubusercontent.com/Bombureuh/ChillCraft/main/logo_mc.png",
}

# --- Mise à jour automatique du launcher ---------------------------------------
LAUNCHER_VERSION = "1.3.0"   # doit être la même que LAUNCHER_VERSION dans launcher_v7.py quand tu publies
LAUNCHER_URL = "https://github.com/Bombureuh/ChillCraft/releases/latest/download/ChillCraftLauncher.exe"
LAUNCHER_EXE = os.path.join("dist", "ChillCraftLauncher.exe")   # .exe local, sert à calculer l'empreinte


def sha1_of(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def pack_sha1(path):
    """Empreinte d'un fichier du pack. Les fichiers texte sont comptés avec des fins de ligne LF,
    car Git (GitHub Desktop) convertit CRLF en LF à l'envoi sous Windows."""
    with open(path, "rb") as f:
        data = f.read()
    if b"\x00" not in data[:8000]:
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha1(data).hexdigest()


# Fichiers générés par le jeu (historique, noms de joueurs...) : inutiles à distribuer
EXCLUDE_PREFIXES = ("config/jei/world/", "config/voicechat/username-cache.json")

files = []
for root, _, names in os.walk(PACK_DIR):
    for name in sorted(names):
        full = os.path.join(root, name)
        rel = os.path.relpath(full, PACK_DIR).replace(os.sep, "/")
        if rel.startswith(EXCLUDE_PREFIXES):
            continue
        files.append({"path": rel, "url": f"{BASE_URL}/{quote(rel)}", "sha1": pack_sha1(full)})

manifest = {
    "minecraft": MINECRAFT_VERSION,
    "loader": LOADER,
    "loader_version": LOADER_VERSION,
    "server": {"name": SERVER_NAME, "ip": SERVER_IP},
    "theme": THEME,
    "files": files,
}

if os.path.exists(LAUNCHER_EXE):
    manifest["launcher"] = {"version": LAUNCHER_VERSION, "url": LAUNCHER_URL, "sha1": sha1_of(LAUNCHER_EXE)}
    print(f"Mise à jour du launcher incluse (version {LAUNCHER_VERSION}).")
else:
    print(f"{LAUNCHER_EXE} introuvable : pas de mise à jour du launcher dans ce manifest.")

with open("manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"manifest.json créé avec {len(files)} fichier(s).")
