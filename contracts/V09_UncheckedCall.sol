pragma solidity ^0.8.19;

contract V09_UncheckedCall {

    function pay(address target)
        external
    {
        target.call("");
    }
}