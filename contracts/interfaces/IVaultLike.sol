// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IVaultLike {
    function deposit(uint256 amount) external returns (uint256);

    function totalAssets() external view returns (uint256);

    function totalShares() external view returns (uint256);

    function balanceOf(address user)
        external
        view
        returns (uint256);
}