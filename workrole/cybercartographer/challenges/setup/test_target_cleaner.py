"""Run with: python3 -m unittest discover -s workrole/cybercartographer/challenges/setup"""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('cleaner', Path(__file__).resolve().parents[2] / 'cyberorg_classroom_targets_cleaner.py')
cleaner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cleaner)


class CleanerTests(unittest.TestCase):
    def test_inventory_validation_and_order(self):
        pasted = 'Ubuntu: 10.15.4.2\nKali (10.15.0.9/17)\nhttp://10.15.4.2:8080\n999.1.2.3 10.15.4.2\nversion1.2.3.4 1.2.3.4.5'
        self.assertEqual(cleaner.extract_addresses(pasted), ['10.15.0.9', '10.15.4.2'])

    def test_244_addresses_and_duplicate_inventory(self):
        addresses = [f'10.15.0.{i}' for i in range(1, 245)]
        self.assertEqual(cleaner.extract_addresses('\n'.join(list(reversed(addresses)) * 2)), addresses)

    def test_output_and_failed_refresh_preserves_previous_list(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'dirty.txt'
            output = Path(folder) / 'clean.txt'
            with patch.object(cleaner, 'SOURCE', source), patch.object(cleaner, 'OUTPUT', output):
                self.assertEqual(cleaner.main(), 1)
                source.write_text('Ubuntu: 10.15.0.5\n10.15.0.5\nKali: 10.15.0.9')
                self.assertEqual(cleaner.main(), 0)
                self.assertEqual(output.read_text(), '10.15.0.5\n10.15.0.9\n')
                source.write_text('No VMs available')
                self.assertEqual(cleaner.main(), 1)
                self.assertEqual(output.read_text(), '10.15.0.5\n10.15.0.9\n')


if __name__ == '__main__':
    unittest.main()
