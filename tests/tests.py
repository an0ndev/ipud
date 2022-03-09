def run_tests (debug: bool):
    import test_ipud

    test = test_ipud.ipudTest (debug)
    for attrib in dir (test):
        if not attrib.startswith ("test_"): continue
        if attrib in test_ipud.disabled_tests: continue

        test.__getattribute__ (attrib) ()
