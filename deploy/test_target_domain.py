from pathlib import Path
import unittest

from importlib.util import module_from_spec, spec_from_file_location

BASE = Path(__file__).resolve().parent
spec = spec_from_file_location('target_domain', BASE / 'target-domain.py')
target_domain = module_from_spec(spec)
spec.loader.exec_module(target_domain)


class DeployDomainTest(unittest.TestCase):
    def test_nginx_template_can_publish_each_environment(self):
        template = (BASE / 'nginx/atlas-app.conf').read_text()
        for domain in ['demo.amontadavalley.com.br', 'comprasabertas.amontadavalley.com.br']:
            with self.subTest(domain=domain):
                actual = target_domain.domain_from_url('https://' + domain)
                rendered = template.replace('__APP_DOMAIN__', actual)
                self.assertIn('server_name ' + domain + ';', rendered)
                self.assertNotIn('__APP_DOMAIN__', rendered)
                self.assertIn('proxy_pass http://127.0.0.1:3001;', rendered)

    def test_accepts_trailing_slash_and_normalizes_domain(self):
        self.assertEqual(target_domain.domain_from_url('https://DEMO.amontadavalley.com.br/'),
                         'demo.amontadavalley.com.br')

    def test_rejects_invalid_or_ambiguous_targets(self):
        for value in ['', 'demo.amontadavalley.com.br', 'http://demo.amontadavalley.com.br',
                      'https://user:password@example.com', 'https://example.com/path',
                      'https://example.com?query=1', 'https://example.com:3000',
                      'https://example.com;include', 'https://example.com\nserver_name other;']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                target_domain.domain_from_url(value)


if __name__ == '__main__':
    unittest.main()
