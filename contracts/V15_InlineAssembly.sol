pragma solidity ^0.8.19;

contract V15_InlineAssembly {

    function test()
        external
        pure
        returns(uint256 x)
    {
        assembly {
            x := 42
        }
    }
}