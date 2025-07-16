#!/usr/bin/env python3

import os
import subprocess
import argparse
import logging

class ContainerManager:
    """
    Encapsulates the logic for creating and running a lightweight container.
    """
    def __init__(self, hostname: str, rootfs: str = "container", memory_limit_mb: int = None):
        self.hostname = hostname
        self.rootfs = rootfs
        self.memory_limit_mb = memory_limit_mb
        self.pid = os.getpid()
        self.cgroup_path = f"/sys/fs/cgroup/memory/container_{self.pid}"

    def apply_memory_limit(self):
        """
        Sets up a memory cgroup for this process and applies a memory limit.
        """
        os.makedirs(self.cgroup_path, exist_ok=True)
        limit_bytes = self.memory_limit_mb * 1024**2
        with open(os.path.join(self.cgroup_path, "memory.limit_in_bytes"), 'w') as limit_file:
            limit_file.write(str(limit_bytes))
        with open(os.path.join(self.cgroup_path, "tasks"), 'w') as tasks_file:
            tasks_file.write(str(self.pid))
        logging.debug(f"Memory limit of {self.memory_limit_mb} MB applied to cgroup {self.cgroup_path}")

    def launch(self):
        """
        Unshares namespaces, optionally applies memory limit, and drops into a shell in the new root.
        """
        logging.info(f"Container starting with PID {self.pid}\nHostname: {self.hostname}\nRootfs: {self.rootfs}")

        if self.memory_limit_mb is not None:
            self.apply_memory_limit()

        command = [
            "unshare", "--uts", "--net", "--pid", "--mount", "--fork",
            "chroot", self.rootfs, "/bin/bash", "-c",
            f"mount -t proc proc /proc && hostname {self.hostname} && exec bash"
        ]
        subprocess.run(command, check=True)
        logging.info("Container process exited")


def parse_args():
    parser = argparse.ArgumentParser(description="Launch an isolated container environment.")
    parser.add_argument(
        "hostname",
        help="Hostname to assign inside the container"
    )
    parser.add_argument(
        "-r", "--rootfs",
        default="container",
        help="Path to the container filesystem root"
    )
    parser.add_argument(
        "-m", "--memory",
        type=int,
        metavar="MB",
        help="Optional memory limit in megabytes"
    )
    return parser.parse_args()


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s"
    )
    args = parse_args()
    manager = ContainerManager(
        hostname=args.hostname,
        rootfs=args.rootfs,
        memory_limit_mb=args.memory
    )
    manager.launch()


if __name__ == "__main__":
    main()

