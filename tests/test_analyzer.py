import unittest
from unittest.mock import MagicMock, patch

from src.analyzer import analyze_wallet


class AnalyzeWalletTests(unittest.TestCase):
    def setUp(self):
        self.address = "0x52908400098527886E0F7030069857D2E4169EE7"
        self.rpc_url = "https://rpc.example.invalid"

    @patch("src.analyzer.Web3")
    def test_returns_wallet_details_without_live_rpc(self, web3_class):
        web3_class.is_address.return_value = True
        web3_class.to_checksum_address.return_value = self.address
        web3_class.from_wei.return_value = "1.5"
        web3 = MagicMock()
        web3.is_connected.return_value = True
        web3.eth.chain_id = 1
        web3.eth.get_balance.return_value = 1_500_000_000_000_000_000
        web3.eth.get_transaction_count.return_value = 7
        web3_class.return_value = web3

        result = analyze_wallet(self.address.lower(), self.rpc_url)

        self.assertEqual(result, {"address": self.address, "chain_id": 1, "balance_eth": "1.5", "nonce": 7})
        web3_class.HTTPProvider.assert_called_once_with(self.rpc_url)
        web3.eth.get_balance.assert_called_once_with(self.address)
        web3.eth.get_transaction_count.assert_called_once_with(self.address)

    @patch("src.analyzer.Web3")
    def test_rejects_invalid_address_before_rpc(self, web3_class):
        web3_class.is_address.return_value = False
        with self.assertRaisesRegex(ValueError, "Invalid EVM address"):
            analyze_wallet("not-an-address", self.rpc_url)
        web3_class.assert_not_called()

    @patch("src.analyzer.Web3")
    def test_raises_when_rpc_is_unavailable(self, web3_class):
        web3_class.is_address.return_value = True
        web3_class.to_checksum_address.return_value = self.address
        web3 = MagicMock()
        web3.is_connected.return_value = False
        web3_class.return_value = web3
        with self.assertRaisesRegex(ConnectionError, "Could not connect"):
            analyze_wallet(self.address, self.rpc_url)
        web3.eth.get_balance.assert_not_called()


if __name__ == "__main__":
    unittest.main()
