app/
│
├── api/
│   ├── router.py
│   └── v1/
│       ├── auth/
│       │   ├── router.py
│       │   └── schema.py
│       │
│       ├── user/
│       │   ├── router.py
│       │   └── schema.py
│       │
│       └── health/
│           └── router.py
│
├── domain/
│   ├── auth/
│   │   ├── actor.py
│   │   └── policies.py
│   │
│   └── user/
│       ├── model.py
│       └── policies.py
│
├── use/
│   ├── auth/
│   │   ├── login.py
│   │   ├── refresh.py
│   │   └── register.py
│   │
│   └── user/
│       ├── create.py
│       ├── get.py
│       ├── list.py
│       └── update.py
│
├── infra/
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── email/
│   ├── messaging/
│   ├── redis/
│   ├── rate_limit/
│   └── security/
│
├── core/
│   ├── config.py
│   ├── exceptions.py
│   ├── exc_handlers.py
│   ├── lifespan.py
│   ├── logging.py
│   └── middleware.py
│
├── main.py
└── __init__.py
