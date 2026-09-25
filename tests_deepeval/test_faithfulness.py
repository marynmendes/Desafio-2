import json
import pytest

from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric
from deepeval.test_case import LLMTestCase

from judge import judge_model
from middleware_client import invoke_agent


# ============================================================
# CARREGA GOLDEN DATASET
# ============================================================

with open("golden_dataset.json", "r", encoding="utf-8") as f:
    golden_dataset = json.load(f)


# ============================================================
# CASOS SELECIONADOS PARA FAITHFULNESS
# ============================================================

SELECTED_IDS = {
    "GD01",
    "GD03",
    "GD07",
    "GD10",
    "GD13",
    "GD16"
}


golden_cases = [
    case
    for case in golden_dataset
    if case["id"] in SELECTED_IDS
]


# ============================================================
# MÉTRICA
# ============================================================

faithfulness_metric = FaithfulnessMetric(
    threshold=0.8,
    model=judge_model
)


# ============================================================
# TESTE
# ============================================================

@pytest.mark.parametrize(
    "golden",
    golden_cases,
    ids=lambda x: x["id"]
)
def test_faithfulness(golden):

    result = invoke_agent(
        golden["input"]
    )

    actual_output = result["actual_output"]

    test_case = LLMTestCase(
        input=golden["input"],

        actual_output=actual_output,

        retrieval_context=[
            golden["reference_context"]
        ]
    )

    assert_test(
        test_case=test_case,
        metrics=[
            faithfulness_metric
        ]
    )