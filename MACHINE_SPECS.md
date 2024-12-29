# Machine Specifications

This document contains the specifications of the machine used for performance analysis and comparison of in-degree distribution implementations.

## System Information

### Operating System
```
Distributor ID: Ubuntu
Description:    Ubuntu 22.04.5 LTS
Release:        22.04
Codename:       jammy
```

### CPU Information
```
Architecture:        x86_64
CPU(s):             2
Model name:         AMD EPYC
Thread(s) per core: 1
Core(s) per socket: 2
Socket(s):          1
L1d cache:          64 KiB (2 instances)
L1i cache:          64 KiB (2 instances)
L2 cache:           1 MiB (2 instances)
L3 cache:           32 MiB (1 instance)
Virtualization:     AMD-V
```

### Memory Information
```
               total        used        free      shared  buff/cache   available
Mem:           7.8Gi       678Mi       1.6Gi        37Mi       5.5Gi       6.8Gi
Swap:             0B          0B          0B
```

### Disk Space
```
Filesystem     Size  Used  Avail  Use%  Mounted on
/dev/vdb       125G  4.7G   114G    4%  /rom/overlay
tmpfs          3.9G     0   3.9G    0%  /dev/shm
```

### Development Environment
```
Python Version: 3.12.7
Java Version:   OpenJDK 17.0.13 (build 17.0.13+11-Ubuntu-2ubuntu122.04)
```

## Notes
- All performance measurements and comparisons were conducted on this machine
- System has adequate memory (7.8GB) and storage (125GB) for handling the graph datasets
- No swap space configured
- Running in a virtualized environment (KVM)
