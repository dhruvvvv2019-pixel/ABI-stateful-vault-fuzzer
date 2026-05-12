// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./MockERC20.sol";

contract VulnerableVault {
    MockERC20 public asset;

    mapping(address => uint256) public balanceOf;

    uint256 public totalShares;

    constructor(address _asset) {
        asset = MockERC20(_asset);
    }

    function totalAssets()
        public
        view
        returns (uint256)
    {
        return asset.balanceOf(address(this));
    }

    function deposit(uint256 amount)
        external
        returns (uint256 shares)
    {
        require(amount > 0, "zero deposit");

        uint256 _totalShares = totalShares;
        uint256 _totalAssets = totalAssets();

        if (_totalShares == 0) {
            shares = amount;
        } else {
            // INTENTIONALLY VULNERABLE
            shares =
                (amount * _totalShares) /
                _totalAssets;
        }

        asset.transferFrom(
            msg.sender,
            address(this),
            amount
        );

        balanceOf[msg.sender] += shares;
        totalShares += shares;
    }
}