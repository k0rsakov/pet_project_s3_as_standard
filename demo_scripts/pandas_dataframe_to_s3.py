import pandas as pd

from utils.pandas_utils import pandas_to_s3_csv
from utils.s3_utils import S3_CONFIGS

df = pd.DataFrame(data={"column": ["a", "b", "c"]})

pandas_to_s3_csv(
    df=df,
    conn_params=S3_CONFIGS["minio"],
    bucket_name=S3_CONFIGS["minio"]["bucket"],
)

pandas_to_s3_csv(
    df=df,
    conn_params=S3_CONFIGS["selectel"],
    bucket_name=S3_CONFIGS["selectel"]["bucket"],
)

pandas_to_s3_csv(
    df=df,
    conn_params=S3_CONFIGS["vk"],
    bucket_name=S3_CONFIGS["vk"]["bucket"],
)

pandas_to_s3_csv(
    df=df,
    conn_params=S3_CONFIGS["aws"],
    bucket_name=S3_CONFIGS["aws"]["bucket"],
)
