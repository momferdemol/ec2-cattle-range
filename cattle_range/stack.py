# cattle-range/stack.py

from aws_cdk import Stack, Tags
from constructs import Construct

from cattle_range.ec2 import Compute
from cattle_range.iam import Permissions
from cattle_range.settings import get_settings
from cattle_range.vpc import Network


class Range(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.profile = Permissions(self, "profile").profile
        self.network = Network(self, "network").vpc
        self.compute = Compute(self, id="compute", network=self.network, profile=self.profile)

        Tags.of(self).add("createdBy", get_settings().owner)
