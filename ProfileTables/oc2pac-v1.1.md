         title: "OpenC2 Actuator Profile for Security Posture Attribute Collection"
       package: "http://oasis-open.org/openc2/oc2pac/v1.1"
    namespaces: {"ls": "http://oasis-open.org/openc2/oc2ls-types/v1.1"}
       exports: ["AP-Target", "AP-Args", "AP-Specifiers", "AP-Results"]

**Type: Action (Enumerated)**

| ID | Item      | Description |
|----|-----------|-------------|
| 3  | **query** |             |

**********

**Type: Target (Enumerated)**

| ID   | Item         | Description |
|------|--------------|-------------|
| 9    | **features** |             |
| 1035 | **pac/**     |             |

**********

**Type: Args (Enumerated)**

| ID | Item                   | Description |
|----|------------------------|-------------|
| 1  | **start_time**         |             |
| 2  | **stop_time**          |             |
| 3  | **duration**           |             |
| 4  | **response_requested** |             |

**********

**Type: Actuator (Enumerated)**

| ID   | Item     | Description |
|------|----------|-------------|
| 1035 | **pac/** |             |

**********

**Type: Results (Enumerated)**

| ID   | Item           | Description |
|------|----------------|-------------|
| 1    | **versions**   |             |
| 2    | **profiles**   |             |
| 3    | **pairs**      |             |
| 4    | **rate_limit** |             |
| 1035 | **pac/**       |             |

**********

Enumerated item values are string literals, not data structures

**Type: Pairs (Enumerated)**

| ID | Item                                   | Description |
|----|----------------------------------------|-------------|
| 3  | **query: features pac/attrs pac/sbom** |             |

**********

**Type: AP-Target (Choice)**

| ID | Name      | Type                 | \# | Description |
|----|-----------|----------------------|----|-------------|
| 1  | **attrs** | Attribute-Specifiers | 1  |             |
| 2  | **sbom**  | SBOM-Specifiers      | 1  |             |

**********

| Type Name         | Type Definition | Description                         |
|-------------------|-----------------|-------------------------------------|
| **AP-Specifiers** | Map             | Profile-defined actuator specifiers |

**********

Profile-defined response results

**Type: AP-Results (Map{1..\*})**

| ID | Name      | Type              | \#   | Description |
|----|-----------|-------------------|------|-------------|
| 1  | **attrs** | PostureAttributes | 0..1 |             |
| 2  | **sbom**  | SBOM-Info         | 0..1 |             |

**********

**Type: Attribute-Specifiers (Map{1..\*})**

| ID | Name             | Type           | \#   | Description |
|----|------------------|----------------|------|-------------|
| 1  | **os_version**   | Boolean        | 0..1 |             |
| 2  | **password_min** | Boolean        | 0..1 |             |
| 3  | **file**         | FileSpecifiers | 0..1 |             |

**********

**Type: SBOM-Specifiers (Map)**

| ID | Name        | Type                               | \# | Description |
|----|-------------|------------------------------------|----|-------------|
| 1  | **type**    | ArrayOf(Enum[SBOM-Info]) unique    | 1  |             |
| 2  | **content** | ArrayOf(Enum[SBOM-Content]) unique | 1  |             |

**********

**Type: PostureAttributes (Map{1..\*})**

| ID | Name             | Type       | \#   | Description |
|----|------------------|------------|------|-------------|
| 1  | **os_version**   | OS-Version | 0..1 |             |
| 2  | **password_min** | Integer    | 0..1 |             |
| 3  | **file**         | File       | 0..1 |             |

**********

**Type: OS-Version (Record)**

| ID | Name                   | Type    | \#   | Description                          |
|----|------------------------|---------|------|--------------------------------------|
| 1  | **name**               | String  | 1    | Distribution or product name         |
| 2  | **version**            | String  | 1    | Suitable for presentation OS version |
| 3  | **major**              | Integer | 1    | Major release version                |
| 4  | **minor**              | Integer | 1    | Minor release version                |
| 5  | **patch**              | Integer | 1    | Patch release                        |
| 6  | **build**              | String  | 1    | Build-specific or variant string     |
| 7  | **platform**           | String  | 1    | OS Platform or ID                    |
| 8  | **platform_like**      | String  | 1    | Closely-related platform             |
| 9  | **codename**           | String  | 1    | OS Release codename                  |
| 10 | **arch**               | OS-Arch | 1    | OS Architecture                      |
| 11 | **install_date**       | Integer | 0..1 | Install date of the OS (seconds)     |
| 12 | **pid_with_namespace** | String  | 0..1 |                                      |
| 13 | **mount_namespace_id** | String  | 0..1 |                                      |

**********

Win: wmic os get osarchitecture, or Unix: uname -m

**Type: OS-Arch (Enumerated)**

| ID | Item       | Description |
|----|------------|-------------|
| 1  | **32-bit** |             |
| 2  | **64-bit** |             |
| 3  | **x86_32** |             |
| 4  | **x86_64** |             |

**********

**Type: FileSpecifiers (Map{1..\*})**

| ID | Name     | Type      | \#   | Description |
|----|----------|-----------|------|-------------|
| 1  | **path** | String    | 0..1 |             |
| 2  | **hash** | ls:Hashes | 0..1 |             |

**********

**Type: File (Record)**

| ID | Name     | Type   | \# | Description |
|----|----------|--------|----|-------------|
| 1  | **data** | Binary | 1  |             |

**********

**Type: SBOM-Info (Map{1..\*})**

| ID | Name        | Type          | \#   | Description                              |
|----|-------------|---------------|------|------------------------------------------|
| 1  | **uri**     | ls:URI        | 0..1 | Unique identifier or locator of the SBOM |
| 2  | **summary** | SBOM-Elements | 0..1 | NTIA Minimumum Elements of an SBOM       |
| 3  | **content** | SBOM-Content  | 0..1 | SBOM structured data                     |
| 4  | **blob**    | SBOM-Blob     | 0..1 | Uninterpreted SBOM bytes                 |

**********

**Type: SBOM-Elements (Record)**

| ID | Name              | Type     | \#    | Description                                                                          |
|----|-------------------|----------|-------|--------------------------------------------------------------------------------------|
| 1  | **supplier**      | String   | 1..\* | Name(s) of entity that creates, defines, and identifies components                   |
| 2  | **component**     | String   | 1..\* | Designation(s) assigned to a unit of software defined by the original supplier       |
| 3  | **version**       | String   | 1     | Identifier used by supplier to specify a change from a previously identified version |
| 4  | **component_ids** | String   | 1..\* | Other identifiers used to identify a component, or serve as a look-yp key            |
| 5  | **dependencies**  | String   | 1..\* | Upstream component(s)                                                                |
| 6  | **author**        | String   | 1     | Name of the entity that creates SBOM data for this component                         |
| 7  | **timestamp**     | DateTime | 1     | Record of the date and time of the SBOM data assembly                                |

**********

**Type: SBOM-Content (Choice)**

| ID | Name          | Type   | \# | Description                          |
|----|---------------|--------|----|--------------------------------------|
| 1  | **cyclonedx** | String | 1  | Placeholder for CycloneDX data model |
| 2  | **spdx2**     | String | 1  | Placeholder for SPDX v2.x data model |
| 3  | **spdx3**     | String | 1  | Placeholder for SPDX v3 data model   |

**********

**Type: SBOM-Blob (Record)**

| ID | Name       | Type                           | \# | Description |
|----|------------|--------------------------------|----|-------------|
| 1  | **format** | Enumerated(Enum[SBOM-Content]) | 1  |             |
| 2  | **data**   | Binary                         | 1  |             |

**********

| Type Name    | Type Definition                                                           | Description     |
|--------------|---------------------------------------------------------------------------|-----------------|
| **DateTime** | String{pattern="^((?:(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2}(?:\.\d+)?))(Z\|[\+-]\d{2}:\d{2})?)$"} | RFC-3339 format |

**********
