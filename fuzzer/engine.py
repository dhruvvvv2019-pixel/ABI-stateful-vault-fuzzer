import json

from bootstrap import setup

from state import StateManager

from executor import Executor

from sequences import (
    generate_sequence,
    mutate_sequence
)

from minimizer import (
    minimize_sequence
)

from config import *


def save_exploit(
    sequence,
    trace
):

    with open(
        "exploit.json",
        "w"
    ) as f:

        json.dump({

            "sequence": sequence,

            "trace": trace

        }, f, indent=4)

    print(
        "\nSaved exploit trace to exploit.json"
    )


(
    w3,
    vault,
    token,
    accounts,
    discovered_functions
) = setup()


state_manager = StateManager(
    w3
)


executor = Executor(
    vault,
    token,
    accounts,
    state_manager
)


population = []

for _ in range(
    POPULATION_SIZE
):

    population.append(
        generate_sequence(
            discovered_functions
        )
    )


for iteration in range(
    ITERATIONS
):

    print(
        f"Iteration: {iteration}"
    )

    next_population = []

    for sequence in population:

        found, trace = (
            executor.run_sequence(
                sequence
            )
        )

        if found:

            minimized = (
                minimize_sequence(
                    sequence,
                    executor
                )
            )

            print(
                "\n🚨 EXPLOIT FOUND 🚨"
            )

            print(minimized)

            save_exploit(
                minimized,
                trace
            )

            exit(0)

        mutated = mutate_sequence(
            sequence,
            discovered_functions
        )

        next_population.append(
            mutated
        )

    population = next_population


print(
    "\nNo exploit discovered."
)