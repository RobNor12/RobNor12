# Azure Hybrid Active Directory Lab

### 📖 Overview

This project is a small hybrid Active Directory lab built in Microsoft Azure to practice Windows administration, Linux administration, Active Directory, DNS, authentication, network segmentation, and Azure networking.

The core environment consists of a Windows Server domain controller, a Windows 11 domain client, and an Ubuntu Linux domain client. Both Windows and Linux systems were successfully joined to and authenticated against the same Active Directory domain.

The project was also designed with security and troubleshooting in mind by separating the virtual machines into individual subnets and applying role-specific Network Security Group (NSG) rules.

---

### 🎯 Project Goals

The primary goals of this project were to:

* Build and configure an Active Directory environment in Azure.
* Configure Active Directory Domain Services (AD DS) and DNS.
* Create and manage organizational units, users, and security groups.
* Join a Windows 11 client to the domain.
* Join an Ubuntu Linux client to the domain.
* Configure Linux authentication through Kerberos, SSSD, `realmd`, and `adcli`.
* Segment workloads into separate Azure subnets.
* Configure NSGs based on the role of each virtual machine.
* Validate that security restrictions did not break required AD functionality.
* Document troubleshooting and configuration decisions throughout the project.

An additional stretch goal is to connect an external VM outside Azure to the Azure-hosted domain through a VPN and validate hybrid connectivity.

---

### 🏗️ Architecture

### Domain

| Setting           | Value               |
| ----------------- | ------------------- |
| AD Domain         | `ad.hybridlab.test` |
| NetBIOS Name      | `AD`                |
| Domain Controller | `DC02`              |
| DC Private IP     | `10.10.10.4`        |

### Virtual Machines

| VM      | Role                    | Operating System                  | Subnet          |
| ------- | ----------------------- | --------------------------------- | --------------- |
| `DC02`  | Domain Controller / DNS | Windows Server 2022 Azure Edition | `10.10.10.0/24` |
| `WIN01` | Windows Domain Client   | Windows 11                        | `10.10.20.0/24` |
| `LNX01` | Linux Domain Client     | Ubuntu 22.04                      | `10.10.30.0/24` |

The virtual machines were intentionally placed into separate subnets instead of a single shared subnet. This allows network traffic to be controlled according to each machine's role.

---

### 🖥️ Azure Resources

The lab uses the following Azure resources:

* Resource Group: `rg-azure-hybrid-lab`
* Virtual Network: `vnet-hybrid-lab`
* Separate subnet for each virtual machine
* One Network Security Group per workload
* Three Azure virtual machines
* Azure-managed networking and private IP addressing

The Azure resources were deployed primarily through Azure PowerShell.

---

### ⚙️ Active Directory Structure

The Active Directory environment uses separate organizational units for different roles:

```text
ad.hybridlab.test
│
├── IT
├── HR
├── Sales
└── DCAdmins
```

Security groups were created to represent the different administrative or organizational roles:

```text
SG-IT
SG-HR
SG-Sales
SG-DCAdmins
```

Test accounts were created and assigned to the appropriate groups to validate group membership and access control.

The domain administrator account was kept separate from the normal test users so that delegated permissions could be tested independently from full domain administration.

---

### 🛠 Domain Controller

`DC02` was deployed as a Windows Server 2022 Azure Edition virtual machine and configured with:

* Active Directory Domain Services
* Active Directory-integrated DNS
* Domain `ad.hybridlab.test`

The domain controller was configured and tested before joining the client machines.

Basic AD validation included:

```powershell
Get-ADDomain
Get-ADDomainController
dcdiag
dcdiag /test:dns
```

The domain was also tested by creating users, security groups, and computer accounts.

---

### Windows Client

`WIN01` was configured to use the domain controller's private IP address (`10.10.10.4`) as its DNS server.

Connectivity to the domain controller was tested before performing the domain join.

Examples of validation performed on the Windows client included:

```powershell
Test-NetConnection 10.10.10.4 -Port 53
Test-NetConnection 10.10.10.4 -Port 88
Test-NetConnection 10.10.10.4 -Port 389
```

After successful connectivity testing, `WIN01` was joined to:

```text
ad.hybridlab.test
```

Domain membership was verified with:

```powershell
(Get-CimInstance Win32_ComputerSystem).PartOfDomain
```

which returned:

```text
True
```

The resulting computer account was then moved from the default `Computers` container into the appropriate organizational unit through Active Directory Users and Computers.

---

### Linux Client

`LNX01` was configured as an Ubuntu 22.04 Active Directory client.

The following Linux components were used:

* `realmd`
* `adcli`
* `sssd`
* `sssd-ad`
* Kerberos
* Samba components
* `packagekit`

Ubuntu was configured to use the Active Directory domain controller as its DNS server:

```text
10.10.10.4
```

The Linux system was joined using:

```bash
sudo realm join ad.hybridlab.test -U 'lab-domain-admin'
```

After joining, the Linux machine was validated with:

```bash
realm list
```

```bash
sudo adcli testjoin
```

```bash
id 'ituser01@ad.hybridlab.test'
```

SSSD was also verified to be running:

```bash
sudo systemctl status sssd
```

The Linux client successfully resolved domain users, authenticated against Active Directory, and established a machine account in AD.

The resulting `LNX01` computer object was moved into the `IT` OU.

---

### 🛡️ Network Security

Each virtual machine has its own Network Security Group so that network traffic can be controlled according to the workload.

### DC02

The domain controller permits inbound traffic required for:

| Service             | Port | Protocol | Purpose                              |
| ------------------- | ---: | -------- | ------------------------------------ |
| RDP                 | 3389 | TCP      | Administrative access                |
| DNS                 |   53 | TCP/UDP  | DNS resolution                       |
| Kerberos            |   88 | TCP/UDP  | Authentication                       |
| LDAP / DC Locator   |  389 | TCP/UDP  | Directory services                   |
| SMB                 |  445 | TCP      | Windows file and AD-related services |
| RPC Endpoint Mapper |  135 | TCP      | Windows RPC                          |

Administrative access is restricted to the administrator's external IP address where applicable.

Outbound traffic from the domain controller was left at the normal Azure defaults because the domain controller provides infrastructure services and may require general outbound connectivity.

### WIN01

Inbound access is primarily restricted to:

```text
TCP 3389 → RDP administration
```

Outbound traffic is restricted to the traffic required to communicate with the domain controller and perform normal client operations.

### LNX01

Inbound access is primarily restricted to:

```text
TCP 22 → SSH administration
```

Outbound traffic includes the required DNS, Kerberos, LDAP, and related Active Directory communication directed toward the domain controller.

The goal was to avoid exposing AD services unnecessarily while maintaining the functionality required by the lab.

---

### 📋 Validation

The completed Azure environment was tested from both Windows and Linux.

### Active Directory

* AD DS installed and operational
* DNS zone for `ad.hybridlab.test` operational
* Test users successfully created
* Security groups successfully created
* Computer accounts successfully created and managed
* Domain controller health verified with AD diagnostic tools

### Windows

* Windows client successfully resolved the domain controller
* Required AD ports were reachable
* Windows client successfully joined the domain
* Domain membership verified
* Domain user authentication verified

### Linux

* Linux client successfully resolved the domain controller
* Kerberos authentication successfully obtained a ticket
* LDAP service ticket successfully obtained
* Linux client successfully joined the domain
* SSSD successfully started
* AD users successfully resolved through SSSD
* Linux machine trust successfully validated with `adcli testjoin`
* Domain user authentication successfully tested

### Network Security

After implementing the NSG rules, connectivity tests were repeated to ensure that required Active Directory functionality remained operational.

This provided a basic validation of the security changes rather than assuming that the rules were correct.

---

### 🔧 Troubleshooting

### Azure VM Allocation and SKU Compatibility

The original domain controller encountered Azure VM allocation problems.

The VM was initially using a SKU that Azure could no longer reliably allocate in the selected region. Several potential replacement SKUs also introduced compatibility restrictions involving NVMe storage and confidential computing.

This ultimately led to rebuilding the domain controller with a supported VM configuration rather than spending the remaining lab time waiting for Azure capacity to change.

### Linux Active Directory Join

The Linux domain join initially returned:

```text
Insufficient permissions to join the domain
```

Verbose `realm join` output revealed that the actual failure was occurring during Kerberos GSSAPI/SASL authentication:

```text
Server not found in Kerberos database
```

The issue was isolated by testing each component independently:

```text
DNS resolution                 → working
Kerberos authentication       → working
LDAP service ticket           → working
AD credentials                → working
```

A hostname/reverse-DNS inconsistency was then addressed by configuring Kerberos not to rely on reverse DNS during service discovery.

The subsequent join succeeded and created the Linux computer account, machine password, SPNs, and Kerberos keytab entries.

### Ubuntu DNS Reverting to Azure DNS

After the Linux VM was restarted, Ubuntu repeatedly returned to Azure's DHCP-provided DNS server:

```text
168.63.129.16
```

instead of consistently using the AD DNS server:

```text
10.10.10.4
```

Direct DNS queries to `10.10.10.4` worked, proving the AD DNS server itself was functioning.

The issue was corrected through the Netplan configuration by preventing DHCP-provided DNS from replacing the manually configured DNS server:

```yaml
dhcp4-overrides:
  use-dns: false

nameservers:
  addresses:
    - 10.10.10.4
```

After the change, normal system resolution successfully located:

```text
dc02.ad.hybridlab.test
```

and the configuration remained functional after subsequent validation.

### NSG Configuration

During security-rule testing, a few configuration mistakes were identified, including an incorrect LDAP destination port.

The NSGs were corrected and connectivity was retested afterward.

This reinforced the importance of validating individual protocol requirements rather than assuming that a generic "AD" rule is sufficient.

---

### 💡 Lessons Learned

This project reinforced several practical administration concepts:

* Active Directory depends heavily on reliable DNS.
* Kerberos authentication is sensitive to hostname and service-principal configuration.
* Linux can integrate with Active Directory through standard identity and authentication components such as SSSD, Kerberos, `realmd`, and `adcli`.
* OUs are useful for organization and policy application, while security groups are better suited for access control.
* Azure VM size availability depends on more than CPU and memory requirements; regional capacity, architecture, storage controller, quota, and security features can all affect deployment.
* NSGs should be designed around the actual traffic requirements of each workload.
* Testing individual network layers makes troubleshooting significantly easier.

---

### 🏗️ Repository Structure

*   **[🧱 assets/](assets/)** 🛠️
    *   Contains the infrastructure "blueprints," including `smb.conf` configurations.
*   **[📖 documentation/](documentation/)** 🖼️
    *   Contains screenshots, diagrams, and other evidence of the completed environment.

---

### 🚀 Future Work

The primary Azure AD environment is complete.

The remaining stretch goal is to establish connectivity from an external VM outside the Azure VNet and validate that the external machine can communicate with and authenticate against the Azure-hosted domain controller.

This would extend the project from an Azure-only Active Directory environment into a more complete hybrid networking demonstration.

---
##
