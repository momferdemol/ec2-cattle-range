# cattle_range/ec2.py

from aws_cdk import CfnOutput
from aws_cdk import aws_autoscaling as autoscaling
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from constructs import Construct

from cattle_range.alb import LoadBalancer
from cattle_range.settings import get_resource_name

with open("./cattle_range/user_data/user_data.sh") as file:
    user_data = file.read()


class Compute(Construct):
    def __init__(self, scope: Construct, id: str, network: ec2.Vpc, profile: iam.Role) -> None:
        super().__init__(scope, id)

        self.profile = profile
        self.network = network
        self.sg = self._build_security_group()
        self.template = self._build_launch_template()
        self.scaling = self._build_auto_scaling()
        self.alb = LoadBalancer(self, "alb", network=self.network, scaling=self.scaling)

    def _build_security_group(self) -> ec2.SecurityGroup:
        sg = ec2.SecurityGroup(
            self,
            "sg",
            vpc=self.network,
            security_group_name=get_resource_name("sg", "-ec2"),
            description="Security group for service",
            allow_all_outbound=True,
        )
        CfnOutput(self, "SecurityGroupServiceId", value=str(sg.security_group_id))

        return sg

    def _build_launch_template(self) -> ec2.LaunchTemplate:
        template: ec2.LaunchTemplate = ec2.LaunchTemplate(
            self,
            "template",
            launch_template_name=get_resource_name("lt", ""),
            instance_initiated_shutdown_behavior=ec2.InstanceInitiatedShutdownBehavior.TERMINATE,
            instance_type=ec2.InstanceType("t3.micro"),
            security_group=self.sg,
            role=self.profile,  # type: ignore
            machine_image=ec2.MachineImage.from_ssm_parameter(
                parameter_name="/cattle_range/ec2/ami",
            ),
            user_data=ec2.UserData.custom(user_data),
        )
        CfnOutput(self, "LaunchTemplateId", value=str(template.launch_template_id))

        return template

    def _build_auto_scaling_update(self) -> autoscaling.UpdatePolicy:
        update_policy: autoscaling.UpdatePolicy = autoscaling.UpdatePolicy.rolling_update(
            min_instances_in_service=1,
            max_batch_size=1,
            wait_on_resource_signals=True,
        )

        return update_policy

    def _build_auto_scaling(self) -> autoscaling.AutoScalingGroup:
        scaling: autoscaling.AutoScalingGroup = autoscaling.AutoScalingGroup(
            self,
            "scaling",
            vpc=self.network,
            launch_template=self.template,
            min_capacity=1,
            max_capacity=2,
            auto_scaling_group_name=get_resource_name("asg", ""),
            update_policy=self._build_auto_scaling_update(),
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
        )
        CfnOutput(self, "AutoScalingGroupArn", value=scaling.auto_scaling_group_arn)

        return scaling
