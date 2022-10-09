// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

contract passwordStorage {
    struct Password {
        string username;
        string password;
    }

    Password[] public Passwords;

    function create(string calldata _username, string calldata _password)
        external
    {
        Passwords.push(Password({username: _username, password: _password}));
    }

    function update(uint _index, string calldata _password) external {
        Password storage password = Passwords[_index];
        password.password = _password;
    }

    function get(uint _index)
        external
        view
        returns (string memory, string memory)
    {
        Password memory password = Passwords[_index];
        return (password.username, password.password);
    }
}
