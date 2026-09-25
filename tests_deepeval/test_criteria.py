import json
import pytest

from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

from judge import judge_model
from middleware_client import invoke_agent


# ============================================================
# CARREGA GOLDEN DATASET
# ============================================================

with open("golden_dataset.json", "r", encoding="utf-8") as f:
    golden_dataset = json.load(f)


# ============================================================
# CASOS SELECIONADOS PARA GEVAL
# ============================================================

SELECTED_IDS = {
    "GD01",
    "GD02",
    "GD03",
    "GD04",
    "GD05",
    "GD06",
    "GD07"
}


golden_cases = [
    case
    for case in golden_dataset
    if case["id"] in SELECTED_IDS
]


# ============================================================
# MÉTRICA GEVAL
# ============================================================

criteria_metric = GEval(
    name="Golden Dataset Criteria",

    criteria=(
        "Avalie se a resposta do agente atende aos critérios "
        "esperados definidos para o caso de teste. "
        "A resposta deve responder corretamente à pergunta, "
        "contemplar os critérios relevantes e utilizar de forma "
        "adequada o contexto de referência fornecido."
    ),

    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.CONTEXT
    ],

    model=judge_model,

    threshold=0.8
)


# ============================================================
# TESTE
# ============================================================

@pytest.mark.parametrize(
    "golden",
    golden_cases,
    ids=lambda x: x["id"]
)
def test_criteria(golden):

    result = invoke_agent(
        golden["input"]
    )

    actual_output = result["actual_output"]

    criteria = "\n".join(
        f"- {criterion}"
        for criterion in golden["expected_criteria"]
    )

    test_case = LLMTestCase(
        input=golden["input"],

        actual_output=actual_output,

        context=[
            criteria,
            golden["reference_context"]
        ]
    )

    assert_test(
        test_case=test_case,
        metrics=[
            criteria_metric
        ]
    )