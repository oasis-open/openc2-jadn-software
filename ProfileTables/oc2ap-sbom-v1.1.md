         title: "OpenC2 SBOM Retrieval Actuator Profile"
       package: "http://oasis-open.org/openc2/oc2ap-sbom/v1.1"
    namespaces: {"ls": "http://oasis-open.org/openc2/oc2ls-types/v1.1"}
       exports: ["AP-Target", "AP-Specifiers", "AP-Results"]

**Type: Action (Enumerated)**

| ID | Item      | Description |
|----|-----------|-------------|
| 3  | **query** |             |

**********

**Type: Target (Enumerated)**

| ID   | Item         | Description |
|------|--------------|-------------|
| 9    | **features** |             |
| 1034 | **sbom**     |             |

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
| 1034 | **sbom** |             |

**********

**Type: Results (Enumerated)**

| ID   | Item           | Description |
|------|----------------|-------------|
| 1    | **versions**   |             |
| 2    | **profiles**   |             |
| 3    | **pairs**      |             |
| 4    | **rate_limit** |             |
| 1034 | **sbom**       |             |

**********

**Type: Pairs (Enumerated)**

| ID | Item                                    | Description |
|----|-----------------------------------------|-------------|
| 3  | **query: features, /sboms, /sbom_list** |             |

**********

Profile-defined targets

**Type: AP-Target (Choice)**

| ID | Name          | Type            | \# | Description                                  |
|----|---------------|-----------------|----|----------------------------------------------|
| 1  | **sboms**     | SBOM-Specifiers | 1  | Return IDs or SBOMs matching filter criteria |
| 2  | **sbom_list** | SBOM-List       | 1  | Return specific SBOMs by ID                  |

**********

| Type Name         | Type Definition | Description                         |
|-------------------|-----------------|-------------------------------------|
| **AP-Specifiers** | Map             | Profile-defined actuator specifiers |

**********

Profile-defined response results

**Type: AP-Results (Map{1..\*})**

| ID | Name      | Type               | \# | Description                               |
|----|-----------|--------------------|----|-------------------------------------------|
| 1  | **sboms** | ArrayOf(SBOM-Info) | 1  | List of all SBOMs matching query criteria |

**********

If none specified, return IDs for all SBOMs

**Type: SBOM-Specifiers (Map)**

| ID | Name       | Type                               | \#   | Description                 |
|----|------------|------------------------------------|------|-----------------------------|
| 1  | **type**   | ArrayOf(Enum[SBOM-Content]) unique | 0..1 | SBOM type                   |
| 2  | **format** | ArrayOf(DataFormat) unique         | 0..1 | Data format                 |
| 3  | **info**   | ArrayOf(Info){1..\*} unique        | 0..1 | Type of SBOM info to return |

**********

**Type: SBOM-List (Map)**

| ID | Name     | Type                        | \#    | Description                 |
|----|----------|-----------------------------|-------|-----------------------------|
| 1  | **sids** | ls:URI                      | 1..\* | SBOM IDs to return          |
| 2  | **info** | ArrayOf(Info){1..\*} unique | 1     | Type of SBOM info to return |

**********

**Type: SBOM-Info (Map)**

| ID | Name        | Type                           | \#   | Description                              |
|----|-------------|--------------------------------|------|------------------------------------------|
| 1  | **type**    | Enumerated(Enum[SBOM-Content]) | 1    | SBOM type (name of standard)             |
| 2  | **format**  | DataFormat                     | 1    | Data (serialization) format              |
| 3  | **sid**     | ls:URI                         | 1    | Unique identifier or locator of the SBOM |
| 4  | **summary** | SBOM-Elements                  | 0..1 | NTIA Minimumum Elements of an SBOM       |
| 5  | **content** | SBOM-Content                   | 0..1 | SBOM structured data                     |
| 6  | **blob**    | Binary                         | 0..1 | Uninterpreted SBOM bytes                 |

**********

SBOM-Info fields to return

**Type: Info (Enumerated)**

| ID | Item        | Description                        |
|----|-------------|------------------------------------|
| 1  | **summary** | NTIA Minimumum Elements of an SBOM |
| 2  | **content** | SBOM structured data               |
| 3  | **blob**    | Uninterpreted SBOM bytes           |

**********

**Type: SBOM-Elements (Record)**

| ID | Name              | Type     | \#    | Description                                                                          |
|----|-------------------|----------|-------|--------------------------------------------------------------------------------------|
| 1  | **supplier**      | String   | 1..\* | Name of entity that creates, defines, and identifies components                      |
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

Serialization Data Formats

**Type: DataFormat (Enumerated)**

| ID | Item         | Description                        |
|----|--------------|------------------------------------|
| 1  | **ttv**      | Text Tag-Value                     |
| 2  | **json**     | JSON verbose                       |
| 3  | **json-m**   | JSON concise/minimized             |
| 4  | **json-ld**  | JSON linked data                   |
| 5  | **cbor**     | CBOR binary                        |
| 6  | **protobuf** | Protocol Buffers binary            |
| 7  | **xml**      | XML                                |
| 8  | **ss-csv**   | Spreadsheet comma separated values |

**********

| Type Name    | Type Definition | Description |
|--------------|-----------------|-------------|
| **DateTime** | Integer{0..*}   |             |

**********
