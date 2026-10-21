"""Validate the public deploy URL before using its hostname in Nginx or SSH."""
import re
import sys
from urllib.parse import urlsplit


def domain_from_url(value):
    if not value or any(character.isspace() for character in value):
        raise ValueError('SITE_URL precisa ser uma URL HTTPS sem espaços')
    url = urlsplit(value)
    if (url.scheme != 'https' or url.username or url.password
            or url.port not in (None, 443) or url.path not in ('', '/')
            or url.query or url.fragment):
        raise ValueError('SITE_URL deve conter somente https:// e o domínio público')
    domain = url.hostname or ''
    label = r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?'
    if len(domain) > 253 or not re.fullmatch(rf'{label}(?:\.{label})+', domain):
        raise ValueError('Domínio público inválido em SITE_URL')
    return domain


if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise ValueError('Informe SITE_URL para configurar o domínio do deploy')
        print(domain_from_url(sys.argv[1]))
    except ValueError as error:
        raise SystemExit(str(error)) from None
