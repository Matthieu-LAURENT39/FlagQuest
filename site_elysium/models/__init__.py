"""
Modèles SQLAlchemy

```mermaid

erDiagram
    %% Tables principales
    users {
        int id "PRIMARY KEY"
        str username "NOT NULL"
        str email "NOT NULL"
        str password_hash "NOT NULL"
        bool is_admin "NOT NULL"

    }

    rooms {
        int id "PRIMARY KEY"
        str name "NOT NULL"
        str url_name "NOT NULL"
        str description "NOT NULL"
        str instructions "NOT NULL"
        str victim_vm_ids "NOT NULL"
    }


    virtual_machines {
        uuid uuid "PRIMARY KEY"
        int proxmox_id "NOT NULL"
        int user_id "NOT NULL"
        int template_vm_id "NOT NULL"
        str mac_address "NOT NULL"
        int room_id
        int display_post
    }

    questions {
        int id "PRIMARY KEY"
        int room_id "NOT NULL"
        str prompt "NOT NULL"
        str answer "NOT NULL"
        int points "NOT NULL"
    }

    %% Tables de jointure
    user_question_data {
        int user_id "PRIMARY KEY"
        int question_id "PRIMARY KEY"
        int solved_at "NOT NULL"
    }

    room_user {
        int room_id "PRIMARY KEY"
        int user_id "PRIMARY KEY"
    }


    %% Relations
    virtual_machines 0+--1 users : "posseder"
    
    rooms 1--1 room_user : "être participer par"
    users 1--1 room_user : "participer à"

    users 1--1 user_question_data : "répondre"
    questions 1--1 user_question_data : "répondu par"

    virtual_machines |o--1 rooms: "créé pour"
    questions 0+--1 rooms: "appartenir"

```
"""
from flask import has_app_context

# Workaround pour faire que le module soit importable
# sans un contexte flask
if has_app_context():
    from .. import db

    _current_base = db.Model
    _current_relationship = db.relationship
    _current_foreign_key = db.ForeignKey
else:
    from sqlalchemy.orm import DeclarativeBase, relationship
    from sqlalchemy import ForeignKey

    class _Base(DeclarativeBase):
        """Base SQLAlchemy placeholder"""

        pass

    _current_base = _Base
    _current_relationship = relationship
    _current_foreign_key = ForeignKey

from .room_user import room_user
from .user_question_data import SolvedQuestionData
from .virtual_machine import VirtualMachine
from .user import User
from .room import Room
from .question import Question
