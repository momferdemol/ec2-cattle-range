# cattle_range/nlb.py

from aws_cdk import CfnOutput
from aws_cdk import aws_autoscaling as autoscaling
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from constructs import Construct

from cattle_range.settings import get_resource_name


class LoadBalancer(Construct):
    def __init__(
        self, scope: Construct, id: str, network: ec2.Vpc, scaling: autoscaling.AutoScalingGroup
    ) -> None:
        super().__init__(scope, id)

        self.network = network
        self.scaling = scaling
        self.sg = self._build_security_group()
        self.alb: elbv2.ApplicationLoadBalancer = self._build_load_balancer()

    def _build_security_group(self) -> ec2.SecurityGroup:
        sg = ec2.SecurityGroup(
            self,
            "sg",
            vpc=self.network,
            security_group_name=get_resource_name("sg", "-alb"),
            description="Security group for application load balancer",
            allow_all_outbound=True,
        )
        CfnOutput(self, "SecurityGroupAlbId", value=str(sg.security_group_id))

        return sg

    def _build_load_balancer(self) -> elbv2.ApplicationLoadBalancer:
        alb: elbv2.ApplicationLoadBalancer = elbv2.ApplicationLoadBalancer(
            self,
            "loadbalancer",
            vpc=self.network,
            internet_facing=True,
            load_balancer_name=get_resource_name("alb", ""),
            security_group=self.sg,
        )
        listener = alb.add_listener(
            "listener",
            port=80,
            open=True,
        )
        listener.add_targets(
            "target",
            port=80,
            health_check=elbv2.HealthCheck(
                enabled=True,
                port="80",
                protocol=elbv2.Protocol.HTTP,
                path="/index.html",
                healthy_threshold_count=2,
                unhealthy_threshold_count=2,
            ),
            targets=[self.scaling],
        )
        CfnOutput(self, "LoadBalancerArn", value=str(alb.load_balancer_arn))

        return alb
