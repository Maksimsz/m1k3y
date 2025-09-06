from m1k3y.security.risk import classify_risk

def test_shutdown_high():
    assert classify_risk("system_command","shutdown","please shutdown","") == "high"

def test_open_medium():
    assert classify_risk("system_command","open","open notepad","") == "medium"