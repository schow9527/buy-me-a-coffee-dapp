// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title BuyMeACoffee
 * @dev 链上咖啡打赏与留言智能合约 (SC6113 DApp)
 */
contract BuyMeACoffee {
    // 咖啡赞助记录结构体
    struct Memo {
        address from;
        uint256 timestamp;
        string name;
        string message;
        uint256 amount;
    }

    // 所有赞助记录存储
    Memo[] private memos;

    // 创作者收款钱包地址 (合约部署者)
    address payable public owner;

    // 购买咖啡事件
    event NewCoffee(
        address indexed from,
        uint256 timestamp,
        string name,
        string message,
        uint256 amount
    );

    constructor() {
        owner = payable(msg.sender);
    }

    /**
     * @dev 购买咖啡：向创作者转账 ETH 并附带留言
     * @param _name 赞助者昵称
     * @param _message 赞助者留言
     */
    function buyCoffee(string memory _name, string memory _message) public payable {
        require(msg.value > 0, "Amount must be greater than 0");

        // 记录到链上数组
        memos.push(Memo(
            msg.sender,
            block.timestamp,
            _name,
            _message,
            msg.value
        ));

        // 将收到的 ETH 自动转给创作者
        owner.transfer(msg.value);

        // 触发事件通知前端
        emit NewCoffee(msg.sender, block.timestamp, _name, _message, msg.value);
    }

    /**
     * @dev 获取链上所有的打赏记录
     */
    function getMemos() public view returns (Memo[] memory) {
        return memos;
    }

    /**
     * @dev 获取最后一条打赏记录（方便像课件一样直接读取元组展示）
     */
    function getLastMemo() public view returns (
        address from,
        string memory name,
        string memory message,
        uint256 amount
    ) {
        if (memos.length == 0) {
            return (address(0), "", "", 0);
        }
        Memo memory last = memos[memos.length - 1];
        return (last.from, last.name, last.message, last.amount);
    }
}
