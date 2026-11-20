from __future__ import annotations

import datetime as dt
import os
import sys
from pathlib import Path

from aliyunsdkcore.client import AcsClient
from aliyunsdkcdn.request.v20180510 import SetCdnDomainSSLCertificateRequest

# 证书根目录，默认 ~/certs；可在 CI 中用 CERT_DIR=/workspace/certs 覆盖
CERT_DIR = Path(os.getenv("CERT_DIR", "~/certs")).expanduser()
REGION = os.getenv("ALIYUN_REGION", "cn-hangzhou")


def get_env_var(key: str) -> str:
    value = os.getenv(key, "").strip()
    if not value:
        raise EnvironmentError(f"Environment variable {key} is not set or empty")
    return value


def split_csv(raw: str) -> list[str]:
    # 环境变量里常出现空项或前后空格，统一清洗
    return [item.strip() for item in raw.split(",") if item.strip()]


def read_non_empty(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError(f"File is empty: {path}")
    return text


def upload_certificate(
    client: AcsClient,
    cdn_domain: str,
    cert_path: Path,
    key_path: Path,
) -> None:
    cert = read_non_empty(cert_path)
    key = read_non_empty(key_path)

    request = SetCdnDomainSSLCertificateRequest.SetCdnDomainSSLCertificateRequest()
    # 证书名称带上精确到秒的 UTC 时间戳，避免同日重复更新重名
    request.set_CertName(
        f"{cdn_domain}-{dt.datetime.now(dt.timezone.utc):%Y%m%d%H%M%S}"
    )
    request.set_DomainName(cdn_domain)
    request.set_CertType("upload")
    request.set_SSLProtocol("on")
    request.set_SSLPub(cert)
    request.set_SSLPri(key)
    request.set_CertRegion(REGION)

    response = client.do_action_with_exception(request)
    print(f"[OK] {cdn_domain}: {response.decode('utf-8')}")


def main() -> int:
    access_key_id = get_env_var("ALIYUN_ACCESS_KEY_ID")
    access_key_secret = get_env_var("ALIYUN_ACCESS_KEY_SECRET")
    domains = split_csv(get_env_var("DOMAINS"))
    cdn_domains = split_csv(get_env_var("ALIYUN_CDN_DOMAINS"))

    if len(domains) != len(cdn_domains):
        raise ValueError(
            f"DOMAINS ({len(domains)}) and ALIYUN_CDN_DOMAINS ({len(cdn_domains)}) "
            f"must have equal length: {domains} vs {cdn_domains}"
        )

    client = AcsClient(access_key_id, access_key_secret, REGION)

    # 单个域名失败不阻断其他域名，最后汇总退出码，CI 能正确感知失败
    failures: list[str] = []
    for domain, cdn_domain in zip(domains, cdn_domains):
        cert_path = CERT_DIR / domain / "fullchain.pem"
        key_path = CERT_DIR / domain / "privkey.pem"
        try:
            upload_certificate(client, cdn_domain, cert_path, key_path)
        except Exception as exc:  # noqa: BLE001
            print(
                f"[FAIL] {cdn_domain}: {type(exc).__name__}: {exc}",
                file=sys.stderr,
            )
            failures.append(cdn_domain)

    if failures:
        print(f"Failed domains: {', '.join(failures)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
