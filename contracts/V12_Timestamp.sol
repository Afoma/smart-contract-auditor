pragma solidity ^0.8.19;

contract V12_Timestamp {

    uint256 public start;

    function expired()
        external
        view
        returns(bool)
    {
        return block.timestamp >
               start + 1 days;
    }
}