*** Settings ***
Documentation     Robot Framework Demo Test Suite
...               Demonstrating Keyword-Driven Testing for QA Automation.
Library           RequestsLibrary
Library           Collections

Suite Setup       Create Session    sut    ${BASE_URL}

*** Variables ***
${BASE_URL}       http://127.0.0.1:8000
${VALID_USER}     student@test.com
${VALID_PASS}     Password123!

*** Test Cases ***
Scenario 1: Health Check Endpoint Returns 200 And Healthy
    [Documentation]    Verify API server availability
    [Tags]             smoke    health
    ${response}=       GET On Session    sut    /api/health
    Status Should Be   200    ${response}
    ${json}=           Set Variable      ${response.json()}
    Should Be Equal As Strings           ${json['status']}    healthy

Scenario 2: Retrieve Product Catalog Successfully
    [Documentation]    Validate product catalog response has items
    [Tags]             regression    products
    ${response}=       GET On Session    sut    /api/products
    Status Should Be   200    ${response}
    ${products}=       Set Variable      ${response.json()}
    Length Should Be Greater Than        ${products}    0
    Dictionary Should Contain Key        ${products[0]}    name

Scenario 3: User Authentication Valid Credentials
    [Documentation]    Keyword-driven test for successful user login
    [Tags]             auth    smoke
    ${body}=           Create Dictionary    email=${VALID_USER}    password=${VALID_PASS}
    ${response}=       POST On Session   sut    /api/login    json=${body}
    Status Should Be   200    ${response}
    Dictionary Should Contain Key        ${response.json()}    token
    Should Be Equal As Strings           ${response.json()['user']}    QA Student

Scenario 4: User Authentication Rejects Invalid Password
    [Documentation]    Negative test expecting 401 Unauthorized
    [Tags]             auth    negative
    ${body}=           Create Dictionary    email=${VALID_USER}    password=BadPassword
    ${response}=       POST On Session   sut    /api/login    json=${body}    expected_status=401
    Status Should Be   401    ${response}
    Dictionary Should Contain Key        ${response.json()}    error
