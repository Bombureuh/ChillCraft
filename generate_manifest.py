"""
Génère manifest.json pour le launcher.

Utilisation :
1. Crée un dossier "pack" à côté de ce script, avec dedans :
     pack/mods/      -> tous les .jar des mods
     pack/config/    -> (optionnel) les fichiers de config à imposer aux joueurs
2. Modifie les constantes ci-dessous.
3. Lance : py generate_manifest.py
4. Héberge le contenu du dossier "pack" ET manifest.json sur ton site/GitHub,
   de façon à ce que BASE_URL + "/mods/xxx.jar" soit téléchargeable.
5. Mets l'URL de manifest.json dans MODPACK_URL du launcher.
"""
import hashlib
import json
import os
from urllib.parse import quote

PACK_DIR = "pack"
BASE_URL = "https://exemple.com/pack"   # sans slash final
MINECRAFT_VERSION = "1.20.1"
LOADER = "forge"                         # "forge", "fabric", "neoforge", "quilt" ou "" (vanilla)
LOADER_VERSION = ""                      # vide = dernière version disponible (mieux vaut fixer la même que le serveur)


def sha1_of(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


files = []
for root, _, names in os.walk(PACK_DIR):
    for name in sorted(names):
        full = os.path.join(root, name)
        rel = os.path.relpath(full, PACK_DIR).replace(os.sep, "/")
        files.append({
            "path": rel,
            "url": f"{BASE_URL}/{quote(rel)}",
            "sha1": sha1_of(full),
        })

manifest = {
    "minecraft": MINECRAFT_VERSION,
    "loader": LOADER,
    "loader_version": LOADER_VERSION,
    "files": files,
}

with open("manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"manifest.json créé avec {len(files)} fichier(s).")
