"""
Classes n'étant pas lié à SQLAlchemy ou WTForms

```mermaid

classDiagram
    class VMManager~ABC~ {
    }

    class ProxmoxVMManager {
    }

    VMManager <|-- ProxmoxVMManager
    ProxmoxVMManager "1" o-- "2" Allocator

        class Allocator~Generic[Resource]~ {
    }
```
"""

from .Allocator import Allocator as Allocator
from .VMManager import VMManager as VMManager, ProxmoxVMManager as ProxmoxVMManager
from .views import (
    AdminModelView as AdminModelView,
    RestrictedAdminIndexView as RestrictedAdminIndexView,
)
