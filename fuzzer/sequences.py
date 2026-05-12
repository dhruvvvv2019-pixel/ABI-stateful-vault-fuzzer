import random

from config import *

ACTORS = [
    "attacker",
    "victim"
]


def generate_argument(param_type):

    if "uint" in param_type:

        return random.randint(
            1,
            10**12
        )

    elif param_type == "address":

        return "vault"

    elif param_type == "bool":

        return random.choice([
            True,
            False
        ])

    return 1


def build_transaction(
    function_meta
):

    args = []

    for inp in function_meta[
        "inputs"
    ]:

        args.append(
            generate_argument(
                inp["type"]
            )
        )

    return {

        "type": "vault",

        "function": function_meta[
            "name"
        ],

        "args": args,

        "actor": random.choice(
            ACTORS
        )
    }


def build_donation_transaction():

    return {

        "type": "donation",

        "function": "transfer",

        "args": [
            "vault",
            random.randint(
                10**8,
                10**12
            )
        ],

        "actor": "attacker"
    }


def generate_sequence(
    discovered_functions,
    depth=INITIAL_DEPTH
):

    sequence = []

    for _ in range(depth):

        # 30% chance direct donation
        if random.random() < 0.3:

            tx = (
                build_donation_transaction()
            )

        else:

            fn = random.choice(
                discovered_functions
            )

            tx = build_transaction(fn)

        sequence.append(tx)

    return sequence


def mutate_sequence(
    sequence,
    discovered_functions
):

    new_sequence = sequence.copy()

    for i in range(
        len(new_sequence)
    ):

        if (
            random.random()
            < MUTATION_RATE
        ):

            if random.random() < 0.3:

                new_sequence[i] = (
                    build_donation_transaction()
                )

            else:

                fn = random.choice(
                    discovered_functions
                )

                new_sequence[i] = (
                    build_transaction(fn)
                )

    if (
        random.random() < 0.2
        and len(new_sequence)
        < MAX_DEPTH
    ):

        if random.random() < 0.3:

            new_sequence.append(
                build_donation_transaction()
            )

        else:

            fn = random.choice(
                discovered_functions
            )

            new_sequence.append(
                build_transaction(fn)
            )

    return new_sequence