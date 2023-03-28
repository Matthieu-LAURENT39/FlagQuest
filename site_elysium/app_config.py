APP_NAME = "ROOT ME"
# Ce sont des URLs.
# Il est possible de placer des fichier dans le dossier /static afin
# de pouvoir les utiliser avec une url de la forme "/static/mon_fichier.png"
APP_LOGO = "/static/img/logo_rootme_inverted.png"
APP_FAVICO = "/static/img/logo_rootme.svg"


# ====== footer =========
CONFIDENTIALITE_LINK = "/confidentalite"
MENTIONS_LEGALES_LINK = "/mention_legales"
CONDITION_GENERALES_D_UTILISATION_LINK = "/Conditions_generales_d_utilisation"

SENTENCE_FOOTER_END = "Root Me : plateforme d'apprentissage dédiée au hacking et à la sécurité de l'information"
COPYRIGHT = "© 2023"

# ===== Liens Footer =====
# Laissé un lien vide pour le retirer
TWITTER_LINK = "https://twitter.com/intent/follow?original_referer=https%3A%2F%2Fwww.root-me.org%2F&region=follow_link&screen_name=rootme_org&tw_p=followbutton"
LINKEDIN_LINK = (
    "https://www.linkedin.com/groups/Root-Me-hacking-and-information-8180601"
)
RSS_FEED_LINK = "https://www.root-me.org/?page=flux_rss&lang=fr"
DISCORD_LINK = "https://discord.gg/XejsBJdUch"


# ========== ADVANCED ==========
# ===== Proxmox =====
PROXMOX_IP = "172.17.50.250:8006"
PROXMOX_HOST = "172.17.50.250"
PROXMOX_LOGIN = "root@pam"
PROXMOX_PASSWORD = "passw0rd"
PROXMOX_VERIFY_SSL = False

VM_NETWORK = "10.0.0.0/16"

VICTIM_VM_PREFIX = "automatic"

ATTACK_VM_TEMPLATE_ID = "104"
ATTACK_VM_USERNAME = "ubuntu"
ATTACK_VM_PASSWORD = "ubuntu"
