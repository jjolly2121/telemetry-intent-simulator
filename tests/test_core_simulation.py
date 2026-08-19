import json
import unittest

from intent_manager import IntentManager, IntentStatus
from safety_gate import SafetyGate
from simulation_bootstrap import build_simulation
from state_engine import SystemState


class IntentManagerTests(unittest.TestCase):
    def test_completed_intent_is_archived(self):
        manager = IntentManager()
        intent = manager.submit_intent("orbit_correction")

        manager.mark_active(intent)
        self.assertEqual(intent.status, IntentStatus.ACTIVE)

        manager.mark_completed(intent)
        manager.archive_completed()

        self.assertEqual(manager.list_active(), [])


class SafetyGateTests(unittest.TestCase):
    def test_safe_mode_blocks_mission_intent(self):
        manager = IntentManager()
        mission_intent = manager.submit_intent("orbit_correction")
        system_state = SystemState()
        system_state.mode = "SAFE"

        decision = SafetyGate().evaluate(mission_intent, system_state)

        self.assertTrue(decision.blocked)
        self.assertEqual(decision.reason, "safe_mode_mission_blocked")


class OrchestratorTests(unittest.TestCase):
    def test_critical_battery_overrides_mission_with_recovery(self):
        system_state, _, telemetry_bus, orchestrator = build_simulation()

        orchestrator.run(cycles=1)

        frame = telemetry_bus.get_frames()[0]["data"]
        self.assertTrue(frame["execution"]["override_applied"])
        self.assertIsNotNone(frame["execution"]["executed_intent_id"])
        self.assertEqual(frame["state"]["mode"], "SAFE")
        self.assertEqual(frame["state"]["position"], 0.0)
        self.assertGreater(frame["state"]["battery_level"], 4.0)

    def test_each_cycle_emits_json_safe_telemetry(self):
        _, _, telemetry_bus, orchestrator = build_simulation()

        orchestrator.run(cycles=5)

        frames = telemetry_bus.get_frames()
        self.assertEqual(len(frames), 5)
        json.dumps(frames)


if __name__ == "__main__":
    unittest.main()
