# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.


import unittest

import pytest
from ops import testing

from tests.unit.charms.magma_orchestrator_interface.v0.dummy_provider_charm.src.charm import (
    DummyMagmaOrchestratorProviderCharm,
)

testing.SIMULATE_CAN_CONNECT = True

BASE_CHARM_DIR = "tests.unit.charms.magma_orchestrator_interface.v0.dummy_requirer_charm.src.charm.DummyMagmaOrchestratorRequirerCharm"  # noqa: E501


class TestMagmaOrchestratorProvider(unittest.TestCase):
    def setUp(self):
        self.relation_name = "orchestrator"
        self.harness = testing.Harness(DummyMagmaOrchestratorProviderCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    def test_given_unit_is_leader_and_remote_unit_joined_relation_when_set_orchestrator_information_then_data_is_added_to_application_databag(  # noqa: E501
        self,
    ):
        self.harness.set_leader(is_leader=True)
        remote_app = "magma-orc8r-requirer"
        relation_id = self.harness.add_relation(
            relation_name=self.relation_name, remote_app=remote_app
        )

        root_ca_certificate = "whatever ca certificate"
        orchestrator_address = "http://orchestrator.com"
        orchestrator_port = 1234
        bootstrapper_address = "http://bootstrapper.com"
        bootstrapper_port = 5678
        fluentd_address = "http://fluentd.com"
        fluentd_port = 9112

        self.harness.charm.orchestrator_provider.set_orchestrator_information(
            root_ca_certificate=root_ca_certificate,
            orchestrator_address=orchestrator_address,
            orchestrator_port=orchestrator_port,
            bootstrapper_address=bootstrapper_address,
            bootstrapper_port=bootstrapper_port,
            fluentd_address=fluentd_address,
            fluentd_port=fluentd_port,
        )

        relation_data = self.harness.get_relation_data(
            relation_id=relation_id, app_or_unit=self.harness.charm.app.name
        )

        assert relation_data["root_ca_certificate"] == root_ca_certificate
        assert relation_data["orchestrator_address"] == orchestrator_address
        assert relation_data["orchestrator_port"] == str(orchestrator_port)
        assert relation_data["bootstrapper_address"] == bootstrapper_address
        assert relation_data["bootstrapper_port"] == str(bootstrapper_port)
        assert relation_data["fluentd_address"] == fluentd_address
        assert relation_data["fluentd_port"] == str(fluentd_port)

    def test_given_unit_is_not_leader_and_remote_unit_joined_relation_when_set_orchestrator_information_then_runtime_error_is_raised(  # noqa: E501
        self,
    ):
        self.harness.set_leader(is_leader=False)
        remote_app = "magma-orc8r-requirer"
        self.harness.add_relation(relation_name=self.relation_name, remote_app=remote_app)

        with pytest.raises(RuntimeError) as e:
            self.harness.charm.orchestrator_provider.set_orchestrator_information(
                root_ca_certificate="whatever ca certificate",
                orchestrator_address="http://orchestrator.com",
                orchestrator_port=1234,
                bootstrapper_address="http://bootstrapper.com",
                bootstrapper_port=5678,
                fluentd_address="http://fluentd.com",
                fluentd_port=9112,
            )
        assert str(e.value) == "Unit must be leader to set application relation data."

    def test_given_unit_is_leader_and_relation_is_not_created_when_set_orchestrator_information_then_runtime_error_is_raised(  # noqa: E501
        self,
    ):
        self.harness.set_leader(is_leader=True)

        with pytest.raises(RuntimeError) as e:
            self.harness.charm.orchestrator_provider.set_orchestrator_information(
                root_ca_certificate="whatever ca certificate",
                orchestrator_address="http://orchestrator.com",
                orchestrator_port=1234,
                bootstrapper_address="http://bootstrapper.com",
                bootstrapper_port=5678,
                fluentd_address="http://fluentd.com",
                fluentd_port=9112,
            )
        assert str(e.value) == "Relation orchestrator not yet created"
