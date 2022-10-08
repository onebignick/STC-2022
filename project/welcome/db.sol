// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

contract Storage {
    string passwordHash;

    struct Passwords {
        string passwordHash;
        string name;
    }

    Passwords[] public password;
    mapping(string => string) public userToPassword;

    function store(string memory _passwordHash) public {
        passwordHash = _passwordHash;
    }

    function retrieve() public view returns (string memory) {
        return passwordHash;
    }

    function addPassword(string memory _username, string memory _passwordHash)
        public
    {
        password.push(Passwords(_passwordHash, _username));
        userToPassword[_username] = _passwordHash;
    }
}
