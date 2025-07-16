#!/usr/bin/env python

import os
import subprocess
import sys


def _build_cgroup_path(pid):
    """Construct the memory cgroup directory for this process."""
    base = "/sys/fs/cgroup/memory"
    return os.path.join(base, f"container_{pid}")


def _ensure_dir(path):
    """Create a directory if it doesn’t already exist."""
    os.makedirs(path, exist_ok=True)


def _write_cgroup_file(cg_path, filename, content):
    """Write a string value into a cgroup control file."""
    file_path = os.path.join(cg_path, filename)
    with open(file_path, 'w') as f:
        f.write(str(content))


def set_memory_limit(limit):
    """
    Public API: limit memory (in MiB) for this container’s cgroup.
    """
    pid = os.getpid()
    cg_path = _build_cgroup_path(pid)
    _ensure_dir(cg_path)

    # Set the memory cap and add this process to the group
    _write_cgroup_file(cg_path, "memory.limit_in_bytes", limit * 1024**2)
    _write_cgroup_file(cg_path, "tasks", pid)


def _compose_unshare_command(hostname, rootfs):
    """Build the subprocess command for unshare + chroot."""
    return [
        "unshare", "--uts", "--net", "--pid", "--mount", "--fork",
        "chroot", rootfs, "/bin/bash", "-c",
        f"mount -t proc proc /proc; hostname {hostname}; exec bash"
    ]


def _run_subprocess(cmd):
    """Run a command and raise if it fails."""
    subprocess.run(cmd, check=True)


def run_container(hostname, rootfs, limit=False):
    """
    Public API: start a minimal containerized bash with optional memory limit.
    """
    my_pid = os.getpid()
    print(f"Container started running with PID: {my_pid}")

    if limit:
        set_memory_limit(limit)

    cmd = _compose_unshare_command(hostname, rootfs)
    _run_subprocess(cmd)


def main():
    """
    CLI entrypoint: usage:
      script.py <hostname> [memory_limit_mib]
    """
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <hostname> [memory_limit_mib]")
        sys.exit(1)

    hostname = sys.argv[1]
    rootfs = "container"

    if len(sys.argv) > 2:
        mem_limit = int(sys.argv[2])
        run_container(hostname, rootfs, limit=mem_limit)
    else:
        run_container(hostname, rootfs)


if __name__ == "__main__":
    main()

