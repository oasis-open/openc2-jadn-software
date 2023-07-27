## Added 27 July 2023:

Files:
 * cdx-1-4-WIP_2023-07-27.jadn
 * cdx-1-4-WIP_2023-07-27.jidl
 * cdx-1-4-WIP_2023-07-27.json
  
Current state of work-in-progress JADN schema based on the [CDX v1.4 JSON schema](https://github.com/CycloneDX/specification/blob/master/schema/bom-1.4.schema.json).  The JIDL and JSON files are generated from the JADN schema.

## Created by: 
David Lemire (HII Mission Technologies)

## Status:

 1) Complete JADN capture from the CDX JSON schema
 2) Has not been tested against any CDX SBOMs
 3) Required / optional values still needed for most record types
 4) May contain duplicative types
 5) Would benefit from re-ordering content more logically
 6) Work needed on connection to SPDX license identifiers
 7) Work needed on specification of signatures
 8) Not all comments / descriptions from the JSON schema have been included in the JADN schema