pragma solidity ^0.8.19;

contract V02_Reentrancy {

    mapping(address => uint256) public credit;

    function donate() external payable {
        credit[msg.sender] += msg.value;
    }

    function claim() external {

        uint256 amount = credit[msg.sender];

        (bool success,) =
            payable(msg.sender).call{value: amount}("");

        require(success);

        credit[msg.sender] = 0;
    }
}