import time

import boto3

regions = {
    'us-east-2': '美国-俄亥俄',
    'us-east-1': '美国-弗吉尼亚',
    'us-west-1': '美国-加利福尼亚',
    'us-west-2': '美国-俄勒冈',
    'af-south-1': '非洲-开普敦',
    'ap-south-1': '印度-孟买',
    'ap-northeast-3': '日本-大阪',
    'ap-northeast-2': '韩国-首尔',
    'ap-southeast-1': '新加坡',
    'ap-southeast-2': '澳洲-悉尼',
    'ap-northeast-1': '日本-东京',
    'ca-central-1': '加拿大',
    'ap-east-1': '中国-香港',
    'cn-north-1': '中国-北京',
    'cn-northwest-1': '中国-宁夏',
    'eu-central-1': '德国-法蘭克福',
    'eu-west-1': '愛爾蘭',
    'eu-west-2': '英国-倫敦',
    'eu-south-1': '意大利-米蘭',
    'eu-west-3': '法国-巴黎',
    'eu-north-1': '瑞典-斯德哥爾摩',
    'me-south-1': '中东-巴林',
    'sa-east-1': '巴西-圣保罗',
}

images = {
    'us-east-2': 'ami-09862fadec6997084',
    'us-east-1': 'ami-06cdbd80022d89537',
    'us-west-1': 'ami-0e17790f211795d99',
    'us-west-2': 'ami-0864290505bf6b170',
    'af-south-1': 'ami-017b2397fedf95383',
    'ap-south-1': 'ami-02e2de7f439974656',
    'ap-northeast-3': 'ami-08bdd6b2b3b230e97',
    'ap-northeast-2': 'ami-0ec37230f5ced8b39',
    'ap-southeast-1': 'ami-05bf486ae7131d636',
    'ap-southeast-2': 'ami-0481b3d323ae68357',
    'ap-northeast-1': 'ami-0d4829cafe34d5d92',
    'ca-central-1': 'ami-05eccd43882a30f9a',
    'ap-east-1': 'ami-0e597d8e7c55ba1ac',
    'cn-north-1': 'ami-0764541358866f84e',
    'cn-northwest-1': 'ami-02441dea73a15a612',
    'eu-central-1': 'ami-032d3b1d0246c218e',
    'eu-west-1': 'ami-0e66021c377d8c8b4',
    'eu-west-2': 'ami-07dd7edad599ff758',
    'eu-south-1': 'ami-026ca3350950f23a8',
    'eu-west-3': 'ami-0516faeafaf906b64',
    'eu-north-1': 'ami-0ba7c2a9aa6ab6466',
    'me-south-1': 'ami-09d26d5583300a357',
    'sa-east-1': 'ami-0e813f6ba5ffa7ebd',
}

arm_images = {
    'af-south-1': 'ami-0eadef81a60d1898b',
    'ap-east-1': 'ami-0be38d8131b219715',
    'ap-northeast-1': 'ami-09524cdc933737da5',
    'ap-south-1': 'ami-0a2ce5a0a74b63975',
    'ap-southeast-1': 'ami-07633ef9689187b90',
    'ca-central-1': 'ami-075d8d90dad320b35',
    'eu-central-1': 'ami-046a6d7ec540a1e3b',
    'eu-north-1': 'ami-0ddd10fd9f73f124a',
    'eu-south-1': 'ami-00a2249139ac35088',
    'eu-west-1': 'ami-05c4ce6dd46c112fc',
    'me-south-1': 'ami-02178aa7d27d8147a',
    'sa-east-1': 'ami-0335b02fbdb9c8f06',
    'us-east-1': 'ami-0a57edb3631e68796',
    'us-west-1': 'ami-0837a588e831878f6',
    'cn-north-1': 'ami-074729b7a36af28b2',
    'cn-northwest-1': 'ami-09b9204d128fd2da6',
    'us-gov-east-1': 'ami-0dc088bbae85b95a9',
    'us-gov-west-1': 'ami-0bdba6deabc11c705',
    'ap-northeast-2': 'ami-016cb567c9a1c4a79',
    'ap-southeast-2': 'ami-04d192f7efd2aa6fb',
    'eu-west-2': 'ami-0e05135dede29b2cd',
    'us-east-2': 'ami-0f8081870765d4317',
    'us-west-2': 'ami-0009ec8bec5fe7ab9',
    'ap-northeast-3': 'ami-07269573a9a1da822',
    'eu-west-3': 'ami-05fcc216b8f7f4cc9',
}



class AwsApi():
    def __init__(self, key_id, key_secret):
        self.region = 'us-east-2'
        self.key_id = key_id
        self.key_secret = key_secret

    def start(self, name='ec2'):
        self.client = boto3.client(name, region_name=self.region, aws_access_key_id=self.key_id,
                                   aws_secret_access_key=self.key_secret)

    # 查询配额
    def get_service_quota(self):
        try:
            self.region = 'us-west-2'
            self.start('service-quotas')
            ret = self.client.get_service_quota(ServiceCode='ec2', QuotaCode='L-1216C47A')
            # ret = aApi.client.list_aws_default_service_quotas(ServiceCode='ec2')
            print(f"当前配额： {int(ret['Quota']['Value'])}")
            return True
        except BaseException as e:
            print(f"配额查询失败 {e}")
            return False

    # 获取全部地区
    def get_describe_regions(self):
        try:
            self.region = 'us-east-2'
            self.start()
            response = self.client.describe_regions()
            text = ''
            self.region_list = []
            for region in response['Regions']:
                # print(region)
                region = region['RegionName']
                text += f'{region} ---- {regions.get(region, region)}\n'
                self.region_list.append(region)
            self.region_text = text
            return True
        except BaseException as e:
            self.region_text = f'获取地区列表失败 {e}'
            return False


    # ec2 查询安全组, 获取默认安全组
    def ec2_describe_default_security_groups(self, name='default'):
        try:
            response = self.client.describe_security_groups(
                GroupNames=[name]
            )
            self.GroupId = response['SecurityGroups'][0]['GroupId']
            self.ec2_authorize_security_group_ingress(self.GroupId)
            return True
        except BaseException as e:
            print(e)
            return False

    # 添加安全组规则
    def ec2_authorize_security_group_ingress(self, GroupID=''):
        try:
            self.client.authorize_security_group_ingress(
                GroupId=GroupID,
                IpPermissions=[
                    {
                        'IpProtocol': '-1',
                        'IpRanges': [
                            {
                                'CidrIp': '0.0.0.0/0',
                                'Description': 'string'
                            },
                        ],
                    },
                ]
            )
            return True
        except:
            return False

    def ec2_create_instances(self, InstanceType='t2.micro', disk_size=8, _type='x86'):
        # 先获取默认安全组
        try:
            self.ec2_describe_default_security_groups()
            BlockDeviceMappings = [
                {
                    "DeviceName": f"/dev/sda1",
                    "Ebs": {
                        "VolumeSize": int(disk_size),
                        "DeleteOnTermination": True,
                        "VolumeType": "gp2"
                    }
                }
            ]

            UserData = """#!/bin/sh
sudo service iptables stop 2> /dev/null ; chkconfig iptables off 2> /dev/null ;
sudo sed -i.bak '/^SELINUX=/cSELINUX=disabled' /etc/sysconfig/selinux;
sudo sed -i.bak '/^SELINUX=/cSELINUX=disabled' /etc/selinux/config;
sudo setenforce 0;
echo root:hostloc!! |sudo chpasswd root;
sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin yes/g' /etc/ssh/sshd_config;
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/g' /etc/ssh/sshd_config;
sudo service sshd restart;
"""
            if _type == 'arm':
                image_id = arm_images.get(self.region)
            else:
                image_id = images.get(self.region)
            response = self.client.run_instances(
                BlockDeviceMappings=BlockDeviceMappings,
                UserData=UserData,
                ImageId=image_id,
                InstanceType=InstanceType,
                MaxCount=1,
                MinCount=1,
                Monitoring={
                    'Enabled': False
                },
                SecurityGroupIds=[
                    self.GroupId,
                ]
            )
            self.response = response
            # 添加标签
            self.instance_id = response['Instances'][0]['InstanceId']
            return True
        except BaseException as e:
            print(str(e))
            self.error_msg = str(e)
            return False

    # 获取实例状态
    def get_instance(self, instance_id):
        try:
            self.start('ec2')
            ret = self.client.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
            # print(ret)
            self.ip = ret['PublicIpAddress']
            if self.ip == '': return False
            self.instance_id = instance_id
            return True
        except BaseException as e:
            print(f'获取实例状态失败, 请重试 {e}')
            return False


def start():
    print('开机助手 v1.1 by: @qikao')
    print('购买AWS账号 @qikao')
    key_info = input("请输入API信息, 格式为 keyid|secret : ")
    if len(key_info.strip().split('|')) != 2:
        print('API信息输入错误')
        return False

    keyid, secret = key_info.strip().split('|')

    aApi = AwsApi(keyid, secret)
    print(f'当前操作的账号 {keyid} | {secret}')

    aApi.get_service_quota()
    if not aApi.get_describe_regions():
        print('获取地区列表失败， 无法进行开机')
        return False
    print(aApi.region_text)
    _region = input('请选择需要开机的区域， 例如： us-east-1 : ') or 'us-east-1'
    _region = _region.strip()
    if _region not in aApi.region_list:
        print(f'该账号不支持 {_region} 区域, 请选择重新操作。')
        return False

    _type = input('请选择需要的平台 ARM 或者 X86, 默认X86 : ') or 'X86'

    _type = _type.lower()

    instance_type = input('请输入需要创建的实例类型：默认 t2.micro  : ') or 't2.micro'

    instance_type = instance_type.strip()

    disk_size = input('请输入磁盘大小， 默认 8 : ') or '8'

    disk_size = int(disk_size)
    aApi.region = _region
    aApi.start()
    if not aApi.ec2_create_instances(instance_type, disk_size=disk_size, _type=_type):
        print('创建失败')
        return False

    print('========实例创建成功=========')
    for num in range(20):
        print(f'第 {num + 1} 次 更新实例状态')
        if aApi.get_instance(aApi.instance_id): break
        time.sleep(5)

    print('========实例信息如下=========')
    print(f'实例ID: {aApi.instance_id}, 实例IP: {aApi.ip}, 实例地区: {_region}({regions.get(_region)}), 机器平台: {_type}')
    return True


if __name__ == '__main__':
    start()
