#!/usr/bin/env python3
"""Test module for client.GithubOrgClient"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        test_payload = {
            "name": org_name,
            "repos_url": f"https://api.github.com/orgs/{org_name}/repos"
        }
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, test_payload)
        mock_get_json.reset_mock()

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct value"""
        test_payload = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }

        with patch(
            'client.GithubOrgClient.org',
            new_callable=PropertyMock,
            return_value=test_payload
        ) as mock_org:
            client = GithubOrgClient("testorg")
            result = client._public_repos_url

            mock_org.assert_called_once()
            self.assertEqual(result, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos method"""
        test_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None},
        ]
        mock_get_json.return_value = test_repos_payload

        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/testorg/repos"
        ) as mock_public_repos_url:
            client = GithubOrgClient("testorg")
            repos = client.public_repos()

            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(repos, expected_repos)
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/testorg/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """Test has_license static method"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up class fixture before running tests"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            """Side effect to return different payloads based on URL"""
            if url.endswith('/orgs/google'):
                return cls.org_payload
            elif url.endswith('/orgs/google/repos'):
                return cls.repos_payload
            return None

        cls.mock_get.return_value.json.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down the class fixture after running tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos without license filter"""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)
        self.mock_get.assert_called()

    def test_public_repos_with_license(self):
        """Test public_repos with Apache 2.0 license filter"""
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)
        self.mock_get.assert_called()


if __name__ == '__main__':
    unittest.main()
