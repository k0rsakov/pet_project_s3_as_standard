from s3_utils import S3_CONFIGS, boto3_list_buckets, minio_list_buckets

# Например, для MinIO:
minio_list_buckets(S3_CONFIGS["aws"])
boto3_list_buckets(S3_CONFIGS["aws"])  # Работает и так!

