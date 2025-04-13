from struktcore_lite.core.config import CONFIG

def test_config_loads():
    assert isinstance(CONFIG, dict)
    assert "model" in CONFIG
    assert "plugins" in CONFIG
