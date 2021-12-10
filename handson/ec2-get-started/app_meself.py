class MyFirstEc2(core.Stack):
	
	def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
		super().__init__(scope, id, **kwargs)

		#VPCの定義
		vpc = ec2.Vpc(
			self, "MyFiesrEc2-Vpc",
			cidr="10.10.0.0/23",
			subnet_configuration=[
				ec2.SubnetConfiguration(
					name="Public",
					subnet_type=ec2.SubnetType.PUBLIC,
				)
			], 
			nat_gateways=0,
		)

		#security groupの定義
		sg = ec2.SecurityGroup(
			self, "MyFirstEc2-Sg",
			vpc =vpc,
			allow_all_outbound=True,
		)
		sg.add_ingress_rule(
			peer = ec2.Peer.any_ipv4(),
			connection = ec2.Port.tcp(22),
		)

		#VPCとSGが付与された，EC2インスタンスの作成
		host = ec2.Instance(
			self, "MyFirstEc2Instance", 
			instance_type=ec2.InstanceType("t2.micro"),
			machine_image=ec2.MachineImage.latest_amazon_linux(),
			vpc=vpc,
			vpc_subnets = ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
			security_group = sg,
			key_name = key_name,
		)




