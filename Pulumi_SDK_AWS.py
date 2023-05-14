import * as aws from "@pulumi/aws";

const vpc = new aws.ec2.Vpc("my-vpc", {
    cidrBlock: "10.0.0.0/16",
});

const subnet = new aws.ec2.Subnet("my-subnet", {
    cidrBlock: "10.0.1.0/24",
    vpcId: vpc.id,
});

const securityGroup = new aws.ec2.SecurityGroup("my-security-group", {
    vpcId: vpc.id,
});

const instance = new aws.ec2.Instance("my-instance", {
    ami: "ami-0c55b159cbfafe1f0",
    instanceType: "t2.micro",
    subnetId: subnet.id,
    securityGroups: [securityGroup.id],
});
