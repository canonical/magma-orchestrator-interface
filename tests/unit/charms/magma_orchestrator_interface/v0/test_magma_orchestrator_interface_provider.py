# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.


import unittest
from unittest.mock import PropertyMock, patch

import pytest
from ops import testing
from parameterized import parameterized

from tests.unit.charms.magma_orchestrator_interface.v0.dummy_provider_charm.src.charm import (
    DummyMagmaOrchestratorProviderCharm,
)

testing.SIMULATE_CAN_CONNECT = True

DUMMY_PROVIDER_CHARM = "tests.unit.charms.magma_orchestrator_interface.v0.dummy_provider_charm.src.charm.DummyMagmaOrchestratorProviderCharm"  # noqa: E501
TEST_ROOT_CA_CERT = "whatever ca certificate"
TEST_ORC8R_ADDRESS = "orchestrator.com"
TEST_ORC8R_PORT = 1111
TEST_BOOTSTRAPPER_ADDRESS = "bootstrapper.com"
TEST_BOOTSTRAPPER_PORT = 2222
TEST_FLUENTD_ADDRESS = "fluentd.com"
TEST_FLUENTD_PORT = 3333


class TestMagmaOrchestratorProvider(unittest.TestCase):
    def setUp(self):
        self.relation_name = "orchestrator"
        self.harness = testing.Harness(DummyMagmaOrchestratorProviderCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    @patch(f"{DUMMY_PROVIDER_CHARM}.DUMMY_ROOT_CA_CERT", new_callable=PropertyMock)
    @patch(f"{DUMMY_PROVIDER_CHARM}.DUMMY_ORC8R_ADDRESS", new_callable=PropertyMock)
    @patch(f"{DUMMY_PROVIDER_CHARM}.DUMMY_ORC8C_PORT", new_callable=PropertyMock)
    @patch(f"{DUMMY_PROVIDER_CHARM}.DUMMY_BOOTSTRAPPER_ADDRESS", new_callable=PropertyMock)
    @patch(f"{DUMMY_PROVIDER_CHARM}.DUMMY_BOOTSTRAPPER_PORT", new_callable=PropertyMock)
    @patch(f"{DUMMY_PROVIDER_CHARM}.DUMMY_FLUENTD_ADDRESS", new_callable=PropertyMock)
    @patch(f"{DUMMY_PROVIDER_CHARM}.DUMMY_FLUENTD_PORT", new_callable=PropertyMock)
    def test_given_unit_is_leader_when_orchestrator_relation_joined_then_data_is_added_to_application_databag(  # noqa: E501
        self,
        patched_fluentd_port,
        patched_fluentd_address,
        patched_bootstrapper_port,
        patched_bootstrapper_address,
        patched_orc8r_port,
        patched_orc8r_address,
        patched_root_ca,
    ):

        self.harness.set_leader(is_leader=True)
        remote_app = "magma-orc8r-requirer"
        patched_root_ca.return_value = TEST_ROOT_CA_CERT
        patched_orc8r_address.return_value = TEST_ORC8R_ADDRESS
        patched_orc8r_port.return_value = TEST_ORC8R_PORT
        patched_bootstrapper_address.return_value = TEST_BOOTSTRAPPER_ADDRESS
        patched_bootstrapper_port.return_value = TEST_BOOTSTRAPPER_PORT
        patched_fluentd_address.return_value = TEST_FLUENTD_ADDRESS
        patched_fluentd_port.return_value = TEST_FLUENTD_PORT

        relation_id = self.harness.add_relation(
            relation_name=self.relation_name, remote_app=remote_app
        )
        self.harness.add_relation_unit(relation_id, f"{remote_app}/0")

        relation_data = self.harness.get_relation_data(
            relation_id=relation_id, app_or_unit=self.harness.charm.app.name
        )
        self.assertEqual(relation_data["root_ca_certificate"], TEST_ROOT_CA_CERT)
        self.assertEqual(relation_data["orchestrator_address"], TEST_ORC8R_ADDRESS)
        self.assertEqual(relation_data["orchestrator_port"], str(TEST_ORC8R_PORT))
        self.assertEqual(relation_data["bootstrapper_address"], TEST_BOOTSTRAPPER_ADDRESS)
        self.assertEqual(relation_data["bootstrapper_port"], str(TEST_BOOTSTRAPPER_PORT))
        self.assertEqual(relation_data["fluentd_address"], TEST_FLUENTD_ADDRESS)
        self.assertEqual(relation_data["fluentd_port"], str(TEST_FLUENTD_PORT))

    @patch(f"{DUMMY_PROVIDER_CHARM}.DUMMY_ROOT_CA_CERT", new_callable=PropertyMock)
    @patch(f"{DUMMY_PROVIDER_CHARM}.DUMMY_ORC8R_ADDRESS", new_callable=PropertyMock)
    @patch(f"{DUMMY_PROVIDER_CHARM}.DUMMY_ORC8C_PORT", new_callable=PropertyMock)
    @patch(f"{DUMMY_PROVIDER_CHARM}.DUMMY_BOOTSTRAPPER_ADDRESS", new_callable=PropertyMock)
    @patch(f"{DUMMY_PROVIDER_CHARM}.DUMMY_BOOTSTRAPPER_PORT", new_callable=PropertyMock)
    @patch(f"{DUMMY_PROVIDER_CHARM}.DUMMY_FLUENTD_ADDRESS", new_callable=PropertyMock)
    @patch(f"{DUMMY_PROVIDER_CHARM}.DUMMY_FLUENTD_PORT", new_callable=PropertyMock)
    def test_given_unit_is_leader_when_multiple_orchestrator_relation_join_then_data_is_added_to_application_databag(  # noqa: E501
        self,
        patched_fluentd_port,
        patched_fluentd_address,
        patched_bootstrapper_port,
        patched_bootstrapper_address,
        patched_orc8r_port,
        patched_orc8r_address,
        patched_root_ca,
    ):

        self.harness.set_leader(is_leader=True)
        remote_app = "magma-orc8r-requirer"
        remote_app_2 = "another-magma-orc8r-requirer"
        patched_root_ca.return_value = TEST_ROOT_CA_CERT
        patched_orc8r_address.return_value = TEST_ORC8R_ADDRESS
        patched_orc8r_port.return_value = TEST_ORC8R_PORT
        patched_bootstrapper_address.return_value = TEST_BOOTSTRAPPER_ADDRESS
        patched_bootstrapper_port.return_value = TEST_BOOTSTRAPPER_PORT
        patched_fluentd_address.return_value = TEST_FLUENTD_ADDRESS
        patched_fluentd_port.return_value = TEST_FLUENTD_PORT

        relation_one_id = self.harness.add_relation(
            relation_name=self.relation_name, remote_app=remote_app
        )
        self.harness.add_relation_unit(relation_one_id, f"{remote_app}/0")
        relation_two_id = self.harness.add_relation(
            relation_name=self.relation_name, remote_app=remote_app_2
        )
        self.harness.add_relation_unit(relation_two_id, f"{remote_app_2}/0")

        relation_one_data = self.harness.get_relation_data(
            relation_id=relation_one_id, app_or_unit=self.harness.charm.app.name
        )
        self.assertEqual(relation_one_data["root_ca_certificate"], TEST_ROOT_CA_CERT)
        self.assertEqual(relation_one_data["orchestrator_address"], TEST_ORC8R_ADDRESS)
        self.assertEqual(relation_one_data["orchestrator_port"], str(TEST_ORC8R_PORT))
        self.assertEqual(relation_one_data["bootstrapper_address"], TEST_BOOTSTRAPPER_ADDRESS)
        self.assertEqual(relation_one_data["bootstrapper_port"], str(TEST_BOOTSTRAPPER_PORT))
        self.assertEqual(relation_one_data["fluentd_address"], TEST_FLUENTD_ADDRESS)
        self.assertEqual(relation_one_data["fluentd_port"], str(TEST_FLUENTD_PORT))

        relation_two_data = self.harness.get_relation_data(
            relation_id=relation_two_id, app_or_unit=self.harness.charm.app.name
        )
        self.assertEqual(relation_two_data["root_ca_certificate"], TEST_ROOT_CA_CERT)
        self.assertEqual(relation_two_data["orchestrator_address"], TEST_ORC8R_ADDRESS)
        self.assertEqual(relation_two_data["orchestrator_port"], str(TEST_ORC8R_PORT))
        self.assertEqual(relation_two_data["bootstrapper_address"], TEST_BOOTSTRAPPER_ADDRESS)
        self.assertEqual(relation_two_data["bootstrapper_port"], str(TEST_BOOTSTRAPPER_PORT))
        self.assertEqual(relation_two_data["fluentd_address"], TEST_FLUENTD_ADDRESS)
        self.assertEqual(relation_two_data["fluentd_port"], str(TEST_FLUENTD_PORT))

    def test_given_unit_is_not_leader_and_remote_unit_joined_relation_when_set_orchestrator_information_then_runtime_error_is_raised(  # noqa: E501
        self,
    ):
        self.harness.set_leader(is_leader=False)
        remote_app = "magma-orc8r-requirer"
        self.harness.add_relation(relation_name=self.relation_name, remote_app=remote_app)

        with pytest.raises(RuntimeError) as e:
            self.harness.charm.orchestrator_provider.set_orchestrator_information(
                root_ca_certificate=TEST_ROOT_CA_CERT,
                orchestrator_address=TEST_ORC8R_ADDRESS,
                orchestrator_port=TEST_ORC8R_PORT,
                bootstrapper_address=TEST_BOOTSTRAPPER_ADDRESS,
                bootstrapper_port=TEST_BOOTSTRAPPER_PORT,
                fluentd_address=TEST_FLUENTD_ADDRESS,
                fluentd_port=TEST_FLUENTD_PORT,
            )
        self.assertEqual(str(e.value), "Unit must be leader to set application relation data.")

    def test_given_unit_is_leader_and_relation_is_not_created_when_set_orchestrator_information_then_runtime_error_is_raised(  # noqa: E501
        self,
    ):
        self.harness.set_leader(is_leader=True)

        with pytest.raises(RuntimeError) as e:
            self.harness.charm.orchestrator_provider.set_orchestrator_information(
                root_ca_certificate=TEST_ROOT_CA_CERT,
                orchestrator_address=TEST_ORC8R_ADDRESS,
                orchestrator_port=TEST_ORC8R_PORT,
                bootstrapper_address=TEST_BOOTSTRAPPER_ADDRESS,
                bootstrapper_port=TEST_BOOTSTRAPPER_PORT,
                fluentd_address=TEST_FLUENTD_ADDRESS,
                fluentd_port=TEST_FLUENTD_PORT,
            )
        self.assertEqual(str(e.value), "Relation orchestrator not yet created")

    @parameterized.expand(
        [
            [-1, 5678, 9112, "Orchestrator port is invalid"],
            [99999, 5678, 9112, "Orchestrator port is invalid"],
            [1234, -1, 9112, "Bootstrapper port is invalid"],
            [1234, 99999, 9112, "Bootstrapper port is invalid"],
            [1234, 5678, -1, "Fluentd port is invalid"],
            [1234, 5678, 99999, "Fluentd port is invalid"],
        ]
    )
    def test_given_orchestrator_port_is_not_valid_when_set_orchestrator_information_then_value_error_is_raised(  # noqa: E501
        self,
        orchestrator_port,
        bootstrapper_port,
        fluentd_port,
        test_expected,
    ):
        self.harness.set_leader(is_leader=True)
        remote_app = "magma-orc8r-requirer"
        self.harness.add_relation(relation_name=self.relation_name, remote_app=remote_app)
        with pytest.raises(ValueError) as e:
            self.harness.charm.orchestrator_provider.set_orchestrator_information(
                root_ca_certificate=TEST_ROOT_CA_CERT,
                orchestrator_address=TEST_ORC8R_ADDRESS,
                orchestrator_port=orchestrator_port,
                bootstrapper_address=TEST_BOOTSTRAPPER_ADDRESS,
                bootstrapper_port=bootstrapper_port,
                fluentd_address=TEST_FLUENTD_ADDRESS,
                fluentd_port=fluentd_port,
            )
        self.assertEqual(str(e.value), test_expected)
