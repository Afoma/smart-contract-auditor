pragma solidity ^0.8.19;

contract V06_TxOrigin {

    address admin;

    constructor() {
        admin = msg.sender;
    }

    function execute() external {

        require(
            tx.origin == admin
        );
    }
}