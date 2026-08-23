"""
Synthetic Device Fingerprint & Telemetry Generator
Models hardware configurations, operating systems, and biometric sensor noise.
"""

from dataclasses import dataclass
from typing import List, Optional
import numpy as np


@dataclass
class DeviceFingerprint:
    device_id: str
    os_family: str
    browser_type: str
    is_mobile: bool
    is_emulator: bool
    base_familiarity: float
    touch_sensor_noise: float


def generate_device_pool(n_devices: int = 150, seed: int = 42) -> List[DeviceFingerprint]:
    """Generates a seeded pool of hardware device fingerprints."""
    rng = np.random.default_rng(seed)
    devices = []

    os_choices = ["iOS", "Android", "macOS", "Windows", "Linux"]
    os_probs = [0.42, 0.38, 0.10, 0.08, 0.02]

    for i in range(n_devices):
        os_name = str(rng.choice(os_choices, p=os_probs))
        is_mobile = os_name in ["iOS", "Android"]
        browser = "Mobile Safari" if os_name == "iOS" else ("Chrome Mobile" if os_name == "Android" else "Chrome")
        is_emulator = False

        devices.append(DeviceFingerprint(
            device_id=f"DEV-{30000 + i}",
            os_family=os_name,
            browser_type=browser,
            is_mobile=is_mobile,
            is_emulator=is_emulator,
            base_familiarity=float(rng.uniform(0.7, 1.0)),
            touch_sensor_noise=float(rng.uniform(0.02, 0.08)),
        ))

    return devices
