from flask import current_app

def is_feature_enabled(flag_name):
    return current_app.config.get("FEATURE_FLAGS", {}).get(flag_name, False)