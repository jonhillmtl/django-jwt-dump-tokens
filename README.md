# Overview

Dump JSON Web Tokens for a Django project

## Installation

`pip install git+https://github.com/jonhillmtl/django-jwt-dump-tokens`

## Usage

- make sure a `JWT_KEY` is set
- ensure your project has a database configured and a User table present
- `jwt_dump_tokens`
    - run it from the same directory as `settings`, it will discover the settings file and modify the PYTHONPATH accordingly
    
```
Usage: jwt_dump_tokens [options]

Options:
  -h, --help            show this help message and exit
  --user_ids=USER_IDS   specify user ids, comma separated
  --user_emails=USER_EMAILS
                        specify user emails, comma separated
  --order_by=ORDER_BY   specify sort order [id, email, username]
  --sort_direction=SORT_DIRECTION
                        specify sort direction [asc, desc]
  --as_json             output as json

```


