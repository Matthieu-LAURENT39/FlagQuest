"""
Fichier de configuration de l'application
"""

APP_NAME: str = "FlagQuest"
"""Le nom de l'application à afficher"""
# Ce sont des URLs.
# Il est possible de placer des fichier dans le dossier /static afin
# de pouvoir les utiliser avec une url de la forme "/static/mon_fichier.png"
APP_LOGO: str = "/static/img/logo.png"
"""Le logo a afficher sur le site"""
APP_FAVICO: str = "/static/img/logo.png"
"""Le logo a afficher pour le favico"""

# ========== Apparence ==========
ENABLE_ANIMATED_BACKGROUND: bool = True
"""Si il faut afficher le fond animé sur la page d'acceuil"""

# ========== footer ==========
CONFIDENTIALITE_LINK: str = "/confidentalite"
"""L'URL vers la page de confidentialité"""
MENTIONS_LEGALES_LINK: str = "/mention_legales"
"""L'URL vers la page des mentions légales"""
CONDITION_GENERALES_D_UTILISATION_LINK = "/Conditions_generales_d_utilisation"
"""L'URL vers la page des conditions générales d'utilisation"""

SENTENCE_FOOTER_END: str = "FlagQuest : plateforme d'apprentissage dédiée au hacking et à la sécurité de l'information"
"""La phrase en haut du footer"""
COPYRIGHT: str = "© 2023"
"""Le copyright a afficher dans le footer"""

# ========== Liens Footer ==========
# Laissé un lien vide pour le retirer
TWITTER_LINK: str = "https://twitter.com/intent/follow?original_referer=https%3A%2F%2Fwww.root-me.org%2F&region=follow_link&screen_name=rootme_org&tw_p=followbutton"
"""L'URL du compte Twitter (laissé vide pour cacher)"""
LINKEDIN_LINK: str = "https://www.linkedin.com/in/flag-quest-825419276/"
"""L'URL du compte Linkedin (laissé vide pour cacher)"""
RSS_FEED_LINK: str = ""
"""L'URL du flux RSS (laissé vide pour cacher)"""
DISCORD_LINK: str = ""
"""L'URL du serveur Discord (laissé vide pour cacher)"""

# ========== ADVANCED ==========
# ===== Proxmox =====
PROXMOX_IP: str = "172.17.50.250:8006"
"""L'adresse IP de l'interface web Proxmox"""
PROXMOX_HOST: str = "172.17.50.250"
"""L'adresse IP de l'hôte Proxmox"""
PROXMOX_LOGIN: str = "root@pam"
"""Le login a utilisé pour Proxmox"""
PROXMOX_PASSWORD: str = "passw0rd"
"""Le mot de passe a utiliser pour Promox"""
PROXMOX_VERIFY_SSL: bool = False
"""Si il faut vérifier le certificat SSL de l'hyperviseur"""

VM_NETWORK: str = "10.0.0.0/16"
"""Le réseau des VM victime, sous notation X.X.X.X/CIDR"""

VICTIM_VM_PREFIX: str = "automatic"
"""Le préfix à ajouté aux nom des VMs victimes"""

ATTACK_VM_TEMPLATE_ID: str = "104"
"""L'ID de la template pour les VMs d'attaques"""
ATTACK_VM_USERNAME: str = "hacker"
"""
Le login pour la VM d'attaque qui sera affiché à l'utilisateur.
Changer cette valeur ne change pas automatiquement le nom d'utilisateur sur la VM!
"""
ATTACK_VM_PASSWORD: str = "kali"
"""
Le mot de passe pour la VM d'attaque.
Changer cette valeur ne change pas automatiquement le mot de passe sur la VM!
"""
