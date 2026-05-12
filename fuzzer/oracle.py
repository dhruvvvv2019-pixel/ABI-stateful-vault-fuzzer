def detect_balance_anomaly(
    actor,
    before_assets,
    after_assets,
    before_shares,
    after_shares,
    amount,
    donation_seen
):

    # assets must increase
    if after_assets <= before_assets:
        return False

    minted = (
        after_shares
        - before_shares
    )

    # TRUE inflation attack:
    #
    # 1. donation manipulation happened
    # 2. victim deposits
    # 3. victim gets zero shares

    if (
        donation_seen
        and actor == "victim"
        and amount > 0
        and minted == 0
    ):

        return True

    return False