// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";

import "../contracts/MockERC20.sol";
import "../contracts/VulnerableVault.sol";

contract Deploy is Script {
    function run() external {
        vm.startBroadcast();

        MockERC20 token = new MockERC20();

        VulnerableVault vault =
            new VulnerableVault(
                address(token)
            );

        token.mint(msg.sender, 1e24);

        console2.log(
            "Token:",
            address(token)
        );

        console2.log(
            "Vault:",
            address(vault)
        );

        vm.stopBroadcast();
    }
}