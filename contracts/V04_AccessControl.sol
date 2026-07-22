pragma solidity ^0.8.19;

contract V04_AccessControl {

    address public owner;

    function withdraw() public {
        payable(msg.sender).transfer(
            address(this).balance
        );
    }
}