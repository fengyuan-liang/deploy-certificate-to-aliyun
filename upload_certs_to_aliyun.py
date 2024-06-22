import os
from aliyunsdkcore.client import AcsClient
from aliyunsdkcdn.request.v20180510 import SetDomainServerCertificateRequest

def get_env_var(key):
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(f"Environment variable {key} not set")
    return value

def upload_certificate(client, domain_name, cert_path, key_path):
    with open(cert_path, 'r') as f:
        cert = f.read()

    with open(key_path, 'r') as f:
        key = f.read()

    request = SetDomainServerCertificateRequest.SetDomainServerCertificateRequest()
    request.set_accept_format('json')
    request.set_DomainName(domain_name)
    request.set_SSLProtocol('on')
    request.set_CertType('upload')
    request.set_SSLPub(cert)
    request.set_SSLPri(key)

    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))

def main():
    access_key_id = get_env_var('ALIYUN_ACCESS_KEY_ID')
    access_key_secret = get_env_var('ALIYUN_ACCESS_KEY_SECRET')
    domains = get_env_var('DOMAINS').split(',')
    cdn_domains = get_env_var('ALIYUN_CDN_DOMAINS').split(',')

    client = AcsClient(access_key_id, access_key_secret, 'cn-hangzhou')

    for domain, cdn_domain in zip(domains, cdn_domains):
        cert_path = f'~/certs/{domain}/fullchain.pem'
        key_path = f'~/certs/{domain}/privkey.pem'
        upload_certificate(client, cdn_domain, cert_path, key_path)

if __name__ == "__main__":
    main()