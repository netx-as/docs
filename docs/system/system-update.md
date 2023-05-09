# System update

System update enables you to add new features and fix bugs. Installing updates for software packages, `netc` or the kernel 
itself, is a highly recommended. NetXOS is derived from RedHat/CentOS distributions and use their standard RPM packages and 
repositories. The package management utilities in NetXOS are already configured to use several repositories:

* **[base]**: The basic packages that make up NetXOS. It is enabled by default. 
* **[updates]**: Updated packages to [base] repository. Contains Security, BugFix, or Enhancements to the [base] software. It is enabled by default. 
* **[extras]** Packages that add functionality to the core distribution. It is enabled by default.
* **[epel]** Extra Packages for Enterprise Linux (EPEL) repository provides set of additional packages for Enterprise Linux. It is enabled by default.
* **[netx]** Repository that contains custom packages designed primarily for NetXOS. These packages add new functionality and updates/enhanced some of the [base], or [updates] packages. The repository provides core NetXOS packages, such as `netc`. It is enabled by default. 
* **[netx-devel]** Development version for [netx] packages. These packages use up-to-date git code and have undergone some basic testing. Users should not use this repository except for a specific reason. It is disabled by default.

## Update naming conventions
NetXOS version uses the same naming convention as CentOS -- see [CentOS Versioning and Releases](https://en.wikipedia.org/wiki/CentOS#Versioning_and_releases) for details. 

`netc` package employs [Semantic Versioning](https://semver.org/) scheme using version number MAJOR.MINOR.PATCH for stable packages. 
MAJOR version is changed when there are incompatible API changes, MINOR version when new functionality is added in a backwards-compatible 
manner, and PATCH version is increased for backwards-compatible bug fixes.

The versioning scheme is changed for devel packages to MAJOR.MINOR.PATCH.C.abrv, where C is number of commits since stable and abrv is 
an abbreviated object name for the commit itself.

## Updating system

Updating system can be done `system update` command. The command will print all packages that can be updated and ask for 
confirmation. For example, the following output shows that `netc` package from devel repository is available in a new version.

```
netx# system update 
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
Resolving Dependencies
--> Running transaction check
---> Package netc.x86_64 0:1.13-1.40.g2f6d346.el7.netx will be updated
---> Package netc.x86_64 0:1.13-1.44.g8a297e7.el7.netx will be an update
--> Finished Dependency Resolution

Dependencies Resolved

===========================================================================================
 Package      Arch           Version                              Repository          Size
===========================================================================================
Updating:
 netc         x86_64         1.13-1.44.g8a297e7.el7.netx          netx-devel          95 k

Transaction Summary
===========================================================================================
Upgrade  1 Package

Total download size: 95 k
Is this ok [y/d/N]: 
```
> [!NOTE]
> `y` stands for yes, `N` for no and `d` means download only. Pressing `d` will not update, just download. 

It's possible to check find out version of the system OS and `netc` package using `show system` command.

```
netx# show system 
Platform:             NetX-X1120
NetX OS version:      NetXOS release 7.4.1708 (Core) 
Netc version:         1.13-1.44.g8a297e7.
Kernel version:       3.10.0-693.17.1.el7.netx.x86_64
Uptime:               up 9 weeks, 5 days, 21 hours, 20 minutes
Power Consumption:    46 W
Service Module IP:    192.168.1.1/24
```

### Update proxy

Updating via HTTP proxy server can be enabled using `system update-proxy` command.
Available command options:
* `server` - hostname or ip address of proxy server
* `port` - optional parameter - default port `3128` used if not configured
* `username` - optional parameter
* `password` - optional parameter

```
netx# system update-proxy server proxy.netx.as port 8080
```

## Enabling devel repo

If there is a specific reason, e.g. you want to try a new feature not available in the stable repo yet, it's possible to enable
devel repository using `system release-channel devel` command. `show system release-channel devel` command can be used to check
if the repository has been enabled properly.

```
netx# system release-channel devel  

! check if the devel repository is enabled

netx# show system release-channel devel
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
Repo-id      : netx-devel/7
Repo-name    : netx-devel
Repo-status  : enabled
Repo-revision: 1540911502
Repo-updated : Tue Oct 30 14:58:23 2018
Repo-pkgs    : 94
Repo-size    : 8.2 M
Repo-baseurl : https://repo.netx.as/netx/7/netx-devel/
Repo-expire  : 21600 second(s) (last: Thu Nov  1 13:24:27 2018)
  Filter     : read-only:present
Repo-filename: /etc/yum.repos.d/netx.repo
```
