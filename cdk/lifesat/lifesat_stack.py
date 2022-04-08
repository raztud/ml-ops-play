import os
import uuid

import aws_cdk.aws_autoscaling as autoscaling
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_iam as iam
import aws_cdk.aws_s3 as s3
from aws_cdk import Stack
from constructs import Construct

BUCKET_PREFIX = "ml-play"
BUCKET_BASE_NAME = "lifesat"
ACCOUNT_ID = os.environ.get("CDK_DEFAULT_ACCOUNT")


class LifesatStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(
            self,
            f"{BUCKET_PREFIX}-{BUCKET_BASE_NAME}-{uuid.uuid4().hex[:12]}",
            versioned=True,
            # removal_policy=RemovalPolicy.DESTROY,
            # auto_delete_objects=True,
        )

        self.create_training_cluster()

    def create_training_cluster(self):
        cluster_name = "ml-play-training-1"
        k8s_ver = "1.21"
        role = self.create_training_cluster_role(cluster_name=cluster_name)
        vpc = self.create_vpc(name=cluster_name)
        sg = self.create_security_group(name=cluster_name, vpc=vpc)

        self.create_eks_cluster(cluster_name=cluster_name, role=role, vpc=vpc, sg=sg)

    def create_security_group(self, name, vpc):
        return ec2.SecurityGroup(self, f"{name}SG", vpc=vpc)

    def create_eks_cluster(self, cluster_name, role, vpc, sg):

        cluster = ecs.Cluster(
            self,
            id="training",
            cluster_name=cluster_name,
            vpc=vpc,
        )

        auto_scaling_group = autoscaling.AutoScalingGroup(
            self,
            f"{cluster_name}ASG",
            vpc=vpc,
            instance_type=ec2.InstanceType("t2.small"),
            machine_image=ecs.EcsOptimizedImage.amazon_linux2(),
            min_capacity=1,
            max_capacity=3,
        )

        capacity_provider = ecs.AsgCapacityProvider(
            self, f"{cluster_name}AsgCapacityProvider", auto_scaling_group=auto_scaling_group
        )

        cluster.add_asg_capacity_provider(capacity_provider)

        return cluster

    def create_vpc(self, name):
        vpc = ec2.Vpc(
            self,
            f"{name}Vpc",
            cidr="10.0.0.0/16",
            max_azs=1,
            # subnet_configuration=[
            #     ec2.SubnetConfiguration(
            #         name="private-subnet-1",
            #         subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
            #         cidr_mask=24,
            #     )
            # ]
        )
        return vpc

    def create_training_cluster_role(self, cluster_name):
        role = iam.Role(
            self,
            id=f"{cluster_name}Role",
            assumed_by=iam.ServicePrincipal("eks.amazonaws.com"),
            description=f"Role for {cluster_name}",
            # inline_policies=
        )

        policy_stmt = iam.PolicyStatement(
            actions=["sts:AssumeRole"],
            effect=iam.Effect.ALLOW,
            resources=[f"arn:aws:eks:region-code:{ACCOUNT_ID}:cluster/{cluster_name}"],
            conditions={
                "ArnLike": {
                    "aws:SourceArn": f"arn:aws:eks:region-code:{ACCOUNT_ID}:cluster/{cluster_name}",
                }
            },
        )

        role.add_to_policy(policy_stmt)

        return role
