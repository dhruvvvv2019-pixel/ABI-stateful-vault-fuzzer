class StateManager:
    def __init__(self, w3):
        self.w3 = w3
        self.snapshot_id = None

    def snapshot(self):
        self.snapshot_id = (
            self.w3.provider.make_request(
                "evm_snapshot",
                []
            )["result"]
        )

    def revert(self):
        if self.snapshot_id:
            self.w3.provider.make_request(
                "evm_revert",
                [self.snapshot_id]
            )

            self.snapshot()