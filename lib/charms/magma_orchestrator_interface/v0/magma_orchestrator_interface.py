# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.

"""Library for the magma-orchestrator relation.

This library contains the Requires and Provides classes for handling the magma-orchestrator
interface.

## Getting Started
From a charm directory, fetch the library using `charmcraft`:

```shell
charmcraft fetch-lib charms.magma_orchestrator_interface.v1.magma_orchestrator_interface
```

Add the following libraries to the charm's `requirements.txt` file:
- jsonschema

### Requirer charm
The requirer charm is the charm requiring to connect to an orchestrator from another charm that
provides this interface.

Example:
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
        pass


if __name__ == "__main__":
    main(DummyMagmaOrchestratorRequirerCharm)

```
"""


import logging

from jsonschema import exceptions, validate  # type: ignore[import]
from ops.charm import CharmBase, CharmEvents, RelationChangedEvent
from ops.framework import EventBase, EventSource, Handle, Object

# The unique Charmhub library identifier, never change it
LIBID = "ec30058c7c6d4850aba6a132d2506efe"

# Increment this major API version when introducing breaking changes
LIBAPI = 0

# Increment this PATCH version before using `charmcraft publish-lib` or reset
# to 0 if you are raising the major API version
LIBPATCH = 1


logger = logging.getLogger(__name__)

REQUIRER_JSON_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "`magma-orchestrator` requirer root schema",
    "type": "object",
    "description": "The `magma-orchestrator` root schema comprises the entire requirer databag for this interface.",  # noqa: E501
    "examples": [
        {
            "root_ca_certificate": "",
            "orchestrator_address": "http://orchestrator.com",
            "orchestrator_port": 1234,
            "bootstrapper_address": "http://bootstrapper.com",
            "bootstrapper_port": 5678,
            "fluentd_address": "http://fluentd.com",
            "fluentd_port": 9112,
        }
    ],
    "properties": {
        "root_ca_certificate": {
            "type": "string",
        },
        "orchestrator_address": {
            "type": "string",
        },
        "orchestrator_port": {
            "type": "integer",
        },
        "bootstrapper_address": {
            "type": "string",
        },
        "bootstrapper_port": {
            "type": "integer",
        },
        "fluentd_address": {
            "type": "string",
        },
        "fluentd_port": {
            "type": "integer",
        },
    },
    "required": [
        "root_ca_certificate",
        "orchestrator_address",
        "orchestrator_port",
        "bootstrapper_address",
        "bootstrapper_port",
        "fluentd_address",
        "fluentd_port",
    ],
    "additionalProperties": True,
}


class OrchestratorAvailableEvent(EventBase):
    """Charm Event triggered when a Orchestrator is available."""

    def __init__(
        self,
        handle: Handle,
        root_ca_certificate: str,
        orchestrator_address: str,
        orchestrator_port: int,
        bootstrapper_address: str,
        bootstrapper_port: int,
        fluentd_address: str,
        fluentd_port: int,
    ):
        """Init."""
        super().__init__(handle)
        self.root_ca_certificate = root_ca_certificate
        self.orchestrator_address = orchestrator_address
        self.orchestrator_port = orchestrator_port
        self.bootstrapper_address = bootstrapper_address
        self.bootstrapper_port = bootstrapper_port
        self.fluentd_address = fluentd_address
        self.fluentd_port = fluentd_port

    def snapshot(self) -> dict:
        """Returns snapshot."""
        return {
            "root_ca_certificate": self.root_ca_certificate,
            "orchestrator_address": self.orchestrator_address,
            "orchestrator_port": self.orchestrator_port,
            "bootstrapper_address": self.bootstrapper_address,
            "bootstrapper_port": self.bootstrapper_port,
            "fluentd_address": self.fluentd_address,
            "fluentd_port": self.fluentd_port,
        }

    def restore(self, snapshot: dict):
        """Restores snapshot."""
        self.root_ca_certificate = snapshot["root_ca_certificate"]
        self.orchestrator_address = snapshot["orchestrator_address"]
        self.orchestrator_port = snapshot["orchestrator_port"]
        self.bootstrapper_address = snapshot["bootstrapper_address"]
        self.bootstrapper_port = snapshot["bootstrapper_port"]
        self.fluentd_address = snapshot["fluentd_address"]
        self.fluentd_port = snapshot["fluentd_port"]


class OrchestratorRequirerCharmEvents(CharmEvents):
    """List of events that the Orchestrator requirer charm can leverage."""

    orchestrator_available = EventSource(OrchestratorAvailableEvent)


class OrchestratorRequires(Object):
    """Class to be instantiated by charms requiring connectivity with Orchestrator."""

    on = OrchestratorRequirerCharmEvents()

    def __init__(self, charm: CharmBase, relationship_name: str):
        """Init."""
        super().__init__(charm, relationship_name)
        self.charm = charm
        self.relationship_name = relationship_name
        self.framework.observe(
            charm.on[relationship_name].relation_changed, self._on_relation_changed
        )

    @staticmethod
    def _relation_data_is_valid(remote_app_relation_data: dict) -> bool:
        try:
            validate(instance=remote_app_relation_data, schema=REQUIRER_JSON_SCHEMA)
            return True
        except exceptions.ValidationError:
            return False

    def _on_relation_changed(self, event: RelationChangedEvent) -> None:
        """Handler triggerred on relation changed events.

        Args:
            event: Juju event

        Returns:
            None
        """
        relation = self.model.get_relation(self.relationship_name)
        if not relation:
            logger.warning(f"No relation: {self.relationship_name}")
            return
        if not relation.app:
            logger.warning(f"No remote application in relation: {self.relationship_name}")
            return
        remote_app_relation_data = relation.data[relation.app]
        if not self._relation_data_is_valid(dict(remote_app_relation_data)):
            logger.warning(
                f"Provider relation data did not pass JSON Schema validation: "
                f"{event.relation.data[event.app]}"
            )
            return
        self.on.orchestrator_available.emit(
            root_ca_certificate=remote_app_relation_data["root_ca_certificate"],
            orchestrator_address=remote_app_relation_data["orchestrator_address"],
            orchestrator_port=remote_app_relation_data["orchestrator_port"],
            bootstrapper_address=remote_app_relation_data["bootstrapper_address"],
            bootstrapper_port=remote_app_relation_data["bootstrapper_port"],
            fluentd_address=remote_app_relation_data["fluentd_address"],
            fluentd_port=remote_app_relation_data["fluentd_port"],
        )
