import os
import subprocess
from unittest import TestCase

class PipelineTest(TestCase):
    def test_execution(self):
        os.chdir('./data')
        subprocess.run(['python3', './pipeline.py'])
        assert os.path.exists('./data.sqlite')
        