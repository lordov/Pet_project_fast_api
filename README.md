
```
pet_project
├─ .env
├─ .gitignore
└─ src
   ├─ api
   │  ├─ auth
   │  │  ├─ models.py
   │  │  ├─ router.py
   │  │  └─ schemas.py
   │  ├─ dependencies
   │  ├─ pages
   │  │  └─ router.py
   │  ├─ tasks
   │  │  ├─ models.py
   │  │  ├─ router.py
   │  │  └─ schemas.py
   │  └─ users
   │     ├─ models.py
   │     ├─ router.py
   │     └─ schemas.py
   ├─ core
   │  ├─ celery_app.py
   │  ├─ config.py
   │  └─ security.py
   ├─ crud
   │  ├─ base.py
   │  ├─ task.py
   │  └─ user.py
   ├─ db
   │  ├─ base.py
   │  ├─ db.py
   │  └─ repositories
   │     ├─ base.py
   │     ├─ task_repository.py
   │     └─ user_repository.py
   ├─ main.py
   ├─ services
   │  ├─ auth.py
   │  ├─ tasks.py
   │  ├─ unit_of_work.py
   │  └─ user.py
   ├─ tests
   │  ├─ test_auth.py
   │  ├─ test_tasks.py
   │  ├─ test_users.py
   │  └─ __init__.py
   └─ utils
      ├─ email.py
      └─ jwt.py

```