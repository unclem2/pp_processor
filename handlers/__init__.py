import importlib
import logging
import os

import coloredlogs

coloredlogs.install(level=logging.INFO, format="[%(levelname)s] %(message)s")


def load_routers():
    modules = []
    base_dir = os.path.basename(os.path.dirname(__file__))
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file != "router.py":
                continue
            path = os.path.join(root, file)[:-3]
            import_path = path.replace("/", ".")

            try:
                module = importlib.import_module(import_path)
                if not hasattr(module, "router"):
                    continue

                router = module.router

                logging.info(
                    f"✔ Loaded: {router.prefix} → Route: {router.prefix}",
                )
                modules.append(router)
            except Exception as e:
                logging.exception("✘ Failed to load: %s", import_path)
                logging.exception("  Reason: %s", e)
    return modules
