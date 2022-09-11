# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.


import unittest
from unittest.mock import patch

from ops import testing

from tests.unit.charms.magma_orchestrator_interface.v0.dummy_requirer_charm.src.charm import (
    DummyMagmaOrchestratorRequirerCharm,
)

testing.SIMULATE_CAN_CONNECT = True

BASE_CHARM_DIR = "tests.unit.charms.magma_orchestrator_interface.v0.dummy_requirer_charm.src.charm.DummyMagmaOrchestratorRequirerCharm"  # noqa: E501


class Test(unittest.TestCase):
    def setUp(self):
        self.relation_name = "orchestrator"
        self.model_name = "whatever"
        self.harness = testing.Harness(DummyMagmaOrchestratorRequirerCharm)
        self.harness.set_model_name(name=self.model_name)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()
        self.maxDiff = None

    @patch(f"{BASE_CHARM_DIR}._on_orchestrator_available")
    def test_given_orchestrator_information_in_peer_relation_data_when_relation_changed_then_orchestrator_available_event_emitted(  # noqa: E501
        self, patch_on_orchestrator_available
    ):
        remote_app = "magma-orc8r-provider"
        relation_id = self.harness.add_relation(
            relation_name=self.relation_name, remote_app=remote_app
        )

        root_ca_certificate = "whatever certificate"
        orchestrator_address = "http://orchestrator.com"
        orchestrator_port = 123
        bootstrapper_address = "http://bootstrapper.com"
        bootstrapper_port = 456
        fluentd_address = "http://fluentd.com"
        fluentd_port = 789
        remote_app_relation_data = {
            "root_ca_certificate": root_ca_certificate,
            "orchestrator_address": orchestrator_address,
            "orchestrator_port": orchestrator_port,
            "bootstrapper_address": bootstrapper_address,
            "bootstrapper_port": bootstrapper_port,
            "fluentd_address": fluentd_address,
            "fluentd_port": fluentd_port,
        }
        self.harness.update_relation_data(
            relation_id=relation_id, app_or_unit=remote_app, key_values=remote_app_relation_data
        )

        patch_on_orchestrator_available.assert_called()
        args, _ = patch_on_orchestrator_available.call_args
        orchestrator_available_event = args[0]
        assert orchestrator_available_event.root_ca_certificate == root_ca_certificate
        assert orchestrator_available_event.orchestrator_address == orchestrator_address
        assert orchestrator_available_event.orchestrator_port == orchestrator_port
        assert orchestrator_available_event.bootstrapper_address == bootstrapper_address
        assert orchestrator_available_event.bootstrapper_port == bootstrapper_port
        assert orchestrator_available_event.fluentd_address == fluentd_address
        assert orchestrator_available_event.fluentd_port == fluentd_port

    @patch(f"{BASE_CHARM_DIR}._on_orchestrator_available")
    def test_given_orchestrator_information_not_in_peer_relation_data_when_relation_changed_then_orchestrator_available_event_not_emitted(  # noqa: E501
        self, patch_on_orchestrator_available
    ):
        remote_app = "magma-orc8r-provider"
        relation_id = self.harness.add_relation(
            relation_name=self.relation_name, remote_app=remote_app
        )

        self.harness.update_relation_data(
            relation_id=relation_id, app_or_unit=remote_app, key_values=dict()
        )

        patch_on_orchestrator_available.assert_not_called()

    @patch(f"{BASE_CHARM_DIR}._on_orchestrator_available")
    def test_given_orchestrator_information_in_peer_relation_data_is_partial_when_relation_changed_then_orchestrator_available_event_not_emitted(  # noqa: E501
        self, patch_on_orchestrator_available
    ):
        remote_app = "magma-orc8r-provider"
        relation_id = self.harness.add_relation(
            relation_name=self.relation_name, remote_app=remote_app
        )
        orchestrator_address = "http://orchestrator.com"
        orchestrator_port = 123
        bootstrapper_address = "http://bootstrapper.com"
        bootstrapper_port = 456
        remote_app_relation_data = {
            "orchestrator_address": orchestrator_address,
            "orchestrator_port": orchestrator_port,
            "bootstrapper_address": bootstrapper_address,
            "bootstrapper_port": bootstrapper_port,
        }
        self.harness.update_relation_data(
            relation_id=relation_id, app_or_unit=remote_app, key_values=remote_app_relation_data
        )

        patch_on_orchestrator_available.assert_not_called()
