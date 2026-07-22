pragma solidity ^0.8.19;

contract V01_Reentrancy {

    mapping(address => uint256) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() external {

        uint256 amount = balances[msg.sender];

        require(amount > 0);

        (bool ok,) = msg.sender.call{value: amount}("");

        require(ok);

        balances[msg.sender] = 0;
    }
}