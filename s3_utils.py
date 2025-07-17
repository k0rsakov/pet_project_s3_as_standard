import boto3
from botocore.client import Config
from minio import Minio
from minio.error import InvalidResponseError, S3Error

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
        "target": "minio",
        "endpoint": s3_minio_endpoint,
        "access_key": s3_minio_access_key,
        "secret_key": s3_minio_secret_key,
        "bucket": s3_minio_bucket_name,
        "secure": False,  # локально часто http
        "region": None,
    },
    "selectel": {
        "target": "selectel",
        "endpoint": s3_selectel_endpoint,
        "access_key": s3_selectel_access,
        "secret_key": s3_selectel_secret,
        "bucket": s3_selectel_bucket_name,
        "secure": True,
        "region": None,
    },
    "vk": {
        "target": "vk",
        "endpoint": s3_vk_endpoint,
        "access_key": s3_vk_access,
        "secret_key": s3_vk_secret,
        "bucket": s3_vk_bucket_name,
        "secure": True,
        "region": None,
    },
    "aws": {
        "target": "aws",
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
    print(f"🦩 With Minio client; Buckets (minio) in {conn_params['target']}:")
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
    try:
        client.make_bucket(bucket_name)
        print(f"🦩 With Minio client; Bucket '{bucket_name}' created in {conn_params['target']}!")
    except (S3Error, InvalidResponseError) as exc:
        msg = str(exc)
        if (
            (hasattr(exc, "code") and getattr(exc, "code", None) in ("BucketAlreadyOwnedByYou", "BucketAlreadyExists"))
            or "BucketAlreadyOwnedByYou" in msg
            or "BucketAlreadyExists" in msg
        ):
            print(f"🦩 With Minio client; Bucket '{bucket_name}' already exists in {conn_params['target']}.")
        else:
            print(f"🦩 With Minio client; Error creating bucket '{bucket_name}' in {conn_params['target']}: {exc}")


def minio_upload_csv(conn_params: dict, bucket_name: str, object_name: str, file_path: str) -> None:
    """
    Ручка для загрузки файла в бакет.

    :param conn_params: Параметры подключения.
    :param bucket_name: Имя бакета.
    :param object_name: Имя файла в бакете.
    :param file_path: Имя файла на диске.
    :return: Ничего.
    """
    client = minio_client(conn_params)
    result = client.fput_object(
        bucket_name=bucket_name,
        object_name=object_name,
        file_path=file_path,
    )
    print(f"🦩 With Minio client; Uploaded {object_name} "
          f"to {bucket_name} in {conn_params['target']} (etag: {result.etag})")


def minio_list_objects(conn_params: dict, bucket_name: str) -> None:
    """
    Ручка для просмотра содержимого бакета.

    :param conn_params: Параметры подключения.
    :param bucket_name: Имя бакета.
    :return: Ничего.
    """
    client = minio_client(conn_params)
    print(f"🦩 With Minio client; Objects in bucket '{bucket_name}' in {conn_params['target']}:")
    for obj in client.list_objects(bucket_name):
        print(obj.object_name, obj.size, obj.last_modified)


def boto3_client(conn_params: dict) -> boto3.client:
    """
    Функция для создания клиента S3.

    :param conn_params: Параметры подключения.
    :return: Клиент S3 (boto3).
    """
    session = boto3.session.Session()
    url = f"https://{conn_params['endpoint']}" \
        if conn_params.get("secure", True) else f"http://{conn_params['endpoint']}"
    return session.client(
        service_name="s3",
        aws_access_key_id=conn_params["access_key"],
        aws_secret_access_key=conn_params["secret_key"],
        endpoint_url=url,
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
    print(f"🪣 With Boto3 client; Buckets (boto3) in {conn_params['target']}:")
    for bucket in resp.get("Buckets", []):
        print(bucket["Name"], bucket["CreationDate"])


# noinspection PyTypeChecker
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
        print(f"🪣 With Boto3 client; Bucket '{bucket_name}' created! in {conn_params['target']}")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"🪣 With Boto3 client; Bucket '{bucket_name}' already exists in {conn_params['target']}.")
    except Exception as e:  # noqa: BLE001
        print(f"🪣 With Boto3 client; Error creating bucket: {e} in {conn_params['target']}")


def boto3_upload_csv(conn_params: dict, bucket_name: str, object_name: str, file_path: str) -> None:
    """
    Ручка для загрузки файла в бакет.

    :param conn_params: Параметры подключения.
    :param bucket_name: Имя бакета.
    :param object_name: Имя файла в бакете.
    :param file_path: Имя файла на диске.
    :return: Ничего.
    """
    if conn_params.get("target") == "vk":
        # VK Cloud лучше работает с Minio клиентом
        minio_upload_csv(
            conn_params=conn_params,
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=file_path,
        )
    else:
        s3 = boto3_client(conn_params)
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"🪣 With Boto3 client; Uploaded {object_name} to {bucket_name} in {conn_params['target']}")


def boto3_list_objects(conn_params: dict, bucket_name: str) -> None:
    """
    Ручка для просмотра содержимого бакета.

    :param conn_params: Параметры подключения.
    :param bucket_name: Имя бакета.
    :return: Ничего.
    """
    s3 = boto3_client(conn_params)
    resp = s3.list_objects_v2(Bucket=bucket_name)
    print(f"🪣 With Boto3 client; Objects in bucket '{bucket_name}' in {conn_params['target']}:")
    for obj in resp.get("Contents", []):
        print(obj["Key"], obj["Size"], obj["LastModified"])
