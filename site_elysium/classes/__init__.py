"""
Classes n'étant pas lié à SQLAlchemy ou WTForms
"""

from .Allocator import Allocator as Allocator
from .VMManager import ProxmoxVMManager as ProxmoxVMManager
from .views import (
    AdminModelView as AdminModelView,
    RestrictedAdminIndexView as RestrictedAdminIndexView,
)
