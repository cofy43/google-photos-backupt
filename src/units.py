import psutil
import math
from typing import Tuple, List

def convert_size(size_bytes: int) -> str:
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def get_disk_partitions() -> Tuple[List[dict], List[dict]]:
    partitions = psutil.disk_partitions()
    internal_disks = []
    external_disks = []

    # List of mount points to exclude
    exclude_mountpoints = [
        '/System', '/private', '/dev', '/Volumes/Preboot', '/Volumes/Recovery', '/Volumes/VM'
    ]

    for partition in partitions:
        if any(partition.mountpoint.startswith(exclude) for exclude in exclude_mountpoints):
            continue

        usage = psutil.disk_usage(partition.mountpoint)
        disk_info = {
            'device': partition.device,
            'mountpoint': partition.mountpoint,
            'total': convert_size(usage.total),
            'used': convert_size(usage.used),
            'free': convert_size(usage.free),
            'percent': usage.percent
        }
        # Detect external drives based on the mount point and partition options
        if 'removable' in partition.opts or '/Volumes' in partition.mountpoint:
            external_disks.append(disk_info)
        else:
            internal_disks.append(disk_info)

    return internal_disks, external_disks
