         title: "OpenC2 device schema for LED panel controller using sFractal blinky interface"
       package: "http://sfractal.com/schemas/blinky/v1.0"
       exports: ["OpenC2-Command", "OpenC2-Response"]

The Command defines an Action to be performed on a Target

**Type: OpenC2-Command (Record)**

| ID | Name           | Type       | \#   | Description                                                                |
|----|----------------|------------|------|----------------------------------------------------------------------------|
| 1  | **action**     | Action     | 1    | The task or activity to be performed (i.e., the 'verb').                   |
| 2  | **target**     | Target     | 1    | The object of the Action. The Action is performed on the Target.           |
| 3  | **args**       | Args       | 0..1 | Additional information that applies to the Command.                        |
| 4  | **profile**    | Profile    | 0..1 | The actuator profile defining the function to be performed by the Command. |
| 5  | **command_id** | Command-ID | 0..1 | An identifier of this Command.                                             |

**********

**Type: Action (Enumerated)**

| ID | Item       | Description                                                                                                                             |
|----|------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| 3  | **query**  | Initiate a request for information.                                                                                                     |
| 6  | **deny**   | Prevent a certain event or action from completion, such as preventing a flow from reaching a destination or preventing access.          |
| 8  | **allow**  | Permit access to or execution of a Target.                                                                                              |
| 15 | **set**    |                                                                                                                                         |
| 16 | **update** | Instruct a component to retrieve, install, process, and operate in accordance with a software update, reconfiguration, or other update. |
| 20 | **delete** | Remove an entity (e.g., data, files, flows).                                                                                            |

**********

**Type: Target (Choice)**

| ID   | Name         | Type          | \# | Description                                                                        |
|------|--------------|---------------|----|------------------------------------------------------------------------------------|
| 9    | **features** | Features      | 1  | A set of items used with the query Action to determine an Actuator's capabilities. |
| 9001 | **blinky/**  | Target$blinky | 1  | Profile-defined targets                                                            |

**********

**Type: Args (Map{1..\*})**

| ID   | Name                   | Type          | \#   | Description                                                                |
|------|------------------------|---------------|------|----------------------------------------------------------------------------|
| 1    | **start_time**         | Date-Time     | 0..1 | The specific date/time to initiate the Command                             |
| 2    | **stop_time**          | Date-Time     | 0..1 | The specific date/time to terminate the Command                            |
| 3    | **duration**           | Duration      | 0..1 | The length of time for an Command to be in effect                          |
| 4    | **response_requested** | Response-Type | 0..1 | The type of Response required for the Command: none, ack, status, complete |
| 9001 | **blinky/**            | Args$blinky   | 0..1 | Profile-defined command arguments                                          |

**********

**Type: Profile (Enumerated)**

| ID   | Item       | Description |
|------|------------|-------------|
| 9001 | **blinky** |             |

**********

**Type: OpenC2-Response (Record)**

| ID | Name            | Type        | \#   | Description                                                                           |
|----|-----------------|-------------|------|---------------------------------------------------------------------------------------|
| 1  | **status**      | Status-Code | 1    | An integer status code.                                                               |
| 2  | **status_text** | String      | 0..1 | A free-form human-readable description of the Response status.                        |
| 3  | **results**     | Results     | 0..1 | Map of key:value pairs that contain additional results based on the invoking Command. |

**********

Response Results

**Type: Results (Map{1..\*})**

| ID   | Name           | Type            | \#    | Description                                                         |
|------|----------------|-----------------|-------|---------------------------------------------------------------------|
| 1    | **versions**   | SemVer unique   | 0..\* | List of OpenC2 language versions supported by this Consumer         |
| 2    | **profiles**   | Profile unique  | 0..\* | List of profiles supported by this Consumer                         |
| 3    | **pairs**      | Pairs           | 0..1  | List of targets applicable to each supported Action                 |
| 4    | **rate_limit** | Number{0.0..\*} | 0..1  | Maximum number of requests per minute supported by design or policy |
| 9001 | **blinky/**    | Results$blinky  | 0..1  | Profile-defined results                                             |

**********

Targets applicable to each action supported by this device

**Type: Pairs (Map{1..\*})**

| ID   | Name        | Type                         | \#   | Description |
|------|-------------|------------------------------|------|-------------|
| 3    | **query**   | ArrayOf(QueryTargets) unique | 1    |             |
| 9001 | **blinky/** | Pairs$blinky                 | 0..1 |             |

**********

**Type: QueryTargets (Enumerated)**

| ID | Item         | Description |
|----|--------------|-------------|
| 9  | **features** |             |

**********

Profile-defined targets

**Type: Target$blinky (Choice)**

| ID | Name     | Type   | \#    | Description |
|----|----------|--------|-------|-------------|
| 1  | **led**  | String | 1     |             |
| 2  | **leds** | String | 1..\* |             |

**********

| Type Name       | Type Definition | Description                       |
|-----------------|-----------------|-----------------------------------|
| **Args$blinky** | Map{1..*}       | Profile-defined command arguments |

**********

| Type Name          | Type Definition | Description                      |
|--------------------|-----------------|----------------------------------|
| **Results$blinky** | Map{1..*}       | Profile-defined response results |

**********

Targets applicable to each action

**Type: Pairs$blinky (Map)**

| ID | Name    | Type                               | \# | Description |
|----|---------|------------------------------------|----|-------------|
| 15 | **set** | ArrayOf(Set-Targets$blinky) unique | 1  |             |

**********

**Type: Set-Targets$blinky (Enumerated)**

| ID | Item     | Description |
|----|----------|-------------|
| 1  | **led**  |             |
| 2  | **leds** |             |

**********

| Type Name    | Type Definition         | Description                                                                |
|--------------|-------------------------|----------------------------------------------------------------------------|
| **Features** | ArrayOf(Feature) unique | An array of names used to query a Consumer for its supported capabilities. |

**********

| Type Name     | Type Definition | Description   |
|---------------|-----------------|---------------|
| **Date-Time** | Integer{0..*}   | Date and Time |

**********

| Type Name    | Type Definition | Description      |
|--------------|-----------------|------------------|
| **Duration** | Integer{0..*}   | A length of time |

**********

Specifies the results to be returned from a query features Command

**Type: Feature (Enumerated)**

| ID | Item           | Description                                                         |
|----|----------------|---------------------------------------------------------------------|
| 1  | **versions**   | List of OpenC2 Language versions supported by this Consumer         |
| 2  | **profiles**   | List of profiles supported by this Consumer                         |
| 3  | **pairs**      | List of supported Actions and applicable Targets                    |
| 4  | **rate_limit** | Maximum number of Commands per minute supported by design or policy |

**********

**Type: Response-Type (Enumerated)**

| ID | Item         | Description                                     |
|----|--------------|-------------------------------------------------|
| 0  | **none**     | No response                                     |
| 1  | **ack**      | Respond when Command received                   |
| 2  | **status**   | Respond with progress toward Command completion |
| 3  | **complete** | Respond when all aspects of Command completed   |

**********

**Type: Status-Code (Enumerated.ID)**

| ID  | Description                                                                                                                                                           |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 102 | **Processing** - an interim Response used to inform the Producer that the Consumer has accepted the Command but has not yet completed it                              |
| 200 | **OK** - the Command has succeeded                                                                                                                                    |
| 201 | **Created** - the Command has succeeded and a new resource has been created as a result of it                                                                         |
| 400 | **Bad Request** - the Consumer cannot process the Command due to something that is perceived to be a Producer error (e.g., malformed Command syntax)                  |
| 401 | **Unauthorized** - the Command Message lacks valid authentication credentials for the target resource or authorization has been refused for the submitted credentials |
| 403 | **Forbidden** - the Consumer understood the Command but refuses to authorize it                                                                                       |
| 404 | **Not Found** - the Consumer has not found anything matching the Command                                                                                              |
| 500 | **Internal Error** - the Consumer encountered an unexpected condition that prevented it from performing the Command                                                   |
| 501 | **Not Implemented** - the Consumer does not support the functionality required to perform the Command                                                                 |
| 503 | **Service Unavailable** - the Consumer is currently unable to perform the Command due to a temporary overloading or maintenance of the Consumer                       |

**********

| Type Name      | Type Definition              | Description        |
|----------------|------------------------------|--------------------|
| **Command-ID** | String{pattern="^\S{0,36}$"} | Command Identifier |

**********

| Type Name  | Type Definition                                 | Description                      |
|------------|-------------------------------------------------|----------------------------------|
| **SemVer** | String{pattern="^(\d{1,4})(\.(\d{1,6})){0,2}$"} | Major.Minor.Patch version number |

**********
