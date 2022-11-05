# STC-2022
Go Big Mode - Our project for Stack The Codes 2022


## Setting Up

### Pip Modules
Use the package maanager [pip] (https://pip.pypa.io/en/stable/) to install the prequisites found in requirements.txt

```bash
pip install django
pip install py-solc-x
pip install web3
```

### Ganache
This project runs off the ganache simulated blockchain, install ganache here (https://trufflesuite.com/ganache/)

Once you have downloaded ganache, start by creating a new project by clicking on *new workspace*.

<img width="854" alt="image" src="https://user-images.githubusercontent.com/47775170/200106196-ae739378-32a1-487c-aeac-6cb386ba3d5e.png">

click on *save workspace*.

<img width="846" alt="image" src="https://user-images.githubusercontent.com/47775170/200106321-98bad9c8-e9d4-41ef-8b78-115cbfff5b56.png">

You will be brought to the following screen.

<img width="846" alt="image" src="https://user-images.githubusercontent.com/47775170/200106343-4bfe596a-63e8-47ad-8052-a80c7c89c7f3.png">

Choose any of the wallets to use as the deployer wallet. Copy and paste the address and private key into *deploy.py*. You can find these by clicking on the key icon next to the wallet. **Below is a sample wallet. Do not use it. Use a wallet that is on your simulated ganache blockchain**

<img width="501" alt="image" src="https://user-images.githubusercontent.com/47775170/200106405-5169730d-7233-434b-8c60-145d3c3214ba.png">




## Usage

### Deploy.py

Start the project by running *deploy.py* it is located at ./welcome/deploy.

```bash
./welcome/deploy
```

### Running the django server

Start the django server in order to access the webpage.

```bash
py manage.py runserver
```

A default admin user will be created. Username: admin Password: root

Feel free to test out the application

## Documentation

### db.sol

The smart contract that django interacts with to store data on the blockchain. Written in solidity

#### Session

Smart contract to store individual sessions of users who log in. Stores username, login date and logout date

```solidity
contract Session {
    string public user;
    uint256 public login_datetime = 0;
    uint256 public logout_datetime = 0;
}
```

##### Constructor

Constructor function to initialise session contract, requires a username and login date.

```solidity
constructor(string memory username, uint256 login) {
        user = username;
        login_datetime = login;
}
```

```solidity
function logoutSession(uint256 logout) public {
        logout_datetime = logout;
}
```
#####
### functions.py






