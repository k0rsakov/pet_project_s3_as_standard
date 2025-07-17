from s3_utils import S3_CONFIGS, boto3_remove_bucket, minio_remove_bucket

# Для создания бакета:
bucket_name = "korsakov-test-s3-as-standard-from-api"
minio_remove_bucket(conn_params=S3_CONFIGS["minio"], bucket_name=bucket_name)
boto3_remove_bucket(conn_params=S3_CONFIGS["minio"], bucket_name=bucket_name)

minio_remove_bucket(conn_params=S3_CONFIGS["selectel"], bucket_name=bucket_name)
boto3_remove_bucket(conn_params=S3_CONFIGS["selectel"], bucket_name=bucket_name)

minio_remove_bucket(conn_params=S3_CONFIGS["vk"], bucket_name=bucket_name)
boto3_remove_bucket(conn_params=S3_CONFIGS["vk"], bucket_name=bucket_name)

minio_remove_bucket(conn_params=S3_CONFIGS["aws"], bucket_name=bucket_name)
boto3_remove_bucket(conn_params=S3_CONFIGS["aws"], bucket_name=bucket_name)
