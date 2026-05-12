def minimize_sequence(
    sequence,
    executor
):

    minimized = sequence.copy()

    changed = True

    while changed:

        changed = False

        for i in range(
            len(minimized)
        ):

            candidate = (
                minimized[:i]
                +
                minimized[i+1:]
            )

            found, _ = (
                executor.run_sequence(
                    candidate
                )
            )

            if found:

                minimized = candidate

                changed = True

                break

    return minimized