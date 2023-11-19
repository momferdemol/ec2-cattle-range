# tests/infra/test_cdk_nag.py

from aws_cdk import App, Aspects
from cdk_nag import AwsSolutionsChecks

from cattle_range.settings import get_stack_name, set_environment
from cattle_range.stack import Range


def test_cdk_nag_aws_solutions() -> None:
    """Test stack against CDK nag AWS Solutions."""
    app = App()

    stack = Range(
        app,
        get_stack_name(""),
        description="CDK nag test",
        env=set_environment("eu"),
        termination_protection=False,
    )
    Aspects.of(stack).add(AwsSolutionsChecks(verbose=True))
