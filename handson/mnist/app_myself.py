from aws_cdk import (
	core,
	aws_ec2 as ec2,
)
import os

class Ec2ForDlU(core.Stack):

	def __init__(self, scope: core.App, name: str, key_name: str, **kwargs) -> None:
		super().__init__(scope, name, **kwargs)

		# The code that defines your stack goes here

		# Create the VPC
		vpc = ec2.Vpc(self, "VPC",
			self, "Ec2ForDl-Vpc",
			max_azs=1,
			cidr="10.10.0.0/23",
			subnet_configuration=[
				ec2.SubnetConfiguration(
					name="Public",
					subnet_type=ec2.SubnetType.PUBLIC,
				)
			], 
			nat_gateways=0,
		)

		#create the security group
		sg = ec2.SecurityGroup(
			self, "Ec2ForDl-Sg", 
			vpc = vpc
			allow_all_outbound=True,
		)

		sg.add_ingress_rule(
			peer=ec2.Peer.any_ipv4(),
			connection=ec2.Port.tcp(22),
		)

		host = ec2.Instance(
			self, "Ec2ForDl-Instance",
			instance_type=ec2.InstanceType("g4dn.xlarge"),
			machine_image=ec2.MachineImage.generic_linux({
				"us-east-1":"ami-060f07284bb6f9faf",
				"ap-northeast-1":"ami-09c0c16fc46a29ed9",
			}),
			vpc =vpc
			vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
			security_group=sg,
			key_name=key_name
		)


