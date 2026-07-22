pragma solidity ^0.8.19;

contract V11_Timestamp {

    function winner()
        external
        view
        returns(bool)
    {
        return block.timestamp % 2 == 0;
    }
}