// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0;

contract SimplaStorage {
    // This whole block are showing how and what are the types of varieble
    uint256 favoriteNumber; // if you dont pass any value to the variable it will be inicialized with 0

    //bool favorite = false;
    //string favoriteString = "String";
    //int256 favoriteInt = -5;
    //address favoriteAddress = 0xd1A1a01272d523E43cA1D3AB2376476aAcE5e28B;
    //bytes32 favorityBytes = "cat"; // In case of bytes the max we can use is bytes max to 32 from 0 to 32

    // in this block we will create an function
    function Store(uint256 _FavoriteNumber) public returns (uint256) {
        favoriteNumber = _FavoriteNumber;
        return _FavoriteNumber;
    }

    // there are two special types of words here - View and Pure non-states changing functions
    // View -> means that we need to see some state of the blockchain , the blue buttons are blue because they represent the view function
    // Public variable automatically are also "View" functions
    //Pure functiions they are used to do some kind of math the sample bellow
    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    //function retrieve(uint256 FavoriteNumber) public pure {
    //  FavoriteNumber + favoriteNumber;
    //}

    struct People {
        uint256 favoriteNumber;
        string name;
        // in this case struct are taking two parameters ,Number -> favority and Name
    }
    People public person = People({favoriteNumber: 2, name: "John"});

    // Here we will add an array of People
    People[] public people; // This type of array is know as a Dynamic Array , an array tha can change size

    // But we can also buils an Fixed sixe array ,arrays that cant be changed size .like this !
    //People[1] public people; //-> this array can only have one person

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People({favoriteNumber: _favoriteNumber, name: _name})); // a simple way to declare variable is (_favoriteNumber , _name)
        nameToFavoriteNumber[_name] = _favoriteNumber;
        // here we are passing the argumment -> memory -> data will only be store during the execution of the function
        // the other options is to use -> storage -> that means that the data will persist even after the function has finish executed
        // string type are actually an array of bites
        // memory -> only used the data until the fuction is in use after that delete forever
        // Storage -> keeps the data
    }

    // In this section  we will work with Mapping
    // Mapping is a dictionary like data structure with 1 value per key
    mapping(string => uint256) public nameToFavoriteNumber;
}
