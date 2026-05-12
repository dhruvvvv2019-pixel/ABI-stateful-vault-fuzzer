from oracle import (
    detect_balance_anomaly
)


INITIAL_BALANCE = 10**24


class Executor:

    def __init__(
        self,
        vault,
        token,
        accounts,
        state_manager
    ):

        self.vault = vault

        self.token = token

        self.accounts = accounts

        self.state_manager = (
            state_manager
        )

    def reset_balances(self):

        for actor in self.accounts.values():

            current_balance = (
                self.token
                .functions
                .balanceOf(actor)
                .call()
            )

            if current_balance < INITIAL_BALANCE:

                difference = (
                    INITIAL_BALANCE
                    - current_balance
                )

                self.token.functions.mint(
                    actor,
                    difference
                ).transact({
                    "from": self.accounts[
                        "attacker"
                    ]
                })

    def normalize_args(
        self,
        args,
        actor
    ):

        normalized = []

        for arg in args:

            if arg == "vault":

                normalized.append(
                    self.vault.address
                )

            else:
                normalized.append(arg)

        return normalized

    def run_sequence(
        self,
        sequence
    ):

        self.state_manager.revert()

        self.reset_balances()

        trace = []

        donation_seen = False

        for tx in sequence:

            tx_type = tx["type"]

            function_name = tx[
                "function"
            ]

            actor = tx[
                "actor"
            ]

            args = self.normalize_args(
                tx["args"],
                actor
            )

            address = self.accounts[
                actor
            ]

            try:

                before_assets = (
                    self.vault
                    .functions
                    .totalAssets()
                    .call()
                )

                before_shares = (
                    self.vault
                    .functions
                    .balanceOf(address)
                    .call()
                )

                # =====================
                # VAULT FUNCTION CALL
                # =====================

                if tx_type == "vault":

                    self.token.functions.approve(
                        self.vault.address,
                        2**256 - 1
                    ).transact({
                        "from": address
                    })

                    fn = getattr(
                        self.vault.functions,
                        function_name
                    )

                    fn(*args).transact({
                        "from": address
                    })

                # =====================
                # DIRECT DONATION
                # =====================

                elif tx_type == "donation":

                    self.token.functions.transfer(
                        self.vault.address,
                        args[1]
                    ).transact({
                        "from": address
                    })

                    donation_seen = True

                after_assets = (
                    self.vault
                    .functions
                    .totalAssets()
                    .call()
                )

                after_shares = (
                    self.vault
                    .functions
                    .balanceOf(address)
                    .call()
                )

                # =====================
                # TRUE INFLATION ORACLE
                # =====================

                anomaly = False

                # only deposits can
                # trigger inflation exploit

                if (
                    tx_type == "vault"
                    and function_name == "deposit"
                ):

                    anomaly = (
                        detect_balance_anomaly(
                            actor,
                            before_assets,
                            after_assets,
                            before_shares,
                            after_shares,
                            args[0]
                            if len(args) > 0
                            else 0,
                            donation_seen
                        )
                    )

                trace.append({

                    "type": tx_type,

                    "function": function_name,

                    "actor": actor,

                    "args": args,

                    "before_assets": before_assets,

                    "after_assets": after_assets,

                    "before_shares": before_shares,

                    "after_shares": after_shares,

                    "anomaly": anomaly
                })

                if anomaly:

                    print(
                        "\n🚨 TRUE INFLATION ATTACK FOUND 🚨"
                    )

                    print(trace)

                    return (
                        True,
                        trace
                    )

            except Exception:
                continue

        return (
            False,
            trace
        )