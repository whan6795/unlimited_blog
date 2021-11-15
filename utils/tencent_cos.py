from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
from tencent_config import *


class TencentCos:

    def __init__(self):
        self.secret_id = TENCENT_SECRET_ID
        self.secret_key = TENCENT_SECRET_KEY
        self.region = TENCENT_REGION
        self.token = TENCENT_TOKEN
        self.scheme = TENCENT_SCHEME
        self.url = TENCENT_URL
        self.bucket = TENCENT_BUCKET
        self.dir = TENCENT_DIRNAME
        self.config = CosConfig(Region=self.region, SecretId=self.secret_id, SecretKey=self.secret_key,
                                Token=self.token, Scheme=self.scheme)
        self.client = CosS3Client(self.config)

    def put_file(self, name, file):
        """
        :param name: 文件名
        :param file: 文件
        """
        result = self.client.put_object(
            Bucket=self.bucket,
            Body=file,
            Key=self.dir + name,
            # StorageClass='STANDARD',
            EnableMD5=False
        )
        # print(result['ETag'])
        return self.url+self.dir+name

    def delete_files(self, file_list):
        result = self.client.delete_objects(
            Bucket=self.bucket,
            Delete={
                'Object': [{'Key': value} for value in file_list],
                # 'Quiet': 'true'
            }
        )
        # print(result)
        # if 'Error' in result.keys():
        #     self.delete_files([info['Key'] for info in result['Error']])

