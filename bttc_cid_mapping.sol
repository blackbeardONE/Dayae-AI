// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BTTC_CID_Mapping {
    // Mapping from user address to array of encrypted CIDs
    mapping(address => string[]) private userCIDs;

    // Event emitted when a new CID is stored
    event CIDStored(address indexed user, string cid);

    /**
     * @dev Store a new encrypted CID for the sender's address.
     * @param cid The encrypted CID string to store.
     */
    function storeCID(string calldata cid) external {
        require(bytes(cid).length > 0, "CID cannot be empty");
        userCIDs[msg.sender].push(cid);
        emit CIDStored(msg.sender, cid);
    }

    /**
     * @dev Retrieve all encrypted CIDs stored for a user address.
     * @param user The address of the user.
     * @return An array of encrypted CID strings.
     */
    function getCIDs(address user) external view returns (string[] memory) {
        return userCIDs[user];
    }
}
