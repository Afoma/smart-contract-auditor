pragma solidity ^0.8.19;

contract V05_TxOrigin {

    address owner;

    constructor() {
        owner = msg.sender;
    }

    function withdraw() public {

        require(
            tx.origin == owner
        );

        payable(msg.sender).transfer(
            address(this).balance
        );
    }
}