# Postman HTTP Tests

## Description

This folder contains the Postman collection developed as part of the
diploma project **"Functional Testing of the PPL.cz Website"**.

The collection verifies the HTTP response returned by the PPL.cz server
when requesting a non-existent page.

------------------------------------------------------------------------

## Request

**Method:** GET

**URL:**

https://www.ppl.cz/this-page-does-not-exist

------------------------------------------------------------------------

## Implemented Tests

-   Verify HTTP status code **404 Not Found**
-   Verify response time is **less than 500 ms**
-   Verify the **Content-Type** response header contains **text/html**

------------------------------------------------------------------------

## Technologies

-   Postman
-   JavaScript (Postman Tests)

------------------------------------------------------------------------

## Expected Result

All tests should pass successfully:

-   Status code is **404 Not Found**
-   Response time is **\< 500 ms**
-   Content-Type contains **text/html**

------------------------------------------------------------------------

## Files

-   **PPL_HTTP_Tests.postman_collection.json** -- Postman collection
    containing the HTTP tests.
