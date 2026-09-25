import json
import pytest

from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

from judge import judge_model
from middleware_client import invoke_agent


# ============================================================
# CARREGA GOLDEN DATASET
# ============================================================

with open("golden_dataset.json", "r", encoding="utf-8") as f:
    golden_dataset = json.load(f)


# ============================================================
# CASOS SELECIONADOS PARA ANSWER RELEVANCY
# ============================================================

SELECTED_IDS = {
    "GD01",
    "GD06",
    "GD09",
    "GD12",
    "GD15",
    "GD20"
}


golden_cases = [
    case
    for case in golden_dataset
    if case["id"] in SELECTED_IDS
]


# ============================================================
# MÉTRICA
# ============================================================

answer_relevancy_metric = AnswerRelevancyMetric(
    threshold=0.7,
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
def test_answer_relevancy(golden):

    result = invoke_agent(
        golden["input"]
    )

    actual_output = result["actual_output"]

    test_case = LLMTestCase(
        input=golden["input"],
        actual_output=actual_output
    )

    assert_test(
        test_case=test_case,
        metrics=[
            answer_relevancy_metric
        ]
    )