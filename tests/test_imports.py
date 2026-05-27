def test_core_imports_do_not_start_runtime():
    from sevilla_reigns.config import settings as config
    import sevilla_reigns.application.event_manager
    import sevilla_reigns.application.effects
    import main

    assert config.screen is None
    assert main.main
