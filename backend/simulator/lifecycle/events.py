"""
AegisPay v2 - Payment Lifecycle Events
Message-level event definitions for multi-stage payment flows.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import time


@dataclass
class PaymentLifecycleEvent:
    event_id: str
    transaction_id: str
    stage: str  # INITIATION, AUTHENTICATION, AUTHORIZATION, PRESENTMENT, SETTLEMENT, DISPUTE
    timestamp_epoch: float
    timestamp_iso: str
    state_payload: Dict[str, Any]
    is_terminal: bool = False


@dataclass
class PaymentSessionLifecycle:
    session_id: str
    transaction_id: str
    rail: str
    current_stage: str
    events: List[PaymentLifecycleEvent] = field(default_factory=list)
    is_completed: bool = False
    is_disputed: bool = False

    def add_event(self, stage: str, payload: Dict[str, Any], timestamp_offset_seconds: float = 0.0) -> PaymentLifecycleEvent:
        now = time.time() + timestamp_offset_seconds
        iso_ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))
        evt = PaymentLifecycleEvent(
            event_id=f"EVT-{self.transaction_id[:8]}-{len(self.events) + 1}",
            transaction_id=self.transaction_id,
            stage=stage,
            timestamp_epoch=now,
            timestamp_iso=iso_ts,
            state_payload=payload,
            is_terminal=(stage in ["SETTLEMENT", "DISPUTE", "REVERSED", "BLOCKED"])
        )
        self.events.append(evt)
        self.current_stage = stage
        if evt.is_terminal:
            self.is_completed = True
        return evt
