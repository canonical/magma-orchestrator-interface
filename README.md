# magma-orchestrator-interface

This charm library contains the Requires and Provides classes for handling the magma-orchestrator
interface.

> **Warning**: Do not deploy this charm. It is meant to only be used as a charm library.

## Getting Started
From a charm directory, fetch the library using `charmcraft`:

```shell
charmcraft fetch-lib charms.magma_orchestrator_interface.v0.magma_orchestrator_interface
```

Add the following libraries to the charm's `requirements.txt` file:
- jsonschema

### Requirer charm
The requirer charm is the charm requiring to connect to an instance of Magma Orchestrator
from another charm that provides this interface.

#### Example

```python

from ops.charm import CharmBase
from ops.main import main

from lib.charms.magma_orchestrator_interface.v0.magma_orchestrator_interface import (
    OrchestratorAvailableEvent,
    OrchestratorRequires,
)


class DummyMagmaOrchestratorRequirerCharm(CharmBase):

    def __init__(self, *args):
        super().__init__(*args)
        self.orchestrator_requirer = OrchestratorRequires(self, "orchestrator")
        self.framework.observe(
            self.orchestrator_requirer.on.orchestrator_available, self._on_orchestrator_available
        )

    def _on_orchestrator_available(self, event: OrchestratorAvailableEvent):
        print(event.root_ca_certificate)
        print(event.orchestrator_address)
        print(event.orchestrator_port)
        print(event.bootstrapper_address)
        print(event.orchestrator_port)
        print(event.fluentd_address)
        print(event.fluentd_port)


if __name__ == "__main__":
    main(DummyMagmaOrchestratorRequirerCharm)
```

### Provider charm

The provider charm is the charm providing information about a Magma Orchestrator
for another charm that requires this interface.

#### Example
```python
from ops.charm import CharmBase, RelationJoinedEvent
from ops.main import main

from lib.charms.magma_orchestrator_interface.v0.magma_orchestrator_interface import (
    OrchestratorProvides,
)


class DummyMagmaOrchestratorProviderCharm(CharmBase):

    def __init__(self, *args):
        super().__init__(*args)
        self.orchestrator_provider = OrchestratorProvides(self, "orchestrator")
        self.framework.observe(
            self.on.orchestrator_relation_joined, self._on_orchestrator_relation_joined
        )

    def _on_orchestrator_relation_joined(self, event: RelationJoinedEvent):
        if self.unit.is_leader():
            self.orchestrator_provider.set_orchestrator_information(
                root_ca_certificate="whatever certificate content",
                orchestrator_address="http://orchestrator.com",
                orchestrator_port=1234,
                bootstrapper_address="http://bootstrapper.com",
                bootstrapper_port=5678,
                fluentd_address="http://fluentd.com",
                fluentd_port=9112,
            )


if __name__ == "__main__":
    main(DummyMagmaOrchestratorProviderCharm)
```
