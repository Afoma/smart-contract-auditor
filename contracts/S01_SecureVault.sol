pragma solidity ^0.8.19;

contract S01_SecureVault {

    address owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function withdraw()
        external
        onlyOwner
    {
    }
}