def test_core_imports_do_not_start_runtime():
    import config
    import core.effects
    import core.event_manager
    import main

    assert config.screen is None
    assert main.main
