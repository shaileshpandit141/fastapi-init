app
├── core/
├── infrastructure
│   ├── __init__.py
│   ├── db/
│   ├── email/
│   ├── messaging/
│   ├── rate_limit/
│   ├── redis/
│   └── security
│       ├── jwt/
│       ├── one_time_password/
│       └── password/
├── __init__.py
├── main.py
├── modules
│   ├── access_control
│   │   ├── dependencies.py
│   │   ├── domain # models/
│   │   │   ├── enums.py
│   │   │   ├── __init__.py
│   │   │   ├── permission.py
│   │   │   ├── role.py
│   │   │   ├── role_permission.py
│   │   │   └── user_role.py
│   │   ├── __init__.py
│   │   ├── policies
│   │   │   ├── __init__.py
│   │   │   ├── permission.py
│   │   │   ├── role_permission.py
│   │   │   ├── role.py
│   │   │   └── user_role.py
│   │   ├── repositories
│   │   │   ├── __init__.py
│   │   │   ├── permission.py
│   │   │   ├── role_permission.py
│   │   │   ├── role.py
│   │   │   └── user_role.py
│   │   ├── routes.py
│   │   ├── schemas
│   │   │   ├── __init__.py
│   │   │   ├── permission.py
│   │   │   ├── role_permission.py
│   │   │   ├── role.py
│   │   │   └── user_role.py
│   │   └── services
│   │       ├── __init__.py
│   │       ├── permission.py
│   │       ├── role_permission.py
│   │       ├── role.py
│   │       └── user_role.py
│   ├── __init__.py
│   └── users
│       ├── dependencies.py
│       ├── domain # models/
│       │   ├── enums.py
│       │   ├── __init__.py
│       │   └── user.py
│       ├── __init__.py
│       ├── policies
│       │   ├── __init__.py
│       │   └── user.py
│       ├── repositories
│       │   ├── __init__.py
│       │   └── user.py
│       ├── routes.py
│       ├── schemas
│       │   ├── __init__.py
│       │   └── user.py
│       └── services
│           ├── __init__.py
│           └── user.py
└── shared
    ├── enums
    │   ├── __init__.py
    │   ├── permission.py
    │   └── role.py
    ├── __init__.py
    ├── policies
    │   ├── base.py
    │   └── __init__.py
    └── response
        ├── __init__.py
        └── schemas.py

