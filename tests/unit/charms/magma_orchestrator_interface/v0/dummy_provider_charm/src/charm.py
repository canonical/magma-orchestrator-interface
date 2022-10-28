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

    DUMMY_ROOT_CA_CERT = "whatever certificate content"
    DUMMY_ORC8R_ADDRESS = "http://orchestrator.com"
    DUMMY_ORC8C_PORT = 1234
    DUMMY_BOOTSTRAPPER_ADDRESS = "http://bootstrapper.com"
    DUMMY_BOOTSTRAPPER_PORT = 5678
    DUMMY_FLUENTD_ADDRESS = "http://fluentd.com"
    DUMMY_FLUENTD_PORT = 9012

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
                root_ca_certificate=self.DUMMY_ROOT_CA_CERT,
                orchestrator_address=self.DUMMY_ORC8R_ADDRESS,
                orchestrator_port=self.DUMMY_ORC8C_PORT,
                bootstrapper_address=self.DUMMY_BOOTSTRAPPER_ADDRESS,
                bootstrapper_port=self.DUMMY_BOOTSTRAPPER_PORT,
                fluentd_address=self.DUMMY_FLUENTD_ADDRESS,
                fluentd_port=self.DUMMY_FLUENTD_PORT,
            )


if __name__ == "__main__":
    main(DummyMagmaOrchestratorProviderCharm)
