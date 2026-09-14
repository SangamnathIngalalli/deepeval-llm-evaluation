from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

from app.claude_client import ClaudeClient
from app.deepeval_config import ClaudeJudge


def test_answer_relevancy_smoke():
    """Minimal test: does the answer address the question?"""
    judge = ClaudeJudge()
    claude = ClaudeClient()

    question = "What is the capital of France?"
    answer = claude.ask(question)

    test_case = LLMTestCase(
        input=question,
        actual_output=answer,
    )

    metric = AnswerRelevancyMetric(
        threshold=0.7,
        model=judge,
        include_reason=True,
    )

    assert_test(test_case, [metric])