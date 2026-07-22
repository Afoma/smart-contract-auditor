pragma solidity ^0.8.19;

contract S02_SecureWallet {

    mapping(address => uint256)
        public balances;

    function deposit()
        external
        payable
    {
        balances[msg.sender] += msg.value;
    }
}