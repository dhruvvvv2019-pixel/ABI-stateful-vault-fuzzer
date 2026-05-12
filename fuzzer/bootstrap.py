import json

from web3 import Web3

RPC_URL = "http://127.0.0.1:8545"


STATE_MUTABILITY_BLACKLIST = {
    "view",
    "pure"
}


BLACKLISTED_FUNCTIONS = {
    "name",
    "symbol",
    "decimals",
    "totalSupply",
    "balanceOf",
    "allowance"
}


def load_artifact(path):

    with open(path, "r") as f:
        return json.load(f)


def load_contract(
    w3,
    artifact_path,
    address
):

    artifact = load_artifact(
        artifact_path
    )

    return w3.eth.contract(
        address=w3.to_checksum_address(address),
        abi=artifact["abi"]
    )


def discover_functions(contract):

    discovered = []

    for item in contract.abi:

        if item["type"] != "function":
            continue

        if item.get(
            "stateMutability"
        ) in STATE_MUTABILITY_BLACKLIST:
            continue

        function_name = item["name"]

        if function_name in BLACKLISTED_FUNCTIONS:
            continue

        discovered.append({
            "name": function_name,
            "inputs": item.get("inputs", [])
        })

    return discovered


def setup():

    w3 = Web3(
        Web3.HTTPProvider(
            RPC_URL
        )
    )

    if not w3.is_connected():

        raise Exception(
            "Failed to connect to Anvil"
        )

    print(
        "\nConnected to Anvil\n"
    )

    vault_address = input(
        "Enter deployed vault address: "
    ).strip()

    token_address = input(
        "Enter deployed token address: "
    ).strip()

    vault = load_contract(
        w3,
        "../out/VulnerableVault.sol/VulnerableVault.json",
        vault_address
    )

    token = load_contract(
        w3,
        "../out/MockERC20.sol/MockERC20.json",
        token_address
    )

    vault_code = w3.eth.get_code(
        w3.to_checksum_address(
            vault_address
        )
    )

    if vault_code == b'':

        raise Exception(
            "Vault contract not found"
        )

    discovered_functions = discover_functions(
        vault
    )

    print(
        "\nDiscovered Functions:"
    )

    for fn in discovered_functions:

        print(
            f"- {fn['name']}"
        )

    accounts = {

        "attacker":
            w3.eth.accounts[1],

        "victim":
            w3.eth.accounts[2],
    }

    return (
        w3,
        vault,
        token,
        accounts,
        discovered_functions
    )