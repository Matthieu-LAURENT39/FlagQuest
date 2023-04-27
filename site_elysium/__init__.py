from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from .backend.filters import markdown_filter
from .flask_config import Config

if TYPE_CHECKING:
    from .models import User


db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id: str) -> Optional["User"]:
    """Chargeur d'utilisateur pour Flask-Login

    Args:
        user_id (str): L'ID de l'utilisateur à charger.

    Returns:
        Optional[User]: L'utilisateur, ou None si il n'existe pas.
    """

    from .models import User

    return User.query.filter_by(id=user_id).first()


def create_app(config: object = Config) -> Flask:
    """App factory pour Flask

    Args:
        config (object, optional): L'objet de configuration à charger. Defaults to Config.

    Returns:
        Flask: l'app Flask
    """
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
        static_url_path="/static",
    )

    # On charge les constantes
    app.config.from_pyfile("app_config.py")

    # Puis on charge la config flask
    app.config.from_object(config)

    # SQLalchemy
    db.init_app(app)

    # flask-login
    login_manager.init_app(app)

    # flask-admin
    # Créer l'instance va a l'encontre des principes de design des app factory, mais
    # on y est contraint du a au design de flask-admin.
    # Voir aussi https://github.com/flask-admin/flask-admin/issues/910
    admin = Admin(name="Interface Admin", template_mode="bootstrap3")

    # remplacer superhero par cerulean pour screens
    app.config["FLASK_ADMIN_SWATCH"] = "superhero"
    admin.init_app(app)

    from .classes import AdminModelView

    with app.app_context():
        from .models import Question, Room, SolvedQuestionData, User, VirtualMachine

    admin.add_view(AdminModelView(User, db.session))
    admin.add_view(AdminModelView(Room, db.session))
    admin.add_view(AdminModelView(VirtualMachine, db.session))
    admin.add_view(AdminModelView(Question, db.session))
    admin.add_view(AdminModelView(SolvedQuestionData, db.session))

    # Register the filters
    app.jinja_env.filters["markdown"] = markdown_filter

    # Register the blueprints
    from .routes import api, main

    app.register_blueprint(main)
    app.register_blueprint(api)

    # Enfin, on créer toutes les données
    if not app.testing:
        setup_app(app)

    # print(app.url_map)

    return app


def setup_app(app: Flask):
    """Génère des données de base dans l'app

    Args:
        app (Flask): l'app où généré les données.
    """
    from .models import Question, Room, User

    with app.app_context():
        db.create_all()

    with app.app_context():
        user = User.query.filter_by(username="admin").first()
        if user is None:
            user = User(
                username="admin",
                email="feur@desu.wa",
                is_admin=True,
            )
            user.set_password("admin")
            db.session.add(user)
            db.session.commit()

        room = Room.query.filter_by(id="1").first()
        if room is None:
            room = Room(
                name="Room 1",
                description="Wow what a cool room **desu wa**",
                url_name="room1",
                instructions="QCM",
                victim_vm_ids=[101],
            )
            room2 = Room(
                name="Introduction à Nmap",
                description="Apprenez les bases de **Nmap**, un outil d'exploration réseau.",
                url_name="introduction_nmap",
                instructions="""Après avoir dressé et borné la prestation de tests d'intrusion, vous devez commencer par la première étape de votre mission : Enumération
Pour mener à bien cette phase, nous allons apprendre à utiliser l'application nmap.

# NMAP
Nmap (« Network Mapper ») est un outil open source d'exploration réseau et d'audit de sécurité.
Les commandes principales sont :
`nmap -v <ip>`

Cette option scanne tous les ports réservés TCP sur la machine <ip> . L'option -v active le mode verbeux.
`nmap -sS -O <ip>/<CIDR>`

Lance un scan furtif (SYN scan) contre chaque machine active. Il essaie aussi de déterminer le système d'exploitation sur chaque hôte actif. Cette démarche nécessite les privilèges de root puisqu'on utilise un SYN scan et une détection d'OS
exemple : `nmap -sS -O 192.168.1.0/24` scanne les 255 machines du NetID 192.168.1
`nmap -sV -p 22,53,110,143,4564 198.116.0-255.1-127`

Lance une recherche des hôtes et un scan TCP dans la première moitié de chacun des 255 sous-réseaux à 8 bits dans l'espace d'adressage de classe B 198.116 Cela permet de déterminer si les systèmes font tourner sshd (22), DNS (53), pop3d(110), imapd(143) ou le port 4564. Pour chacun de ces ports qui sont ouverts, la détection de version est utilisée pour déterminer quelle application est actuellement lancée.

### Flags intéréssant
##### Détection d'un système d'exploitation:
`-O`: Active la détection d'OS
##### Détection de services/versions:
`-sV`: Teste les ports ouverts pour déterminer le service en écoute et sa version
##### Spécification des ports et ordre de scan:
`-p` <plage de ports>: Ne scanne que les ports spécifiés
##### Méthode de scan:
`-sS` / `-sT` / `-sA` / `-sW`/ `-sM`: Scans TCP SYN/Connect()/ACK/Window/Maimon 
`-sN`/`-sF`/`-sX`: Scans TCP Null, FIN et Xmas
`-sU`: Scan UDP

##### Divers:
`-6`: Active le scan IPv6
`-A`: Active la détection du système d'exploitation, des versions et génère un tracert (traceroute)
""",
            )
            room3 = Room(
                name="John The Ripper",
                description="Apprenez à casser des mots de passe !",
                url_name="john",
                instructions="""
# John the Ripper
[John the Ripper](https://www.openwall.com/john/) (JTR ou John) est un logiciel libre permettant de tester la sécurité d'un mot de passe.

## Installation
*Cet outils est déjà installé sur la VM d'attaque, cette explication est simplement à but éducatif.*

### Sous Linux
On peut l'installer via **apt-get** ou **snap** :
```
$ sudo apt-get update
$ sudo apt-get install john -y
```

### Sous Windows
Passez par [Cygwin](https://www.cygwin.com/) qui est une bibliothèque de logiciels libres permettant d'émuler un système Linux sous différentes versions de Windows.
Voici un petit guide : `https://miloserdov.org/?p=4961#15`

# Utilisation
Les commandes principales sont :
`john --wordlist=</path/to/wordlist/wordlists.txt>`

## Les 3 différents modes
### Mode simple (Single crack)
En mode simple, john se génère des variations de chaînes de caractères en fonction du nom d'utilisateur présent dans le fichier. Si le nom d'utilisateur est "voiture", le mode simple va tester les mots de passe suivants : "Voiture", "VOIRTURE2000", "voiTure", ...

Le contenu du fichier doit être sous la forme `username:hash`.
Exemple :
    `jardinier:a69c316fbc7ec7da1305e72f95c164a8`

La commande doit spécifier le paramètre `--single` ainsi que le format du hash :
`john --single --format=<hash-format> <filename>`


### Attaque par dictionnaire (Wordlist)
L'attaque par dictionnaire test le hash avec tout les mots de passe présents dans une liste de mots (de passe) aussi appelée **wordlist**.

Une des plus célèbre est RockYou, elle est issue d'une fuite de donnée du réseau social californien Rockyou en 2009.

Wordlist : `https://github.com/danielmiessler/SecLists`

`john --wordlist=</path/to/wordlist>` --format=<hash-format> <filename>`

### Mode incrémental (Incremental)
Dans ce mode, John essaie tout les combinaisons de caractères possible pour trouver le mot de passe.

Spécifier que l'on veut utiliser que des chiffres :
`john -i=<MODE> --format=<hash-format> <filename>`
Exemple :
`john --incremental=digits --format=raw-md5 pass.txt`

""",
            )
            room4 = Room(
                name="Introduction à Hydra",
                description="Trouvez le mot de passe du  serveur FTP !",
                url_name="hydra",
                instructions="""
# Hydra
[Hydra](https://github.com/vanhauser-thc/thc-hydra) est un logiciel libre permettant de craquer un mot de passe en ligne par **bruteforce**.

## Installation
*Cet outils est déjà installé sur la VM d'attaque, cette explication est simplement à but éducatif.*

### Sous Linux
On peut l'installer via **apt-get** ou **snap** :
```
$ sudo apt-get update
$ sudo apt-get install hydra -y
```

### Sous Windows
Passez par [Cygwin](https://www.cygwin.com/) qui est une bibliothèque de logiciels libres permettant d'émuler un système Linux sous différentes versions de Windows.

# Utilisation

                """,
            )
            room5 = Room(
                name="Room 5",
                description="lorem ipsum dolor sit amet",
                url_name="room5",
                instructions="QCM",
            )
            room6 = Room(
                name="Room 6",
                description="lorem ipsum dolor sit amet",
                url_name="room6",
                instructions="QCM",
            )

            db.session.add(room)
            db.session.add(room2)
            db.session.add(room3)
            db.session.add(room4)
            db.session.add(room5)
            db.session.add(room6)

            db.session.commit()

            # room.users.append(user)
            # backend.db.session.commit()

        question = Question.query.filter_by(id="1").first()
        if question is None:
            question = Question(
                room_id=1,
                prompt="""**Qui** a écrit *cette* __question__?
Indice: `matt`
Et voici un code block
```py
import random
n = random.randint(1,10)
print(n)
```""",
                answer="matt",
                points=15,
            )
            db.session.add(question)

            db.session.add(
                Question(
                    room_id=1,
                    prompt="Quel est le nombre associé à la célèbre chanteuse virtuelle, **Hatsune Miku**?",
                    answer="39",
                    points=39,
                )
            )

            for i in range(6):
                question = Question(
                    room_id=1, prompt=f"{i}+1=?", answer=str(i + 1), points=2
                )
                db.session.add(question)

            # question room2

            db.session.add(
                Question(
                    room_id=2,
                    prompt="Quel est l'argument permettant d'identifier l'OS et la version?",
                    answer="-A",
                    points=2,
                )
            )

            db.session.add(
                Question(
                    room_id=2,
                    prompt="""Quels sont les machines qui ont un serveur FTP appartenant au réseau **10.10.12.128/25**?
Réponse attendu sous la forme `X.X.X.X/X`""",
                    answer="10.10.12.128/25",
                    points=2,
                )
            )

            db.session.add(
                Question(
                    room_id=2,
                    prompt="Combien de services sont disponibles sur ce serveur?",
                    answer="3",
                    points=2,
                )
            )

            db.session.add(
                Question(
                    room_id=2,
                    prompt="Quel est la version du serveur Web?",
                    answer="Apache/2.4.18",
                    points=2,
                )
            )

            db.session.add(
                Question(
                    room_id=2,
                    prompt="Que trouvons-nous sur le port 21?",
                    answer="ProFTPD 1.3.3c",
                    points=2,
                )
            )

            db.session.add(
                Question(
                    room_id=2,
                    prompt="Quel est le titre de la page web?",
                    answer="it works",
                    points=2,
                )
            )

            db.session.commit()

            # question room3 - john the ripper

            db.session.add(
                Question(
                    room_id=3,
                    prompt="Quel est le mot de passe correspondant au hash suivant (sha256): *4cffb4ed84e2986f067c9e373ef87bf6d5eddc7866fb2cdd41eb48429743f50d*. Utilisez le mode simple.",
                    answer="ludovic4000",
                    points=2,
                )
            )

            db.session.add(
                Question(
                    room_id=3,
                    prompt="Quel est le mot de passe correspondant au hash suivant (sha1): *26e2440a5730bccb5cf325e8856ac3c38fae9273*. Utilisez la méthode incremental en mode **digits**",
                    answer="52821071",
                    points=2,
                )
            )

            db.session.add(
                Question(
                    room_id=3,
                    prompt="Quel est le mot de passe correspondant au hash suivant (md5): *117735823fadae51db091c7d63e60eb0*. Utilisez l'attaque via la wordlist **rockyou**",
                    answer="francisco",
                    points=2,
                )
            )
