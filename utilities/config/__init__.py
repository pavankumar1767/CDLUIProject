
def load_config(env):
    """
    Load the configuration for the specified environment.

    :param env: The environment (e.g., 'stage', 'qa', 'prod').
    :return: The configuration class for the specified environment.
    """
    if env == "stage":
        from .config_stage import Config
    elif env == "qa":
        from .config_qa import Config
    elif env == "prod":
        from .config_prod import Config
    else:
        raise ValueError(f"Unsupported environment: {env}")

    return Config