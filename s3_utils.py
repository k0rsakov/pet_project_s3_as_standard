import boto3
from botocore.client import Config
from minio import Minio

from cred import (
    s3_aws_access_key,
    s3_aws_bucket_name,
    s3_aws_endpoint,
    s3_aws_secret_key,
    s3_minio_access_key,
    s3_minio_bucket_name,
    s3_minio_endpoint,
    s3_minio_secret_key,
    s3_selectel_access,
    s3_selectel_bucket_name,
    s3_selectel_endpoint,
    s3_selectel_secret,
    s3_vk_access,
    s3_vk_bucket_name,
    s3_vk_endpoint,
    s3_vk_secret,
)

# Универсальные словари для подключения (можно расширять!)
S3_CONFIGS = {
    "minio": {
        "endpoint": s3_minio_endpoint,
        "access_key": s3_minio_access_key,
        "secret_key": s3_minio_secret_key,
        "bucket": s3_minio_bucket_name,
        "secure": False,  # локально часто http
        "region": None,
    },
    "selectel": {
        "endpoint": s3_selectel_endpoint,
        "access_key": s3_selectel_access,
        "secret_key": s3_selectel_secret,
        "bucket": s3_selectel_bucket_name,
        "secure": True,
        "region": None,
    },
    "vk": {
        "endpoint": s3_vk_endpoint,
        "access_key": s3_vk_access,
        "secret_key": s3_vk_secret,
        "bucket": s3_vk_bucket_name,
        "secure": True,
        "region": None,
    },
    "aws": {
        "endpoint": s3_aws_endpoint,
        "access_key": s3_aws_access_key,
        "secret_key": s3_aws_secret_key,
        "bucket": s3_aws_bucket_name,
        "secure": True,
        "region": "us-east-1",
    },
}


def minio_client(conn_params: dict) -> Minio:
    """
    Создает экземпляр Minio.

    :param conn_params: Параметры подключения.
    :return: Клиент Minio.
    """
    return Minio(
        endpoint=conn_params["endpoint"],
        access_key=conn_params["access_key"],
        secret_key=conn_params["secret_key"],
        secure=conn_params.get("secure", True),
    )


def minio_list_buckets(conn_params: dict) -> None:
    """
    Отображает список бакетов.

    :param conn_params: Параметры подключения.
    :return: Ничего.
    """
    client = minio_client(conn_params)
    buckets = client.list_buckets()
    print("Buckets (minio):")
    for bucket in buckets:
        print(bucket.name, bucket.creation_date)


def minio_create_bucket(conn_params: dict, bucket_name: str) -> None:
    """
    Ручка для создания бакета.

    :param conn_params: Параметры подключения.
    :param bucket_name: Имя бакета.
    :return: Ничего.
    """
    client = minio_client(conn_params)
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print(f"Bucket '{bucket_name}' created!")
    else:
        print(f"Bucket '{bucket_name}' already exists.")


def minio_upload_csv(conn_params: dict, bucket_name: str, object_name: str, file_path: str) -> None:
    """
    Ручка для загрузки файла в бакет.

    :param conn_params: Параметры подключения.
    :param bucket_name: Имя бакета.
    :param object_name: Имя файла в бакете.
    :param file_path: Имя файла на диске.
    :return: Ничего.
    """
    client = minio_client(conn_params)
    result = client.fput_object(
        bucket_name=bucket_name,
        object_name=object_name,
        file_path=file_path,
    )
    print(f"Uploaded {object_name} to {bucket_name} (etag: {result.etag})")

def minio_list_objects(conn_params: dict, bucket_name: str) -> None:
    """
    Ручка для просмотра содержимого бакета.

    :param conn_params: Параметры подключения.
    :param bucket_name: Имя бакета.
    :return: Ничего.
    """
    client = minio_client(conn_params)
    print(f"Objects in bucket '{bucket_name}':")
    for obj in client.list_objects(bucket_name):
        print(obj.object_name, obj.size, obj.last_modified)


def boto3_client(conn_params: dict) -> boto3.client:
    """
    Функция для создания клиента S3.

    :param conn_params: Параметры подключения.
    :return: Клиент S3 (boto3).
    """
    session = boto3.session.Session()
    return session.client(
        service_name="s3",
        aws_access_key_id=conn_params["access_key"],
        aws_secret_access_key=conn_params["secret_key"],
        endpoint_url=f"https://{conn_params['endpoint']}" if conn_params.get("secure", True) else f"http://{conn_params['endpoint']}",
        region_name=conn_params.get("region"),
        config=Config(signature_version="s3v4"),
    )


def boto3_list_buckets(conn_params: dict) -> None:
    """
    Отображает список бакетов.

    :param conn_params: Параметры подключения.
    :return: Ничего.
    """
    s3 = boto3_client(conn_params)
    resp = s3.list_buckets()
    print("Buckets (boto3):")
    for bucket in resp.get("Buckets", []):
        print(bucket["Name"], bucket["CreationDate"])


def boto3_create_bucket(conn_params: dict, bucket_name: str) -> None:
    """
    Ручка для создания бакета.

    :param conn_params: Параметры подключения.
    :param bucket_name: Имя бакета.
    :return: Ничего.
    """
    s3 = boto3_client(conn_params)
    try:
        params = {"Bucket": bucket_name}
        if conn_params.get("region") and conn_params.get("region") != "us-east-1":
            params["CreateBucketConfiguration"] = {"LocationConstraint": conn_params["region"]}
        s3.create_bucket(**params)
        print(f"Bucket '{bucket_name}' created!")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"Bucket '{bucket_name}' already exists.")
    except Exception as e:  # noqa: BLE001
        print(f"Error creating bucket: {e}")


def boto3_upload_csv(conn_params: dict, bucket_name: str, object_name: str, file_path: str) -> None:
    """
    Ручка для загрузки файла в бакет.

    :param conn_params: Параметры подключения.
    :param bucket_name: Имя бакета.
    :param object_name: Имя файла в бакете.
    :param file_path: Имя файла на диске.
    :return: Ничего.
    """
    s3 = boto3_client(conn_params)
    s3.upload_file(file_path, bucket_name, object_name)
    print(f"Uploaded {object_name} to {bucket_name}")


def boto3_list_objects(conn_params: dict, bucket_name: str) -> None:
    """
    Ручка для просмотра содержимого бакета.

    :param conn_params: Параметры подключения.
    :param bucket_name: Имя бакета.
    :return: Ничего.
    """
    s3 = boto3_client(conn_params)
    resp = s3.list_objects_v2(Bucket=bucket_name)
    print(f"Objects in bucket '{bucket_name}':")
    for obj in resp.get("Contents", []):
        print(obj["Key"], obj["Size"], obj["LastModified"])
