pragma solidity ^0.8.19;

contract V14_Selfdestruct {

    function kill() external {

        selfdestruct(
            payable(msg.sender)
        );
    }
}