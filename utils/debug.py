def print_all_routes(router):
    print("Registered routes:")

    for route in router.routes:
        if not hasattr(route, "path"):
            continue

        if hasattr(route, "methods"):
            methods = ", ".join(sorted(route.methods))
            print(f"{route.name}: {route.path} [{methods}]")
        else:
            print(f"{route.name}: {route.path} [WEBSOCKET]")
