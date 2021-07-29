
import os
import sys

import torch
import torch.distributed as dist

torch.backends.cuda.matmul.allow_tf32 = False

if not dist.is_available():
    print("Distributed not available, skipping tests", file=sys.stderr)
    sys.exit(0)

from torch.testing._internal.common_utils import run_tests, TEST_WITH_ASAN, NO_MULTIPROCESSING_SPAWN
from torch.testing._internal.distributed.distributed_test import (
    DistributedTest, TestDistBackend
)

if TEST_WITH_ASAN:
    print("Skip ASAN as torch + multiprocessing spawn have known issues", file=sys.stderr)
    sys.exit(0)

if NO_MULTIPROCESSING_SPAWN:
    print("Spawn not available, skipping tests.", file=sys.stderr)
    sys.exit(0)

BACKEND = os.environ["BACKEND"]

if BACKEND == "gloo" or BACKEND == "nccl" or BACKEND == "_internal_ucc":
    class TestDistBackendWithSpawn(TestDistBackend, DistributedTest._DistTestBase):

        def setUp(self):
            super().setUp()
            self._spawn_processes()
            torch.backends.cudnn.flags(allow_tf32=False).__enter__()


if __name__ == "__main__":
    run_tests()
