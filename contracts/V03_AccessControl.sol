pragma solidity ^0.8.19;

contract V03_AccessControl {

    uint256 public total;

    function mint(uint256 amount) public {
        total += amount;
    }
}