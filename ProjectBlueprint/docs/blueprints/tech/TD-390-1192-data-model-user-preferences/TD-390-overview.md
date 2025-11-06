---
id: TD-390
title: "**1.19.2 Data model & user preferences**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-390-1192-data-model-user-preferences\TD-390-overview.md"
parent_id: 
anchor: "TD-390"
checksum: "sha256:b60dcf6ab7455fcac2a2f6cd0e38de4fb3352c96b2290d38734ee672804c7a2b"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-390"></a>
## **1.19.2 Data model & user preferences**

**SQL migration**  
**Recommended path:** *db/migrations/019_i18n_user_prefs.sql*

*alter table "user"*  
*add column locale text not null default 'en-US',*  
*add column timezone text not null default 'UTC',*  
*add column prefers_24h boolean not null default false,*  
*add column reduced_motion boolean not null default false,*  
*add column high_contrast boolean not null default false;*  
  
*create index on "user"(locale);*  
*create index on "user"(timezone);*  

**GraphQL SDL**  
**Recommended path:** *api/schema/i18n.graphql*

*type UserPrefs {*  
*locale: String!*  
*timezone: String!*  
*prefers24h: Boolean!*  
*reducedMotion: Boolean!*  
*highContrast: Boolean!*  
*}*  
*extend type Query { mePrefs: UserPrefs! }*  
*extend type Mutation {*  
*updatePrefs(locale: String, timezone: String, prefers24h: Boolean, reducedMotion: Boolean, highContrast: Boolean): UserPrefs!*  
*}*  

**Policy:** never infer locale silently after the user explicitly chooses one; store choice; still set *lang*/*dir* attributes server‑side.
