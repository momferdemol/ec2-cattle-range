# cattle-range/vpc.py

from aws_cdk import CfnOutput
from aws_cdk import aws_ec2 as ec2
from constructs import Construct

from cattle_range.settings import get_resource_name


class Network(Construct):
    def __init__(self, scope: Construct, id: str) -> None:
        super().__init__(scope, id)

        self.vpc: ec2.Vpc = self._build_vpc()

    def _build_vpc(self) -> ec2.Vpc:
        vpc: ec2.Vpc = ec2.Vpc(
            self,
            "vpc",
            vpc_name=get_resource_name("vpc", ""),
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="public",
                    cidr_mask=21,
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    name="private",
                    cidr_mask=21,
                ),
            ],
        )
        CfnOutput(self, "VpcId", value=str(vpc.vpc_id))

        return vpc
