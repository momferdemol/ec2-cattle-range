# cattle-range/iam.py

# cattle_range/iam.py

from aws_cdk import CfnOutput
from aws_cdk import aws_iam as iam
from constructs import Construct

from cattle_range.settings import get_resource_name


class Permissions(Construct):
    def __init__(self, scope: Construct, id: str) -> None:
        super().__init__(scope, id)

        self.profile: iam.Role = self._build_instance_profile()

    def _build_instance_profile(self) -> iam.Role:
        profile: iam.Role = iam.Role(
            self,
            "profile",
            role_name=get_resource_name("role", "-profile"),
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
        )
        profile.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
        )
        CfnOutput(self, "InstanceProfileArn", value=str(profile.role_arn))

        return profile
