#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.


"""Charm the service."""

from ops.charm import CharmBase, RelationJoinedEvent
from ops.main import main

from lib.charms.magma_orchestrator_interface.v0.magma_orchestrator_interface import (
    OrchestratorProvides,
)


class DummyMagmaOrchestratorProviderCharm(CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        """Init."""
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
