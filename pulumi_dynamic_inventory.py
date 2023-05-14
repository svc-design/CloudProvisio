
#!/usr/bin/env python

import boto3
import json
import argparse

# AWS S3 存储桶名称和文件名
S3_BUCKET_NAME = 'your-s3-bucket-name'
S3_FILE_NAME = 'your-s3-file-name'

# AWS 访问密钥 ID 和访问密钥
AWS_ACCESS_KEY_ID = 'your-aws-access-key-id'
AWS_SECRET_ACCESS_KEY = 'your-aws-secret-access-key'

# Ansible inventory 字典
inventory = {
    '_meta': {
        'hostvars': {}
    },
    'all': {
        'children': []
    }
}

# 获取 AWS EC2 实例列表
ec2 = boto3.resource('ec2', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
instances = ec2.instances.all()

# 循环遍历 EC2 实例并将其添加到 Ansible inventory 中
for instance in instances:
    # 获取 EC2 实例的标签
    tags = {}
    for tag in instance.tags:
        tags[tag['Key']] = tag['Value']

    # 将 EC2 实例添加到 Ansible inventory 中
    group_name = tags.get('ansible_group', 'ungrouped')
    inventory.setdefault(group_name, {'hosts': []})
    inventory[group_name]['hosts'].append(instance.private_ip_address)
    inventory['all']['children'].append(group_name)

    # 将 EC2 实例的元数据添加到 Ansible inventory 中
    inventory['_meta']['hostvars'][instance.private_ip_address] = {
        'ansible_host': instance.private_ip_address,
        'ansible_user': tags.get('ansible_user', 'ubuntu'),
        'ansible_ssh_private_key_file': tags.get('ansible_ssh_private_key_file', '~/.ssh/id_rsa'),
        'ansible_python_interpreter': tags.get('ansible_python_interpreter', '/usr/bin/python')
    }

# 将 Ansible inventory 字典输出为 JSON 格式
print(json.dumps(inventory))

# 定义一个函数，用于返回Ansible所需的主机清单
def get_inventory():
    # 定义一个字典，用于存储主机清单
    inventory = {
        "web": {
            "hosts": [
                "web1.example.com",
                "web2.example.com"
            ],
            "vars": {
                "ansible_ssh_user": "ubuntu"
            }
        },
        "db": {
            "hosts": [
                "db1.example.com",
                "db2.example.com"
            ],
            "vars": {
                "ansible_ssh_user": "ubuntu"
            }
        },
        "_meta": {
            "hostvars": {
                "web1.example.com": {
                    "ansible_ssh_private_key_file": "/path/to/web1/private/key"
                },
                "web2.example.com": {
                    "ansible_ssh_private_key_file": "/path/to/web2/private/key"
                },
                "db1.example.com": {
                    "ansible_ssh_private_key_file": "/path/to/db1/private/key"
                },
                "db2.example.com": {
                    "ansible_ssh_private_key_file": "/path/to/db2/private/key"
                }
            }
        }
    }

    # 将主机清单转换为JSON格式并返回
    return json.dumps(inventory)

# 定义一个函数，用于解析命令行参数
def parse_args():
    parser = argparse.ArgumentParser(description="Ansible dynamic inventory script")
    parser.add_argument("--list", help="List all hosts", action="store_true")
    parser.add_argument("--host", help="Get variables for a specific host")
    return parser.parse_args()

# 如果脚本被调用时传入了--list参数，则打印主机清单并退出
# 如果脚本被调用时传入了--host参数，则打印指定主机的变量并退出
# 否则，打印脚本的使用说明并退出
if __name__ == "__main__":
    args = parse_args()
    if args.list:
        print(get_inventory())
    elif args.host:
        print("{}")
    else:
        print("Usage: {} [--list] [--host <hostname>]".format(__file__))
