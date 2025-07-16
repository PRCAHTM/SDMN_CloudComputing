hostname
ps fax
echo "‑‑ Namespace inodes (should differ from host) ‑‑"
for ns in uts pid mnt net ; do readlink /proc/1/ns/$ns ; done
-e
echo "‑‑ Namespace inodes (should differ from host) ‑‑"
if [ -f /sys/fs/cgroup/memory.max ]; then     cat /sys/fs/cgroup/memory.max          # cgroup v2 (bytes or "max")
else     cat /sys/fs/cgroup/memory.limit_in_bytes   # cgroup v1
fi
exit
