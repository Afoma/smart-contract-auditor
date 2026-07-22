pragma solidity ^0.8.19;

contract S04_SecureStorage {

    uint256 value;

    function setValue(
        uint256 x
    )
        external
    {
        value = x;
    }
}