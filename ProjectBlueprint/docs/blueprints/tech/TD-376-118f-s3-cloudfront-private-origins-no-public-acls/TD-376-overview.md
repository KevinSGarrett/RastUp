---
id: TD-376
title: "**1.18.F S3 & CloudFront: Private Origins, No Public ACLs**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-376-118f-s3-cloudfront-private-origins-no-public-acls\TD-376-overview.md"
parent_id: 
anchor: "TD-376"
checksum: "sha256:5e4a9a66900c6e476e624f3903a4bec8d9ae7eeb607279a122aff4f78e60cbb7"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-376"></a>
## **1.18.F S3 & CloudFront: Private Origins, No Public ACLs**

**Recommended path:** *security/s3/policies.md*

*{*  
*"Version":"2012-10-17",*  
*"Statement":\[*  
*{"Sid":"DenyPublicACL","Effect":"Deny","Principal":"\*","Action":"s3:PutBucketAcl","Resource":"arn:aws:s3:::cdn.rastup.com"},*  
*{"Sid":"DenyNotUsingTLS","Effect":"Deny","Principal":"\*","Action":"s3:\*","Resource":\["arn:aws:s3:::cdn.rastup.com","arn:aws:s3:::cdn.rastup.com/\*"\],"Condition":{"Bool":{"aws:SecureTransport":"false"}}},*  
*{"Sid":"AllowOACOnly","Effect":"Allow","Principal":{"Service":"cloudfront.amazonaws.com"},"Action":"s3:GetObject","Resource":"arn:aws:s3:::cdn.rastup.com/\*","Condition":{"StringEquals":{"AWS:SourceArn":"arn:aws:cloudfront::\<acct\>:distribution/\<id\>"}}}*  
*\]*  
*}*  

Use **CloudFront Origin Access Control (OAC)**; disable **Public Access** and ACLs; use **Object Ownership = Bucket owner enforced**.
