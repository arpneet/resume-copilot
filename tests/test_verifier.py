from src.verifier import rule_check


def test_blocks_injected_python():
    assert rule_check("Built dashboards in Power BI",
                      "Built Python dashboards in Power BI")


def test_blocks_injected_number():
    assert rule_check("Built dashboards in Power BI",
                      "Built dashboards in Power BI, cutting time 40%")


def test_allows_faithful_rewrite():
    assert rule_check("Built dashboards in Power BI",
                      "Developed dashboards in Power BI") == []