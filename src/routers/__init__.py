from routers import task, token, auth, users

routers = (
    task.router,
    token.router,
    auth.router,
    users.router,
)

