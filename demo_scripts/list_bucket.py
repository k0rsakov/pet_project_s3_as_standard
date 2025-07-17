from utils.s3_utils import S3_CONFIGS, boto3_list_buckets, minio_list_buckets

minio_list_buckets(conn_params=S3_CONFIGS["minio"])
boto3_list_buckets(conn_params=S3_CONFIGS["minio"])

minio_list_buckets(conn_params=S3_CONFIGS["selectel"])
boto3_list_buckets(conn_params=S3_CONFIGS["selectel"])

minio_list_buckets(conn_params=S3_CONFIGS["vk"])
boto3_list_buckets(conn_params=S3_CONFIGS["vk"])

minio_list_buckets(conn_params=S3_CONFIGS["aws"])
boto3_list_buckets(conn_params=S3_CONFIGS["aws"])

