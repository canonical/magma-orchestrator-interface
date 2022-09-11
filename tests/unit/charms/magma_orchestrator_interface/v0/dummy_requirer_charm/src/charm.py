#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.


"""Charm the service."""

from ops.charm import CharmBase
from ops.main import main

from lib.charms.magma_orchestrator_interface.v0.magma_orchestrator_interface import (
    OrchestratorAvailableEvent,
    OrchestratorRequires,
)


class DummyMagmaOrchestratorRequirerCharm(CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        """Init."""
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
