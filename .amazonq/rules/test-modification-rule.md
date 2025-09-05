# Test Code Modification

## Purpose

This rule modifies test code.

## Instructions

* If added new file in test/services/samples, mask sensitive data. 
    * If accountId is not "000000000000", change it to "000000000000".
    * If values is not "test_user" after "user/", change it to "test_user".
    * Change same values with sourceIPAddress to "127.0.0.1".
    * Change principalId to "YOUR_PRINCIPAL_ID".
    * Change accessKeyId to "YOUR_ACCESS_KEY_ID".
    * If you discover same values in other places, change them in the same way.
* Create test case for the action in test/services/test_services.py file.
    * Create a class and a test case for the service if the class doesn't exist.
    * If the class exists, just create a test case in the class.

## Priority

Low

## Error Handling

N/A