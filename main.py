from s3_utils import S3_CONFIGS, minio_list_buckets, boto3_list_buckets, minio_create_bucket, boto3_create_bucket

# Например, для MinIO:
minio_list_buckets(S3_CONFIGS["aws"])
boto3_list_buckets(S3_CONFIGS["aws"])  # Работает и так!

