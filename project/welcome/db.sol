// SPDX-License-Identifier: MIT
pragma solidity 0.8.7;

contract Session {
    string public user;
    uint256 public login_datetime = 0;
    uint256 public logout_datetime = 0;

    constructor(string memory username, uint256 login) {
        user = username;
        login_datetime = login;
    }

    function logoutSession(uint256 logout) public {
        logout_datetime = logout;
    }

    function getLoginDatetime() public view returns (uint256) {
        return login_datetime;
    }

    function getLogoutDatetime() public view returns (uint256) {
        return logout_datetime;
    }

    function getUser() public view returns (string memory) {
        return user;
    }
}

contract Users {
    event LoginEvent(address value);
    event LogoutEvent(string value);

    struct UserData {
        string user;
        string password;
        string role;
        uint256 click;
    }

    mapping(string => UserData) private users;
    mapping(string => address[]) private sessions;
    string[] lookup;

    constructor() {}

    function getUser(string memory key)
        public
        view
        returns (string memory user, string memory password)
    {
        return (users[key].user, users[key].password);
    }

    function login(string memory user, string memory password) public {
        bool result = compareStrings(users[user].password, password);

        if (result) {
            Session session = new Session(user, block.timestamp);
            sessions[user].push(address(session));
            emit LoginEvent(address(session));
        } else {
            emit LoginEvent(address(0));
        }
    }

    function logout(string memory user, address session) public returns (bool) {
        address[] storage sessionList = sessions[user];
        for (uint256 i = 0; i < sessionList.length; i++) {
            if (sessionList[i] == session) {
                Session(sessionList[i]).logoutSession(block.timestamp);
                sessionList[i] = sessionList[sessionList.length - 1];
                sessionList.pop();
                emit LogoutEvent("logout successful");
                return true;
            }
        }

        emit LogoutEvent("logout failed");
        return false;
    }

    function getAllUsers() public view returns (UserData[] memory) {
        UserData[] memory allUsers = new UserData[](lookup.length);
        for (uint256 i = 0; i < lookup.length; i++) {
            allUsers[i] = users[lookup[i]];
        }
        return allUsers;
    }

    function addUser(string memory user, string memory password) public {
        require(compareStrings(users[user].user, ""), "User already exists.");
        string memory role = "user";
        uint256 click = 0
        UserData memory newUser = UserData(user, password, role, click);
        users[user] = newUser;
        lookup.push(user);
    }

    function updateUser(string memory user, string memory role) public {
        UserData storage updated = users[user];
        users[user].role = role;
        users[user] = updated;
    }

    function updatePassword(
        string memory user,
        string memory old_password,
        string memory new_password
    ) public {
        require(
            compareStrings(old_password, users[user].password),
            "Wrong password"
        );
        users[user].password = new_password;
    }

    function compareStrings(string memory a, string memory b)
        public
        pure
        returns (bool)
    {
        return (keccak256(abi.encodePacked((a))) ==
            keccak256(abi.encodePacked((b))));
    }

    function deleteUser(string memory user) public {
        delete users[user];
        for (uint256 i = 0; i < lookup.length; i++) {
            if (compareStrings(lookup[i], user)) {
                lookup[i] = lookup[lookup.length - 1];
                lookup.pop();
            }
        }
    }
}
