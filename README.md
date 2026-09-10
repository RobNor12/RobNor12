# Hybrid Active Directory Lab: Windows 11 Enterprise & Ubuntu Integration

A multi-OS enterprise lab environment featuring a cloud-hosted Windows Server Domain Controller (`RNORRIS-LAB.LOCAL`), a native Windows 11 Enterprise client, and an Ubuntu Linux client integrated via Samba, Winbind, and PAM.

### 🏗️ Architecture & Topology

- **Domain Controller (DC):** Windows Server (`cwm3382.rnorris-lab.local`)
  - **IP Address:** `104.225.141.208`
  - **Domain Name:** `RNORRIS-LAB.LOCAL` (NetBIOS: `LAB`)
- **Client 1:** Windows 11 Enterprise (`WIN-CLIENT01`) (Natively joined via Active Directory domain join)
- **Client 2:** Ubuntu Linux (`rnorris-ubuntu`) (Integrated via Samba/Winbind & PAM)

---

### 🛠️ Key Technical Challenges & Solutions

### Ubuntu Linux Client Integration 

Integrating Linux clients with an Active Directory domain introduces notorious cross-platform friction. Below are the primary infrastructure hurdles and solutions implemented in this lab:

* **1. DNS Resolution & `systemd-resolved` Routing** 
  * **The Challenge:** Ubuntu’s local resolver (`127.0.0.53`) failed to resolve internal `.local` Active Directory SRV records (`_ldap._tcp.dc._msdcs.RNORRIS-LAB.LOCAL`), causing domain join authentication dropouts (*"No logon servers are currently available"*).
  * **The Solution:** Explicitly forced network interface DNS routing to point directly to the cloud Domain Controller and bound the domain search suffix:
    ```
    bash
    sudo resolvectl dns <INTERFACE_NAME> 104.225.141.208
    sudo resolvectl domain <INTERFACE_NAME> ~rnorris-lab.local
    ```
* **2. Samba & Winbind ID Mapping (smb.conf)**
  * **The Challenge:** Default Winbind settings failed to translate Active Directory Security IDs (SIDs) into valid Linux UIDs/GIDs, resulting in no such user errors when querying domain accounts like administrator.

  * **The Solution:** Configured an explicit RID-based ID mapping block and enabled user enumeration in /etc/samba/smb.conf:
    ```
    bash
    [global]
    security = ads
    workgroup = LAB
    realm = RNORRIS-LAB.LOCAL
  
    idmap config * : backend = tdb
    idmap config * : range = 3000-7999
    idmap config LAB : backend = rid
    idmap config LAB : range = 10000-999999
  
    winbind use default domain = yes
    winbind enum users = yes
    winbind enum groups = yes
    template shell = /bin/bash
    template homedir = /home/%D/%U
    ```
* **3. Automated PAM Home Directory Provisioning**
  * **The Challenge:** Authenticating domain users via su or SSH succeeded, but left them without a local working directory or shell environment.

  * **The Solution:** Configured and verified Pluggable Authentication Modules (PAM) to auto-provision home directories upon initial login:
  ```
  bash
  sudo pam-auth-update # Enabled "Create home directory on login"
  ```

### Windows 11 Enterprise Client Integration

Unlike the Linux client, the Windows 11 Enterprise endpoint was provisioned using the native operating system workflow:

1. **Domain Join:** Configured the system properties (`sysdm.cpl`) to join the `RNORRIS-LAB.LOCAL` domain using administrative credentials.
2. **DNS Validation:** Verified network adapter IPv4 settings pointed correctly to the cloud Domain Controller (`104.225.141.208`).
3. **Authentication Check:** Validated successful domain sign-in and remote management connectivity back to `cwm3382`.

---

### 🧪 Verification & Testing
* **1. Domain Join Status (Ubuntu Client)**
```
Bash
sudo net ads testjoin
```
Expected Output:

```
Plaintext
Join is OK
```

* **2. DC Connection & Trust Verification**
```
Bash
wbinfo --ping-dc
```

Expected Output:

```
Plaintext
checking the NETLOGON for domain[LAB] dc connection to "CWM3382.rnorris-lab.local" succeeded
```

* **3. Active Directory User Resolution**
```
Bash
id administrator
```
Expected Output:

```
Plaintext
uid=10500(administrator) gid=10513(domain users) groups=10513(domain users),10500(administrator),...
```

* **4. Fleet Inventory (PowerShell on Domain Controller)**

```
PowerShell
Get-ADComputer -Filter * -Properties OperatingSystem, LastLogonDate | Select-Object Name, OperatingSystem, LastLogonDate
```
Expected Output:

```Plaintext
Name            OperatingSystem        LastLogonDate
----            ----------------       -------------
CWM3382         Windows Server...      ...
ROBERT-WIN11    Windows 11 Enterprise  ...
robert-ubuntu   Ubuntu                 ...
```

---

### 📂 Repository Structure
*   **[🧱 assets/](assets/)** 🛠️
    *   Contains the infrastructure "blueprints," including `smb.conf` configurations.
*   **[📖 documentation/](documentation/)** 🖼️
    *   Houses the project documentation, including architectural diagrams, workflow logic, and screenshots of the active directory.

---

### 🚀 Future Enhancements
Implementing Group Policy Objects (GPOs) to restrict SSH access on Linux clients to specific AD security groups.

Integrating log shipping and auditing through SIEM agents (e.g., Wazuh/TheHive lab configuration).

---

### Return page

[Return to Repository Hub](https://github.com/RobNor12/IT-Automation-Engineering/blob/main/README.md)
