pragma solidity ^0.8.19;

contract V08_Delegatecall {

    address public impl;

    function upgrade(
        bytes calldata data
    ) external {

        impl.delegatecall(data);
    }
}