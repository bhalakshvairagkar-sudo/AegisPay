"""
AegisPay v2 - Device Entity
Synthetic device fingerprint representation with hardware age, OS family, and network telemetry.
"""

from typing import Dict, Any, List
from dataclasses import dataclass, field
import hashlib


@dataclass
class DeviceEntity:
    device_id: str
    device_fingerprint_id: str  # Synthetic representation of hardware canvas/WebGL profile
    os_family: str  # iOS, Android, Windows, macOS, Linux
    browser_family: str  # Chrome, Safari, Firefox, Edge, MobileAppWebView
    device_age_days: int
    is_rooted_or_emulator: bool = False
    bound_accounts: List[str] = field(default_factory=list)
    last_known_ip: str = "192.168.1.100"

    @classmethod
    def create_synthetic(cls, device_id: str, os_family: str, browser_family: str, age_days: int, is_rooted: bool = False) -> "DeviceEntity":
        fp_raw = f"{device_id}:{os_family}:{browser_family}:{age_days}"
        fp_id = f"FP-{hashlib.sha256(fp_raw.encode()).hexdigest()[:12]}"
        return cls(
            device_id=device_id,
            device_fingerprint_id=fp_id,
            os_family=os_family,
            browser_family=browser_family,
            device_age_days=age_days,
            is_rooted_or_emulator=is_rooted
        )

    def compute_fanout(self) -> int:
        """Returns the number of unique accounts accessed from this device."""
        return len(set(self.bound_accounts))
