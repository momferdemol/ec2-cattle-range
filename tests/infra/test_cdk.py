# tests/infra/test_cdk.py

from aws_cdk import App
from aws_cdk.assertions import Template

from cattle_range.settings import get_stack_name, set_environment
from cattle_range.stack import Range


def test_synthesizes_stack_properly() -> None:
    """Test synthesizes correct stack resources."""
    app = App()

    stack = Range(
        app,
        get_stack_name(""),
        description="CDK nag test",
        env=set_environment("eu"),
        termination_protection=False,
    )

    template = Template.from_stack(stack)

    template.resource_count_is("AWS::IAM::Role", 1)
    template.resource_count_is("AWS::EC2::VPC", 1)
    template.resource_count_is("AWS::EC2::LaunchTemplate", 1)
    template.resource_count_is("AWS::AutoScaling::AutoScalingGroup", 1)
