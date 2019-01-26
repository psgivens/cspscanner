# CSP Scanner Requirements

**In Scope** 
* Replace CSP with imposible rules
* Option: Replace CSP reporting url
* Option: Report-Only
* Create a report 
* * report from flow dump
* * filter during report generation
* * Option: Show all 'inline' findings
* User mannually maps the application through browser
* Specify the domain to record
* Simple script which launches firefox with proxy

**Stretch**
* Configure filters for recording
* Record findings in a database

**Out of Scope**
* Spider application
* Record and reply
* Session management
* Automated full site scan
* Authenticate the application
* Replace the session cookie (sticky sessions)

## Notes for further development

**Options**
* Turn on sticky cookies

|                    |  script  | browser |  mitm |
|--------------------|:--------:|:-------:|:-----:|
| Authentication     | x        |         |       |
| Session management |          | x       |       |
| CSP recording      |          |         | x     |
| CSP report         | x        |         | x     |
| Spider             | x        | x       |       |