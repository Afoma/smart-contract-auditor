pragma solidity ^0.8.19;

contract V07_Delegatecall {

    function run(
        address target,
        bytes calldata data
    ) external {

        target.delegatecall(data);
    }
}