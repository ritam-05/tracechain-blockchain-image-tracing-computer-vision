// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title ContentRegistry
 * @dev Stores cryptographic fingerprints of verified content to prove authenticity over time.
 */
contract ContentRegistry {
    
    struct Record {
        string sourceUrl;
        uint256 timestamp;
        address registrant;
        bool exists;
    }

    // Mapping a bytes32 fingerprint to its Record
    mapping(bytes32 => Record) public registry;

    // Event emitted when a new record is saved (helps frontends and scripts track history)
    event ContentRegistered(bytes32 indexed fingerprint, string sourceUrl, uint256 timestamp);

    /**
     * @dev Registers a new content fingerprint.
     * @param fingerprint The SHA-256 hash of the canonical content metadata.
     * @param sourceUrl The URL where the original content was found.
     */
    function registerContent(bytes32 fingerprint, string memory sourceUrl) public {
        // Prevent accidental duplicate registrations
        require(!registry[fingerprint].exists, "Fingerprint is already registered!");

        // Save the record
        registry[fingerprint] = Record({
            sourceUrl: sourceUrl,
            timestamp: block.timestamp,
            registrant: msg.sender,
            exists: true
        });

        // Broadcast the event to the blockchain
        emit ContentRegistered(fingerprint, sourceUrl, block.timestamp);
    }

    /**
     * @dev Checks if a fingerprint exists in the registry.
     * @param fingerprint The SHA-256 hash to check.
     * @return bool True if registered, false otherwise.
     */
    function isRegistered(bytes32 fingerprint) public view returns (bool) {
        return registry[fingerprint].exists;
    }
}