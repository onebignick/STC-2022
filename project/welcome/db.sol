// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

contract userData {
    // Data structure of each user
    struct user {
        string username;
        string password;
    }

    // Hash each username to data
    mapping(string => uint256) UserID;
    user[] public Users;

    function create_user(string calldata _username, string calldata _password)
        public
    {
        Users.push(user({username: _username, password: _password}));
        uint256 _userID = Users.length - 1;
        UserID[_username] = _userID;
    }

    function update_user_password(
        string calldata _username,
        string calldata _password
    ) public {
        uint256 _userID = UserID[_username];
        Users[_userID].password = _password;
    }

    function get_user_password(string calldata _username)
        external
        view
        returns (string memory)
    {
        uint256 _userID = UserID[_username];
        return (Users[_userID].password);
    }
}
