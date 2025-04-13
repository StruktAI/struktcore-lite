from struktcore_lite.core.plugin_loader import load_plugins

def test_plugins_load():
    plugins = load_plugins()
    assert isinstance(plugins, dict)
    for name, mod in plugins.items():
        assert hasattr(mod, "run")
