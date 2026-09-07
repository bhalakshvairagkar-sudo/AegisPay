"""
AegisPay v2 - Relational Entity Graph
Tracks topology, fan-outs, concentration, and cross-entity reuse across users, devices, accounts, merchants, and beneficiaries.
"""

from typing import Dict, Any, List, Set, Optional
from collections import defaultdict


class RelationalEntityGraph:
    """In-memory relational graph computing topological fraud signals."""

    def __init__(self):
        # device_id -> set of account_ids
        self.device_to_accounts: Dict[str, Set[str]] = defaultdict(set)
        # account_id -> set of device_ids
        self.account_to_devices: Dict[str, Set[str]] = defaultdict(set)
        # account_id -> set of beneficiary_ids
        self.account_to_beneficiaries: Dict[str, Set[str]] = defaultdict(set)
        # beneficiary_id -> set of sending account_ids (fan-in)
        self.beneficiary_to_accounts: Dict[str, Set[str]] = defaultdict(set)
        # device_id -> set of merchant_ids
        self.device_to_merchants: Dict[str, Set[str]] = defaultdict(set)
        # user_id -> set of device_ids
        self.user_to_devices: Dict[str, Set[str]] = defaultdict(set)

    def record_transaction_event(
        self,
        user_id: str,
        account_id: str,
        device_id: str,
        merchant_id: Optional[str] = None,
        beneficiary_id: Optional[str] = None
    ):
        """Records an observed interaction in the relational graph."""
        if device_id and account_id:
            self.device_to_accounts[device_id].add(account_id)
            self.account_to_devices[account_id].add(device_id)

        if user_id and device_id:
            self.user_to_devices[user_id].add(device_id)

        if account_id and beneficiary_id:
            self.account_to_beneficiaries[account_id].add(beneficiary_id)
            self.beneficiary_to_accounts[beneficiary_id].add(account_id)

        if device_id and merchant_id:
            self.device_to_merchants[device_id].add(merchant_id)

    def get_device_account_fanout(self, device_id: str) -> int:
        """Number of distinct accounts accessed from this device."""
        return len(self.device_to_accounts.get(device_id, set()))

    def get_account_device_fanout(self, account_id: str) -> int:
        """Number of distinct devices used by this account."""
        return len(self.account_to_devices.get(account_id, set()))

    def get_beneficiary_fanin(self, beneficiary_id: str) -> int:
        """Number of distinct sending accounts transferring into this beneficiary."""
        return len(self.beneficiary_to_accounts.get(beneficiary_id, set()))

    def is_cross_account_device_reuse(self, device_id: str) -> bool:
        """Returns True if device is shared across 3 or more distinct accounts."""
        return self.get_device_account_fanout(device_id) >= 3

    def get_graph_relational_features(
        self,
        user_id: str,
        account_id: str,
        device_id: str,
        beneficiary_id: Optional[str] = None,
        merchant_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Extracts numerical graph signals for feature pipelines."""
        dev_fanout = self.get_device_account_fanout(device_id)
        acct_fanout = self.get_account_device_fanout(account_id)
        ben_fanin = self.get_beneficiary_fanin(beneficiary_id) if beneficiary_id else 1
        is_shared = 1 if self.is_cross_account_device_reuse(device_id) else 0

        # Normalized risk contributions
        fanout_risk = min(1.0, (dev_fanout - 1) * 0.25)
        mule_fanin_risk = min(1.0, (ben_fanin - 1) * 0.30)

        return {
            "device_account_fanout": dev_fanout,
            "account_device_fanout": acct_fanout,
            "beneficiary_fanin_count": ben_fanin,
            "cross_account_device_reuse_flag": is_shared,
            "graph_fanout_risk_score": round(fanout_risk, 4),
            "graph_mule_risk_score": round(mule_fanin_risk, 4)
        }


entity_graph = RelationalEntityGraph()
