**§1.1 — Role System Design (continued, deep detail)**

You asked us to finish each sub-section to 99.9% before moving on. Below are the **additional technical details** to fully close §1.1—schemas, validators, index definitions, RBAC, content-safety thresholds, error models, and test specs. When you’re happy with this, we’ll mark §1.1 FINAL.

**1.1.P Role field schemas (canonical JSON + Zod)**

We store per-role fields in *service_profile.about_fields*, *pricing_fields*, and *social_fields*. Below are the **canonical JSON shapes** and the **validation rules** we enforce at API level (Zod examples included for developers).

**Common fields (all roles)**

*{*

*"bio": "string, ≤ 600 chars",*

*"city": "string",*

*"region": "string",*

*"travel_notes": "string? (≤ 300)",*

*"languages": \["string"\],*

*"tags": \["string"\] // e.g., fashion, commercial, editorial*

*}*

**Validation**

- *bio* required, max length.
- *city* required; *region* optional but recommended.
- *languages* max 5; *tags* max 12.

**Model.about_fields**

*{*

*"height_cm": 175,*

*"bust_cm": 86, "waist_cm": 63, "hips_cm": 91,*

*"hair_color": "Brunette",*

*"eye_color": "Brown",*

*"genres": \["fashion","editorial","commercial"\],*

*"experience_years": 3*

*}*

Rules:

- height 120–210 cm; measurements 40–150 cm; genres from allowlist; experience 0–50.

**Photographer.about_fields**

*{*

*"specialties": \["portrait","fashion","editorial"\],*

*"gear": \["Canon R5","Sigma 24-70"\],*

*"editing_turnaround_days": 7,*

*"insurance": true,*

*"studio_access": false*

*}*

Rules:

- specialties from allowlist; turnaround 0–30; insurance boolean required.

**Videographer.about_fields**

*{*

*"specialties": \["music","commercial","wedding"\],*

*"camera_rigs": \["FX3","BMPCC6K"\],*

*"audio_capability": true,*

*"editing_turnaround_days": 10,*

*"deliverable_formats": \["mp4","prores"\]*

*}*

**Creator.about_fields / FanSub.about_fields**

*{*

*"platforms": \["instagram","tiktok","youtube","x"\],*

*"categories": \["fashion","beauty","lifestyle"\],*

*"brand_safety_notes": "string≤300"*

*}*

Rules:

- For **FanSub** role, the **18+ flag** is mandatory and surfaces only behind age-gated views (public thumbnails still SFW).

**Pricing fields (all roles)**

*\[*

*{*

*"package_id": "pkg_xxx", "name": "2-Hour Shoot",*

*"price_cents": 20000, "duration_min": 120,*

*"includes": \["10 edited photos"\],*

*"addons": \[{"name":"Extra retouch per image","price_cents":1500}\],*

*"licensing": {"type":"standard","notes":"social, web up to 1y"}*

*}*

*\]*

Rules:

- At least one package with *price_cents \>= 1000* and *duration_min \>= 30*.
- *addons* optional; each must have *price_cents \>= 100*.

**Social fields (optional)**

*{*

*"instagram":* [*{"handle":"@name","verified":true,"followers":182000,"engagement_rate":0.028*]()*},*

*"tiktok": {"handle":"@name","followers":530000,"avg_views":120000},*

*"youtube": {"handle":"@name","subscribers":48000,"avg_views":23000}*

*}*

Rules:

- Numeric fields non-negative; *verified* boolean requires OAuth proof (stored separately).

*(Developers: I can supply complete Zod schemas on request; they are 200+ lines and omitted here to keep this section readable.)*

**1.1.Q Availability model & conflict rules**

- *availability_json* is **advisory** for search hints; authoritative blocks come from accepted booking legs.
- When creating a draft or confirming a booking leg, we check **overlaps across all SPs** owned by the same account and across any **studio listing** the account owns if the owner will be present/required.
- Conflict outcomes: warn on soft conflicts (availability windows); hard-block on accepted overlaps unless the user explicitly opts for back-to-back with buffer (configurable minimum, e.g., 60 min).

**Overlap detection (UTC):**

- Normalize proposed *(start,end)* to UTC; query legs for the owner in *\[start-buffer, end+buffer\]*.
- If any accepted leg overlaps → reject; if pending holds overlap → show conflict UI with manage options.

**1.1.R Typesense/OpenSearch schemas & analyzers**

**People index (*****people_v1*****)**

- Fields: *id (string)*, *userId*, *role*, *city*, *geo* (lat,lon), *isPublished* (bool), *completenessScore (int)*, *instantBook (bool)*, *ratingAvg (float)*, *ratingCount (int)*, *priceFromCents (int)*, *verification.id (bool)*, *verification.bg (bool)*, *verification.social (bool)*, *availabilityBuckets (string\[\])*, *genres/specialties (string\[\])*, **selected role filters** (e.g., *height_cm*, *studio_access*).
- Facets: *role*, *city*, *verification.id*, *instantBook*, *genres/specialties*, price buckets (derived).
- Sorting: *\_text_match* → *verification.id desc* → *ratingAvg desc* → *abs(priceFromCents - queryBudget) asc* → *created_at desc*.

**Studios index (*****studios_v1*****)**

- Fields: *id*, *city*, *geo*, *amenities (string\[\])*, *depositRequired (bool)*, *verifiedStudio (bool)*, *ratingAvg*, *ratingCount*.
- Facets: *city*, *amenities*, *verifiedStudio*.

**Analyzers & normalization**

- Lowercase/ASCII fold; synonyms for common tags (e.g., “glamour” ~ “glam”); numeric filters for height/price.
- Safe-Mode filtering occurs in the query layer: if Safe-Mode=ON → exclude *nsfw_band=2* assets from cards; prefer blur on 1.

**Index refresh & backfill**

- Mutation outbox → indexer Lambda; nightly full backfill per city; integrity check (counts vs DB) with alert if \>1% deviation.

**1.1.S Content-safety thresholds & pipelines**

- **Upload path:** client → signed S3 upload (previews only) → SQS → Lambda scan.

- **Scanner result →** ***nsfw_band*****:**

  - 0 = Allow (public thumbnail fine)
  - 1 = Blur (mild adult; blur radius 8–16)
  - 2 = Block (explicit; no public display)

- **Appeals:** owner submits appeal; T&S reviews; on override, we store *override_reason*, *actor*, *timestamp*. All decisions audited.

**1.1.T Admin RBAC (for this section)**

|  |  |  |  |
|----|----|----|----|
| **Admin role** | **Can view** | **Can edit** | **Approvals required** |
| Support | SP/studio status, completeness, basic fields | Unpublish SP/studio on policy breach | 1 approver |
| Trust & Safety | NSFW decisions, overrides, link removals | Override scan; set *nsfw_band* | 2-person approval |
| Promotions | N/A (1.1 only) | N/A | N/A |
| City Ops | City allowlists for visibility | Toggle city gate on SP exposure | 2-person on city gate changes |
| Finance | N/A | N/A | N/A |
| Legal/Compliance | Audit log access | Lock records (litigation hold) | 2-person |

All admin actions write immutable audits: actor, action, before/after, reason.

**1.1.U Error model (API) & codes**

- *SP_INCOMPLETE* — cannot publish: missing fields or portfolio too small.
- *SP_UNSAFE_PUBLIC* — Safe-Mode restrictions prevent display.
- *SP_FORBIDDEN_LINK_STUDIO* — link attempt by non-owner.
- *SP_CONFLICT_CALENDAR* — hard overlap detected on accept/confirm.
- *SP_NOT_FOUND* — unpublished or nonexistent role page.

Each error includes *error_code*, *message*, *hint*, *path*, and a user-safe remediation tip.

**1.1.V Test plan (deterministic; CI-runnable)**

30. **Create & publish SP**: missing fields → *SP_INCOMPLETE*; add required fields + 6+ portfolio items → publish succeeds; role appears in search.
31. **Role-scoped reviews**: add review to Model SP; ensure Photographer SP rating untouched; studio rating untouched.
32. **Studio chip**: link/detach SP↔Studio; search result shows chip; ratings do not merge.
33. **Safe-Mode enforcement**: upload explicit preview → *nsfw_band=2*; guest sees blocked asset, logged-in with Safe-Mode ON sees blur or placeholder.
34. **Calendar block**: accept booking for Model SP; attempt overlapping booking for Photographer SP owned by same user → error.
35. **Index integrity**: mutate SP fields → index doc updates; nightly reindex parity within 1%; alert if not.
36. **Admin audits**: T&S override recorded with reason; City Ops toggles gate with two approvals.

**1.1.W Cost checklist (for this section)**

- Aurora Serverless v2 min ACUs ≤ 2 in prod; auto-pause in dev.
- Typesense single node (or OpenSearch Serverless minimal OCU cap).
- S3 lifecycle to Intelligent-Tiering for previews; 30-day expiration for orphaned assets.
- Content-scan Lambda throttle to cap concurrency (protects costs).

**§1.1 — Finalization checklist**

We will mark **§1.1 FINAL** only when:

- SQL and GraphQL from this section are implemented and deployed.
- Validators for all roles are live; publish gate works.
- Search indices and indexers are live; result cards render correctly with Safe-Mode.
- Admin moderation + studio verification panels and audits are live.
- All tests in 1.1.V pass in CI.
- Cost alarms for DB, search, and S3 are configured and quiet for 48h under synthetic load.

# 

# 

# 

# 

# 

# **§1.2 — Role‑Specific Search & Filters (Search Service, end‑to‑end)**

**Purpose.** Implement a fast, fair, and policy‑compliant discovery system that reflects the product contract: role‑true discovery for *people* (Service Profiles) and *places* (Studios), Safe‑Mode defaults, city gates, verification gates, Instant‑Book, and promotions density caps. This section fully specifies the **data model, indexes, analyzers, API contracts, ranking, caching, telemetry, admin tools, tests, and cost controls**. We will not move forward until this subsection is complete.

## **1.2.A Surfaces & UX contract**

**Where search appears**

47. **Search home** (role picker + location field + date and budget quick filters).
48. **Role‑scoped search** (tabs): *Models*, *Photographers*, *Videographers*, *Creators*.
49. **Studios search** (separate surface; can be “attached in flow” during checkout).
50. **Saved searches & alerts** (optional for MVP; schema below).
51. **Admin**: Reindex, synonyms, density caps, city gates, invalid‑click dashboard.

**Non‑negotiable behaviors**

- Clicking a search card **always** deep‑links to the **role canonical page** (*/u/{handle}/{role}*) or **studio page** (*/studio/{slug}*), never the account shell alone.
- Safe‑Mode ON by default for guests; public thumbnails follow NSFW rules.
- **Studios are listings (places)**; role results never mix studio ratings or badges.
- Social metrics appear *only when verified*; otherwise show “Unverified”.

## **1.2.B Engine & collections**

We implement the Search Service to be **engine‑agnostic** with a default **Typesense** deployment (low fixed cost), and an optional **OpenSearch** backend behind the same adapter.

**Collections**

- *people_v1* — one document per **Service Profile** (SP).
- *studios_v1* — one document per **Studio**.

**Sharding/partitioning**

- Logical shards by *city* and *role* (we keep physical topology simple at MVP—one node w/ replica or small serverless OCU cap).
- Daily compaction to prune stale docs; reindex per city when policy/flags change.

## **1.2.C Index schema (canonical)**

***people_v1*** **(Service Profiles)**

*{ "id": "srv_mdl_01h...", "userId": "usr_01h...", "role": "model \| photographer \| videographer \| creator \| fansub", "handle": "kevin", "slug": "model", // for /u/{handle}/{role} "isPublished": true, "completenessScore": 82, "createdAt": "2025-10-30T19:00:00Z", "updatedAt": "2025-11-05T14:12:00Z", "city": "Houston", "region": "TX", "geo": { "lat": 29.7604, "lon": -95.3698 }, "radiusKm": 80, // willing-to-travel hint "safeModeBandMax": 1, // 0 allow, 1 blur OK, 2 block on public "verification": { "id": true, "bg": false, "socialVerified": true }, "instantBook": true, "ratingAvg": 4.92, "ratingCount": 27, "priceFromCents": 15000, // min package price "priceMedianCents": 25000, // optional "currency": "USD", "availabilityBuckets": \["2025-11-10","2025-11-11","2025-11-14"\], "roleFields": { "model": { "height_cm": 175, "genres": \["fashion","editorial"\] }, "photographer": { "specialties": \["portrait"\], "studio_access": false }, "videographer": { "specialties": \["music"\] }, "creator": { "platforms": \["instagram","tiktok"\] } }, "social": { "igFollowers": 182000, "igEngagementRate": 0.028, "ttFollowers": 530000, "ttAvgViews": 120000 }, "policySignals": { "disputeRate30d": 0.0, "cancelRate90d": 0.02, "lateDeliveryRate90d": 0.01 }, "boosts": { "trustedPro": 0, // +1 if BG passed "newSellerFloor": 1, // protect cold start "studioLinked": 0 // +1 if linked studio (has chip) }}*

***studios_v1*** **(Studio Listings)**

*{ "id": "std_01h...", "ownerUserId": "usr_01h...", "title": "East End Loft", "slug": "east-end-loft", "city": "Houston", "region": "TX", "geo": {"lat": 29.75, "lon": -95.35}, "isPublished": true, "verifiedStudio": true, "amenities": \["natural light","backdrops","makeup area","parking"\], "depositRequired": true, "ratingAvg": 4.85, "ratingCount": 41, "priceFromCents": 3500, // per-hour or base slot price (normalized) "availabilityBuckets": \["2025-11-10","2025-11-12"\]}*

## **1.2.D Analyzers & normalization**

**Text fields**

- Lowercase, ASCII‑fold; stopwords minimal; synonyms (see Admin §1.2.N) for common fashion/creator terms: *"glamour" ~ "glam"*, *"bnw" ~ "black and white"*, *"H‑Town" ~ "Houston"*.

**Numeric**

- Height, price, rating stored as numerics for range queries.

**Geo**

- Store *geo* as lat/lon. We support **radius** queries at MVP (polygon later).

**Availability**

- Bucket by ISO calendar days; daily job populates buckets for the next N days (N configurable; default 30).

**NSFW/Safe‑Mode**

- For **public search**, apply a query‐time filter:

  - Safe‑Mode ON → *safeModeBandMax \<= 1* (block band 2 entirely).
  - Safe‑Mode OFF for verified adults → *safeModeBandMax \<= 2* (still no explicit thumbnails if the product policy forbids explicit public imagery).

## **1.2.E Filters & UI chips**

**Global filters (people)**

- Role (tab), Location (city/radius), Date (single or range), Budget (min/max), Verification (ID Verified badge), Instant Book toggle, Rating (≥ threshold), Safe‑Mode on/off (if signed‑in and age‑verified), Availability (specific day), Sort (Default, Top Rated, Price Low→High, New).

**Role‑specific filters**

- **Models**: Height (cm/in ranges), Genres (allowlist), Experience (years), Travel ready (bool).
- **Photographers**: Specialties, Studio Access (has studio link), Turnaround (days), Insurance (bool).
- **Videographers**: Specialties, Audio capability (bool), Deliverable format (enum).
- **Creators**: Platforms (IG/TT/YT/X), Category, Verified social (bool), Min followers (range).
- **Studios**: Amenities (multi‑select), Deposit required (bool), Size/Capacity buckets, Natural light (bool), Parking (bool).

**Promotion chips (when feature flag on)**

- “Featured” label (above the fold) or “Boosted” (below); both must be visually distinct and disclose paid placement.

## **1.2.F Query grammar & API contracts**

**GraphQL (AppSync)**

*input SearchInput { surface: SearchSurface! \# PEOPLE or STUDIOS role: RoleType \# required when surface=PEOPLE city: String! lat: Float lon: Float radiusKm: Int = 50 date: AWSDate \# single day dateRange: DateRangeInput \# optional alternative budgetMinCents: Int budgetMaxCents: Int ratingMin: Float verifiedOnly: Boolean instantBookOnly: Boolean safeMode: Boolean = true \# Role-specific filters: model: ModelFiltersInput photographer: PhotographerFiltersInput videographer: VideographerFiltersInput creator: CreatorFiltersInput studios: StudiosFiltersInput sort: SearchSort = DEFAULT page: String \# opaque cursor pageSize: Int = 20} type SearchResult { items: \[SearchCard!\]! facets: \[Facet!\]! page: String \# next cursor} type Query { search(input: SearchInput!): SearchResult! searchSuggest(query: String!, surface: SearchSurface!, role: RoleType, city: String!): \[SuggestItem!\]! savedSearches: \[SavedSearch!\]!} type Mutation { saveSearch(name: String!, input: SearchInput!): SavedSearch! deleteSavedSearch(id: ID!): Boolean!}*

**Cursor‑based pagination**

- Results return opaque *page* tokens (do not leak engine details).
- We cache the last N cursors per user/session (server‑side) to enable back/forward replay.

**Query normalization**

- City is canonicalized to a region/city id; if *lat/lon* present, we compute city from reverse geocoding and warn on mismatches.
- Role‑specific filters are ignored unless *role* matches the relevant type.

## **1.2.G Ranking & fairness**

**Base score**  
*score = w_text\*textMatch + w_geo\*geoScore + w_rep\*repScore + w_verify\*verifyBoost + w_price\*priceFit + w_avail\*availBoost + w_recency\*recency*

- *textMatch*: keyword/synonym features (if query text present).
- *geoScore*: distance‑decay (radius Gaussian; 0 beyond radius).
- *repScore*: f(ratingAvg, ratingCount) with Laplace smoothing to avoid low‑sample overweighting.
- *verifyBoost*: +X if ID Verified, +Y if Trusted Pro (BG passed).
- *priceFit*: penalty for large deviation from user budget (if set).
- *availBoost*: +Z if the requested date is in *availabilityBuckets*.
- *recency*: mild boost for recently updated profiles (helps cold start).

**Fairness & diversity constraints**

- **Provider diversity**: impose a max of K results per owner within the top N (avoid multi‑role flooding).
- **New‑seller floor**: ensure a minimum presence (M slots in top N reserved for low‑history but complete/verified profiles).
- **Studio diversity**: different studio owners in top M.
- **Policy penalties**: suppress results if *policySignals* exceed thresholds (dispute, late delivery). Thresholds configured via Admin.

**Promotions blending (when enabled)**

- **Featured**: eligible results can occupy fixed slots (e.g., 1–2 positions in top 20) but **never break filters**.
- **Boost**: cost‑per‑click uplift—insert additional slots every X organic results after position P.
- Both obey density caps: e.g., ≤2 Featured in top 20; ≤1 above the fold.

## **1.2.H Promotions integrity (invalid‑click handling)**

- Real‑time click stream with fingerprinting (device, IP block, user id, session id).
- **Deduplicate** multiple clicks from same session/user within T seconds.
- **Invalid click rules**: excessive repeat clicks, out‑of‑geo anomalies, bot signals → flagged and **not billed**.
- **Make‑good credits** auto‑issued for flagged traffic (logged as ledger entries).
- Holdouts (A/B) maintain an organic control set for unbiased impact analysis.

## **1.2.I Caching, rate limits, and SLOs**

**Result caching**

- Key: hash of normalized *SearchInput* (without page) + city + role + safeMode + version.
- TTL 60–120s (config), **stale‑while‑revalidate** to keep p95 low.
- Pagination cursors cached separately for short time (120s).

**Rate limits**

- Per IP and per account; stricter for anonymous traffic; separate limits for suggest vs full search.

**SLOs (MVP)**

- p95 latency: **≤350ms** for cached hits, **≤600ms** for cold queries at launch city scale.
- Error rate (5xx) \< 0.5%; availability ≥99.9% monthly for the API.

## **1.2.J Ingestion & update pipeline**

**Write sources**

- SP publish/update, rating updates, verification/badge changes, availability updates, policy signals, studio verification toggles.

**Mechanics**

- **Outbox** on mutations → SQS → Indexer Lambda → engine upsert.
- **Nightly backfill** per city to guarantee convergence.
- **On booking accept**: emit event to add date to *availabilityBuckets* for the participant SP and studio (if applicable).
- **On cancellation**: remove bucket(s) if time still in future.
- **On policy change** (Safe‑Mode, city gate, eligibility): bulk partial update.

**Consistency**

- If index write fails, retry with exponential backoff; stale card renders are guarded by server query filters.

## **1.2.K Telemetry & analytics**

**Events**

- *search.open*, *search.filters.apply*, *search.query.execute*, *search.results.render*, *search.result.impression*, *search.result.click*, *search.result.save*, *search.error*, *search.latency*.
- Promotions: *promo.slot.impression*, *promo.slot.click*, *promo.invalid_click.flag*, *promo.credit.issued*.
- Integrity: *search.integrity.invalid_request*, *search.abuse.robot_detected*.

**Metrics**

- CTR by role/facet; budget fit distribution; verified share; availability hit rate; density cap compliance; diversity indices.

## **1.2.L Admin tools (console)**

**Search Admin**

- **Reindex** city/role; **dry‑run** to preview doc deltas.
- **Synonyms** & stopwords editor; import/export.
- **Density caps** (Featured/Boost) with city gates.
- **Eligibility rules** (e.g., verified‑only for certain placements).
- **Invalid click** dashboard with credit issuance.
- **Index health**: doc counts vs DB counts, last update lag, error logs.

**Config safety**

- All changes require reason, actor, and (for money/placement) **two‑person approval**.
- Rollback to previous config version.

## **1.2.M Error model (API)**

- *SEARCH_INVALID_LOCATION* — unresolvable or mismatched city vs lat/lon.
- *SEARCH_UNDERAGE_SAFEMODE* — attempted explicit toggle without age verification.
- *SEARCH_ROLE_FILTER_CONFLICT* — role‑specific filter provided for wrong role.
- *SEARCH_CITY_GATED* — surface disabled for this city.
- *SEARCH_TOO_MANY_PARAMS* — exceeded allowed number of facets.
- *SEARCH_ENGINE_ERROR* — upstream engine error (masked; logged with corrId).

All error payloads include *code*, *message*, *hint*, and a correlation id.

## **1.2.N Synonyms & taxonomies (starter sets)**

**Genres (Models)**: fashion, editorial, commercial, runway, beauty, swim, fitness.  
**Specialties (Photographers/Videographers)**: portrait, fashion, editorial, wedding, music, commercial, product.  
**Amenities (Studios)**: natural light, cyc wall, blackout, backdrops, makeup area, dressing room, parking, AC/heating.

**Synonyms example**

- “bnw” ↔ “black and white”; “glam” ↔ “glamour”; “studio access” ↔ “has studio”.

## **1.2.O Security, privacy, safety controls**

- **Safe‑Mode** enforced at query and render time.
- **Age‑gate** required to see certain role tabs (Fan‑Sub); explicit public images still disallowed.
- **PII** never stored in index documents.
- **Abuse**: aggressive rate limiting and bot heuristics for suggest endpoints.

## **1.2.P Cost controls**

- **Typesense**: single small node (or managed starter), vertical scale when QPS rises; replica optional for HA.
- **OpenSearch Serverless** (if chosen): **OCU cap** per region; alarms on sustained OCU \> 80%.
- Cache TTLs keep engine calls low; nightly reindex batched to off‑peak hours.

## **1.2.Q Test plan (must‑pass)**

**Unit & contract**

- Filter parsing/normalization; role‑filter gating; city & safe‑mode checks; error codes.

**Search correctness**

- Role true: a multi‑role user queried in “Model” must link to */u/{handle}/model*; ratings don’t leak across roles.
- Studios separated: amenities filters never affect people surface.

**Ranking & fairness**

- Diversity: same owner appears ≤K times in top N.
- New‑seller floor: at least M cold‑start profiles surface in top N given enough eligible docs.
- Verify boosts: ID Verified outranks equal unverified, all else equal.

**Promotions**

- Density caps obeyed; placements never bypass filters; invalid clicks removed from billable stream.

**Performance**

- p95 latency within SLO for cached and uncached queries under synthetic city load.

**Resilience**

- Indexer retry & DLQ; search fallback message (non‑blocking) if engine unreachable.

## **1.2.R Work packages (for your 4 Cursor agents)**

**Agent C — Search/Index**

- WP‑SRCH‑01: Define Typesense collections; create indexer Lambda; implement upsert paths from outbox.
- WP‑SRCH‑02: Build query layer with normalization (city, radius) and safe‑mode enforcement; cursor pagination.
- WP‑SRCH‑03: Implement ranking features and fairness constraints; write unit tests.

**Agent A — API/BFF**

- WP‑API‑SRCH‑01: Implement GraphQL *search*, *searchSuggest*, *saveSearch* with auth & rate limits; error model and correlation ids.
- WP‑API‑SRCH‑02: Result caching (SWR) + per‑user cursor cache.

**Agent B — Web**

- WP‑WEB‑SRCH‑01: Search UI (role tabs, chips, facets, sort); result cards; disclosure for paid slots.
- WP‑WEB‑SRCH‑02: Saved searches & alerts (optional flag).

**Agent D — Admin & QA**

- WP‑ADM‑SRCH‑01: Console pages (reindex, synonyms, density caps, invalid‑clicks).
- WP‑QA‑SRCH‑01: E2E tests for correctness, fairness, promotions, and SLOs; synthetic dataset & golden files.

## **1.2.S Acceptance criteria (mark §1.2 FINAL only when ALL are true)**

152. **Correctness**: Role‑true discovery and studio separation verified; safe‑mode & age‑gate enforced; city gate honored.
153. **Filters**: All global and role‑specific filters work; social metrics shown only when verified.
154. **Ranking**: Diversity caps & new‑seller floor active; verify boosts and price fit working.
155. **Promotions** (if flag on): featured/boost slots respect density caps; no filter bypass; invalid clicks removed from billing.
156. **Performance**: p95 within SLO; cache hit rate ≥60% under synthetic load.
157. **Resilience**: Indexer DLQ empty after backfill; backfill parity within ±1% of DB records.
158. **Telemetry**: Events emitted; dashboards show CTR, filter usage, fairness metrics, index lag.
159. **Cost**: Engine within budget; cache prevents \>40% of engine calls; alarms quiet for 48h.

# 

# 

# **§1.3 — Booking & Checkout (Linked Booking Group, Escrow, Deposits, Docs‑Before‑Pay, Tax, Refunds, Disputes)**

**Purpose.** Specify the end‑to‑end technical design and guarantees for creating, validating, paying for, amending, and settling bookings—both single‑leg and **Linked Booking Groups (LBG)** where a *Talent leg* and a *Studio leg* are confirmed together but keep independent policies, receipts, and payouts. This section includes domain models, state machines, APIs, ledgers, taxes, deposits, refunds, disputes, attach‑in‑flow studios, admin tools, telemetry, SLOs, and a full test plan. We will stay in §1.3 until it is complete to your 99.9% bar.

## **1.3.A Canon & invariants**

- **Two distinct ledgers:** Talent leg and Studio leg are independent commercial contracts (prices, taxes, refunds, payouts, disputes). **LBG** is a *container* that synchronizes timing and UX but **never** merges their policies or reviews.
- **Docs‑before‑pay:** Required packs (SOW, Model Releases, Studio House Rules) must be assembled and signed **before** any charge is authorized or captured.
- **Escrow‑like handling:** Buyer is charged at confirmation; payouts are **withheld** until completion or acceptance window close (escrow mimic), with deposits handled separately for Studios.
- **Atomicity:** LBG confirmation succeeds **only if both legs validate and fund**; otherwise nothing commits.
- **Money correctness:** Sum of lines = totals; taxes computed per leg; cents (integer); idempotency on all external I/O.
- **Attach‑in‑flow Studio:** During Talent checkout, the buyer can add a Studio leg that matches time/location rules; both legs confirm together if valid.

## **1.3.B Domain model (Aurora PostgreSQL, source of record)**

Money in cents; timestamps UTC.

*-- Linked Booking Group (container)create table lbg ( lbg_id text primary key, -- lbg\_... buyer_user_id text not null, -- usr\_... status text not null check (status in ('draft','awaiting_docs','awaiting_payment','confirmed','in_progress','completed','cancelled','failed')), city text not null, start_at timestamptz not null, -- group reference window end_at timestamptz not null, acceptance_until timestamptz, -- buyer acceptance window end currency text not null default 'USD', created_at timestamptz not null default now(), updated_at timestamptz not null default now(), version bigint not null default 0); -- Booking legs (one per seller/role or per studio)create type leg_type as enum ('talent','studio'); create table booking_leg ( leg_id text primary key, -- leg\_... lbg_id text references lbg(lbg_id) on delete cascade, type leg_type not null, seller_user_id text not null, -- usr\_... (for studio, owner_user_id) service_profile_id text, -- talent leg (srv\_\*), null for studio leg studio_id text, -- studio leg (std\_\*), null for talent leg title text not null, -- shown on receipt start_at timestamptz not null, end_at timestamptz not null, -- pricing snapshot (immutable after confirm; use amendments for changes) subtotal_cents int not null, tax_cents int not null default 0, fees_cents int not null default 0, -- platform/service fees for this leg total_cents int not null, -- subtotal + tax + fees currency text not null default 'USD', policy_json jsonb not null default '{}'::jsonb, -- cancel windows, change windows doc_pack_id text, -- e-sign envelope id status text not null check (status in ('draft','awaiting_docs','awaiting_payment','confirmed','in_progress','completed','cancelled','failed')), created_at timestamptz not null default now(), updated_at timestamptz not null default now(), version bigint not null default 0); -- Charges (one LBG-level charge holds buyer funds; legs reference splits)create table charge ( charge_id text primary key, -- chg\_... lbg_id text not null references lbg(lbg_id) on delete cascade, processor text not null, -- 'stripe' processor_intent text not null, -- pi\_... (PaymentIntent) status text not null check (status in ('requires_action','authorized','captured','succeeded','canceled','failed')), amount_cents int not null, currency text not null default 'USD', payment_method text, -- 'card','ach_debit' created_at timestamptz not null default now(), updated_at timestamptz not null default now(), unique (processor, processor_intent)); -- Charge allocations per legcreate table charge_split ( charge_id text references charge(charge_id) on delete cascade, leg_id text references booking_leg(leg_id) on delete cascade, amount_cents int not null, primary key (charge_id, leg_id)); -- Studio deposits (separate auth/hold via SetupIntent)create table deposit_auth ( deposit_id text primary key, -- dep\_... leg_id text not null references booking_leg(leg_id) on delete cascade, -- studio leg only processor text not null, -- 'stripe' processor_setup text not null, -- seti\_... status text not null check (status in ('requires_action','authorized','captured','voided','expired')), authorized_cents int not null, captured_cents int not null default 0, currency text not null default 'USD', created_at timestamptz not null default now(), updated_at timestamptz not null default now(), unique (processor, processor_setup)); -- Amendments (change orders, extras/overtime); each produces delta lines and tax recalcscreate table amendment ( amendment_id text primary key, -- amd\_... leg_id text not null references booking_leg(leg_id) on delete cascade, kind text not null check (kind in ('change_order','overtime','refund_line','admin_adjustment')), delta_subtotal_cents int not null, delta_tax_cents int not null, delta_fees_cents int not null, delta_total_cents int not null, note text, created_by text not null, -- usr\_... (buyer, seller, admin) created_at timestamptz not null default now()); -- Payouts per leg (Connect transfers)create table payout ( payout_id text primary key, -- pay\_... leg_id text not null references booking_leg(leg_id) on delete cascade, processor text not null, -- 'stripe' processor_payout text, -- po\_... status text not null check (status in ('queued','in_transit','paid','failed','canceled','paused')), amount_cents int not null, currency text not null default 'USD', scheduled_for timestamptz, created_at timestamptz not null default now(), updated_at timestamptz not null default now()); -- Tax transactions (per leg)create table tax_txn ( tax_txn_id text primary key, -- tax\_... leg_id text not null references booking_leg(leg_id) on delete cascade, provider text not null, -- 'taxjar' or 'avalara' or 'stripe_tax' provider_id text not null, jurisdiction_json jsonb not null, -- state/city, rates quote_cents int not null, committed boolean not null default false, created_at timestamptz not null default now()); -- Refunds & disputescreate table refund ( refund_id text primary key, -- rfd\_... lbg_id text not null references lbg(lbg_id) on delete cascade, leg_id text not null references booking_leg(leg_id) on delete cascade, processor text not null, processor_refund text, -- re\_... amount_cents int not null, reason text not null, status text not null check (status in ('pending','succeeded','failed')), created_at timestamptz not null default now()); create table dispute ( dispute_id text primary key, -- dsp\_... leg_id text not null references booking_leg(leg_id) on delete cascade, processor text not null, -- 'stripe' processor_dispute text, -- dp\_... reason text not null, status text not null check (status in ('needs_response','under_review','won','lost','warning_closed')), evidence_due_at timestamptz, created_at timestamptz not null default now());*

**Indices**

- *booking_leg (seller_user_id, start_at)* for seller calendars.
- *booking_leg (service_profile_id)* and *booking_leg (studio_id)* for lookups.
- *charge_split (leg_id)* for rollups.
- Partial indexes on *booking_leg(status in ('confirmed','in_progress'))* for ops scans.

## **1.3.C State machines (per leg and for LBG)**

**Leg state:**  
*draft → awaiting_docs → awaiting_payment → confirmed → in_progress → completed*  
Failures: *cancelled*, *failed*

**LBG state:**

- Derived from legs: *draft* if any leg *draft/awaiting\_\**; *confirmed* if **both** legs *confirmed*; *in_progress* if any leg *in_progress*; *completed* if **both** *completed*; *cancelled* if both cancelled (or group cancelled prior to start); *failed* on atomicity failure pre‑confirm.

**Transitions (high‑level)**

171. **startCheckout** → create LBG + one leg (Talent) in *awaiting_docs*.
172. **attachStudioInFlow** (optional) → add Studio leg; both legs now *awaiting_docs*.
173. **createDocPack & sign** → both legs *awaiting_payment*.
174. **authorize & capture LBG charge** (PaymentIntent) → *confirmed* if both legs funded; else rollback.
175. **before start_at**: allow **amendments** (extras), re‑quote tax, adjust charge (incremental capture or second charge).
176. **at start_at**: move legs to *in_progress*.
177. **completion**: buyer acceptance or window expiry → queue **payouts**; auto‑void unused deposit holds.
178. **dispute/refund**: flows do not alter leg status but affect payout/finance ledgers; receipts amended.

**Studio deposit** lives outside the main charge and is captured only on approved claim within a policy window.

We implement these as an **AWS Step Functions** saga for LBG with per‑leg substates, plus outbox events to keep UI in sync.

## **1.3.D Checkout & payment flows**

**Payment providers:** Stripe only at launch (cards + ACH via Financial Connections). Adapter makes it swappable later.

**Strategy (escrow mimic):**

- **Capture the LBG charge at confirmation** (no long holds). Funds sit in platform/connected accounts.
- **Delay payouts** until completion/acceptance window.
- **Deposits** for Studio are handled via **SetupIntent** authorization (separate from GMV) and captured only if a valid claim is approved.

**Stripe objects**

- **PaymentIntent** (one per LBG) with **separate transfers** to legs on payout; metadata contains *lbg_id*, *leg_ids\[\]* and split details.
- **SetupIntent** for Studio deposit with *payment_method_options\[card\]\[capture_method\]=manual* semantics at claim time.
- **Transfers** at payout time per leg to the seller’s Connect account.
- **Refunds** per leg (partial allowed).

**ACH specifics**

- ACH debit is **captured** when *succeeded*; we hold payouts until enough settlement confidence or policy window.

**3DS / SCA**

- Use Stripe’s Payment Element; handle *requires_action* client‑side; webhook transitions keep our state machine consistent.

**Idempotency**

- All create/confirm/refund/payout calls carry an *Idempotency-Key* (persisted), and webhooks are verified (HMAC) + deduped.

## **1.3.E Tax & jurisdictions**

- Use **TaxJar/Avalara** (adapter) or **Stripe Tax** if we decide to keep vendors lean for MVP; either way, **quote is per leg** and stored in *tax_txn* with jurisdiction granularity.
- **Commit** tax on confirmation; **amend** on change orders; **refund** tax appropriately on cancellations/refunds per provider rules.

**Edge cases**

- Cross‑city bookings: compute tax based on **service location** (studio’s city or talent’s service location if no studio).
- Tax‑exempt flags (rare) require admin approval and audit.

## **1.3.F Amendments, extras & overtime**

- **Change Orders** produce *amendment* rows with deltas; tax re‑quoted; receipts updated.
- **Overtime**: triggered from thread/project during/after the session; priced per policy; may generate an extra **PaymentIntent** or **incremental capture** (cards) if allowed; for ACH, create a second charge.

## **1.3.G Refunds & cancellations**

**Policy engine**

- Encodes time‑banded refunds per leg (e.g., 72h+, 24–72h, \<24h).
- Computes buyer refund and seller forfeiture; **platform fees** refundability follows policy.
- **Group cancellation**: apply each leg’s policy independently; the group summary is a sum (displayed on the group receipt).

**Technical flow**

- Create *refund* records per leg; call Stripe *refunds.create* with *amount*; reconcile via webhooks; update receipts and Gold facts.

## **1.3.H Disputes**

- Stripe disputes → *dispute* table per leg; evidence kit assembled from doc packs, chat transcripts, deliverable manifests, check‑in/out timestamps, and studio rules acknowledgments.
- Admin console tracks deadlines, statuses, and outcomes; *won/lost* are mirrored in finance facts.

## **1.3.I GraphQL API (checkout & lifecycle) — key operations**

*type Mutation { startCheckout(leg: StartLegInput!, when: DateTimeRange!, city: String!): CheckoutDraft! attachStudioInFlow(draftId: ID!, studioId: ID!): CheckoutDraft! \# validates time/conflicts createDocPack(draftId: ID!): DocPack! \# returns envelope links markDocSigned(draftId: ID!, packId: ID!, envelopeId: ID!): DocPack! \# Payment createPaymentIntent(draftId: ID!, method: PaymentMethodInput!): PaymentIntentClientSecret! confirmPayment(draftId: ID!): CheckoutConfirmation! \# triggers atomic confirm \# Amendments addChangeOrder(lbgId: ID!, legId: ID!, change: ChangeOrderInput!): Amendment! addOvertime(lbgId: ID!, legId: ID!, minutes: Int!): Amendment! \# Post-session markCompleted(lbgId: ID!): CompletionReceipt! \# or auto after acceptance window fileDepositClaim(legId: ID!, amountCents: Int!, reason: String!): DepositClaimResult!} type Subscription { checkoutStatus(lbgId: ID!): CheckoutEvent!}*

**Guards**

- *attachStudioInFlow* checks studio availability, deposit policy, and buyer acceptance of additional terms.
- *createDocPack* enforces pack content per leg type and role; blocks payment steps until **both** legs have signed docs recorded.
- *confirmPayment* fails atomically if **any** leg fails validation or funding.

## **1.3.J Receipts & statements**

- **Per‑leg receipts** (line items, taxes, policy, refunds) + **Group summary** receipt for the LBG.
- Each receipt includes doc pack hashes (immutable), jurisdiction codes, PaymentIntent id, and split allocations.

## **1.3.K Payout scheduler & reserves**

- Default payout policy: queue **on completion** (or acceptance window end).
- **Reserves** (first‑payout or risk‑flagged sellers): hold for *N* days configurable per seller; Admin can override.
- Stripe transfers created with idempotency and reconciled via webhooks.

## **1.3.L Admin surfaces (Finance, Support, Trust)**

- **Finance**: payment/refund ledger, payout scheduler, reserve settings, tax commits, deposit claim approvals, reconciliation status, daily close.
- **Support**: cancel/partial refund tools with policy simulator; resend receipts; check‑in/out timeline; evidence export.
- **Trust**: dispute management, evidence pack builder, doc pack audit, chargeback trend analytics.

All actions are audited (actor, reason, before/after) and gated by RBAC + two‑person approvals where money moves.

## **1.3.M Telemetry (immutable events)**

- *lbg.create*, *leg.create*, *checkout.start*, *docs.pack.create*, *docs.envelope.signed*,
- *payment.intent.created*, *payment.intent.requires_action*, *payment.capture.succeeded\|failed*,
- *deposit.auth.authorized\|captured\|voided\|expired*,
- *amendment.added*, *tax.quote*, *tax.commit*,
- *payout.queued\|paid\|failed*, *refund.created\|succeeded\|failed*,
- *dispute.opened\|evidence_submitted\|won\|lost*.

These feed Bronze→Silver→Gold with money checks (Σsplits = charge, Σpayouts + fees + refunds = charge over time).

## **1.3.N SLOs & cost**

- **SLOs:** Checkout p95 \< **2s** (incl. tax/3DS); charge error rate \< **1%** (excluding user cancellations); payout queue drain \< **15 min** after completion; document pack creation \< **3s** p95.
- **Cost:** Stripe pay‑as‑you‑go; deposits are rare operations; tax provider billed per transaction; Step Functions + Lambdas are event‑driven; no always‑on compute.

## **1.3.O Error taxonomy (client‑safe)**

- *CHK_DOCS_REQUIRED* — pack not complete.
- *CHK_STUDIO_CONFLICT* — studio unavailable at requested time.
- *CHK_CARD_ACTION_REQUIRED* — 3DS step required.
- *CHK_ACH_NOT_VERIFIED* — bank link incomplete.
- *CHK_ATOMIC_FAIL* — one leg failed validation; nothing charged.
- *REFUND_POLICY_BLOCK* — requested refund outside policy window.
- *DEPOSIT_CLAIM_DENIED* — claim exceeds policy/evidence.

Error payloads include *code*, *message*, *hint*, *corrId*, and suggested next steps.

## **1.3.P Test plan (must‑pass, CI + sandbox)**

**Happy paths**

227. **Single‑leg Talent booking** (card): docs → pay → confirm → complete → payout queued.
228. **LBG Talent + Studio** (card+deposit auth): attach studio → docs for both legs → confirm → complete → studio deposit voided automatically → payouts queued.

**Alternates**  
3) **ACH flow**: bank link → confirm → settlement window; payouts delayed.  
4) **3DS challenge**: requires_action → client completes → webhook resumes.

**Edge & failure**  
5) **Atomicity fail**: after docs, Talent ok but Studio deposit auth fails → no charge; both legs remain *awaiting_payment*.  
6) **Change order**: add overtime → new charge or incremental capture; receipts updated; taxes re‑quoted.  
7) **Cancellation banding**: test each policy window; verify computed refunds per leg and group summary.  
8) **Dispute**: receive dispute webhook → evidence pack built → outcome recorded; payout clawback applied if lost.  
9) **Reconciliation**: daily close matches sums; artificial mismatch triggers red alert and payout pause.  
10) **Idempotency**: duplicate webhook deliveries don’t double‑apply state; duplicate client calls return same objects.

## **1.3.Q Work packages (Cursor agents)**

- **Agent B (Domain/API)**  
  WP‑CHK‑01: SQL migrations for lbg/leg/charge/split/deposit/tax_txn/refund/dispute/payout/amendment.  
  WP‑CHK‑02: GraphQL mutations/queries/subscriptions (see 1.3.I).  
  WP‑CHK‑03: Step Functions saga + Lambda handlers; idempotency store.
- **Agent C (Integrations)**  
  WP‑INT‑PAY‑01: Stripe adapter (PI, SI, transfers, refunds, disputes) + webhooks + mappers.  
  WP‑INT‑TAX‑01: Tax adapter (quote/commit/refund).  
  WP‑INT‑ESIGN‑01: Doc pack builder (Dropbox Sign/DocuSign) + gating.
- **Agent A (Web)**  
  WP‑WEB‑CHK‑01: Checkout UI with LBG container, attach‑studio pane, docs step, payment step, acceptance window UI, receipts.  
  WP‑WEB‑CHK‑02: Overtime/extras flows from thread/project panel.
- **Agent D (Admin & QA)**  
  WP‑ADM‑FIN‑01: Finance panel (ledger, payouts, reserves, refunds).  
  WP‑ADM‑SUP‑01: Support tools (policy simulator, cancel/refund wizard).  
  WP‑QA‑CHK‑01: E2E scenarios 1–10; synthetic Stripe/Tax/ESign sandboxes.

## **1.3.R Acceptance criteria (mark §1.3 FINAL only when ALL true)**

233. **Atomic LBG**: Both legs confirm together or neither does; receipts & tax per leg; group summary rendered.
234. **Docs‑before‑pay** gating enforced; envelopes signed and hashed on receipts.
235. **Main charge captured** at confirm; **payouts delayed** until completion/acceptance window; studio **deposit** authorized separately and auto‑voided absent approved claim.
236. **Amendments** (extras/overtime) produce correct deltas and taxes; payments succeed for deltas; receipts updated.
237. **Refunds** computed per leg policy; processed; receipts amended; taxes refunded per provider rules.
238. **Disputes** lifecycle fully supported; evidence packs produced; outcomes reflected in ledgers.
239. **Reconciliation** daily close green 5/5 days; SLOs met for checkout and payout queue.
240. **Telemetry** events present end‑to‑end; idempotency verified; error taxonomy used.
241. **Cost** within budget; no always‑on compute; Stripe/Tax usage aligns with traffic.

# **§1.3 — Booking & Checkout**

**(Linked Booking Group, Docs‑before‑Pay, Taxes, Deposits, Refunds, Disputes)**

We will complete §1.3 in multiple parts. **Part 1** (previous reply) delivered: entities, state machines, core Aurora schema, checkout API contracts, “Docs before Pay,” charge/deposit strategy, Stripe/Tax adapters, error taxonomy, and Part‑1 test plan.  
Below is **Part 2/3**, which covers **change orders & overtime, cancellation/refund policy engine, acceptance windows, deposit claims, receipts, and webhook mapping** in full build detail. After Part 2, I’ll continue with **Part 3/3** (payouts, reserves/instant payouts, disputes evidence kits, daily close, admin consoles, full E2E test matrix).

## **1.3.K Change Orders, Extras & Overtime (full specification)**

### **K.1 Purpose & invariants**

- **Change Orders** modify scope before the session starts (e.g., additional deliverables, time shift).
- **Overtime** is an in‑session or post‑session extension beyond the booked end time.
- All changes are tracked as immutable **amendment lines**; the original booking price snapshot remains unchanged.
- Taxes are **re‑quoted per leg** for each amendment that affects taxable amount.
- Payments for positive deltas are collected immediately (card incremental capture if available; otherwise a new PaymentIntent). For ACH, create a **second** PaymentIntent.

### **K.2 Data model (amendments, already introduced; here are line details)**

*create table amendment ( amendment_id text primary key, -- amd\_... leg_id text not null references booking_leg(leg_id) on delete cascade, kind text not null check (kind in ('change_order','overtime','admin_adjustment')), line_json jsonb not null, -- {name, qty, unit_price_cents, notes} delta_subtotal_cents int not null, delta_tax_cents int not null, delta_fees_cents int not null, delta_total_cents int not null, created_by text not null, -- usr\_... (buyer, seller, admin) created_at timestamptz not null default now());*

- ***line_json*** examples:

  - Change order: *{ "name":"Additional look","qty":1,"unit_price_cents":5000,"notes":"adds 5 edits" }*
  - Overtime: *{ "name":"Overtime (30m)","qty":1,"unit_price_cents":7500 }*

### **K.3 API**

*input ChangeOrderInput { legId: ID! name: String! qty: Int! = 1 unitPriceCents: Int! notes: String} input OvertimeInput { legId: ID! minutes: Int!} type Amendment { amendmentId: ID! legId: ID! kind: String! line: JSON! deltaSubtotalCents: Int! deltaTaxCents: Int! deltaFeesCents: Int! deltaTotalCents: Int! createdBy: ID! createdAt: AWSDateTime!} extend type Mutation { addChangeOrder(input: ChangeOrderInput!): Amendment! addOvertime(input: OvertimeInput!): Amendment!}*

### **K.4 Flow**

248. Client requests a change order or overtime.

249. Server validates policy (allowed windows, caps, seller/buyer approvals required).

250. Quote **tax** for the delta (per leg, per jurisdiction).

251. **Collect payment** for positive deltas:

     - **Card**: try **incremental capture** if the original PI allows; else create a **new PI** for the delta.
     - **ACH**: always create a **new PI** for the delta.

252. On success: write *amendment* row, update **receipts**, emit telemetry.

253. On failure: respond with error (*AMENDMENT_PAYMENT_FAILED*) and leave original booking untouched.

### **K.5 Validation & caps**

- Overtime limit per policy (e.g., ≤120 minutes).
- Rate source: leg policy or global catalog.
- Seller approval required if buyer initiates post‑session changes (configurable).

### **K.6 Telemetry**

- amendment.change_order.request/approved/paid/failed
- amendment.overtime.request/approved/paid/failed

## **1.3.L Cancellation & Refund Policy Engine**

### **L.1 Invariants**

- Policies are **per leg**, not per LBG. Group summary sums per‑leg outcomes.
- Time‑banded windows (e.g., ≥72h, 24–72h, \<24h) determine buyer refunds and seller retention.
- **Platform fees** refundability is configurable (default: refundable if cancellation initiated promptly or due to provider fault).

### **L.2 Policy schema**

*{ "version": 1, "bands": \[ { "from_hours": 72, "to_hours": null, "buyer_refund_pct": 100, "seller_payout_pct": 0 }, { "from_hours": 24, "to_hours": 72, "buyer_refund_pct": 50, "seller_payout_pct": 50 }, { "from_hours": 0, "to_hours": 24, "buyer_refund_pct": 0, "seller_payout_pct": 100 } \], "provider_cancel_full_refund": true, "admin_override_allowed": true}*

### **L.3 Engine behavior**

- Compute **hours_to_start = start_at - cancel_request_time (UTC)**.
- Select band; compute buyer refund and seller retained amount per **leg total**, **then** re‑compute taxes/refunds per provider rules.
- If **provider cancels**, buyer gets **full refund** by default.
- **Admin override** permitted with audit fields (*reason*, *actor*, *evidence_ref*).

### **L.4 API**

*input CancelLegInput { lbgId: ID!, legId: ID!, reason: String! }type RefundOutcome { legId: ID!, refundCents: Int!, sellerRetainedCents: Int!, taxRefundCents: Int! }extend type Mutation { quoteCancellation(lbgId: ID!, legId: ID!): RefundOutcome! cancelLeg(input: CancelLegInput!): RefundOutcome!}*

### **L.5 Refund execution**

- Create *refund* rows (per leg) and call Stripe *refunds.create(amount)*; track status via webhook.
- Update receipts and Gold facts; emit *refund.created\|succeeded\|failed*.

### **L.6 Edge cases**

- **Partial LBG cancel**: If one leg cancels, LBG remains but marks counterpart leg for buyer choice (continue or cancel); show **group summary** delta.
- **ACH pending**: If original ACH has not settled, we execute refunds only after settlement or via cancel API where available; display “pending” state to buyer.

## **1.3.M Acceptance Window (Buyer Confirmation After Session)**

### **M.1 Contract**

- After session end, buyer gets an **acceptance window** (e.g., 48h) to confirm satisfactory completion.
- If accepted → **queue payouts** immediately. If no response → **auto‑accept** at deadline.
- If buyer reports issue within the window → open a **dispute** or **resolution ticket**; payouts are **paused** for that leg pending outcome.

### **M.2 Data points**

- *lbg.acceptance_deadline* set at confirm time: *end_at + window*.
- *leg.status* remains *confirmed* until accepted → *completed*.

### **M.3 Implementation**

- **Scheduler**: SQS delayed messages or Step Functions **Wait** state; on deadline, transition.
- **Idempotency**: completing twice is safe; second call no‑ops.

### **M.4 Telemetry**

- *acceptance.window.start*, *acceptance.buyer.accept*, *acceptance.auto_accept*, *acceptance.issue_reported*.

## **1.3.N Studio Deposit Claims**

### **N.1 Purpose**

- Protect studio assets via a **separate authorization** (not GMV). Claims allowed for damage, overages not otherwise captured, or rule violations.

### **N.2 Flow**

279. Studio files claim with **amount** and **reason**, referencing evidence (doc packs, photos, timestamped messages).
280. Support triage → approve/deny/partial.
281. On approval → **capture** part or all of the deposit PaymentIntent.
282. Update receipts and notify buyer; disputes process available.

### **N.3 API & data**

*input DepositClaimInput { legId: ID!, amountCents: Int!, reason: String!, evidenceRefs: \[String!\] }type DepositClaimResult { legId: ID!, capturedCents: Int!, status: String! } extend type Mutation { fileDepositClaim(input: DepositClaimInput!): DepositClaimResult! approveDepositClaim(claimId: ID!, amountCents: Int!): DepositClaimResult! denyDepositClaim(claimId: ID!): DepositClaimResult!}*

- Store claims in a *deposit_claim* table with audit fields and evidence links.

### **N.4 Constraints**

- Max capture ≤ authorized amount; must be within studio policy claim window (e.g., 72h).
- Requires admin approval; two‑person rule optional for high amounts.

## **1.3.O Receipts (Per‑Leg + Group Summary)**

### **O.1 Templates**

- **Per‑leg**: role/studio header, booking window, itemization (base, extras), taxes (jurisdiction lines), platform fees attribution, payments/adjustments (amendments, refunds), doc pack hashes, dispute links.
- **Group**: LBG summary (both legs), subtotal/tax/fees/total, payment method summary (PI id), deposit (if any) separate.

### **O.2 Rendering**

- Deterministic JSON → server‑rendered PDF via headless Chromium or a PDF service; stored in S3 (immutable), linked to receipts and emails.

### **O.3 Rounding**

- Use **banker’s rounding** only where required by tax provider; otherwise all math in **integer cents**.

## **1.3.P Webhooks → Normalized Events (Mapping)**

### **P.1 Stripe (examples)**

- *payment_intent.succeeded* → *fin.charge.succeeded* (lbg_id, leg_ids\[\], amount_cents).
- *charge.refunded* → *fin.refund.succeeded* (leg_id, amount_cents).
- *dispute.created* → *fin.dispute.opened* (leg_id, reason, evidence_due_at).
- *payout.paid/failed* (covered in Part 3).

**Idempotency**: Deduplicate by *(provider_event_id)*; store last processed id per event type.

### **P.2 Tax provider**

- *quote.response* and *commit.response* summarized into *tax.quote*, *tax.commit* with jurisdiction payloads.

### **P.3 E‑sign vendor**

- *envelope.completed* → *doc.envelope.completed* (leg_id, envelope_id, pdf_hash).

## **1.3.Q Error Taxonomy (additions for this part)**

- *AMENDMENT_NOT_ALLOWED_WINDOW* — change order outside allowed window.
- *AMENDMENT_PAYMENT_FAILED* — delta payment failed.
- *CANCEL_POLICY_BAND* — cancellation falls into a specific band; hints show computed amounts.
- *DEPOSIT_CLAIM_WINDOW_EXPIRED* — claim filed after allowed window.
- *RECEIPT_RENDER_FAIL* — PDF renderer error (server retries; user gets fallback HTML).

## **1.3.R Test Plan (Part 2 focus)**

301. **Change Order** (pre‑session): positive delta → taxes re‑quoted → payment collected → amendment row saved → receipts updated.
302. **Overtime** (in‑session): card incremental capture; fall back to second PI if incremental capture not allowed; ACH always second PI.
303. **Cancellation bands**: simulate 96h/48h/12h cases; verify buyer refund and seller retention match policy; tax refunds correct.
304. **Partial LBG cancel**: cancel studio leg; talent leg remains; group receipt shows correct summary; buyer warned.
305. **Acceptance window**: buyer accepts vs auto‑accept; payouts queued accordingly (Part 3 will verify payouts).
306. **Deposit claim**: studio files claim; approve partial capture; receipts updated and buyer notified.
307. **Receipts**: verify line math and PDF rendering; hashes stored; email links valid.
308. **Webhooks mapping**: Stripe refund, dispute created, e‑sign completed → normalized events created once (idempotency).

## **1.3.S Acceptance Criteria (Part 2)**

We will mark **§1.3 (Part 2) COMPLETE** only when **all** are true:

- Change orders & overtime create amendment lines, collect payments properly, and re‑quote tax.
- Cancellation engine returns accurate band outcomes and executes refunds; partial LBG cancellation handled with clear UX and math.
- Acceptance window logic gates payouts correctly; auto‑accept on deadline.
- Deposit claim flow (auth → claim → capture/void) functions with audits and caps.
- Receipts (leg + group) render deterministically with tax and doc hashes.
- Webhook mappings produce normalized events idempotently.
- Part‑2 test suite green in CI and under sandbox smoke.
- No unexpected cost spikes (incremental captures vs new PIs measured; renderer concurrency capped).

# **§1.3 — Booking & Checkout**

**Part 3/3: Payouts & Reserves · Disputes & Evidence · Daily Close & Recon · Admin Consoles · Full E2E Test Matrix & SLOs**

This completes §1.3. We won’t move forward to §1.4 until you’re satisfied this sub-section is covered to your 99.9% bar.

## **1.3.T Payouts, Reserves, Instant Payouts (timing & failure modes)**

### **T.1 Principles**

- **Funds capture** happens at LBG confirmation (cards/ACH).
- **Payouts** are **per-leg** (Talent leg, Studio leg) and are queued only on **completion** (buyer accept) or **auto-accept** (acceptance window end).
- **Reserves** (platform risk) can delay or reduce the first or risky payouts.
- **Instant payouts** are optional and fee-bearing, subject to risk controls.

### **T.2 Data & states**

- *payout* table (per leg) holds: status (*queued\|in_transit\|paid\|failed\|canceled\|paused*), amount, scheduled time, and external payout id.
- Reserve policy table (or config): per-seller reserve %, minimum balance, and release cadence.

### **T.3 Computation of payout amounts**

Per **leg** on completion/accept:

*seller_gross = leg.total_cents – platform_fees_cents – refunds_cents – chargeback_reserve_hold_centsseller_net = max(0, seller_gross)*

- If seller has **reserve%** (e.g., 10%), we split:

  - transfer_now = floor(seller_net \* (1 - reserve%))
  - reserve_hold = seller_net - transfer_now

- Track reserves by seller with line-item provenance (which legs contributed).

### **T.4 Scheduler & execution**

- A **Payout Scheduler** runs on event or short cron:

  - For each eligible leg → compute amounts, **create Stripe transfer** to the seller’s Connect account with idempotency key tied to *(leg_id, payout_seq)*.
  - On success → status *in_transit* then *paid* (via webhook).
  - On failure → *failed*; retry with back-off and display admin action items.

### **T.5 Instant payouts (optional)**

- If enabled for a seller and platform policy allows:

  - Expose “Instant Payout” in Seller → transfers *transfer_now* immediately (Stripe instant) minus **instant fee**.
  - Blocked when: recent disputes, excessive refunds, negative balance, or flagged risk.
  - All instant payouts audited.

### **T.6 Failure modes & handling**

- **ACH settlement uncertainty**: For recent ACH payments, payouts **wait** until settlement confidence time or policy window.
- **Negative net** (post-refund/dispute loss): mark seller balance negative; future payouts net it out; Admin can arrange manual debit if required.
- **Webhook gaps**: if we miss a payout webhook, a reconciliation job fetches payout objects and backfills states idempotently.

### **T.7 Telemetry**

- *payout.queued\|in_transit\|paid\|failed\|canceled\|paused*, *reserve.hold\|release*, *payout.instant.request\|approved\|denied*.

## **1.3.U Disputes (chargebacks) & Evidence Kits**

### **U.1 Sources of evidence**

- **Doc packs** (SOW, releases, studio rules) with immutable PDF hashes.
- **Thread transcript** (messages + action cards timestamps).
- **Deliverable manifest** (checksums, names, upload times).
- **Check-in/out** time evidence (session start/end).
- **Studio deposit policy** and photos (if relevant).
- **Buyer acceptance** event (if occurred) or issue report details (within window).

### **U.2 Flow**

337. Stripe webhook *dispute.created* → create *dispute* row (per leg).
338. **Evidence kit assembler** collates sources into a zip/PDF bundle + summary template.
339. Support fills in narrative, attaches evidences, **submits** to processor before *evidence_due_at*.
340. Webhooks update status → *under_review* → *won\|lost*.
341. If **lost**, apply **clawback** (adjust seller balance; reserve may absorb); update receipts/Gold facts; notify parties.

### **U.3 Admin console (Trust & Finance)**

- Timeline & deadline tracker; evidence editor; one-click export; outcomes log; dispute rates by seller/city; flags for investigation.

### **U.4 Telemetry**

- *dispute.opened\|evidence_submitted\|won\|lost*, *chargeback.clawback.applied*, *seller.flag.risk_breach*.

## **1.3.V Daily Finance Close & Reconciliation (hard gate)**

### **V.1 Purpose**

Guarantee money correctness between **processor records** and our **ledger/Gold facts**, and gate payouts/tax filings when variances exceed thresholds.

### **V.2 Inputs**

- Processor extracts: payments, refunds, disputes, payouts (settled date, amount, ids).
- Our facts: *charge*, *charge_split*, *refund*, *payout*, *tax_txn*, *amendment*, *reserve*.

### **V.3 Checks (examples)**

- **Σcharge_splits per LBG == charge.amount** (cents).
- **Σleg totals** == **Σ(allocations + refunds + platform_fees + tax)** within tolerance.
- **Σpayouts + reserves pending** equals **Σseller_net** over time windows.
- All external ids exist and are unique; duplicate webhooks are deduped.
- Tax committed count/amount matches provider reports.

### **V.4 Flow**

351. Extract → Stage → Compare (by day, tz aware).
352. **Variance threshold** (e.g., 0.5%) → **gate**: pause payouts, alert Finance/Eng, show recon diff tiles.
353. Quarantine bad rows; **replay** or **adjust** via Admin tooling with audit.
354. When green → **close day** → emit *finance.close.succeeded* event.

### **V.5 Admin tiles**

- Summary widgets: charges/refunds/payouts/tax; heatmap of variances; quick links to diff detail.
- Adjustment ledger UI: create/view adjustments with reason and linked records.

### **V.6 Telemetry**

- *finance.close.start\|succeeded\|failed*, *recon.variance.notice*, *adjustment.created*, *payouts.paused\|resumed*.

## **1.3.W Admin Consoles (Finance · Support · Trust · City Ops)**

### **W.1 Finance**

- **Ledger** per leg & seller; **Payout scheduler** queue; **Reserves** config & releases; **Tax** commits & exports; **Recon** dashboard; **Close day** button (two-person approval).
- Actions require reason; some require dual approval (money-moving).

### **W.2 Support**

- **Cancellation/refund** simulator + execution; resend receipts; edit buyer contact on receipts; acceptance window overrides; deposit claims approval UI.

### **W.3 Trust & Safety**

- **Disputes** timeline; evidence builder; policy rulebook; NSFW overrides; seller risk flags; rate limits for abuse.

### **W.4 City Ops / Promotions**

- City allowlists; **Promotions** density caps; eligibility toggles; invalid-click credits.

**RBAC**: least-privilege by role; JIT elevation for sensitive ops; **immutable audits** on every admin action.

## **1.3.X Error & Incident Playbook (selected)**

- **PI fail after docs** → user sees *CHK_ATOMIC_FAIL*; LBG remains awaiting payment; guide to retry or change method.
- **ACH return** → auto-notify; re-attempt as allowed; payouts halted until resolution.
- **Payout failed** → retry; if repeated, set *paused* and notify Finance; show Seller banner.
- **Recon gate** → payouts paused; visible banner in Admin; action required to unpause.
- **Deposit claim abuse** → T&S review; throttle studio claims; require additional evidence.

## **1.3.Y Full E2E Test Matrix (implement in CI + sandbox)**

**Booking & Payment**

368. Single-leg, card.
369. LBG, card + studio deposit auth.
370. Single-leg, ACH (settlement wait).
371. 3DS challenge.
372. Atomic failure → no charge.
373. Retry with different method.

**Docs & Receipts**  
7. Doc pack gating; signatures required; hashes on receipts.  
8. PDF receipts (leg + group), immutable & downloadable.

**Amendments**  
9. Change order pre-session → delta math & tax.  
10. Overtime during session → incremental capture/new PI, receipts updated.

**Cancellations/Refunds**  
11. Provider cancel → full refund to buyer.  
12. Buyer cancel across 72h/48h/12h bands.  
13. Partial LBG cancel (one leg only).

**Acceptance & Payouts**  
14. Buyer accept → payouts queued; reserve applied.  
15. Auto-accept → payouts queued.  
16. Instant payout allowed vs denied (risk).  
17. Payout webhook sync to *paid*.

**Disputes**  
18. Dispute open → evidence build → submit → won.  
19. Dispute lost → clawback; receipts/Gold reflect.

**Recon & Close**  
20. Daily close green.  
21. Inject small variance → payouts paused → adjustment → green.  
22. Webhook duplication → idempotent handling.

**Performance**  
23. Checkout p95 \< 2s with tax/3DS mix.  
24. Payout queue drain \< 15 min on completion spikes.

**Cost**  
25. Renderer throttling; OpenSearch/Typesense calls within budget; Stripe/Tax cost alarms quiet.

## **1.3.Z Acceptance Criteria — mark §1.3 FINAL only when ALL true**

374. **Atomic LBG**, **Docs-before-Pay**, **Deposits**, **Amendments**, **Refunds**, **Disputes**, **Payouts/Reserves**, **Acceptance Window** all function as specified.
375. Receipts (leg + group) include line items, taxes, doc hashes, amendments, refunds, payouts.
376. Scheduler/Step Functions drive end-to-end state reliably; retries are idempotent.
377. Finance **daily close** runs green for 5 consecutive days; variances gate payouts correctly.
378. Admin consoles (Finance/Support/Trust/City Ops) provide the actions above with immutable audits and dual approvals where required.
379. Telemetry is complete (events listed across 1.3); observability dashboards green.
380. p95 **Checkout ≤ 2s**, payout drain ≤ 15m, and costs stay within budget alarms.
381. The **full E2E test matrix** passes in CI and sandbox (card/ACH/3DS/atomic/cancel/dispute/recon).

# **§1.4 — Messaging & Project Panel (threads, action cards, deliverables, approvals)**

**Goal.** Implement a role‑aware, booking‑aware messaging system with a **Project Panel** embedded in the conversation: briefs, moodboard, shot list, files (previews + external manifests), docs & e‑sign status, expenses/amendments, and one‑click **action cards** (reschedule, extras, overtime, deliverable approvals, deposit claims, dispute/report). This section gives the **full technical spec**—data models, APIs, realtime behavior, file pipeline, moderation/safety rules, notifications, admin tooling, telemetry, SLOs, tests, and cost levers.

We will not move to §1.5 until §1.4 hits your **99.9% coverage** bar.

## **1.4.A Canon & invariants**

- Thread kinds.

  - **Inquiry thread** (pre‑booking; can transition into a project on accept).
  - **Project thread** (post‑accept; bound to a **leg** or an **LBG**; unlocks Project Panel + action cards).

- **Project Panel anchors the contract.** It exposes structured tabs *inside* the conversation: **Brief**, **Moodboard**, **Shot list**, **Files**, **Docs & e‑sign**, **Expenses/Adjustments**, **Actions**.

- **Action cards** are typed, stateful message objects that **invoke domain flows** (reschedule, extras, overtime, deliverables accept/changes, cancellations/refunds, deposit claim, dispute). All are idempotent and audit‑friendly.

- **Files: “storage‑sane.”** Public previews only in S3; final deliverables stay external (Drive/Dropbox/S3 owner links) captured as **immutable manifests** (name, size, checksum, URL).

- **Safety & policy.** Safe‑Mode thumbnails; NSFW scanning; anti‑circumvention nudges; role‑scoped moderation; report/block tools.

## **1.4.B Data model & storage**

**Hot path** in DynamoDB (messages, presence, ephemeral states). **Source of truth** for bookings/legs/LBG/docs in Aurora (§1.3). S3 for previews/manifests; EventBridge for async; AppSync GraphQL for API & realtime.

### **B.1 DynamoDB single‑table (messaging)**

**Partition & sort:**

- **PK** = *THR#{threadId}*

- **SK**:

  - *THR* — thread metadata (one item)
  - *PART#{userId}* — participant membership & read cursors
  - *MSG#{ts}#{messageId}* — message frames (append‑only)
  - *CARD#{messageId}* — action‑card shadow (current state)
  - *TAB#{tab}* — project panel tab state (denormalized snapshot for fast read)

**Core items:**

- Thread (THR)

*{*  
*pk: "THR#thrd\_...",*  
*sk: "THR",*  
*kind: "inquiry\|project",*  
*lbgId: "lbg\_..." \| null,*  
*legId: "leg\_..." \| null,*  
*buyerUserId: "usr\_...",*  
*sellerUserId: "usr\_...",*  
*participants: \["usr\_...", "usr\_..."\],*  
*city: "Houston",*  
*createdAt, updatedAt,*  
*status: "open\|archived\|locked",*  
*lastMessageAt,*  
*safeModeRequired: true\|false*  
*}*  

- Participant (PART#user)

*{*  
*pk: "THR#thrd\_...",*  
*sk: "PART#usr\_...",*  
*roleContext: "buyer\|seller\|admin",*  
*lastReadMsgId: "msg\_...",*  
*lastReadAt,*  
*muted: bool,*  
*blockedUntil: ISO \| null*  
*}*  

- Message (MSG#ts#id)

*{*  
*pk: "THR#thrd\_...",*  
*sk: "MSG#2025-11-05T14:12:07.123Z#msg\_...",*  
*type: "text\|asset\|system\|action",*  
*body: "sanitized markdown or plaintext",*  
*attachments: \[ { kind: "preview\|manifest", s3Key\|manifestRef, mime, w, h } \],*  
*action: { type, payload, state, version } \| null,*  
*authorUserId: "usr\_...",*  
*nsfwBand: 0\|1\|2,*  
*flags: { moderation: "clean\|flagged\|blocked", policyHints: \[...\] },*  
*createdAt*  
*}*  

- Project Panel tab state (TAB#{tab})

  - *TAB#brief*, *TAB#moodboard*, *TAB#shotlist*, *TAB#files*, *TAB#docs*, *TAB#expenses*, *TAB#actions*  
    Snapshot JSON for fast open; canonical data lives in Aurora when contractual (docs, amendments, receipts).

**GSIs:**

- **GSI1 (inbox list)**: *GSI1PK = PARTICIPANT#usr\_...*, *GSI1SK = lastMessageAt desc → threadId* (materialized via write fan‑out).
- **GSI2 (project threads by lbg/leg)**: *GSI2PK = LBG#lbg\_...* or *LEG#leg\_...*, *GSI2SK = createdAt*.

### **B.2 Presence & typing (ephemeral)**

- **Presence table** (DDB) with TTL (e.g., 60s): *presence#threadId#userId = lastSeen, typing=true/false*.
- Subscriptions broadcast presence changes; server filters access by membership.

### **B.3 S3 buckets (previews only)**

- *msg-previews* — public‑size thumbs/videos (auto‑transcoded on upload); NSFW scan assigns *nsfwBand*.
- *msg-quarantine* — for flagged items pending T&S review.
- **No finals**: refer to external manifests stored in Aurora *deliverable_manifest* (by leg).

## **1.4.C GraphQL API (AppSync) — types, queries, mutations, subscriptions**

**Note:** Field‑level auth via Cognito + server checks (membership). All mutations emit domain events to EventBridge.

### **C.1 Core types (excerpt)**

*enum ThreadKind { INQUIRY PROJECT }*  
*enum MessageType { TEXT ASSET SYSTEM ACTION }*  
*enum ActionType {*  
*RESCHEDULE REQUEST_EXTRA OVERTIME_START OVERTIME_STOP*  
*DELIVERABLE_PROOF DELIVERABLE_FINAL APPROVE_DELIVERABLE REQUEST_REVISIONS*  
*CANCEL_REQUEST REFUND_REQUEST ACCEPTANCE_ACK*  
*DEPOSIT_CLAIM_OPEN DISPUTE_OPEN*  
*}*  
  
*type Thread {*  
*threadId: ID!*  
*kind: ThreadKind!*  
*lbgId: ID*  
*legId: ID*  
*participants: \[User!\]!*  
*lastMessageAt: AWSDateTime!*  
*status: String!*  
*projectPanel: ProjectPanel!*  
*}*  
  
*type ProjectPanel {*  
*brief: Brief*  
*moodboard: Moodboard*  
*shotlist: Shotlist*  
*files: FileShelf*  
*docs: DocStatus*  
*expenses: Expenses*  
*actions: \[ActionCard!\]!*  
*}*  
  
*type Message {*  
*messageId: ID!*  
*type: MessageType!*  
*author: User!*  
*body: String*  
*attachments: \[Attachment!\]*  
*action: ActionCard*  
*createdAt: AWSDateTime!*  
*nsfwBand: Int!*  
*}*  
  
*type ActionCard {*  
*actionId: ID!*  
*type: ActionType!*  
*payload: AWSJSON!*  
*state: String! \# e.g., PENDING\|ACCEPTED\|DECLINED\|PAID\|CLOSED*  
*version: Int!*  
*createdBy: User!*  
*createdAt: AWSDateTime!*  
*updatedAt: AWSDateTime!*  
*}*  

### **C.2 Queries**

*type Query {*  
*inbox(limit: Int = 25, cursor: String): InboxPage! \# lists user's threads*  
*thread(threadId: ID!): Thread!*  
*messages(threadId: ID!, cursor: String, limit: Int = 50): MessagePage!*  
*projectPanel(threadId: ID!): ProjectPanel!*  
*}*  

### **C.3 Mutations (selected)**

*type Mutation {*  
*\# Inquiry → Project promotion happens when checkout succeeds (webhook promotes)*  
*startInquiry(sellerServiceProfileId: ID!, buyerBrief: BriefInput!): Thread!*  
  
*sendMessage(threadId: ID!, body: String!, attachments: \[AttachmentInput!\]): Message!*  
  
*\# Action cards (all idempotent; server enforces state)*  
*proposeReschedule(threadId: ID!, newTime: DateTimeRange!): ActionCard!*  
*requestExtra(threadId: ID!, name: String!, priceCents: Int!): ActionCard!*  
*startOvertime(threadId: ID!, minutes: Int!): ActionCard!*  
*stopOvertime(threadId: ID!): ActionCard!*  
  
*postDeliverableProof(threadId: ID!, manifestRef: ID!, note: String): ActionCard!*  
*postDeliverableFinal(threadId: ID!, manifestRef: ID!, note: String): ActionCard!*  
*approveDeliverable(threadId: ID!, deliverableId: ID!): ActionCard!*  
*requestRevisions(threadId: ID!, deliverableId: ID!, note: String!): ActionCard!*  
  
*requestCancel(threadId: ID!, legId: ID!, reason: String!): ActionCard!*  
*requestRefund(threadId: ID!, legId: ID!, reason: String!, amountCents: Int): ActionCard!*  
  
*acknowledgeCompletion(threadId: ID!): ActionCard! \# buyer acceptance*  
  
*openDepositClaim(threadId: ID!, amountCents: Int!, reason: String!, evidence: \[String!\]): ActionCard!*  
*openDispute(threadId: ID!, legId: ID!, reason: String!, details: String!): ActionCard!*  
*}*  

Each action card mutates both **DynamoDB** (message frame + CARD shadow) and **Aurora** (leg/LBG state via §1.3 services). For example, *requestExtra* calls the **Checkout/Amendments** service to price & charge the delta.

### **C.4 Subscriptions**

*type Subscription {*  
*threadEvents(threadId: ID!): ThreadEvent! \# message new, edited, action state, presence*  
*inboxEvents: InboxEvent! \# new thread, unread counts*  
*presence(threadId: ID!): PresenceEvent! \# typing, online/lastSeen*  
*}*  

## **1.4.D Project Panel tabs — schemas & behavior**

### **D.1 Brief**

- **Schema**: title, goals, style references (links), mood notes, must‑have shots, constraints, budget notes.
- **Versioning**: optimistic concurrency; edits write a new version and emit *panel.brief.update*.

### **D.2 Moodboard**

- **Pins**: references to portfolio assets or external URLs (image cards with source attribution).
- **Ordering**: drag‑drop; server persists index.
- **NSFW**: Safe‑Mode rules (blur/hidden) apply to pins as with messages.

### **D.3 Shot list**

- **Items**: *{ id, name, notes, refs:\[pinId\], owner:userId, status: "todo\|done" }*.
- **Templates**: start from roles’ presets; saved as reusable templates.
- **Stats**: completion percentage for the day; surfaces in thread header.

### **D.4 Files**

- **Buckets**: *Proofs* (previews in S3), *Finals* (external manifests).
- **Guardrails**: finals must be **external**; internal proofs have size limits; virus & NSFW scans on upload.
- **Manifests**: table in Aurora *deliverable_manifest (legId, manifestId, entries\[\], checksum, externalProvider, immutable=true)*.

### **D.5 Docs & e‑sign**

- Read‑only in panel: envelope status (per leg); links to PDF (hashed). If unsigned, show **action card** to prompt sign.

### **D.6 Expenses**

- Live rollup of **amendments** (extras/overtime) & **refunds** from §1.3; sum per leg and group; clickable to open receipts.

### **D.7 Actions**

- List **open action cards** (state machines): accept/decline/resubmit; all actions audit to thread + domain event.

## **1.4.E Action cards — contract & state machines (examples)**

**All actions share:** *actionId*, *type*, *payload{}*, *state*, *version*, *createdBy*, timestamps, and **idempotencyKey**.

- Reschedule

  - *payload*: *{ old: DateRange, proposed: DateRange }*
  - *state*: *PENDING → ACCEPTED\|DECLINED\|EXPIRED*
  - Accept transitions booking (§1.3) to new times if conflict‑free.

- Request Extra / Overtime

  - *payload*: *{ name, priceCents }* or *{ minutes }*
  - *state*: *PENDING → PAID\|DECLINED*
  - On approve → calls **Amendments**; on pay fail → *FAILED* with error code.

- Deliverables

  - Proof/Final cards include *manifestRef* to aura row.
  - Buyer: *APPROVE_DELIVERABLE* → *APPROVED*; or *REQUEST_REVISIONS* → *REVISION_REQUESTED* (optional extra cost via change order).

- Cancel/Refund

  - Calls §1.3 policy engine; returns quoted outcome; Support/Admin can override via console (dual‑approval).

- Deposit claim

  - Studio opens claim with amount + evidence; Support approves/denies; on approve → capture deposit hold.

- Dispute

  - Opens processor dispute row; triggers evidence kit builder; timeline pinned in panel.

## **1.4.F Presence, read receipts, typing**

- **Read receipts**: per participant, store *lastReadMsgId* and *lastReadAt*; messages with ts ≤ lastReadAt show as read.
- **Typing**: client emits ephemeral *typing=true* events throttle‑debounced; server writes presence TTL item; subscription broadcasts.
- **Online**: presence entries updated on ping; absences \> TTL means offline.

## **1.4.G Moderation, safety, anticircumvention**

- **Text filters**: regex + ML models for PII/banlist (emails, phone, Venmo/CashApp handles).

  - First hit → **nudge** (educational banner).
  - Repeat → **soft block** sending with “Use on‑platform checkout.”
  - Abuse → escalation to T&S; rate‑limits or temp mutes per thread.

- **NSFW**: all previews scanned; respect Safe‑Mode (blur/blocked).

- **Report/Block**: per thread; blocks hide typing & DMs, and notify Support.

- **Audit**: every moderation action writes immutable admin audit with reason.

## **1.4.H Notifications (email, push, SMS)**

- **Triggers**: new message (not self), action card state change, deliverable posted, doc sign needed, acceptance window nearing end.
- **Quiet hours**: user‑settable; we queue non‑urgent notifications and send digest.
- **Templates**: centralized in Comms adapter; no sensitive content in SMS; deeplinks to thread/role context.
- **Backpressure**: dedupe within a 2–5 minute window; collapse multiple messages into a single notification.

## **1.4.I File pipeline & limits**

- **Uploads**: signed S3 URLs; client streams **previews** only; large files rejected; user pointed to “attach external link.”
- **Scanning**: Lambda antivirus + vision safety; quarantine bucket for suspects; admin override with audit.
- **Preview transforms**: Lambda@Edge resizes images on demand; video previews transcoded to HLS snippets with caps.
- **Limits (launch)**: preview ≤ 20 MB; images ≤ 12k px max dimension; videos ≤ 60s preview.

## **1.4.J Admin consoles (Support, T&S, Finance)**

- **Support**: view thread & panel, impersonate read‑only, run policy simulator, send system notices, approve/deny reschedules (if needed), manage refunds (hooks §1.3).
- **T&S**: moderation queue, content decisions, anticircumvention violations, mutes/blocks, audit exports.
- **Finance**: expenses rollups vs receipts; deposit claims queue; links to payouts/reserves pages.

All admin acts require reason and generate immutable audits; sensitive actions require **two‑person approval**.

## **1.4.K Observability, telemetry, and lineage**

**Events (immutable):**  
*thread.create*, *thread.promoted_to_project*,  
*message.send*, *message.asset.attach*, *message.blocked*,  
*presence.typing_on/off*, *presence.online/offline*,  
*panel.brief.update*, *panel.moodboard.pin*, *panel.shotlist.update*, *panel.files.add*,  
*action.create*, *action.state_change*,  
*deliverable.proof.posted*, *deliverable.final.posted*, *deliverable.approved*,  
*cancel.requested*, *refund.requested*,  
*deposit.claim.opened\|approved\|denied*,  
*dispute.opened*,  
*notification.sent*,  
*admin.moderation.\**.

**Lineage:** for every action that touches money/docs/booking, emit correlating IDs (*leg_id*, *lbg_id*, *doc_id*, *amendment_id*) so evidence kits can be assembled reliably (§1.3.U).

## **1.4.L Performance & cost**

- **DynamoDB**: write patterns append‑only; 1KB–8KB avg items; *MSG#ts#id* packs a capped body length (server truncates oversize with link to file). TTL on ephemeral presence rows.
- **AppSync**: subscriptions filtered by *threadId*; pagination uses forward cursors; cache last N cursors per user for back/forward UX.
- **S3/CF**: thumbnails & short previews only; lifecycle to Intelligent‑Tiering after 30 days; egress minimized.
- **Compute**: Lambdas on demand; webhook processors for action side‑effects; no always‑on servers.

## **1.4.M Error taxonomy (client‑safe)**

- *MSG_POLICY_BLOCKED* — text violates anticircumvention policy.
- *MSG_NSFW_BLOCKED* — preview blocked under Safe‑Mode.
- *THREAD_NOT_MEMBER* — user not participant.
- *THREAD_LOCKED* — admin lock.
- *ACTION_INVALID_STATE* — e.g., approve deliverable already closed.
- *ACTION_CONFLICT* — reschedule overlaps; check §1.3 validation.
- *PANEL_VERSION_CONFLICT* — optimistic concurrency failed.
- *UPLOAD_QUARANTINED* — file in safety review.

All error payloads include *code*, *message*, *hint*, *corrId*.

## **1.4.N Test plan (CI + sandbox)**

**Threads & inbox**

450. Create inquiry; promote to project on checkout success.
451. Inbox lists threads with unread counts; mute suppresses notifications.

**Messages & presence**  
3) Send text + preview; Safe‑Mode blur/blocked behavior verified; read receipts correct.  
4) Presence/typing TTLs work; offline after TTL.

**Project Panel**  
5) Brief edit versioning and merge conflict.  
6) Moodboard pin/ordering & NSFW rules.  
7) Shot list CRUD + completion stats.  
8) Files: preview upload → scanned; finals via manifest; blocked file path.

**Action cards**  
9) Reschedule propose/accept/decline; booking reflects new time.  
10) Request Extra → amendment created & paid (card/ACH flows).  
11) Overtime start/stop → billed and appended to receipts.  
12) Deliverable proofs/finals → approve/revise loop; receipts unaffected unless change orders occur.  
13) Cancel/Refund → policy engine invoked; math aligns with §1.3.  
14) Deposit claim → approval path; partial capture; receipts reflect.  
15) Dispute open → evidence kit seeded; timeline shows deadlines.

**Moderation**  
16) Anticircumvention: first nudge, then soft block on repeat.  
17) Report/Block actions; muted user can’t DM; audit written.

**Notifications**  
18) Dedup window coalesces bursts; quiet hours batching.

**Performance/cost**  
19) p95: open thread ≤ 300 ms (cached) / ≤ 600 ms (cold) at city scale; subscriptions stable.  
20) S3/CF egress stable; DDB RCU/WCU within budget.

## **1.4.O Work packages (Cursor agents)**

- **Agent B — API / Realtime**  
  WP‑MSG‑01: DDB table & GSIs; resolvers for inbox, thread, messages, project panel; subscriptions.  
  WP‑MSG‑02: Presence/typing TTL flows; read receipts.
- **Agent C — Actions / Domain hooks**  
  WP‑ACT‑01: Implement action cards + state machines; integrate §1.3 services (reschedule, amendments, deposit, dispute).  
  WP‑ACT‑02: Webhook handlers → normalized events → DDB/Aurora updates.
- **Agent A — Web**  
  WP‑WEB‑MSG‑01: Inbox UI, thread UI (role chips, Safe‑Mode), Project Panel tabs with optimistic updates.  
  WP‑WEB‑MSG‑02: Upload UI → scanned previews; external manifest attach; action card components.
- **Agent D — Moderation/QA**  
  WP‑MOD‑01: Anticircumvention filters + UI nudges; T&S console; audit trails.  
  WP‑QA‑MSG‑01: Full test matrix; fixtures; golden snapshots.

## **1.4.P Acceptance criteria (mark §1.4 FINAL only when ALL true)**

456. Inquiry → Project promotion path live; project thread bound to leg or LBG.
457. Messaging works with presence, read receipts, Safe‑Mode previews, and NSFW scanning.
458. Project Panel tabs (brief, moodboard, shot list, files, docs, expenses, actions) are fully functional; finals handled by external manifests.
459. Action cards trigger §1.3 domain flows correctly and idempotently; states visible and auditable in thread.
460. Moderation, report/block, and anticircumvention nudges operate with audits; policy cannot be bypassed by guests.
461. Notifications (email/push/SMS) are batched, deduped, and respect quiet hours.
462. Telemetry covers lifecycle, panel, actions, moderation, and notifications; dashboards show health & lag \< threshold.
463. p95 performance meets targets; DDB/AppSync/S3 costs within budget alarms for 48h of synthetic load.

# **§1.5 — Smart Docs & E‑Sign CMS**

*(Clause library · variables · pack assembly · e‑signature · PDF hashing · retention · rollbacks · comms templates · admin & audits)*

**Purpose.** Create a versioned, auditable **Smart Docs CMS** that generates legal‑quality documents for bookings and linked booking groups (LBG): SOW (Statement of Work), Model Release(s), and Studio House Rules. These are assembled into **Doc Packs** that must be **fully signed before payment** (Docs‑Before‑Pay), with immutable storage (hashing), retention, re‑issue rules, and end‑to‑end lineage for disputes and finance.

We won’t move to §1.6 until §1.5 meets your 99.9% bar.

## **1.5.A Canon & invariants**

464. **Docs‑Before‑Pay:** Checkout cannot capture funds unless **every required doc** for each leg has been generated and fully signed (all signers complete).
465. **Per‑leg packs:** LBG has **one Doc Pack per leg** (Talent leg pack; Studio leg pack). Packs can contain multiple documents.
466. **Immutable evidence:** Rendered PDFs are hashed (SHA‑256) and written to S3 with WORM‑like retention; every receipt references doc hashes.
467. **Versioned clauses:** All doc content is composed from a **clause library** with semantic versioning and city gates.
468. **Re‑issue on change:** Any scope/time/location change that affects the contract content **invalidates** prior signatures and requires re‑issue (with clear UX).
469. **Privacy & redaction:** PII and signatures are stored securely; evidence exports support **minimal disclosure** redactions for disputes.
470. **Seven‑year retention** (configurable) for all signed docs and envelope metadata.

## **1.5.B Data model (Aurora Postgres + S3)**

*-- Clause library (atomic building blocks)*  
*create table doc_clause (*  
*clause_id text primary key, -- cls\_...*  
*name text not null, -- "SOW: Base Terms", "Model Release: Adult", "House Rules: Standard"*  
*version int not null, -- semantic versions across edits*  
*city_gate text\[\], -- list of allowed city codes (null = global)*  
*role_gate text\[\], -- \['model','photographer','studio'\] filter*  
*is_active boolean default true,*  
*body_markdown text not null, -- authoring format*  
*variables_json jsonb not null, -- schema of variables required*  
*created_by text not null,*  
*created_at timestamptz not null default now(),*  
*published_at timestamptz,*  
*unique (name, version)*  
*);*  
  
*-- Document templates (ordered lists of clauses + layout & signers)*  
*create table doc_template (*  
*template_id text primary key, -- tpl\_...*  
*name text not null, -- "Talent SOW v3", "Studio House Rules v2"*  
*version int not null,*  
*city_gate text\[\],*  
*role_gate text\[\],*  
*clauses_ordered jsonb not null, -- e.g., \[{clause_id, version, order}\]*  
*layout_json jsonb not null, -- header/footer/logo, page breaks*  
*signer_roles jsonb not null, -- e.g., \[{role:'buyer'},{role:'talent'},{role:'witness'?}\]*  
*is_active boolean default true,*  
*created_by text not null,*  
*created_at timestamptz not null default now(),*  
*published_at timestamptz,*  
*unique (name, version)*  
*);*  
  
*-- Doc pack (generated for each leg at checkout)*  
*create table doc_pack (*  
*pack_id text primary key, -- dpk\_...*  
*leg_id text not null references booking_leg(leg_id) on delete cascade,*  
*status text not null check (status in ('draft','issued','signed','voided','superseded')),*  
*generator_ver text not null, -- codegen version hash*  
*city text not null,*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now(),*  
*unique (leg_id, status) deferrable initially deferred*  
*);*  
  
*-- Documents within a pack*  
*create table doc_instance (*  
*doc_id text primary key, -- doc\_...*  
*pack_id text not null references doc_pack(pack_id) on delete cascade,*  
*template_id text not null references doc_template(template_id),*  
*template_version int not null,*  
*variables_filled jsonb not null, -- resolved values at generate time*  
*render_pdf_s3 text, -- s3://bucket/key.pdf*  
*render_pdf_sha256 text, -- SHA-256 of PDF bytes*  
*envelope_id text, -- e-sign envelope id*  
*envelope_status text check (envelope_status in ('none','sent','completed','voided','expired')) default 'none',*  
*signer_map_json jsonb not null, -- mapping of signer roles -\> users/emails*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
  
*-- Signer evidence log*  
*create table doc_sign_event (*  
*sign_event_id text primary key, -- dse\_...*  
*doc_id text not null references doc_instance(doc_id) on delete cascade,*  
*actor_role text not null, -- 'buyer','talent','studio_owner','witness'*  
*actor_user_id text,*  
*actor_email text,*  
*event text not null check (event in ('envelope_sent','viewed','signed','declined','voided','expired')),*  
*provider_payload jsonb not null,*  
*created_at timestamptz not null default now()*  
*);*  

**S3 layout**

*s3://docs/prod/packs/{pack_id}/*  
*doc\_{doc_id}\_v1.pdf \# immutable versioned PDF*  
*envelope\_{doc_id}.json \# e-sign provider metadata*  
*hash\_{doc_id}.txt \# SHA-256 digest*  

**Retention & legal hold**

- Bucket policy applies **7‑year retention**; legal hold flag per doc if Support/Legal initiates a hold.

## **1.5.C Clause library & variables**

**Clause authoring**

- Authored in **Markdown** with limited components: headings, lists, clause refs, and **variable placeholders** in *{{snake_case}}*.
- Variables must be declared in *variables_json* with type, description, and example. Supported types: *string*, *int*, *money_cents*, *datetime*, *date*, *duration*, *enum{…}*, *address*.

**Examples**

- SOW “Base Terms” requires: *{{service_date}}*, *{{start_time}}*, *{{end_time}}*, *{{location_address}}*, *{{deliverables_summary}}*, *{{total_price}}*, *{{taxes}}*, *{{cancellation_policy_summary}}*.
- Model Release (Adult) requires: *{{model_legal_name}}*, *{{model_dob}}* (age verification gate), *{{usage_scope}}*, *{{territory}}*, *{{duration}}*, *{{compensation_summary}}*.
- Studio Rules requires: *{{studio_name}}*, *{{safety_rules}}*, *{{deposit_amount}}*, *{{damage_policy}}*.

**City & role gates**

- Clauses and templates can be constrained by **city** (local rules) and **role** (e.g., Model Releases apply only to Talent legs). City gates align to your feature‑flag model.

**Versioning**

- Clauses are immutable once published; edits create a **new version**. Templates reference clause **name + version** explicitly to guarantee reproducible renders.

## **1.5.D Template composition**

**Templates at launch**

- **Talent SOW (v1)** → ordered clauses: Base Terms, Responsibilities, IP & Licensing, Payment & Escrow, Cancellation, Safety & Conduct, Limitation of Liability, Governing Law.
- **Model Release (Adult, v1)** → fields enforce 18+ check; explicitly **disallows explicit content** on public surfaces; usage scope limited per blueprint positioning.
- **Studio House Rules (v1)** → capacity, amenity rules, deposit, damages, cleaning fees, overtime procedure.

**Signer roles**

- **Talent SOW:** Buyer & Seller (talent).
- **Model Release:** Model (may be same as talent or separate field), Photographer (counter‑sign). *No minors allowed at MVP.*
- **Studio House Rules:** Buyer (responsible party) & Studio Owner/Manager.

**Layout**

- Header: brand, booking ref (*lbg_id* / *leg_id*), doc id, template & clause versions.
- Footer: page X/Y, hash fingerprint, generated timestamp UTC.

## **1.5.E Pack assembly (Docs‑Before‑Pay)**

**When generated:**

- During checkout after *startCheckout*, **before** payment.
- For each **leg**, resolve which **template(s)** apply via city/role gates and pack them.

**Resolver inputs:**

- Leg times, location, price lines, tax quote, deposit policy (for studios), buyer/seller identities, role fields, SOW deliverables (from Brief/Shot list summary if present).

**Algorithm (high‑level):**

490. Determine applicable templates (by *leg.type*, city, role).
491. Validate all required variables can be bound; if not, return *DOC_VARS_MISSING* with a list.
492. Fill variables (see mapping in §1.5.F).
493. Render Markdown → PDF (headless Chromium or a template renderer).
494. Create envelopes with the e‑sign provider; map **signer roles → emails**; send.
495. Update *doc_pack* → *issued* and *doc_instance.envelope_status='sent'*.
496. Block payment step until **every envelope** in both relevant packs is *completed*.

**Re‑issue rules:**

- If *start_at/end_at*, *location*, *deliverables*, *deposit_policy*, or **counterparty** changes → invalidate pack (*superseded*) and re‑generate (fresh template version selection).
- All **previous** PDFs remain immutable evidence; receipts reference the **active** pack.

## **1.5.F Variable binding (examples)**

|  |  |
|----|----|
| **Variable** | **Source** |
| *service_date*, *start_time*, *end_time* | *booking_leg.start_at/end_at* (UTC → local tz of city gate) |
| *location_address* | *studio.address_json* if studio leg, else buyer‑provided shoot location |
| *buyer_legal_name*, *buyer_email* | Account profile / checkout identity |
| *seller_legal_name* | Talent SP owner legal name |
| *deliverables_summary* | From Brief/Shot list (if provided) + chosen packages |
| *total_price*, *taxes* | From leg price snapshot (*total_cents*, *tax_cents*) |
| *cancellation_policy_summary* | Derived from *policy_json* bands |
| *deposit_amount* | *deposit_policy.auth_cents* (studio leg) |
| *usage_scope*, *territory*, *duration* | Defaults from template, can be narrowed by seller; never wider than template allows |
| *model_dob* | From IDV provider (age 18+ required for Model Release at MVP) |

Validation runs both in the **API** and during **render**. Any failure returns explicit error codes.

## **1.5.G E‑sign adapter (Dropbox Sign / DocuSign)**

**Adapter contract**

- *create_envelope(doc_id, signer_map, pdf_s3)* → returns *envelope_id*, signer URLs (embedded) or email invites.
- *void_envelope(envelope_id, reason)* (on re‑issue).
- Webhooks: *envelope.sent*, *recipient.viewed*, *recipient.signed*, *envelope.completed*, *envelope.declined*, *envelope.voided*, *envelope.expired*.

**Security & idempotency**

- HMAC‑verified webhooks; store *provider_event_id*; dedupe.
- Signer links time‑limited; deep links route through our app to enforce auth and logging.

**Signer experience**

- In‑app embedded signing preferred; email fallback.
- Save/resume; clear error for expired/voided.

**Failure handling**

- *ENVELOPE_EMAIL_BOUNCE* → allow email change & re‑send (admin or user).
- *ENVELOPE_EXPIRED* → re‑issue pack (new doc version).

## **1.5.H Hashing & immutability**

- After rendering, compute **SHA‑256** of PDF bytes; store in *doc_instance.render_pdf_sha256*.
- Include the hash (shortened) in the PDF footer.
- All envelopes completed → verify provider’s returned PDF by recomputing a **post‑sign hash**; store both **pre‑sign** and **post‑sign** hashes with a small allowed delta (some providers stamp signatures).
- **Receipts** reference *doc_id* and *post_sign_hash*.
- **Evidence export** pulls PDFs and a CSV/JSON of envelope metadata + sign events.

## **1.5.I Access control & privacy**

- Doc packs visible to **buyer**, **seller**, and **studio owner** (for studio packs), plus **admins** per RBAC.
- PII fields are masked in UI except where legally required.
- Downloads are signed URLs; access logged (actor, time, reason for admin).
- **Legal hold** blocks deletions and re‑issues until released.

## **1.5.J Integrations with §§1.3–1.4**

- **Checkout (§1.3):** *createDocPack* and *markDocSigned* mutations; payment step hard‑blocked until all envelopes are *completed*.
- **Messaging (§1.4):** Doc status appears in Project Panel “Docs & e‑sign” tab; **action card** prompts sign; completion posts a system message with doc ids and hashes.

## **1.5.K Notifications & templates**

- Triggers: envelope sent, signer reminder (24h cadence), nearing expiry, completed.
- Channels: email (primary), push (secondary), SMS (reminders only, no links to PII).
- Templates parameterized by *{role}*, *{doc_name}*, *{deadline}*, *{thread_url}*; live in the Comms adapter.

## **1.5.L Admin console (Legal, Support, City Ops)**

- **Clause Library:** create/edit/publish clause versions; preview with variable fills; city/role gates; diff viewer.
- **Templates:** compose clauses, manage signer roles, publish; A/B testing slot (flag‑gated).
- **Packs:** search by *pack_id*, *leg_id*, *lbg_id*, *status*; void/re‑issue; change signer email; resend invites.
- **Audits:** immutable logs of every change and envelope event; export function for legal.
- **Dual approval:** Required to publish templates or clauses that affect **money/safety/legal**.

## **1.5.M Telemetry & lineage**

- doc.pack.create\|issued\|signed\|voided\|superseded
- doc.envelope.sent\|viewed\|signed\|completed\|declined\|expired
- *doc.pdf.rendered*, *doc.pdf.hash_verified*
- doc.admin.publish_clause\|publish_template\|void_envelope
- Correlate with *leg_id*, *lbg_id*, *charge_id* for end‑to‑end traceability.

## **1.5.N Error taxonomy**

- *DOC_VARS_MISSING* — required variables absent or invalid.
- *DOC_TEMPLATE_GATED* — template not available for city/role.
- *DOC_SIGNER_MISSING* — signer role not mapped to a valid email/user.
- *DOC_RENDER_FAIL* — renderer error (retry with backoff).
- *ENVELOPE_CREATE_FAIL* — provider API error.
- *ENVELOPE_HMAC_INVALID* — webhook rejected.
- *DOC_REISSUE_REQUIRED* — leg change invalidated pack; re‑issue needed.
- *DOC_LEGAL_HOLD* — action blocked until hold removed.

All error payloads include *code*, *message*, *hint*, *corrId*.

## **1.5.O Performance & cost**

- Rendering happens in Lambda with **concurrency caps**; fall back to a headless render service if pages \> threshold.
- E‑sign costs are **per envelope**; we minimize packs to one Talent pack and one Studio pack at MVP.
- S3 + lifecycle rules keep storage costs low; PDFs are compacted (fonts embedded once) and gzipped for transport.

## **1.5.P Test plan (CI + sandbox)**

**Library & templates**

543. Create/publish clause v2; ensure v1 remains immutable; template references correct clause versions.
544. City/role gates: Houston‑only template isn’t applied in non‑gated city.
545. Variables: missing var → *DOC_VARS_MISSING* with exact field list.

**Pack assembly & signing**  
4) Generate packs for LBG (Talent + Studio); envelopes created; Doc‑Before‑Pay enforced.  
5) Signer email bounce → re‑send after email change.  
6) Envelope expired → re‑issue pack; prior PDFs retained as superseded.

**Hashing & evidence**  
7) Render & store PDF; verify pre‑sign vs post‑sign hash strategy; receipts reference post‑sign hash.  
8) Evidence export contains PDFs, metadata, and sign events.

**Re‑issue triggers**  
9) Reschedule booking time → pack invalidated; re‑generated; prior pack voided.  
10) Change deposit or deliverables → pack invalidated; new pack required.

**Admin**  
11) Clause edit requires dual approval; diff viewer shows exact changes; publish logs audit.  
12) Void envelope audit trail present; legal hold blocks changes.

**Integration**  
13) Messaging panel shows live doc status; action cards prompt signing; completion system message posted.  
14) Checkout blocks payment until all envelopes completed; then proceeds to payment intent confirm.

## **1.5.Q Work packages (Cursor 4‑agent lanes)**

- **Agent A — Docs CMS & Templates**  
  WP‑DOCS‑01: SQL for *doc_clause*, *doc_template*, *doc_pack*, *doc_instance*, *doc_sign_event*.  
  WP‑DOCS‑02: Clause & Template authoring UI in Admin (create/edit/publish, preview with variable binding).  
  WP‑DOCS‑03: Variable resolver library (maps from *leg*/*LBG*/profile/brief to variables).
- **Agent B — Rendering & Storage**  
  WP‑REND‑01: Markdown→PDF renderer (headless) with layout json; S3 write; SHA‑256 hash.  
  WP‑REND‑02: Evidence export builder (ZIP + JSON manifest).
- **Agent C — E‑sign Adapter**  
  WP‑SIGN‑01: Envelope create/void; signer link flows; webhooks with HMAC verify; status mapper.  
  WP‑SIGN‑02: Retry and error handling; email change + re‑send; expiration handling.
- **Agent D — Product Integration**  
  WP‑CHK‑DOCS‑01: Checkout gating (Docs‑Before‑Pay) + GraphQL mutations (*createDocPack*, *markDocSigned*).  
  WP‑MSG‑DOCS‑01: Messaging Project Panel “Docs & e‑sign” tab + action cards.  
  WP‑QA‑DOCS‑01: Full test matrix above in CI & sandbox.

## **1.5.R Acceptance criteria — mark §1.5 FINAL only when ALL true**

550. Clause & Template library supports versioning, city/role gates, previews, and dual approvals for publish.
551. Pack assembly resolves variables, renders PDFs, creates envelopes, and enforces Docs‑Before‑Pay across both legs in an LBG.
552. Completed envelopes change pack status to *signed*; payment capture proceeds; receipts reference doc IDs and **post‑sign hashes**.
553. Re‑issue logic invalidates packs when scope/time/location/party/deposit changes; prior PDFs retained and auditable.
554. Hashing verified; S3 storage and retention policies active; legal hold works.
555. Messaging displays doc status and action prompts; Admin can search/void/resend with full audits.
556. Telemetry complete; evidence export works; error taxonomy produced for all failure modes.
557. Costs within budget; renderer concurrency capped; e‑sign envelopes within allowance.

# **§1.6 — Trust, Verification & Background Checks**

*(ID Verification · Age Gate (18+) · Trusted Pro (BG) · Social Verification · Risk Signals · Badges & Gating · Admin & Audits · Privacy)*

**Purpose.** Design and implement the full trust layer: identity verification (IDV) for 18+ and Instant Book eligibility; optional FCRA-compliant background checks for the **Trusted Pro** badge; verified-social signals; risk scoring & throttles; and the badges/gates that flow into search, booking, messaging, and payouts. This section includes data models, adapters, APIs, admin tools, privacy and retention, telemetry, error taxonomy, tests, SLOs, and cost controls. We will not move on until §1.6 meets your 99.9% bar.

## **1.6.A Canon & invariants**

558. **IDV is prerequisite** for: (a) **Instant Book**, (b) **18+ media gating** (e.g., Fan-sub role visibility), and (c) **elevated trust ranking** in search.
559. **BG checks (FCRA)** are **optional**; passing BG grants the **Trusted Pro** badge and additional ranking/eligibility boosts.
560. **Badges are scoped to the Account** (user), but **search boosts and gates are applied per Service Profile**.
561. **No raw PII is stored** from providers; we store tokens/refs and statuses only.
562. **Adverse action** workflows (for BG) are handled via standardized templates and cooling-off periods.
563. **All trust decisions are auditable**; Admin actions require reasons; sensitive overrides use two-person approval.

## **1.6.B Data model (Aurora + DynamoDB)**

*-- Identity Verification (IDV) status & metadata*  
*create table idv_status (*  
*idv_id text primary key, -- idv\_...*  
*user_id text not null, -- usr\_...*  
*provider text not null, -- 'persona' or 'stripe_identity' etc.*  
*provider_ref text not null, -- external session/check id*  
*status text not null check (status in ('pending','passed','failed','expired','requires_review')),*  
*checks_json jsonb not null, -- document, selfie, liveness, match scores (non-PII summaries)*  
*age_verified boolean not null default false,*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now(),*  
*unique (user_id, provider_ref)*  
*);*  
  
*-- Background Check (FCRA) status*  
*create table bg_status (*  
*bg_id text primary key, -- bg\_...*  
*user_id text not null,*  
*provider text not null, -- 'checkr' etc.*  
*provider_ref text not null,*  
*status text not null check (status in ('invited','in_progress','clear','consider','suspended','disputed','withdrawn','expired')),*  
*package text not null, -- e.g. 'basic_us'*  
*adjudication text, -- provider adjudication summary (non-PII)*  
*report_url text, -- provider-hosted report link (if allowed)*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now(),*  
*unique (user_id, provider_ref)*  
*);*  
  
*-- Social verification (per platform)*  
*create table social_verification (*  
*soc_id text primary key, -- soc\_...*  
*user_id text not null,*  
*platform text not null check (platform in ('instagram','tiktok','youtube','x')),*  
*handle text not null,*  
*verified boolean not null default false,*  
*snapshot_json jsonb, -- follower counts, ER, etc. (non-secret)*  
*last_checked_at timestamptz*  
*);*  
  
*-- Trust badges (derived)*  
*create table trust_badge (*  
*badge_id text primary key, -- tbg\_...*  
*user_id text not null,*  
*kind text not null check (kind in ('id_verified','trusted_pro','social_verified')),*  
*source_id text, -- idv_id, bg_id, or soc_id*  
*issued_at timestamptz not null default now(),*  
*expires_at timestamptz -- optional expiry for recert*  
*);*  
  
*-- Risk signals snapshots*  
*create table trust_risk_signal (*  
*signal_id text primary key, -- rsk\_...*  
*user_id text not null,*  
*window daterange not null, -- \[start,end)*  
*disputes_opened int not null default 0,*  
*refunds_asked int not null default 0,*  
*cancellations int not null default 0,*  
*late_delivery int not null default 0,*  
*charge_failures int not null default 0,*  
*bad_clicks int not null default 0,*  
*flags_json jsonb not null default '{}'::jsonb,*  
*score int not null default 0, -- aggregate score (0-100; lower is riskier)*  
*computed_at timestamptz not null default now()*  
*);*  

**DynamoDB (hot path cache):** a small *trust_cache* item per user (IDV passed?, Trusted Pro?, social verified?, risk score) to avoid DB round trips on search and booking.

## **1.6.C Adapters (IDV, BG, Social) — contracts**

**Common adapter shape (idempotent):**

- *start(user_id, params)* → *{ provider_ref, redirect_url/embedded_session }*
- *status(provider_ref)* → status enum + minimal signals (no raw PII)
- *webhook(event)* → HMAC verified; dedupe by provider_event_id
- Emits normalized events: *idv.started\|passed\|failed\|expired*, *bg.invited\|clear\|consider\|disputed\|expired*, *social.verified\|revoked*, all correlated by *user_id*.

**IDV provider options** (choose one; both fit the contract):

- **Persona** or **Stripe Identity**. We default to **Persona** for breadth; Stripe Identity is acceptable if cost/licensing or Stripe consolidation is preferred.

**BG provider**:

- **Checkr** with FCRA flow; alternative vendors possible with same contract.

**Social**:

- **Instagram Graph / TikTok / YouTube / X** OAuth; nightly snapshot; **verified** when OAuth proof valid and platform marks the account verified (or our threshold met).

## **1.6.D Badge logic, gates & expiration**

- **ID Verified (badge)** → issued when IDV status transitions to *passed* and *age_verified = true*.
- **Trusted Pro (badge)** → issued when BG status == *clear* with no pending adverse action.
- **Social Verified (badge)** → issued when OAuth verified AND snapshot passes thresholds (e.g., follower minimum or platform verification).

**Expiration / recert (configurable):**

- IDV: re-verify after 24 months (or upon provider signal).
- BG: re-check annually or upon key incidents (dispute rate spike).
- Social: nightly refresh; badge revoked if OAuth disconnects or signals stale \> N days.

**Gates driven by badges:**

- **Instant Book** requires **ID Verified** (+ optionally minimum reputation).
- **Fan-sub role visibility** requires **age_verified** and Safe-Mode OFF by adult viewers.
- **Search boosts**: ID Verified \> Social Verified \> Trusted Pro (configurable weights); Trusted Pro may also unlock promotions eligibility.

## **1.6.E GraphQL API (user-facing flows)**

*type IdvSession { provider: String!, url: String, clientToken: String }*  
*type BgInvitation { provider: String!, url: String }*  
  
*type TrustStatus {*  
*idVerified: Boolean!*  
*ageVerified: Boolean!*  
*trustedPro: Boolean!*  
*socialVerified: Boolean!*  
*riskScore: Int!*  
*lastIdvAt: AWSDateTime*  
*lastBgAt: AWSDateTime*  
*}*  
  
*type Query {*  
*trustStatus: TrustStatus!*  
*socialConnections: \[SocialConnection!\]!*  
*}*  
  
*type Mutation {*  
*startIdv: IdvSession! \# create new provider session*  
*refreshIdvStatus: TrustStatus! \# polling fallback*  
*startBackgroundCheck: BgInvitation! \# sends FCRA consent flow*  
*disconnectSocial(platform: SocialPlatform!): Boolean!*  
*connectSocial(platform: SocialPlatform!): SocialConnection! \# returns OAuth URL*  
*}*  

**Server rules**

- *startBackgroundCheck* prompts user with **FCRA consents** and a clear explanation; check is optional; badge used as a positive signal only.
- *startIdv* requires logged-in user; if an active IDV *pending*, returns that session to avoid duplicates.

## **1.6.F Integration points**

- **Search (§1.2)**: include *verification.id*, *trustedPro*, *socialVerified* in index docs; apply **verified-only** filter when toggled; ranking boosts as configured.

- **Booking & Checkout (§1.3)**:

  - **Instant Book** path checks *idVerified=true* before allowing.
  - For Fan-sub or 18+ toggles, ensure **age_verified=true** before exposing surfaces.

- **Messaging (§1.4)**: show badges on thread headers; anticircumvention policies apply regardless of badges.

- **Admin**: trust tiles show IDV/BG status; overrides require reasons and are flagged for later audit.

## **1.6.G Risk signals & throttles**

**Signals (rolled up daily/weekly):**

- Disputes opened, refunds requested, cancellations late, late delivery ratio, payment failures, invalid-click attributions (as buyer/seller), moderation flags.

**Score (0–100):**  
Weighted sum with decay—recent events weigh more. Thresholds:

- **Watch (≤60)** → warnings; **limit** high-risk features (promotions, instant payouts).
- **Action (≤40)** → suspend **Instant Book** and **Promotions**; manual review.
- **Critical (≤25)** → pause payouts pending review; city-gated exposure reduced.

**Throttles:**

- Limit number of open proposals, outgoing messages per minute, or daily instant payout requests when below thresholds.

## **1.6.H Admin consoles & workflows**

**Trust Dashboard**

- Global view of IDV/BG states, expiring badges, risk heatmap, and incident queues.

**IDV review**

- Queue for *requires_review* statuses; approve/deny with reason; can trigger re-run.

**BG adverse action**

- Pre-adverse and adverse templates (email); waiting period timers; record of user acknowledgment; **no details** beyond provider’s permitted disclosure. All steps audited.

**Overrides**

- Temporarily grant/revoke badges (two-person approval); set review flags; lock user for legal holds.

**Exports**

- CSV of trust states; incident logs; provider reconciliation reports.

## **1.6.I Webhooks → normalized events**

- idv.started\|passed\|failed\|expired
- bg.invited\|in_progress\|clear\|consider\|suspended\|disputed\|expired
- social.connected\|verified\|revoked
- *risk.score.updated*  
  Each event includes *user_id*, provider_ref, and relevant timestamps.

**Idempotency:** dedupe by *(provider, provider_event_id)*; keep last processed id per provider.

## **1.6.J Privacy & retention**

- **Store only** provider refs/state and non-PII summaries (age-verified boolean, adjudication summaries).
- No images/scans of IDs at rest in our DB/S3.
- Retention windows: IDV and BG statuses kept for 7 years or as required by policy; social snapshots roll daily with 30–90 day retention.

**Access control:**

- Trust data visible to user (their statuses) and Admin roles only; not exposed to other users.
- Audit logs for every access by Admin with reason.

## **1.6.K Error taxonomy (client-safe)**

- *IDV_PROVIDER_UNAVAILABLE* — retry or switch later.
- *IDV_FAILED* — provide appeal/retry path.
- *BG_CONSENT_REQUIRED* — user must accept consents.
- *BG_IN_PROGRESS* — already running; point to status view.
- *SOCIAL_OAUTH_FAILED* — include retry link.
- *TRUST_OVERRIDE_FORBIDDEN* — admin lacked permission/two-person approval.

## **1.6.L Telemetry & SLOs**

**SLOs**

- IDV completion success rate (init→pass): ≥ **85%** MVP.
- BG turnaround (invite→clear): median **\<48h**; 90th **\<5d**.
- Social refresh lag: **\<24h**.
- Risk recompute latency: **\<15min** after new events.

**Dashboards**

- Funnel: startIdv → passed; startBg → clear; badge distributions; watch/action/critical counts; Instant Book enablement rate.

## **1.6.M Cost controls**

- IDV and BG are pay-per-use: expose as a **benefit** (badges, search boost, IB access) to motivate self-selection.
- Batch social refresh nightly; rate-limit on API quotas; cache snapshots.
- Background rechecks (recerts) scheduled by cohort to smooth spend.

## **1.6.N Test plan (CI + sandbox)**

619. **IDV pass** → badge issued, *age_verified=true*, Instant Book enabled; search boost visible.
620. **IDV fail/expired** → badge removed; IB disabled; 18+ surfaces gated.
621. **BG clear** → Trusted Pro badge issued; search boost; promotions eligibility allowed.
622. **BG consider** → no badge; Admin adverse-action flow required; user notified with correct template.
623. **Social verified** → badge appears; snapshot in index; revoke removes badge.
624. **Risk score thresholds** → throttles engage correctly; admin override works with dual approval.
625. **Privacy** → no PII in our storage; access logs for Admin views; legal hold respected.
626. **Webhooks idempotent** → duplicate events do not double-apply.
627. **SLO monitors** → IDV funnel and BG turnaround within targets on synthetic load.

## **1.6.O Work packages (Cursor agents)**

- **Agent C — Trust Integrations**  
  WP-TRUST-IDV-01: Provider adapter (Persona or Stripe Identity) + webhooks + HMAC + normalized events.  
  WP-TRUST-BG-01: FCRA BG adapter (Checkr) + invite/status + adverse-action scaffolding.  
  WP-TRUST-SOC-01: OAuth connections for IG/TT/YT/X; nightly snapshot job.
- **Agent B — Domain/API**  
  WP-API-TRUST-01: GraphQL resolvers for *startIdv*, *startBackgroundCheck*, *trustStatus*; trust cache.  
  WP-RISK-01: Risk rollups & score compute jobs; throttles integration.
- **Agent A — Web**  
  WP-WEB-TRUST-01: Trust center UI (badges, flows, status); IDV/BG wizards; social connect pages.  
  WP-WEB-IB-01: Wire Instant Book gate; age gate for Fan-sub surfaces.
- **Agent D — Admin & QA**  
  WP-ADM-TRUST-01: Trust dashboard, IDV review queue, BG adverse-action tools, overrides with dual approval.  
  WP-QA-TRUST-01: Full test matrix above; webhooks idempotency; privacy audits.

## **1.6.P Acceptance criteria (mark §1.6 FINAL only when ALL true)**

632. IDV flow works end-to-end; badge & age gate applied; Instant Book correctly gated.
633. BG flow (optional) works with FCRA consents, statuses, adverse-action templates, and audit trails; Trusted Pro badge granted on **clear**.
634. Social verification connects/revokes; nightly snapshot reflected in search and badges.
635. Risk score updates from domain events and enforces throttles at thresholds; overrides require dual approval.
636. Admin consoles cover review, overrides, exports, and adverse-action steps with immutable audits.
637. Privacy posture holds (no raw PII stored; access logs); retention policies configured.
638. Telemetry/SLO dashboards for funnels and turnaround; all targets met under synthetic load.
639. Costs remain within budget; batch refreshes and cohort recerts smoothed.

# **§1.7 — Promotions & Advertising**

*(eligibility · placements · targeting · blending & fairness · budgets & pacing · click validation · billing & credits · admin tools · telemetry · error taxonomy · tests · cost controls)*

**Purpose.** Provide a complete, auditable ad system that allows eligible sellers to promote their **Service Profiles** (people) and, later, **Studios** (places) within search/browse—**without** breaking filters or user trust. Promotions must be transparent (“Promoted”), capped in density, city‑gated, safe‑mode compliant, verifiable against fraud, and cost‑controlled.

We will not move to §1.8 until §1.7 satisfies your 99.9% bar.

## **1.7.A Canon & invariants**

640. **No filter bypass.** Promoted results must **match the user’s filters** (role, city, price bands, availability, Safe‑Mode) and respect city gates.
641. **Transparency by design.** Promoted units are marked (“Promoted”/“Featured”) and visually distinct.
642. **Density caps.** Fixed, configurable caps (e.g., ≤2 promoted in top‑20; ≤1 above the fold).
643. **Eligibility gates.** Sellers must be **ID Verified**, have minimum **completeness score**, and be policy‑clean. Studios must be verified to advertise.
644. **Pay only for valid clicks.** Deduplicate & filter suspicious clicks; issue automatic make‑good credits.
645. **Budget safety.** Daily & total budgets; pacing to avoid early day burn; automatic pause when funds low or policy violated.
646. **Auditable.** Every impression/click/charge/credit is traceable, immutable, and reconcilable to Stripe.

## **1.7.B Surfaces & formats (MVP)**

- **Role search results** (people): boostable cards (same card template with a “Promoted” chip).
- **Studio search results** (places): enabled later behind a flag—same transparency rules.
- **No feed/native content** placements at MVP; keep to search and browse only.

**Formats (MVP):**

- **Featured**: occupies specific reserved slots (e.g., positions 2 and 8) when eligible; rotates fairly among eligible campaigns.
- **Boosted**: appears interleaved at set intervals after position *P* (e.g., after every 5 organic results).

Both formats **never override filters** and **never** show if the candidate doesn’t qualify for that query.

## **1.7.C Eligibility & safety gates**

- **Required:** ID Verified, profile completeness ≥ threshold, policy‑clean (recent dispute/late delivery thresholds not exceeded), city allowlisted, Safe‑Mode‑compatible thumbnails.
- **Disallowed:** Under review by Trust & Safety, unsafe NSFW band for public surfaces, negative balance or unpaid ad bills, flagged fraud.
- **Studios:** must be verified studio with house rules published; deposit policy configured.

Violations pause campaigns automatically; Admin may override (two‑person approval).

## **1.7.D Data model (Aurora + DynamoDB + S3)**

### **D.1 Core SQL tables**

*-- Advertiser (seller) settings*  
*create table promo_advertiser (*  
*advertiser_id text primary key, -- padv\_...*  
*user_id text not null, -- usr\_...*  
*default_payment_id text, -- Stripe customer/payment method (for postpaid or top-ups)*  
*status text not null check (status in ('active','paused','suspended')),*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
  
*-- Campaigns (one per role/SP or studio)*  
*create table promo_campaign (*  
*campaign_id text primary key, -- pcmp\_...*  
*advertiser_id text not null references promo_advertiser(advertiser_id),*  
*target_entity_type text not null check (target_entity_type in ('service_profile','studio')),*  
*target_entity_id text not null, -- srv\_\* or std\_\**  
*name text not null,*  
*surface text not null check (surface in ('people_search','studio_search')),*  
*format text not null check (format in ('featured','boosted')),*  
*city_targets text\[\] not null, -- list of city codes*  
*keyword_targets text\[\] default '{}', -- optional*  
*status text not null check (status in ('draft','active','paused','ended','suspended')),*  
*start_date date not null,*  
*end_date date,*  
*cpc_cents int not null, -- flat CPC at MVP*  
*daily_budget_cents int not null,*  
*total_budget_cents int, -- optional cap*  
*pacing_mode text not null check (pacing_mode in ('even','accelerated')) default 'even',*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
  
*-- Budget ledger (prepaid credits + spend)*  
*create table promo_budget_ledger (*  
*entry_id text primary key, -- pble\_...*  
*campaign_id text not null references promo_campaign(campaign_id) on delete cascade,*  
*kind text not null check (kind in ('topup','spend','credit','adjustment')),*  
*amount_cents int not null,*  
*processor text, -- 'stripe'*  
*processor_ref text, -- charge id, invoice id*  
*reason text,*  
*created_at timestamptz not null default now()*  
*);*  
  
*-- Impression & click logs (immutable, append-only)*  
*create table promo_event (*  
*event_id text primary key, -- pevt\_...*  
*campaign_id text not null,*  
*impression_id text not null, -- corr id across imp/click*  
*type text not null check (type in ('impression','click','invalid_click')),*  
*role text, -- role tab if surface=people*  
*city text not null,*  
*query_hash text not null, -- normalized query signature*  
*user_id text, -- viewer user (null if anon hashed)*  
*anon_fp_hash text, -- fingerprint hash for anon viewers*  
*ip_hash text not null,*  
*ua_hash text not null,*  
*ts timestamptz not null default now(),*  
*extra_json jsonb default '{}'::jsonb*  
*);*  
  
*-- Pricing & caps by city/role (admin configurable)*  
*create table promo_policy (*  
*policy_id text primary key, -- ppol\_...*  
*surface text not null,*  
*role text, -- nullable for studios*  
*city text not null,*  
*cpc_floor_cents int not null,*  
*max_density_top20 int not null, -- e.g., 2*  
*max_above_fold int not null, -- e.g., 1*  
*updated_at timestamptz not null default now()*  
*);*  

### **D.2 DynamoDB (hot path)**

- ***promo_active_by_city***: keyed by *(surface#city#role)* → list of active campaign ids, pacing pointers, and remaining daily budget.
- ***promo_cursor_cache***: per search response for cursor pagination (to ensure stable ad rotation within a session).
- ***promo_click_dedupe***: short‑TTL cache of recent impression/click tuples to drop duplicates.

S3 optionally stores compacted hourly parquet of promo events for analytics (Bronze→Silver→Gold ETL).

## **1.7.E Targeting & matching**

**Mandatory:** *surface*, *city*, and (for people) *role*.  
**Optional:** keywords (prefix/synonyms), price bands, availability day hints.

**Matching algorithm (MVP):**

658. Start with campaigns active in *surface* + *city* (+ *role* if people).
659. Filter out those failing **eligibility** (trust, policy, completeness, Safe‑Mode).
660. Filter by **query filters** (price range, availability day if required, etc.).
661. Apply **budget availability** (daily balance left) & **pacing** (even distribution: remaining_budget / remaining_slots).
662. Produce a ranked **candidate set** ordered by: compliance → campaign freshness → spend vs target pacing (under‑pacing gets slight priority) → random tiebreaker for fairness.
663. Blend into organic results per §1.7.F.

## **1.7.F Blending & fairness**

**Density rules (configurable via** ***promo_policy*****):**

- At most *max_density_top20* promoted results in top‑20.
- At most *max_above_fold* promoted slots within the first screen.
- Never two promoted results back‑to‑back unless inventory is extremely low (flag‑gated).

**Featured slots**: reserve fixed positions (e.g., \#2, \#8). If fewer eligible than slots, leave slot organic.

**Boosted slots**: insert after every *N* organic results starting after position *P* (e.g., start at \#6, then every 5 cards). Skip if no eligible candidates.

**Diversity & rotation:**

- Per owner: at most one promoted result **from the same owner** in the top‑N to avoid crowd‑out.
- Rotation window ensures that if a campaign lost a slot in this query earlier, it gets priority next time (pacing).
- City‑wide fairness health metric monitors share of voice (% impressions) by owner.

## **1.7.G Click validation & fraud defenses**

**Instrumentation:**

- Every impression returns a unique ***impression_id*** embedded in the card.
- Clicks POST back with *{ impression_id }* + signed token; server enriches with *ip_hash*, *ua_hash*, *anon_fp_hash*, *user_id*.

**Dedup & windows:**

- Deduplicate multiple clicks from the **same session+impression** within **T seconds** (e.g., 45s).
- Only bill the **first valid click** per impression.

**Invalid click detection (near‑real‑time):**

- Heuristics: excessive frequency per IP block/FP, impossible geos vs city, bot UA, scroll‑less clicks, zero‑dwell.
- Scores and thresholds → if invalid: log *invalid_click* and **do not bill**.
- If billed earlier and later flagged in batch re‑processing → issue **make‑good credit** (ledger *kind='credit'*).

**Abuse control:**

- Rate‑limit by IP block/FP; hard ban patterns into WAF; suspicious campaigns auto‑pause with alert to Admin.

## **1.7.H Budgets, pacing & pausing**

- **Budgets**: *daily_budget_cents* and optional *total_budget_cents*.

- **Pacing**:

  - *Even*: estimate eligible query volume and drip impressions/clicks over the day; slow or pause when spend exceeds expected pace.
  - *Accelerated*: allow faster delivery while respecting caps and eligibility.

- **Auto‑pause** when: daily budget exhausted, total budget reached, policy violation, or Trust score drops below threshold.

- **Resume rules**: manual or next day reset; spending resumes when budget refills or policy clears.

## **1.7.I Billing & credits (cost‑conscious MVP)**

**MVP billing model: Prepaid credits (lowest complexity)**

- Advertiser tops up credits via **Stripe** (platform customer).
- Spend ledger debits for each **valid click** at campaign’s *cpc_cents*.
- When balance low (\< threshold), show in‑product **“low balance”** banner; auto‑recharge (optional).
- **Make‑good credits** issued on invalid‑click findings as positive ledger entries.
- Monthly statements available (CSV/PDF) with impressions, clicks, CPC, charges, credits, net spend.

**Phase‑up (optional): Stripe Billing metered**

- Create a metered product *promoted_click*; report usage daily; Stripe invoices monthly (postpaid).
- Keep **internal ledger** regardless for exact traceability and fraud credits.

**Tax on ad fees**

- If applicable by jurisdiction, apply sales tax to **ad purchases/top‑ups** (separate from marketplace taxes). Use the same tax adapter.

**Accounting separation**

- Ad revenue is **non‑GMV**; in analytics, keep separate revenue streams and costs to avoid inflating marketplace take.

## **1.7.J GraphQL API (seller‑facing & admin)**

*\# Seller APIs*  
*type Campaign {*  
*campaignId: ID!*  
*name: String!*  
*status: String!*  
*surface: String!*  
*format: String!*  
*targetEntityId: ID!*  
*cities: \[String!\]!*  
*cpcCents: Int!*  
*dailyBudgetCents: Int!*  
*totalBudgetCents: Int*  
*spendTodayCents: Int!*  
*spendTotalCents: Int!*  
*}*  
  
*type CampaignStats {*  
*campaignId: ID!*  
*date: AWSDate!*  
*impressions: Int!*  
*clicks: Int!*  
*ctr: Float!*  
*avgCpcCents: Int!*  
*invalidClicks: Int!*  
*creditsCents: Int!*  
*}*  
  
*type Query {*  
*myCampaigns: \[Campaign!\]!*  
*campaignStats(campaignId: ID!, from: AWSDate!, to: AWSDate!): \[CampaignStats!\]!*  
*adBalance: Int! \# current prepaid credits*  
*}*  
  
*input CampaignInput {*  
*targetEntityId: ID!*  
*surface: String!*  
*format: String!*  
*cities: \[String!\]!*  
*cpcCents: Int!*  
*dailyBudgetCents: Int!*  
*totalBudgetCents: Int*  
*keywords: \[String!\]*  
*startDate: AWSDate!*  
*endDate: AWSDate*  
*}*  
  
*type Mutation {*  
*createCampaign(input: CampaignInput!): Campaign!*  
*updateCampaign(campaignId: ID!, input: CampaignInput!): Campaign!*  
*pauseCampaign(campaignId: ID!): Campaign!*  
*resumeCampaign(campaignId: ID!): Campaign!*  
*topUpAdCredits(amountCents: Int!): Boolean!*  
*}*  
  
*\# Admin APIs*  
*type Mutation {*  
*setPromoPolicy(surface: String!, role: String, city: String!, cpcFloorCents: Int!, maxDensityTop20: Int!, maxAboveFold: Int!): Boolean!*  
*suspendCampaign(campaignId: ID!, reason: String!): Boolean!*  
*issuePromoCredit(campaignId: ID!, amountCents: Int!, reason: String!): Boolean!*  
*}*  

**Server guards**

- *createCampaign* validates eligibility, floors (*cpc_cents \>= cpc_floor*), and city allowlists; seeds pacing counters.
- *topUpAdCredits* creates a Stripe PaymentIntent and writes a *topup* ledger entry on success.

## **1.7.K Admin consoles**

- **Policy board**: edit *cpc_floor* and density caps by city/role; publish with two‑person approval; rollback versions.
- **Campaign review**: search/suspend/restore; see trust posture and rule hits; city coverage visual.
- **Fraud dashboard**: invalid click streams, IP/FP heatmaps, auto‑pauses, and make‑good credits.
- **Billing**: top‑ups, balances, monthly statements; export CSVs; reconciliation status against Stripe.

All actions are audited (actor, reason, before/after).

## **1.7.L Telemetry & reconciliation**

**Events**

- promo.campaign.create\|activate\|pause\|resume\|end\|suspend
- *promo.policy.update* (with version)
- *promo.impression*, *promo.click*, *promo.invalid_click*
- *promo.spend.debit*, *promo.credit.issue*, *promo.topup.charge.succeeded\|failed*
- promo.recon.variance.notice

**Recon jobs (daily)**

- Compare **Σvalid_clicks × CPC** to **Σledger.spends**; verify against Stripe top‑ups/invoices.
- Variance \> threshold gates campaign serving in affected city until resolved (flag‑gated).

## **1.7.M Error taxonomy (client‑safe)**

- *PROMO_ELIGIBILITY_FAILED* — trust, completeness, or policy not met.
- *PROMO_CPC_BELOW_FLOOR* — CPC under city/role floor.
- *PROMO_BUDGET_EXHAUSTED* — daily/total budget hit.
- *PROMO_INVALID_CITY* — city not allowlisted.
- *PROMO_PAYMENT_FAILED* — top‑up failed.
- *PROMO_SUSPENDED* — admin or auto policy suspension.
- *PROMO_CLICK_INVALIDATED* — click rejected; user is never shown this, used in logs/analytics.

## **1.7.N Performance & cost**

- **Server path**: ad selection is a lightweight filter + sample on a cached active list per *(surface, city, role)*; no heavy joins.
- **Cache**: refresh active campaigns every 30–60s; query‑result cursors keep rotation stable.
- **Storage**: events compacted hourly; cold storage lifecycle after 90 days.
- **Compute**: fraud scoring runs in near‑real‑time with modest concurrency; batch re‑processing off‑peak.

## **1.7.O Test plan (CI + sandbox)**

**Correctness**

715. Eligible campaign appears only when it **matches filters** and city; ineligible campaigns never show.
716. Density caps respected with mixed inventory; no back‑to‑back promoted cards unless flag forces.
717. Featured slot reserved; if empty, organic card fills.

**Budget & pacing**  
4) Daily budget drains gradually in **even** mode under stable traffic; accelerated spends faster.  
5) Budget exhausted → campaign paused; resumes next day or after top‑up.

**Fraud & billing**  
6) Duplicate clicks within window deduped; bot UA/ip patterns flagged; only valid clicks billed.  
7) Post‑hoc invalidation issues **make‑good credits**.  
8) Ledger totals == Σ(valid_clicks × CPC); recon green vs Stripe top‑ups.

**Admin**  
9) Floor & cap updates take effect with versioning; rollback works; two‑person approval enforced.  
10) Campaign suspension/restore applies immediately; audit logged.

**Performance**  
11) p95 selection ≤ 30 ms after cache warm; ≤ 120 ms cold; overall search p95 still meets §1.2 SLOs.

**UX**  
12) “Promoted” chip visible; disclosure link opens policy page; analytics counts impressions/clicks.

## **1.7.P Work packages (Cursor agents)**

- **Agent C — Serving & Fraud**  
  WP‑PROMO‑SERVE‑01: Active‑campaign cache, matcher, blender; density caps.  
  WP‑PROMO‑FRAUD‑01: Click endpoint, dedupe, heuristics, make‑good credits, WAF integration.
- **Agent B — Ledger & Billing**  
  WP‑PROMO‑LEDGER‑01: Budget ledger (+recon jobs), top‑ups via Stripe, statements.  
  WP‑PROMO‑RECON‑01: Daily recon and variance gating.
- **Agent A — Web**  
  WP‑PROMO‑WEB‑01: Promoted card chips, disclosures; seller Campaign Manager pages (create, budgets, stats).
- **Agent D — Admin & QA**  
  WP‑PROMO‑ADMIN‑01: Policy board, fraud dashboard, campaign review, audits.  
  WP‑PROMO‑QA‑01: Full test matrix automation; synthetic traffic generator.

## **1.7.Q Acceptance criteria (mark §1.7 FINAL only when ALL true)**

722. Promoted units **never** bypass filters or city gates and are transparently labeled.
723. Density caps and diversity rules hold; blending preserves organic integrity and fairness.
724. Eligibility gates (IDV/completeness/safety) enforced; auto‑pause on breaches.
725. Budgets, pacing, pauses/resumes work; spend never exceeds budget caps.
726. Click validation rejects duplicates/bad traffic; make‑good credits issued; fraud dashboard active.
727. Billing (prepaid) works with Stripe; ledger equals Σ(valid_clicks × CPC); recon green.
728. Admin policy edits versioned with dual approval; suspensions & credits audited.
729. p95 selection latency within target; infra/costs within budget alarms for 48h synthetic load.

# **§1.8 — Reviews & Reputation**

*(per-entity scopes · write rules · fraud controls · weighting & decay · surfacing · moderation & appeals · admin · telemetry · tests · cost)*

**Purpose.** Implement a trustworthy reputation system that reflects real, recent performance, scoped correctly to *people* (Service Profiles) and *places* (Studios). Prevent abuse (self-reviews, review rings), handle disputes and takedowns, and surface aggregate reputation into search, booking, messaging, and promotions eligibility—without leaking ratings across scopes.

We will not advance to §1.9 until §1.8 satisfies your 99.9% bar.

## **1.8.A Canon & invariants**

730. **Scope is sacred.** Reviews for **Service Profiles (SPs)** and **Studios** are separate. No cross-pollination.
731. **Eligibility to review:** Only the **buyer** on a **completed leg** (or auto-accepted group) can review that **leg’s counterparty**.
732. **One review per leg per author**, editable once within a short window (e.g., 24 h), then locked.
733. **Star + text + structured facets** (e.g., communication, timeliness, quality, cleanliness for studios).
734. **Abuse controls**: block self-reviews, ring patterns, retaliatory bursts, hate speech, doxxing.
735. **Display rules**: recent-weighted average with minimum sample guard; show distributions and recent highlights.
736. **Appeals & moderation**: content policy applies; T&S can remove/restore with immutable audits.

## **1.8.B Data model (Aurora Postgres)**

*-- Reviews are scoped to either a Service Profile (person) or a Studio (place)*  
*create table review (*  
*review_id text primary key, -- rev\_...*  
*target_type text not null check (target_type in ('service_profile','studio')),*  
*target_id text not null, -- srv\_\* or std\_\**  
*author_user_id text not null, -- usr\_\* (buyer on the leg)*  
*leg_id text not null, -- leg\_\* (used to enforce 1:1 and eligibility)*  
*rating smallint not null check (rating between 1 and 5),*  
*title text,*  
*body text,*  
*facets_json jsonb not null default '{}'::jsonb, -- {communication:1-5, quality:1-5, ...}*  
*photos_json jsonb not null default '\[\]'::jsonb, -- review photos (previews only)*  
*status text not null check (status in ('published','hidden','removed','pending')),*  
*policy_flags jsonb not null default '{}'::jsonb, -- {toxicity:0-1, nsfw:0-1, fraud_score:0-1}*  
*source text not null default 'first_party', -- reserved for future imports*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now(),*  
*unique (leg_id, author_user_id)*  
*);*  
  
*-- Aggregates per entity (denormalized for fast reads)*  
*create table reputation_aggregate (*  
*agg_id text primary key, -- rag\_...*  
*target_type text not null, -- 'service_profile' \| 'studio'*  
*target_id text not null,*  
*rating_avg numeric(3,2) not null default 0,*  
*rating_count int not null default 0,*  
*rating_recent_avg numeric(3,2) not null default 0, -- time-decayed*  
*last_review_at timestamptz,*  
*facet_avgs_json jsonb not null default '{}'::jsonb, -- per-facet averages*  
*fraud_signal numeric(3,2) not null default 0, -- 0-1*  
*updated_at timestamptz not null default now(),*  
*unique (target_type, target_id)*  
*);*  
  
*-- Moderation decisions (immutable)*  
*create table review_moderation_audit (*  
*audit_id text primary key, -- rma\_...*  
*review_id text not null references review(review_id) on delete cascade,*  
*action text not null check (action in ('hide','remove','restore','edit_mask')),*  
*reason_code text not null, -- 'hate_speech','doxxing','fraud_ring','by_request', etc.*  
*actor_user_id text not null, -- admin*  
*details_json jsonb not null default '{}'::jsonb,*  
*created_at timestamptz not null default now()*  
*);*  
  
*-- Reports (user flags)*  
*create table review_report (*  
*report_id text primary key, -- rr\_...*  
*review_id text not null references review(review_id) on delete cascade,*  
*reporter_user_id text not null,*  
*reason_code text not null,*  
*details text,*  
*created_at timestamptz not null default now()*  
*);*  

**Indexes**

- *review(target_type, target_id, status)* for listing.
- *review(author_user_id, created_at)* to detect bursts.
- *reputation_aggregate(target_type, rating_recent_avg desc)* for search surfacing.

## **1.8.C Write rules & lifecycle**

740. **Eligibility check** on *createReview*:

     88. *leg.status ∈ {completed}* and *leg.buyer_user_id = author_user_id*.
     89. No prior review by the same author for this *leg_id*.

741. **Edit window**: author may update title/body/facets within 24 h (config), but not the **rating** (to prevent score gaming).

742. **Photos**: preview-size only; NSFW scan; Safe-Mode on public surfaces.

743. **Status transitions**: *published → hidden/removed* (moderation), *removed → restored* (appeal).

744. **Deletion**: no hard delete—use *removed* + audit.

## **1.8.D API (GraphQL) — user-facing**

*type Review {*  
*reviewId: ID!*  
*targetType: String!*  
*targetId: ID!*  
*rating: Int!*  
*title: String*  
*body: String*  
*facets: AWSJSON*  
*photos: \[Attachment!\]!*  
*status: String!*  
*createdAt: AWSDateTime!*  
*}*  
  
*type Reputation {*  
*ratingAvg: Float!*  
*ratingCount: Int!*  
*ratingRecentAvg: Float!*  
*facetAvgs: AWSJSON*  
*lastReviewAt: AWSDateTime*  
*}*  
  
*input CreateReviewInput {*  
*legId: ID!*  
*targetType: String! \# 'service_profile' or 'studio'*  
*targetId: ID!*  
*rating: Int!*  
*title: String*  
*body: String*  
*facets: AWSJSON*  
*photos: \[AttachmentInput!\]*  
*}*  
  
*type Query {*  
*reviews(targetType: String!, targetId: ID!, cursor: String, limit: Int = 10): ReviewPage!*  
*reputation(targetType: String!, targetId: ID!): Reputation!*  
*myEligibleToReview: \[LegRef!\]! \# legs completed but not yet reviewed*  
*}*  
  
*type Mutation {*  
*createReview(input: CreateReviewInput!): Review!*  
*editReview(reviewId: ID!, title: String, body: String, facets: AWSJSON): Review! \# within window*  
*reportReview(reviewId: ID!, reason: String!, details: String): Boolean!*  
*}*  

**Server guards**

- Verify target matches the leg’s counterparty (SP for talent leg; Studio for studio leg).
- Deny self-review (*author_user_id == seller_user_id*), deny cross-scope attempts.
- Rate-limit review write attempts per user.

## **1.8.E Weighting, decay & aggregation**

**Base average:** simple mean over *published* reviews only.  
**Recent-weighted average:** apply exponential decay with half-life *H* (e.g., 180 days) to emphasize recent performance:  
*weighted_score = Σ (rating \* e^{-Δt/H}) / Σ e^{-Δt/H}*.

**Minimum sample guard:**

- If *rating_count \< K* (e.g., 5), show **“New — limited reviews”**; still display stars but deemphasize in ranking.
- For search ranking, combine *rating_recent_avg* with count via a Wilson interval or Laplace smoothing.

**Facet aggregation:**

- Per facet mean and count; show as radar or bar chips; used in filters later.

**Fraud signal:**

- Score 0–1 from heuristics (see 1.8.F). If \> threshold, suppress the review from aggregates pending T&S review.

**Update cadence:**

- On every write/mod decision, recompute aggregates; also nightly full recompute for consistency.

## **1.8.F Fraud & abuse controls**

**Heuristics (near-real-time):**

- **Self-review**: author matches seller or same household (IP/device cluster) → block.
- **Ring behavior**: small set of accounts reviewing each other frequently across short intervals.
- **Burst anomalies**: many 5-star or 1-star reviews in a short window relative to baseline.
- **Retaliation pattern**: reciprocal low star after a dispute outcome.
- **Content policy**: toxicity/hate/off-platform coercion detected by classifier → auto-hide and queue for T&S.

**Signals collected:** author age of account, spend history, dispute/refund context, message sentiment trend, IP/UA/device fingerprints, city mismatch.

**Actions:**

- Auto-hide with *status='hidden'*, set *policy_flags.fraud_score*, enqueue moderation; notify author about review under review (no details that reveal heuristics).
- If confirmed, *removed* with reason; if cleared, *restore*.

**Rate limits:**

- Per account: N reviews/day, with backoff.

## **1.8.G Surfacing & UX**

**On SP and Studio pages:**

- Star average + count; recent highlights (last 90 days); facet bars; distribution histogram.
- Show **verified badges** alongside stars; link to policy page about how reviews work.
- For low-sample: “New — limited reviews” message.

**In search cards:**

- Show stars (recent-weighted) and count; for low sample, show “New” chip; include **Trusted Pro/ID Verified** badges (from §1.6).

**In booking & thread:**

- Show counterpart’s stars and count in headers; after completion, show **nudge to review** card until dismissed or submitted.

## **1.8.H Moderation & appeals (Admin console)**

- **Queue** of hidden/flagged reviews with fraud scores and policy classifiers.
- **Actions:** hide/remove/restore/edit-mask PII with regex (e.g., phone/email); dual approval for removals.
- **Bulk ops** for ring takedowns (multi-review action).
- **Audit trail** pane (immutable log).
- **Appeals:** author can appeal once; T&S response logged; restored reviews recalc aggregates.

## **1.8.I Notifications**

- Buyer reminder to review at 24 h / 72 h; opt-out respected.
- Seller notified on new review; ability to **publicly reply** (one reply, editable once within 24 h; anti-harassment rules).
- If review hidden/removed → author notified with high-level reason and appeal link.

## **1.8.J Telemetry & lineage**

- *review.eligible.opened*, *review.create.attempt\|success\|fail*, *review.edit*,
- *review.report*, *review.hide\|remove\|restore*,
- *reputation.recompute*, *reputation.flag.fraud*,
- *notification.sent.review_reminder*, *notification.sent.review_published*,
- Correlate with *leg_id*, *target_id*, *author_user_id*.

**Analytics dashboards**: review funnels (invite→posted), star distributions, facet trends, fraud queue size/latency, moderation outcomes, impact on search CTR and conversion.

## **1.8.K Error taxonomy (client-safe)**

- *REVIEW_NOT_ELIGIBLE* — leg not completed or author mismatch.
- *REVIEW_DUPLICATE* — already reviewed this leg.
- *REVIEW_WINDOW_CLOSED* — edit beyond 24 h window.
- *REVIEW_POLICY_BLOCKED* — content violates policy (details not disclosed).
- *REVIEW_TOO_MANY_TODAY* — rate limit.
- *REPLY_NOT_ALLOWED* — duplicate or window closed.

## **1.8.L Performance & cost**

- **Reads** dominate; aggregates cached and invalidated on write.
- **Writes** relatively small; classifiers run serverless with concurrency caps.
- S3 storage minimal (preview photos); lifecycle to Intelligent-Tiering after 30 days.

## **1.8.M Test plan (CI + sandbox)**

**Eligibility & write path**

788. Completed leg → buyer can post one review; seller cannot; duplicate blocked.
789. Edit within 24 h succeeds; rating edit blocked; after window, edit blocked.

**Fraud controls**  
3) Self-review attempt blocked.  
4) Ring/burst simulated → auto-hide & queue for T&S; restoration path verified.  
5) Toxic content flagged → hidden; appeal → restore.

**Aggregation**  
6) Weighted average & decay verified vs golden file; low-sample indicator shown correctly.  
7) Facet averages computed; distribution histograms accurate.

**Surfacing**  
8) Search cards show correct stars/counts; “New” chip for low sample.  
9) Profile page shows highlights and facet bars; recent window updates.

**Admin**  
10) Hide/remove/restore writes audits; bulk ring takedown works; reply moderation enforced.

**Performance**  
11) p95 entity reputation fetch ≤ 120 ms (cached); recompute job under 1 min per 10k entities.

## **1.8.N Work packages (Cursor agents)**

- **Agent B — Domain/API**  
  WP-REV-01: SQL tables + GraphQL resolvers (create, edit, list, reputation).  
  WP-REV-02: Aggregation jobs (real-time & nightly full), cache invalidation.
- **Agent C — Integrity**  
  WP-REV-FRD-01: Fraud heuristics, classifiers integration, auto-hide queue.  
  WP-REV-FRD-02: Rate limiter; ring detection; report intake.
- **Agent A — Web**  
  WP-WEB-REV-01: UI components for stars, distributions, facets, highlights, replies; review composer.  
  WP-WEB-REV-02: Nudges & inbox cards; moderation states in UI.
- **Agent D — Admin & QA**  
  WP-ADM-REV-01: Moderation console, audits, appeals.  
  WP-QA-REV-01: Full test matrix automation; golden datasets for aggregation math.

## **1.8.O Acceptance criteria (mark §1.8 FINAL only when ALL true)**

794. Only eligible buyers can review; one per leg; edit window enforced; content scanned.
795. Aggregates computed with decay and sample guards; fraud-flagged reviews excluded pending review.
796. Surfacing correct on SP/Studio pages, search cards, booking/thread headers; “New” chip behavior correct.
797. Moderation & appeals operate with immutable audits; bulk actions for rings.
798. Notifications for reminders/public replies sent; rate limits enforced; policy respected.
799. Telemetry complete; dashboards reflect health and abuse trends.
800. Performance & cost within targets; caches invalidate correctly on updates.

# **§1.9 — Payments & Wallet**

*(Platform fees · Taxes on fees · Separate “ads” credits vs. buyer wallet · Statements · Accounting & revenue recognition · GL & recon · APIs · Admin · Telemetry · Tests · Cost)*

**Purpose.** Define the *financial core* that separates marketplace **GMV** from **platform fee revenue**, treats **taxes correctly**, keeps “ads credits” separate from “buyer wallet,” and drives statements, accounting, and reconciliation. This section makes our booking money flows audit‑grade and implementation‑ready across **data model, fee math, GL entries, APIs, admin tools, telemetry, SLOs, and tests**. It aligns with §§1.3 (Checkout), 1.4 (Messaging/Project Panel), and 1.7 (Promotions).

We will not advance to §1.10 until §1.9 satisfies your 99.9% bar.

## **1.9.A Canon & invariants**

801. Money in integer cents (UTC timestamps).

802. **One buyer charge per LBG** (already in §1.3), with **per‑leg allocations** and **escrow‑like holds** (payouts only on completion/acceptance window).

803. **Platform fee ≠ GMV.** Fees are **not** the seller’s price; fees are separate lines and recognized as **revenue** for the platform only when *earned*.

804. **Taxes split correctly**: (a) **service taxes** on the seller’s service (pass‑through liability to seller or to tax authority depending on “merchant‑of‑record” (MoR) configuration), and (b) **platform fee taxes** (platform’s own tax obligation) — never recognized as revenue.

805. **Two distinct credits**:

     92. **Ads credits**: for §1.7 promotions (advertiser side).
     93. **Buyer wallet**: marketplace credits for buyers (refund residuals, goodwill, referrals). **These must not mingle.**

806. **Accounting gates**: daily close/reconciliation must be green to release payouts (ties to §1.3.V).

807. **Idempotency & lineage everywhere** (PI ids, transfer ids, refund ids, ledger ids; stable joins for recon).

## **1.9.B Fee taxonomy (launch)**

Keep MVP simple, configurable in AppConfig. All fees are computed **per leg** so partial cancels/refunds work cleanly.

- **Marketplace (buyer) fee** — percentage + floor/ceiling; charged to buyer; per‑leg line *platform_fee_cents*.
- **Platform fee tax** — via tax adapter (city‑aware), per‑leg line *platform_fee_tax_cents*.
- **Payment processing fee** — Stripe fees (variable + fixed); *expense* on the platform (not charged to buyer at MVP).
- **Optional seller fee (withheld)** — **off** at MVP; if enabled later, it reduces seller payout and is recognized as revenue when earned.
- **Rounding** — leg‑local, banker’s only if tax provider requires; otherwise pure cents math.

Result per **leg** at confirmation snapshot:

*buyer_pays_leg_total*  
*= (seller_subtotal + service_tax)*  
* + platform_fee_cents*  
* + platform_fee_tax_cents*  

Totals across legs roll up to **LBG charge amount**.

## **1.9.C Data model (SQL additions for fees, wallet & GL)**

Extends §1.3 schema.

*-- Per-leg fee snapshot (immutable after confirm; amendments add new rows)*  
*alter table booking_leg*  
*add column platform_fee_cents int not null default 0,*  
*add column platform_fee_tax_cents int not null default 0;*  
  
*-- Wallet for BUYERS (not advertisers)*  
*create table wallet_account (*  
*wallet_id text primary key, -- wlt\_...*  
*user_id text unique not null, -- usr\_...*  
*currency text not null default 'USD',*  
*balance_cents int not null default 0,*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
  
*create table wallet_txn (*  
*wallet_txn_id text primary key, -- wtx\_...*  
*wallet_id text not null references wallet_account(wallet_id) on delete cascade,*  
*kind text not null check (kind in ('credit','debit','adjustment')),*  
*source text not null check (source in ('refund_residual','goodwill','referral','checkout_apply','reversal')),*  
*lbg_id text,*  
*leg_id text,*  
*amount_cents int not null, -- positive; sign inferred by kind*  
*note text,*  
*idempotency_key text not null,*  
*created_at timestamptz not null default now()*  
*);*  
*create index on wallet_txn(wallet_id, created_at desc);*  
*create unique index on wallet_txn(idempotency_key);*  
  
*-- Platform fee ledger (deferrals→earned)*  
*create table fee_ledger (*  
*fee_entry_id text primary key, -- fle\_...*  
*leg_id text not null,*  
*stage text not null check (stage in ('deferred','earned','reversed')),*  
*platform_fee_cents int not null,*  
*platform_fee_tax_cents int not null,*  
*reason text not null, -- 'confirm','complete','refund','dispute'*  
*created_at timestamptz not null default now()*  
*);*  
  
*-- GL journal (exportable to accounting)*  
*create table gl_entry (*  
*gl_id text primary key, -- gl\_...*  
*occurred_at timestamptz not null,*  
*lbg_id text,*  
*leg_id text,*  
*account_dr text not null, -- e.g., 'Cash:Stripe', 'Deferred:PlatformFees'*  
*account_cr text not null, -- e.g., 'Liability:SellerPayable'*  
*amount_cents int not null,*  
*memo text,*  
*ext_ref text, -- stripe bal_txn id, charge id, payout id*  
*created_at timestamptz not null default now()*  
*);*  
*create index on gl_entry(occurred_at);*  
*create index on gl_entry(lbg_id, leg_id);*  

**Note:** Advertiser **ads credits** ledger from §1.7 remains separate (*promo_budget_ledger*). Buyer wallet and promo credits **never** touch each other.

## **1.9.D Accounting model & GL entries (MVP)**

We model journal entries so Finance can export them or sync to a downstream system.

### **D.1 At capture (LBG confirmed & charge succeeded)**

Let:

- *Σseller_subtotal+service_tax* across legs = **SellerPayable** (if seller remits tax).
- *Σplatform_fee_cents* = **PlatformFeesDeferred**.
- *Σplatform_fee_tax_cents* = **PlatformFeeTaxPayable**.

**Entry 1: Record cash and liabilities**

*Dr Cash:Stripe total_charge_cents*  
*Cr Liability:SellerPayable Σ(seller_subtotal + service_tax)*  
*Cr Deferred:PlatformFees Σ(platform_fee_cents)*  
*Cr Liability:TaxPayable:PlatformFeeTax Σ(platform_fee_tax_cents)*  

If **platform** is MoR for service tax, split accordingly:

*Cr Liability:TaxPayable:ServiceTax Σ(service_tax)*  
*Cr Liability:SellerPayable Σ(seller_subtotal)*  

**Entry 2: Record Stripe processing fees (when balance txn posts)**

*Dr Expense:PaymentProcessing stripe_fee_cents*  
*Cr Cash:Stripe stripe_fee_cents*  

**Fee ledger row**: *stage='deferred'*, reason='confirm' for each leg.

### **D.2 On completion/accept (leg earns platform fee revenue)**

*Dr Deferred:PlatformFees platform_fee_cents*  
*Cr Revenue:PlatformFees platform_fee_cents*  

**Fee ledger**: add *stage='earned'*, reason='complete' for the leg.

### **D.3 On payout transfer to seller (per leg)**

*Dr Liability:SellerPayable transfer_amount_cents*  
*Cr Cash:Stripe transfer_amount_cents*  

### **D.4 Refunds (leg policy or admin)**

- Reverse revenue if already earned; otherwise reduce deferral.
- Service tax and platform fee tax reversed per provider rules.

**If refund before completion (unearned):**

*Dr Deferred:PlatformFees refund_platform_fee_cents*  
*Dr Liability:TaxPayable:PlatformFeeTax refund_platform_fee_tax_cents*  
*Dr Liability:SellerPayable refund_service_total_cents*  
*Cr Cash:Stripe total_refund_cents*  

**If refund after completion (earned):**

*Dr Revenue:PlatformFees refund_platform_fee_cents*  
*Dr Liability:TaxPayable:PlatformFeeTax refund_platform_fee_tax_cents*  
*Dr Liability:SellerPayable refund_service_total_cents*  
*Cr Cash:Stripe total_refund_cents*  

### **D.5 Chargebacks (lost dispute)**

*Dr Expense:Chargebacks disputed_amount_cents*  
*Cr Cash:Stripe disputed_amount_cents*  

Then adjust liabilities/deferrals/revenue as needed (mirror of D.4 based on timing).

## **1.9.E Wallet (buyer credits) — rules & flows**

**Use cases:** residuals from partial refunds, goodwill credits, referral bonuses.  
**Important:** wallet *reduces* the **PaymentIntent** amount at checkout; it is never auto‑withdrawn to bank/card.

**Flows**

- **Credit**: create *wallet_txn(kind='credit', source='refund_residual'\|'goodwill'\|'referral')*; increase balance.
- **Apply at checkout**: before creating PI, debit wallet up to available balance (*kind='debit', source='checkout_apply'*) and reduce charge amount; store the applied amount on the LBG for receipts.
- **Reversal**: if a checkout fails post‑debit, write *reversal* credit with same idempotency key to restore balance.

**GraphQL**

*type Wallet { balanceCents: Int!, currency: String! }*  
*type WalletTxn { walletTxnId: ID!, kind: String!, source: String!, amountCents: Int!, createdAt: AWSDateTime! }*  
  
*type Query { myWallet: Wallet!, myWalletTxns(limit:Int=50, cursor:String): \[WalletTxn!\]! }*  
*type Mutation {*  
*applyWalletToCheckout(draftId: ID!, maxCents: Int!): ApplyWalletResult! \# returns appliedCents*  
*}*  

**Constraints**

- One wallet per user per currency (USD MVP).
- Wallet cannot go negative.
- Expiry on promo/referral credits optional (tracked in *note* or extended field later).

## **1.9.F Taxes on platform fees**

- Use same **Tax adapter** as §1.3 (TaxJar/Avalara/Stripe Tax).
- Quote **per leg** for *platform_fee_cents* → *platform_fee_tax_cents* using the buyer’s tax nexus vs city gate rules.
- Record *TaxPayable:PlatformFeeTax* at capture; reverse appropriately on refunds.
- Include platform fee tax lines in buyer receipts and in platform tax reports.

## **1.9.G Statements & exports**

**Seller statement (monthly)**

- Payouts by date with links to legs/LBGs; adjustments (reserves, corrections); net totals.
- CSV + PDF; downloadable from Seller Finance console.
- If seller is MoR for service tax, clearly state seller‑level tax totals.

**Buyer statement (optional monthly)**

- Charges and refunds grouped; wallet credits/debits; tax totals; downloadable from account billing.

**Platform finance exports**

- **GL export**: *gl_entry* within date range.
- **Tax reports**: platform fee tax totals by city.
- **Stripe recon**: extract of balance transactions (charges, refunds, fees, transfers, payouts) and our correlated ids.

## **1.9.H APIs (GraphQL) — finance views**

*type ChargeSummary { lbgId: ID!, amountCents: Int!, capturedAt: AWSDateTime!, method: String! }*  
*type PayoutSummary { legId: ID!, amountCents: Int!, status: String!, scheduledFor: AWSDateTime }*  
*type StatementLink { url: AWSURL!, kind: String!, period: String! }*  
  
*type Query {*  
*myCharges(from: AWSDate!, to: AWSDate!): \[ChargeSummary!\]!*  
*myPayouts(from: AWSDate!, to: AWSDate!): \[PayoutSummary!\]!*  
*myStatements(period: String): \[StatementLink!\]! \# '2025-11'*  
*}*  

Server enforces least‑privilege (buyer sees their charges; seller sees their payouts; admins see all).

## **1.9.I Admin consoles (Finance)**

- **Fees & taxes**: fee rules by city/role; dry‑run previews on example legs; dual‑approval for rule changes.
- **Wallet**: credit/debit/adjustment tools with reason; hard caps for goodwill per admin.
- **GL & recon**: daily close board (tie‑in to §1.3.V), variance tiles, drill‑down to *gl_entry* and Stripe balance txn ids.
- **MoR toggle** (city gate): determines whether service taxes go to Seller Payable or Tax Payable.
- **Exports**: GL CSV, statements batch, tax reports.
- **Audits**: every money‑affecting admin action logged with before/after and two‑person approval when required.

## **1.9.J Telemetry & lineage**

- *fee.compute*, *fee.deferred.recorded*, *fee.earned.recorded*,
- *wallet.credit\|debit\|reversal*,
- *gl.entry.write*, *gl.export*,
- *recon.daily.start\|succeeded\|failed*, *recon.variance.notice*.  
  Every event includes *lbg_id/leg_id*, amounts, and relevant external refs (PI id, refund id, transfer id, balance txn id).

## **1.9.K SLOs & cost posture**

- **SLOs**:

  - Fee compute latency: **\<100 ms** p95.
  - Wallet apply latency: **\<75 ms** p95.
  - Daily close completes by **T+8h** local time; variance gating works.

- **Cost**: entirely serverless; no always‑on compute. S3 lifecycle on statements and exports (cold storage after 90 days). Stripe fees are pass‑through expenses; tax adapter paid per transaction.

## **1.9.L Error taxonomy (client‑safe)**

- *FEE_RULE_MISSING* — no fee rule for city/role.
- *WALLET_INSUFFICIENT_FUNDS* — requested apply exceeds balance.
- *WALLET_STALE_APPLY* — PI amount changed; recompute then apply.
- *GL_EXPORT_RANGE_TOO_LARGE* — split into batches.
- *MOR_MISCONFIGURED* — MoR toggle inconsistent with tax settings (admin‑only).

## **1.9.M Test plan (CI + sandbox)**

**Fees & taxes**

852. Compute per‑leg fees & fee tax for different cities/roles; verify rounding; receipts show lines.
853. Earn revenue on completion; deferral → earned; reverse on refund both pre‑ and post‑earn.

**Wallet**  
3) Credit on refund residual; apply to checkout; reversal on failed PI; double‑debit prevented by idempotency key.

**GL & recon**  
4) GL entries written at capture, completion, payout, refund, dispute; sums balance.  
5) Recon: Σcharges == Cash delta ± Stripe fees; Σtransfers == Seller Payable delta; variance gates payouts when off.

**MoR switch**  
6) Service tax to Seller Payable vs Tax Payable toggles correctly and flows to statements/reports.

**Seller/Buyer statements**  
7) Generate period statements; totals tie to underlying legs/payouts/charges.

**Performance**  
8) Fee compute p95 \< 100 ms; wallet apply p95 \< 75 ms under load.

## **1.9.N Work packages (Cursor agents)**

- Agent B — Domain/Finance

  - WP‑FIN‑01: SQL migrations for *fee_ledger*, *wallet\_\**, *gl_entry*; fee calculator; MoR switch.
  - WP‑FIN‑02: GL writer and export; tie into §1.3 events; recon joins vs Stripe balance txns.

- Agent C — Integrations

  - WP‑FIN‑TAX‑01: Tax adapter for platform fee tax; refund handling.
  - WP‑FIN‑STR‑01: Stripe balance transaction fetcher; mapping; webhooks.

- Agent A — Web

  - WP‑WEB‑FIN‑01: Wallet UI and statements pages (buyer/seller).
  - WP‑WEB‑FIN‑02: Fee disclosure UI at checkout.

- Agent D — Admin & QA

  - WP‑ADM‑FIN‑01: Finance console (rules, wallet adjustments, GL exports, MoR).
  - WP‑QA‑FIN‑01: Full test matrix automation; golden GL snapshots.

## **1.9.O Acceptance criteria (mark §1.9 FINAL only when ALL true)**

858. Platform fees computed per leg; fee taxes quoted; shown on receipts; earned on completion.
859. Wallet credits/debits behave atomically; cannot overdraft; idempotent reversals on failure paths.
860. GL entries capture capture/earn/payout/refund/dispute correctly; exports work; daily recon green 5/5 days.
861. MoR toggle correctly routes **service tax** to Seller Payable vs Tax Payable; platform fee tax always stays in Tax Payable.
862. Statements (buyer/seller) accurate and downloadable; platform exports ready for accounting.
863. Telemetry complete; SLOs met; costs within budget alarms.

# **§1.9 — Payments & Wallet**

*(Platform fees · Taxes on fees · Separate “ads” credits vs. buyer wallet · Statements · Accounting & revenue recognition · GL & recon · APIs · Admin · Telemetry · Tests · Cost)*

**Purpose.** Define the *financial core* that separates marketplace **GMV** from **platform fee revenue**, treats **taxes correctly**, keeps “ads credits” separate from “buyer wallet,” and drives statements, accounting, and reconciliation. This section makes our booking money flows audit‑grade and implementation‑ready across **data model, fee math, GL entries, APIs, admin tools, telemetry, SLOs, and tests**. It aligns with §§1.3 (Checkout), 1.4 (Messaging/Project Panel), and 1.7 (Promotions).

We will not advance to §1.10 until §1.9 satisfies your 99.9% bar.

## **1.9.A Canon & invariants**

864. Money in integer cents (UTC timestamps).

865. **One buyer charge per LBG** (already in §1.3), with **per‑leg allocations** and **escrow‑like holds** (payouts only on completion/acceptance window).

866. **Platform fee ≠ GMV.** Fees are **not** the seller’s price; fees are separate lines and recognized as **revenue** for the platform only when *earned*.

867. **Taxes split correctly**: (a) **service taxes** on the seller’s service (pass‑through liability to seller or to tax authority depending on “merchant‑of‑record” (MoR) configuration), and (b) **platform fee taxes** (platform’s own tax obligation) — never recognized as revenue.

868. **Two distinct credits**:

     118. **Ads credits**: for §1.7 promotions (advertiser side).
     119. **Buyer wallet**: marketplace credits for buyers (refund residuals, goodwill, referrals). **These must not mingle.**

869. **Accounting gates**: daily close/reconciliation must be green to release payouts (ties to §1.3.V).

870. **Idempotency & lineage everywhere** (PI ids, transfer ids, refund ids, ledger ids; stable joins for recon).

## **1.9.B Fee taxonomy (launch)**

Keep MVP simple, configurable in AppConfig. All fees are computed **per leg** so partial cancels/refunds work cleanly.

- **Marketplace (buyer) fee** — percentage + floor/ceiling; charged to buyer; per‑leg line *platform_fee_cents*.
- **Platform fee tax** — via tax adapter (city‑aware), per‑leg line *platform_fee_tax_cents*.
- **Payment processing fee** — Stripe fees (variable + fixed); *expense* on the platform (not charged to buyer at MVP).
- **Optional seller fee (withheld)** — **off** at MVP; if enabled later, it reduces seller payout and is recognized as revenue when earned.
- **Rounding** — leg‑local, banker’s only if tax provider requires; otherwise pure cents math.

Result per **leg** at confirmation snapshot:

*buyer_pays_leg_total*  
*= (seller_subtotal + service_tax)*  
* + platform_fee_cents*  
* + platform_fee_tax_cents*  

Totals across legs roll up to **LBG charge amount**.

## **1.9.C Data model (SQL additions for fees, wallet & GL)**

Extends §1.3 schema.

*-- Per-leg fee snapshot (immutable after confirm; amendments add new rows)*  
*alter table booking_leg*  
*add column platform_fee_cents int not null default 0,*  
*add column platform_fee_tax_cents int not null default 0;*  
  
*-- Wallet for BUYERS (not advertisers)*  
*create table wallet_account (*  
*wallet_id text primary key, -- wlt\_...*  
*user_id text unique not null, -- usr\_...*  
*currency text not null default 'USD',*  
*balance_cents int not null default 0,*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
  
*create table wallet_txn (*  
*wallet_txn_id text primary key, -- wtx\_...*  
*wallet_id text not null references wallet_account(wallet_id) on delete cascade,*  
*kind text not null check (kind in ('credit','debit','adjustment')),*  
*source text not null check (source in ('refund_residual','goodwill','referral','checkout_apply','reversal')),*  
*lbg_id text,*  
*leg_id text,*  
*amount_cents int not null, -- positive; sign inferred by kind*  
*note text,*  
*idempotency_key text not null,*  
*created_at timestamptz not null default now()*  
*);*  
*create index on wallet_txn(wallet_id, created_at desc);*  
*create unique index on wallet_txn(idempotency_key);*  
  
*-- Platform fee ledger (deferrals→earned)*  
*create table fee_ledger (*  
*fee_entry_id text primary key, -- fle\_...*  
*leg_id text not null,*  
*stage text not null check (stage in ('deferred','earned','reversed')),*  
*platform_fee_cents int not null,*  
*platform_fee_tax_cents int not null,*  
*reason text not null, -- 'confirm','complete','refund','dispute'*  
*created_at timestamptz not null default now()*  
*);*  
  
*-- GL journal (exportable to accounting)*  
*create table gl_entry (*  
*gl_id text primary key, -- gl\_...*  
*occurred_at timestamptz not null,*  
*lbg_id text,*  
*leg_id text,*  
*account_dr text not null, -- e.g., 'Cash:Stripe', 'Deferred:PlatformFees'*  
*account_cr text not null, -- e.g., 'Liability:SellerPayable'*  
*amount_cents int not null,*  
*memo text,*  
*ext_ref text, -- stripe bal_txn id, charge id, payout id*  
*created_at timestamptz not null default now()*  
*);*  
*create index on gl_entry(occurred_at);*  
*create index on gl_entry(lbg_id, leg_id);*  

**Note:** Advertiser **ads credits** ledger from §1.7 remains separate (*promo_budget_ledger*). Buyer wallet and promo credits **never** touch each other.

## **1.9.D Accounting model & GL entries (MVP)**

We model journal entries so Finance can export them or sync to a downstream system.

### **D.1 At capture (LBG confirmed & charge succeeded)**

Let:

- *Σseller_subtotal+service_tax* across legs = **SellerPayable** (if seller remits tax).
- *Σplatform_fee_cents* = **PlatformFeesDeferred**.
- *Σplatform_fee_tax_cents* = **PlatformFeeTaxPayable**.

**Entry 1: Record cash and liabilities**

*Dr Cash:Stripe total_charge_cents*  
*Cr Liability:SellerPayable Σ(seller_subtotal + service_tax)*  
*Cr Deferred:PlatformFees Σ(platform_fee_cents)*  
*Cr Liability:TaxPayable:PlatformFeeTax Σ(platform_fee_tax_cents)*  

If **platform** is MoR for service tax, split accordingly:

*Cr Liability:TaxPayable:ServiceTax Σ(service_tax)*  
*Cr Liability:SellerPayable Σ(seller_subtotal)*  

**Entry 2: Record Stripe processing fees (when balance txn posts)**

*Dr Expense:PaymentProcessing stripe_fee_cents*  
*Cr Cash:Stripe stripe_fee_cents*  

**Fee ledger row**: *stage='deferred'*, reason='confirm' for each leg.

### **D.2 On completion/accept (leg earns platform fee revenue)**

*Dr Deferred:PlatformFees platform_fee_cents*  
*Cr Revenue:PlatformFees platform_fee_cents*  

**Fee ledger**: add *stage='earned'*, reason='complete' for the leg.

### **D.3 On payout transfer to seller (per leg)**

*Dr Liability:SellerPayable transfer_amount_cents*  
*Cr Cash:Stripe transfer_amount_cents*  

### **D.4 Refunds (leg policy or admin)**

- Reverse revenue if already earned; otherwise reduce deferral.
- Service tax and platform fee tax reversed per provider rules.

**If refund before completion (unearned):**

*Dr Deferred:PlatformFees refund_platform_fee_cents*  
*Dr Liability:TaxPayable:PlatformFeeTax refund_platform_fee_tax_cents*  
*Dr Liability:SellerPayable refund_service_total_cents*  
*Cr Cash:Stripe total_refund_cents*  

**If refund after completion (earned):**

*Dr Revenue:PlatformFees refund_platform_fee_cents*  
*Dr Liability:TaxPayable:PlatformFeeTax refund_platform_fee_tax_cents*  
*Dr Liability:SellerPayable refund_service_total_cents*  
*Cr Cash:Stripe total_refund_cents*  

### **D.5 Chargebacks (lost dispute)**

*Dr Expense:Chargebacks disputed_amount_cents*  
*Cr Cash:Stripe disputed_amount_cents*  

Then adjust liabilities/deferrals/revenue as needed (mirror of D.4 based on timing).

## **1.9.E Wallet (buyer credits) — rules & flows**

**Use cases:** residuals from partial refunds, goodwill credits, referral bonuses.  
**Important:** wallet *reduces* the **PaymentIntent** amount at checkout; it is never auto‑withdrawn to bank/card.

**Flows**

- **Credit**: create *wallet_txn(kind='credit', source='refund_residual'\|'goodwill'\|'referral')*; increase balance.
- **Apply at checkout**: before creating PI, debit wallet up to available balance (*kind='debit', source='checkout_apply'*) and reduce charge amount; store the applied amount on the LBG for receipts.
- **Reversal**: if a checkout fails post‑debit, write *reversal* credit with same idempotency key to restore balance.

**GraphQL**

*type Wallet { balanceCents: Int!, currency: String! }*  
*type WalletTxn { walletTxnId: ID!, kind: String!, source: String!, amountCents: Int!, createdAt: AWSDateTime! }*  
  
*type Query { myWallet: Wallet!, myWalletTxns(limit:Int=50, cursor:String): \[WalletTxn!\]! }*  
*type Mutation {*  
*applyWalletToCheckout(draftId: ID!, maxCents: Int!): ApplyWalletResult! \# returns appliedCents*  
*}*  

**Constraints**

- One wallet per user per currency (USD MVP).
- Wallet cannot go negative.
- Expiry on promo/referral credits optional (tracked in *note* or extended field later).

## **1.9.F Taxes on platform fees**

- Use same **Tax adapter** as §1.3 (TaxJar/Avalara/Stripe Tax).
- Quote **per leg** for *platform_fee_cents* → *platform_fee_tax_cents* using the buyer’s tax nexus vs city gate rules.
- Record *TaxPayable:PlatformFeeTax* at capture; reverse appropriately on refunds.
- Include platform fee tax lines in buyer receipts and in platform tax reports.

## **1.9.G Statements & exports**

**Seller statement (monthly)**

- Payouts by date with links to legs/LBGs; adjustments (reserves, corrections); net totals.
- CSV + PDF; downloadable from Seller Finance console.
- If seller is MoR for service tax, clearly state seller‑level tax totals.

**Buyer statement (optional monthly)**

- Charges and refunds grouped; wallet credits/debits; tax totals; downloadable from account billing.

**Platform finance exports**

- **GL export**: *gl_entry* within date range.
- **Tax reports**: platform fee tax totals by city.
- **Stripe recon**: extract of balance transactions (charges, refunds, fees, transfers, payouts) and our correlated ids.

## **1.9.H APIs (GraphQL) — finance views**

*type ChargeSummary { lbgId: ID!, amountCents: Int!, capturedAt: AWSDateTime!, method: String! }*  
*type PayoutSummary { legId: ID!, amountCents: Int!, status: String!, scheduledFor: AWSDateTime }*  
*type StatementLink { url: AWSURL!, kind: String!, period: String! }*  
  
*type Query {*  
*myCharges(from: AWSDate!, to: AWSDate!): \[ChargeSummary!\]!*  
*myPayouts(from: AWSDate!, to: AWSDate!): \[PayoutSummary!\]!*  
*myStatements(period: String): \[StatementLink!\]! \# '2025-11'*  
*}*  

Server enforces least‑privilege (buyer sees their charges; seller sees their payouts; admins see all).

## **1.9.I Admin consoles (Finance)**

- **Fees & taxes**: fee rules by city/role; dry‑run previews on example legs; dual‑approval for rule changes.
- **Wallet**: credit/debit/adjustment tools with reason; hard caps for goodwill per admin.
- **GL & recon**: daily close board (tie‑in to §1.3.V), variance tiles, drill‑down to *gl_entry* and Stripe balance txn ids.
- **MoR toggle** (city gate): determines whether service taxes go to Seller Payable or Tax Payable.
- **Exports**: GL CSV, statements batch, tax reports.
- **Audits**: every money‑affecting admin action logged with before/after and two‑person approval when required.

## **1.9.J Telemetry & lineage**

- *fee.compute*, *fee.deferred.recorded*, *fee.earned.recorded*,
- *wallet.credit\|debit\|reversal*,
- *gl.entry.write*, *gl.export*,
- *recon.daily.start\|succeeded\|failed*, *recon.variance.notice*.  
  Every event includes *lbg_id/leg_id*, amounts, and relevant external refs (PI id, refund id, transfer id, balance txn id).

## **1.9.K SLOs & cost posture**

- **SLOs**:

  - Fee compute latency: **\<100 ms** p95.
  - Wallet apply latency: **\<75 ms** p95.
  - Daily close completes by **T+8h** local time; variance gating works.

- **Cost**: entirely serverless; no always‑on compute. S3 lifecycle on statements and exports (cold storage after 90 days). Stripe fees are pass‑through expenses; tax adapter paid per transaction.

## **1.9.L Error taxonomy (client‑safe)**

- *FEE_RULE_MISSING* — no fee rule for city/role.
- *WALLET_INSUFFICIENT_FUNDS* — requested apply exceeds balance.
- *WALLET_STALE_APPLY* — PI amount changed; recompute then apply.
- *GL_EXPORT_RANGE_TOO_LARGE* — split into batches.
- *MOR_MISCONFIGURED* — MoR toggle inconsistent with tax settings (admin‑only).

## **1.9.M Test plan (CI + sandbox)**

**Fees & taxes**

915. Compute per‑leg fees & fee tax for different cities/roles; verify rounding; receipts show lines.
916. Earn revenue on completion; deferral → earned; reverse on refund both pre‑ and post‑earn.

**Wallet**  
3) Credit on refund residual; apply to checkout; reversal on failed PI; double‑debit prevented by idempotency key.

**GL & recon**  
4) GL entries written at capture, completion, payout, refund, dispute; sums balance.  
5) Recon: Σcharges == Cash delta ± Stripe fees; Σtransfers == Seller Payable delta; variance gates payouts when off.

**MoR switch**  
6) Service tax to Seller Payable vs Tax Payable toggles correctly and flows to statements/reports.

**Seller/Buyer statements**  
7) Generate period statements; totals tie to underlying legs/payouts/charges.

**Performance**  
8) Fee compute p95 \< 100 ms; wallet apply p95 \< 75 ms under load.

## **1.9.N Work packages (Cursor agents)**

- Agent B — Domain/Finance

  - WP‑FIN‑01: SQL migrations for *fee_ledger*, *wallet\_\**, *gl_entry*; fee calculator; MoR switch.
  - WP‑FIN‑02: GL writer and export; tie into §1.3 events; recon joins vs Stripe balance txns.

- Agent C — Integrations

  - WP‑FIN‑TAX‑01: Tax adapter for platform fee tax; refund handling.
  - WP‑FIN‑STR‑01: Stripe balance transaction fetcher; mapping; webhooks.

- Agent A — Web

  - WP‑WEB‑FIN‑01: Wallet UI and statements pages (buyer/seller).
  - WP‑WEB‑FIN‑02: Fee disclosure UI at checkout.

- Agent D — Admin & QA

  - WP‑ADM‑FIN‑01: Finance console (rules, wallet adjustments, GL exports, MoR).
  - WP‑QA‑FIN‑01: Full test matrix automation; golden GL snapshots.

## **1.9.O Acceptance criteria (mark §1.9 FINAL only when ALL true)**

921. Platform fees computed per leg; fee taxes quoted; shown on receipts; earned on completion.
922. Wallet credits/debits behave atomically; cannot overdraft; idempotent reversals on failure paths.
923. GL entries capture capture/earn/payout/refund/dispute correctly; exports work; daily recon green 5/5 days.
924. MoR toggle correctly routes **service tax** to Seller Payable vs Tax Payable; platform fee tax always stays in Tax Payable.
925. Statements (buyer/seller) accurate and downloadable; platform exports ready for accounting.
926. Telemetry complete; SLOs met; costs within budget alarms.

# **§1.10 — Notifications & Comms**

*(templates & variables · channels (email/push/SMS/in‑app) · quiet hours & preferences · deliverability & bounces · dedupe & batching · audits · admin · telemetry · tests · cost)*

**Purpose.** Build a cost‑efficient, privacy‑safe, and auditable communications layer that delivers the right message on the right channel at the right time—without noise, policy risk, or surprises. This section specifies **data models, providers, APIs, message templates, preference/quiet‑hours logic, deliverability & suppression, dedupe & batching, admin tools, telemetry, SLOs, tests, and cost levers**. We will *not* move on until §1.10 reaches your 99.9% bar.

**Note on scope alignment:** §1.10 covers platform communications (system emails, SMS, push, and in‑app notifications). Thread messages and action cards live in §1.4; finance emails/statements are integrated but defined here for sending rules.

We’ll complete §1.10 in **two parts** in case length exceeds limits. This reply delivers **Part 1** (architecture, data model, templates, providers, preferences/quiet hours, API, dedupe/batching). Next reply (still §1.10) will cover **deliverability (DKIM/DMARC), suppression/bounces, in‑app notification center, experiments/localization, admin console, telemetry/SLOs, test matrix, and cost**.

## **1.10.A Canon & invariants**

927. **User control first:** channel‑level **preferences** (opt‑in/out by category) and **quiet hours** are enforced server‑side for all non‑critical comms.
928. **Critical vs non‑critical:** payment receipts, security, and legal notices always send (with minimal content); marketing is opt‑in and rate‑limited.
929. **One source of truth:** every message is a **templated document** with **variables** and an **audit trail** (who/what/why/when).
930. **Dedupe & batching:** collapse bursts (e.g., 5 rapid messages → 1 digest) and never notify a user about their **own** action unless explicitly warranted.
931. **Deliverability & compliance:** authenticated domains (SPF/DKIM/DMARC), bounce/complaint suppression, List‑Unsubscribe, CAN‑SPAM/TCPA/GDPR hygiene.
932. **Cost aware:** SES for email (default); FCM/APNs for push; SNS/Twilio for SMS behind a cost gate; in‑app first where possible.

## **1.10.B Providers & architecture**

- **Email**: Amazon **SES** (default). Optional SendGrid adapter (feature‑flag).
- **Push**: Web push via Firebase **FCM**; mobile push via **APNs** (iOS) and **FCM** (Android).
- **SMS**: AWS **SNS SMS** (default) or **Twilio** via adapter (feature‑flag & per‑country pricing).
- **In‑app**: Real‑time via AppSync subscriptions; persisted in Aurora for unread counters.

**Pipeline (event‑driven):**  
Domain event → **Comms Router** (rules engine) → **Renderer** (select template, fill variables, localize) → **Channel workers** (email/push/SMS/in‑app) → Provider → **Webhook ingesters** (deliveries, opens, bounces, complaints) → **Suppression & analytics**.

**Backpressure & retries:** SQS queues per channel with DLQ; exponential backoff with idempotency keys.

## **1.10.C Data model (Aurora + DynamoDB + S3)**

*-- 1) Template catalog (versioned)*  
*create table comms_template (*  
*template_id text primary key, -- tpl\_...*  
*name text not null, -- "booking_confirmed_buyer"*  
*version int not null,*  
*channel text not null check (channel in ('email','push','sms','inapp')),*  
*locale text not null default 'en-US',*  
*category text not null, -- 'transactional','security','legal','product','marketing'*  
*subject_mjml text, -- for email (subject pre-render)*  
*body_mjml text, -- email MJML or HTML*  
*body_text text, -- fallback plain text*  
*push_json jsonb, -- title/body/data for push*  
*sms_text text, -- SMS body*  
*inapp_json jsonb, -- in-app payload template*  
*variables_json jsonb not null, -- required vars schema*  
*is_active boolean default true,*  
*created_by text not null,*  
*created_at timestamptz not null default now(),*  
*published_at timestamptz,*  
*unique (name, version, locale, channel)*  
*);*  
  
*-- 2) Preference categories (system-defined)*  
*create table comms_category (*  
*category_id text primary key, -- cat\_...*  
*key text unique not null, -- 'booking','messages','reviews','promotions','security','legal'*  
*description text not null,*  
*critical boolean not null default false -- if true, cannot fully opt-out*  
*);*  
  
*-- 3) User preferences & quiet hours*  
*create table comms_pref (*  
*pref_id text primary key, -- prf\_...*  
*user_id text not null, -- usr\_...*  
*channel text not null check (channel in ('email','push','sms','inapp')),*  
*category_key text not null references comms_category(key),*  
*opted_in boolean not null default true, -- default true except marketing/SMS*  
*updated_at timestamptz not null default now(),*  
*unique (user_id, channel, category_key)*  
*);*  
  
*create table comms_quiet_hours (*  
*user_id text primary key, -- usr\_...*  
*tz text not null, -- IANA tz string*  
*start_local time not null, -- e.g., '21:00:00'*  
*end_local time not null -- e.g., '08:00:00'*  
*);*  
  
*-- 4) Message audit & status*  
*create table comms_message (*  
*msg_id text primary key, -- cms\_...*  
*user_id text not null, -- recipient*  
*channel text not null,*  
*template_name text not null,*  
*template_version int not null,*  
*category_key text not null,*  
*locale text not null,*  
*dedupe_key text not null, -- for collapsing bursts*  
*subject text,*  
*body_rendered_s3 text, -- emails: rendered HTML in S3 (immutable)*  
*body_text text, -- plaintext snapshot (where safe)*  
*status text not null check (status in ('queued','sent','delivered','bounced','complained','dropped','suppressed','failed')),*  
*provider_ref text, -- SES message id, etc.*  
*cause_event text not null, -- domain event name*  
*cause_ref text not null, -- leg_id/lbg_id/thread_id/etc.*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
  
*-- 5) Suppression & bounces (email/SMS)*  
*create table comms_suppression (*  
*suppress_id text primary key, -- sup\_...*  
*channel text not null,*  
*address_hash text not null, -- hashed email or phone*  
*reason text not null check (reason in ('hard_bounce','complaint','manual')),*  
*created_at timestamptz not null default now(),*  
*unique (channel, address_hash)*  
*);*  
  
*-- 6) In-app notifications*  
*create table inapp_notification (*  
*inapp_id text primary key, -- iap\_...*  
*user_id text not null,*  
*category_key text not null,*  
*title text not null,*  
*body text not null,*  
*deep_link text,*  
*unread boolean not null default true,*  
*created_at timestamptz not null default now()*  
*);*  

**DynamoDB (hot path):**

- *comms_tokens* (push tokens per device, per user, with expiry, platform).
- *comms_dedupe* (keyed by *dedupe_key*, TTL 2–5 minutes) to collapse bursts.
- *comms_queue_cursor* to preserve stable batches during paging.

**S3:**

- *comms-rendered/…* stores immutable HTML bodies & PDFs (statements) referenced by *comms_message.body_rendered_s3*.

## **1.10.D Template system & variables**

- **Authoring**: Email uses **MJML** → compiled to inline‑styled HTML. SMS uses strict text length (truncate & link to in‑app). Push uses *{title, body, data}*. In‑app stores *{title, body, deep_link}*.
- **Variables**: Declared in *variables_json* with type, description, and required flag. Types: *string*, *int*, *money_cents*, *date*, *datetime*, *duration*, *enum{…}*, *url*.
- **Localization**: Templates can exist per *locale* (start with *en-US*). Fallback: *en-US* if no locale‑specific template.

**Core templates (MVP, examples)**

- Booking lifecycle: *booking_confirmed_buyer*, *booking_confirmed_seller*, *booking_rescheduled*, *booking_cancellation_outcome*.
- Docs: *doc_sign_request*, *doc_sign_reminder*, *doc_complete*.
- Payments: *charge_receipt*, *refund_receipt*, *payout_queued*, *payout_paid*, *statement_ready*.
- Messaging: *new_message_digest*, *deliverable_posted*, *review_reminder*.
- Trust: *idv_start*, *idv_reminder*, *bg_invited*, *badge_awarded*.
- Promotions: *promo_low_balance*, *promo_statement_ready*.

*(I can include full MJML bodies upon request; they’re verbose.)*

**Variable resolution**

- Resolver library maps domain objects → template variables (e.g., leg dates in local timezone, names, amounts with currency formatting, doc links with signed URLs).
- Hard **PII minimization**: SMS never includes full names + addresses + money in the same text; use in‑app deep links.

## **1.10.E Routing rules (Comms Router)**

**Input**: domain event *{name, user_id(s), cause_ref, payload}*.

**Steps**

952. **Select template(s)** for event + role (buyer/seller/admin).
953. **Apply preferences** and **quiet hours** for the recipient (skip or schedule).
954. **Dedupe** using *dedupe_key* (e.g., *THREAD:{id}:{minute}* for rapid message bursts; *BOOKING:{lbg}:{state}*).
955. **Batch**: gather multiple low‑priority items into digest (e.g., daily message digest).
956. **Render** with locale detection; push to channel queues with idempotency keys.

**Critical overrides**

- Security, legal, receipts ignore quiet hours and opt‑out (except SMS jurisdiction where consent is required—then fallback to email/in‑app).
- If a channel is suppressed (hard bounce/complaint), auto‑fallback to in‑app + email to an alternate verified address (if present).

## **1.10.F Preferences & quiet hours (user‑facing)**

**Categories (initial)**

- *security* (critical), *legal* (critical), *booking*, *messages*, *reviews*, *promotions* (marketing), *finance* (receipts/statements).

**Defaults**

- Email: opt‑in for all except *promotions* (opt‑out default ON).
- Push: opt‑in for *booking*, *messages*, *reviews* only after device grants permission.
- SMS: **opt‑out by default**; explicit opt‑in per category where used (*booking* status or *security*).
- In‑app: always on; controlled by red dot/unread.

**Quiet hours**

- Store *tz*, *start_local*, *end_local*.
- Router schedules non‑critical notifications inside allowed windows (e.g., 8 am–9 pm local).
- Per‑category overrides (e.g., allow *booking* during quiet hours).

**GraphQL API (user settings)**

*type CommsPreference {*  
*channel: String!*  
*categoryKey: String!*  
*optedIn: Boolean!*  
*updatedAt: AWSDateTime!*  
*}*  
  
*type QuietHours { tz: String!, startLocal: String!, endLocal: String! }*  
  
*type Query {*  
*commsPreferences: \[CommsPreference!\]!*  
*quietHours: QuietHours*  
*}*  
  
*type Mutation {*  
*setCommsPreference(channel: String!, categoryKey: String!, optedIn: Boolean!): \[CommsPreference!\]!*  
*setQuietHours(tz: String!, startLocal: String!, endLocal: String!): QuietHours!*  
*unsubscribeAllEmail(): Boolean! \# sets all email categories to optedIn=false except critical*  
*}*  

**List‑Unsubscribe**

- Email headers include *List-Unsubscribe* mailto + HTTPS link to a **one‑click** suppression endpoint (sets *comms_pref* to opted‑out for marketing categories and records *comms_suppression* if required by provider).

## **1.10.G Channel workers & dedupe/batching**

**Email worker (SES)**

- Receives rendered HTML + text, sets **SPF/DKIM domains**, **List‑Unsubscribe** headers, adds **message‑id** for threading, queues to SES.
- Stores a copy of rendered HTML in S3 and writes *comms_message*.

**Push worker**

- Sends to device tokens (APNs/FCM) with *collapse_key* to dedupe on device; respects per‑device language; drops invalid tokens and prunes from *comms_tokens*.

**SMS worker**

- Enforces country gating and high cost flags; trims body to length; inserts short links; checks suppression and opt‑in.
- Templated STOP/HELP footer where required.

**Batching**

- **Message digest**: compile last N thread updates into one email if user inactive for M minutes; include counts and deep links.
- **Review reminders**: send at 24 h and 72 h unless user already reviewed; cancel if review arrives.

**Idempotency & replays**

- All workers use *(template_name, user_id, cause_ref, version)* as idempotency key; retries do not duplicate sends or audits.

## **1.10.H Error taxonomy (client‑safe and admin)**

- *COMMS_PREF_BLOCKED* — user opted out for that category/channel.
- *COMMS_QUIET_HOURS* — scheduled due to quiet hours (not an error; informational).
- *COMMS_SUPPRESSED* — address on suppression list (hard bounce/complaint).
- *COMMS_TEMPLATE_MISSING_VAR* — variable resolver missing data (developer error; logged).
- *COMMS_PROVIDER_FAIL* — provider transient error; retried with backoff.
- *COMMS_RATE_LIMITED* — SMS or push throttled.

## **1.10.I Work packages (Cursor agent lanes)**

- **Agent B — Comms Core**  
  WP‑COMMS‑01: SQL for templates/prefs/quiet‑hours/messages/suppression/in‑app.  
  WP‑COMMS‑02: Comms Router & Renderer (MJML compile, variable resolver, locale fallback).  
  WP‑COMMS‑03: Channel workers (SES, APNs/FCM, SNS/Twilio) with idempotency & retries.
- **Agent A — Web (Settings & UX)**  
  WP‑WEB‑COMMS‑01: Notification Preferences UI + Quiet Hours UI + List‑Unsubscribe landing.  
  WP‑WEB‑COMMS‑02: In‑app notification center (bell, unread counts, pagination, mark read).
- **Agent C — Integrations/Deliverability**  
  WP‑DLV‑01: Domain auth (SPF/DKIM/DMARC), bounce/complaint webhooks, suppression list processor.  
  WP‑DLV‑02: Link tracking & UTM, open pixel (email only) with privacy guardrails.
- **Agent D — Admin & QA**  
  WP‑ADM‑COMMS‑01: Template manager (versioning, preview, publish with dual approval for legal/security).  
  WP‑QA‑COMMS‑01: Full test matrix automation (see Part 2), synthetic provider sandboxes.

## **1.10.J Acceptance criteria (for Part 1) — we won’t move to Part 2 until all hold**

986. Template catalog exists with MJML→HTML render and variable schemas; at least the MVP templates are authored (booking, docs, payments, messages, trust, promotions).
987. Providers wired (SES, APNs/FCM, SNS/Twilio behind flags); Comms Router applies preferences, quiet hours, dedupe, and batching.
988. Message audits stored with immutable link to rendered bodies (email) or payload snapshots (push/SMS/in‑app).
989. User Preference & Quiet Hours UI/APIs functional; List‑Unsubscribe endpoints live and audited.
990. Channel workers respect cost gates (e.g., SMS limited to critical flows where configured).
991. Idempotency & retries verified; dedupe prevents burst spam.

# **§1.10 — Notifications & Comms**

**Part 2/2: deliverability, suppression, in‑app center, experiments & localization, tracking & privacy, admin, telemetry/SLOs, full test matrix, acceptance**

This completes the communications layer begun in §1.10 (Part 1). We won’t move to the next major subsection until §1.10 passes the 99.9% bar.

## **1.10.R Deliverability setup (email)**

**R.1 Domain authentication (SES, production domain e.g.,** ***notify.rastup.com*****)**

- **SPF**: *v=spf1 include:amazonses.com -all*
- **DKIM**: enable **Easy DKIM** in SES; publish 3 CNAMEs; rotate annually (calendar reminder + auto‑rotate playbook).
- **DMARC**: start with *v=DMARC1; p=quarantine;* [*rua=mailto:dmarc@rastup.com*](mailto:rua=mailto:dmarc@rastup.com)*;* [*ruf=mailto:dmarc@rastup.com*](mailto:ruf=mailto:dmarc@rastup.com)*; fo=1; pct=50*, graduate to *p=reject* after warmup.
- **BIMI** (optional, post‑DMARC‑reject): publish SVG logo and VMC (later, cost‑gated flag).

**R.2 SES configuration**

- Verify domain + sender identities ([*no-reply@notify.rastup.com*](mailto:no-reply@notify.rastup.com) for system, *billing@notify…* for finance, *support@…* for support).
- **Event destinations** → SNS topics for *Delivery*, *Bounce*, *Complaint*, *Open* (optional), *Click* (optional).
- Shared IPs at MVP; consider **dedicated IPs** after steady volume (requires warmup).

**R.3 IP warmup (if dedicated IPs)**

- Ramp plan for first 2–4 weeks: daily volume ladder + mix of high‑engagement templates (booking receipts) to build reputation.
- Dashboards: deliverability by mailbox provider (Gmail, Outlook, Yahoo), bounce/complaint thresholds.

**R.4 From/Reply‑To policy**

- Transactional: *From: RastUp \<no-reply@notify…\>* with **Reply‑To support** when useful.
- Avoid sending marketing from transactional subdomain.

## **1.10.S Bounce/complaint handling & suppression**

**S.1 Webhooks → suppression list**

- **Hard bounce** or **complaint** → write *comms_suppression* (*channel='email'*, *reason='hard_bounce'\|'complaint'*, *address_hash=SHA256(email)*), set *comms_message.status='bounced'\|'complained'*.
- **Soft bounces** (4xx) → retry with backoff; if ≥3 within 72h → convert to suppression (*reason='manual'*) pending user correction.

**S.2 Unsubscribe & re‑permissioning**

- **List‑Unsubscribe**: one‑click HTTPS endpoint sets *comms_pref.email.promotions=false* (and any non‑critical marketing categories).
- Re‑permission only via explicit user action in settings; no automatic re‑enable after a bounce/complaint.

**S.3 Global blocklist**

- Maintain **platform blocklist** (legal/compliance). Any send to these addresses is dropped with *status='suppressed'* and audited.

## **1.10.T In‑app Notification Center (details)**

**T.1 Data & pagination**

- *inapp_notification* (already defined) stores immutable items; add indices for *(user_id, created_at desc)*.
- Pagination: cursor by *(created_at, id)* to ensure stable ordering.

**T.2 UX contract**

- **Bell** icon shows unread count; badge hides during DND/quiet hours logic (but count still increments).
- **Grouping**: coalesce similar events (e.g., “3 new thread updates”).
- **Actions**: “Mark all read”, per‑item “Mark read”, per‑group clear.
- **Pinning**: high‑priority items (security, legal) appear pinned until dismissed.

**T.3 Retention**

- Default retention 90 days; archive older items (user can fetch via “Load older” until 1 year, then cold storage).
- Privacy: no sensitive PII in in‑app bodies; deep link to secure pages.

## **1.10.U Experiments & localization**

**U.1 Experiments**

- **Bucketing**: sticky, per user (UUID‑v4 salted hash).
- Testable assets: email subject/preview text, CTA wording, send‑time (outside quiet hours), digest cadence.
- Metrics: delivery→open→click→conversion, unsubscribe delta; guardrails (bounce/complaint ceilings).
- Rollouts: feature flag controls + staged %; automatic rollback on guardrail breach.

**U.2 Localization**

- Locale resolution order: user setting → browser *Accept-Language* → city default → *en-US*.
- Templates per locale (name/version stable). Fallback to *en-US* when missing.
- Pluralization rules (CLDR), local date/time formatting using recipient’s **timezone** (from quiet hours setting).
- Right‑to‑Left support in MJML (dir attribute), font fallback stacks.

## **1.10.V Link tracking & privacy**

- **Link wrapper**: */l/{token}* where *token = HMAC(user_id\|template_name\|msg_id\|url)*; logs *click* then 302 to *url*.
- **No tracking** for security/legal emails (privacy first) and unsubscribe links.
- **Open pixel** optional; respect **DNT** and suppress tracking for sensitive categories.
- **UTM** parameters for non‑critical emails only; strip PII.
- **Data minimization**: SMS never includes full names + full addresses + amounts in combination; use in‑app deep links.

## **1.10.W Admin console (Comms)**

- **Template Manager**: search, diff, preview (with sample variables), MJML validation, multi‑locale versions, **dual approval** for security/legal templates; staged rollout with kill‑switch.
- **Test send**: to whitelisted addresses only; record as *status='sent'* with *cause_event='admin.test'*.
- **Suppression Viewer**: search by hashed email/phone; show reasons; **re‑permission** only on explicit user opt‑in.
- **Campaigns/Digests**: configure digest cadence, review experiment assignments; simulate send volumes with cost estimates.
- **Audit log**: all admin actions immutable with actor, reason, diffs.

## **1.10.X Telemetry, dashboards & SLOs**

**X.1 Metrics**

- Volume per channel, delivery %, soft/hard bounces, complaints, opens, clicks, unsubscribe rate, digest suppression %, send latency (event→queue→provider), cost per 1k sends (email/SMS), push invalid token rate.

**X.2 SLOs**

- Event→queued **≤ 150 ms p95**; queued→provider **≤ 1 s p95**.
- Delivery rate ≥ **98.5%** on transactional (ex‑bounces/complaints).
- Complaint rate ≤ **0.1%**; hard bounce ≤ **0.3%** rolling 7‑day.
- In‑app notification fetch **≤ 120 ms p95**.

**X.3 Alerts**

- Bounce/complaint spikes by provider; quiet‑hours scheduler backlog; SMS spend anomalies; push invalid token surges.

## **1.10.Y Full test matrix (Part 2)**

**Deliverability**

1040. SPF/DKIM/DMARC pass; BIMI optional path.
1041. Shared IP warm sends; dedicated IP warmup plan verified (if enabled).
1042. From/Reply‑To policies applied; DMARC alignment OK.

**Suppression**  
4) Hard bounce → suppression; retry rules for soft bounces; complaint → global suppression.  
5) One‑click unsubscribe toggles correct categories; re‑permission requires explicit user action.

**In‑app**  
6) Pagination, grouping, unread counts, pinning; accessibility roles/labels.

**Experiments**  
7) Stable bucketing; hold‑out analyses; guardrail auto‑rollback triggers.

**Localization**  
8) Locale fallback path; pluralization; timezone formatting.

**Tracking & privacy**  
9) Link wrapper logs click; no tracking for security/legal; UTM only on allowed templates; DNT honored.

**Admin**  
10) Template versioning diff + dual approval; test sends whitelisted only; suppression viewer actions audited.

**Performance & cost**  
11) Event→send SLOs met under synthetic load; SMS cost gates observed; SES cost within envelope.

## **1.10.Z Acceptance criteria — mark §1.10 FINAL only when ALL true**

1043. **Comms Router** applies preferences, quiet hours, dedupe/batching; channel workers deliver idempotently with retries.
1044. Domain authentication (SPF/DKIM/DMARC) configured; bounces/complaints generate suppressions; unsubscribe pathway honored.
1045. In‑app notification center functions with grouping, unread, pinning, and retention; p95 ≤ 120 ms.
1046. Experiments and localization pipelines operate with guardrails and correct fallbacks.
1047. Link tracking respects privacy rules; no tracking on sensitive templates; DNT honored.
1048. Admin console supports template lifecycle, test sends, suppression viewing, and campaign controls with immutable audits and dual approvals where required.
1049. Telemetry & SLOs green for 48h synthetic run; costs within budget alarms.

# **§1.11 — Studios (Place Listings) & Amenities**

*(data model · onboarding & verification · pricing & deposits · availability & buffers · attach‑in‑flow · search facets · images & safety · house rules & compliance docs · APIs · admin · telemetry · tests · cost)*

**Purpose.** Specify studios as **place listings** that buyers can book directly or attach in‑flow to a talent booking. Studios are distinct commercial legs with independent policies, taxes, deposits, reviews, payouts, and verification—never mixed with person (Service Profile) ratings or badges.

## **1.11.A Canon & invariants**

1050. **Studios are places**, not people. Ratings, verification, search facets, and policies are **separate** from Service Profiles (SPs).
1051. **Independent leg math**: a Studio leg has its own price, taxes, deposit policy, refunds, receipts, payout, and dispute/deposit-claim flows (see §1.3).
1052. **Attach‑in‑flow**: a Studio can be added during Talent checkout. Confirmation is **atomic** across legs (all‑or‑nothing).
1053. **Verification before boost**: only **verified studios** are eligible for “Verified Studio” badge and advertising (see §1.7).
1054. **Safe content**: public thumbnails are SFW; NSFW scanning rules apply to any images.
1055. **Cost‑conscious**: asset storage minimal (previews only), intelligent S3 tiering, lean search indices, and throttled scans.

## **1.11.B Data model (Aurora Postgres, source of record)**

*create table studio (*  
*studio_id text primary key, -- std\_...*  
*owner_user_id text not null, -- usr\_...*  
*title text not null,*  
*slug text not null unique, -- /studio/{slug}*  
*description text not null,*  
*city text not null,*  
*region text not null, -- state/province*  
*country text not null default 'US',*  
*geo_lat numeric(9,6) not null,*  
*geo_lon numeric(9,6) not null,*  
*address_json jsonb not null, -- {line1,line2,city,region,postal,country}; private UI*  
*is_published boolean not null default false,*  
*verified_studio boolean not null default false,*  
*verification_json jsonb not null default '{}'::jsonb, -- docs summary (no images)*  
*deposit_required boolean not null default false,*  
*deposit_auth_cents int not null default 0, -- default auth amount (can be 0)*  
*capacity_people int not null default 0,*  
*size_sqft int, -- optional*  
*house_rules_json jsonb not null default '\[\]'::jsonb,*  
*amenities_json jsonb not null default '\[\]'::jsonb, -- string\[\] canonical keys*  
*insurance_confirmed boolean not null default false,*  
*rating_avg numeric(3,2) not null default 0.00,*  
*rating_count int not null default 0,*  
*price_from_cents int not null default 0, -- normalized floor*  
*currency text not null default 'USD',*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
  
*-- Pricing schedules (hourly, slot, or day rates with peak/off-peak)*  
*create type studio_rate_kind as enum ('hourly','slot','day');*  
  
*create table studio_rate (*  
*rate_id text primary key, -- srt\_...*  
*studio_id text not null references studio(studio_id) on delete cascade,*  
*kind studio_rate_kind not null,*  
*name text not null, -- "Weekday Hourly", "Weekend Slot"*  
*dow int\[\] not null, -- 0=Sun..6=Sat*  
*start_local time not null, -- for 'hourly' window or slot start*  
*end_local time not null, -- for 'hourly' window or slot end*  
*slot_minutes int, -- required for 'slot'*  
*price_cents int not null, -- per hour/slot/day depending on kind*  
*overtime_cents_per_30m int not null default 0,*  
*min_booking_minutes int not null default 60,*  
*max_booking_minutes int, -- optional cap*  
*tax_inclusive boolean not null default false, -- rarely true; standard is false*  
*active boolean not null default true,*  
*created_at timestamptz not null default now()*  
*);*  
  
*-- Blackouts and buffers*  
*create table studio_blackout (*  
*blackout_id text primary key, -- sbo\_...*  
*studio_id text not null references studio(studio_id) on delete cascade,*  
*start_at timestamptz not null,*  
*end_at timestamptz not null,*  
*reason text*  
*);*  
  
*-- Default buffers & cleanup windows (applies to all bookings unless overridden)*  
*create table studio_policy (*  
*studio_id text primary key references studio(studio_id) on delete cascade,*  
*buffer_before_min int not null default 30,*  
*buffer_after_min int not null default 30,*  
*cleaning_min int not null default 0,*  
*cancellation_policy jsonb not null default '{}'::jsonb -- bands like §1.3.L*  
*);*  
  
*-- Media (previews only; S3 keys; NSFW band)*  
*create table studio_media (*  
*media_id text primary key, -- smd\_...*  
*studio_id text not null references studio(studio_id) on delete cascade,*  
*kind text not null check (kind in ('image','video')),*  
*s3_key text not null,*  
*width int,*  
*height int,*  
*nsfw_band int not null default 0, -- 0 allow, 1 blur, 2 block*  
*position int not null default 0,*  
*created_at timestamptz not null default now()*  
*);*  
*create index on studio_media(studio_id, position);*  
  
*-- Studio verification audit trail*  
*create table studio_verification_audit (*  
*sva_id text primary key, -- sva\_...*  
*studio_id text not null references studio(studio_id) on delete cascade,*  
*action text not null check (action in ('submitted','approved','rejected','revoked')),*  
*actor_user_id text not null, -- admin*  
*reason text,*  
*created_at timestamptz not null default now()*  
*);*  

**Indices**

- *studio(city, is_published)* for city listing.
- *studio(owner_user_id, updated_at desc)* for owner dashboards.
- Partial index: *studio(is_published and verified_studio)* for search gating.

## **1.11.C Amenity taxonomy (canonical keys)**

Start with a small, expressive set (expandable in Admin):

- **Lighting**: *natural_light*, *north_light*, *blackout*, *strobe_included*
- **Backdrops**: *paper_seamless*, *cyc_wall*, *green_screen*
- **Facilities**: *makeup_area*, *dressing_room*, *restroom*, *kitchenette*
- **Logistics**: *parking*, *freight_elevator*, *ground_floor*, *loading_dock*
- **Comfort**: *ac*, *heating*, *wifi*
- **Audio**: *sound_treated*, *basic_audio_kit*
- **Furnishings/Props**: *props_basic*, *furniture_variety*
- **Power**: *30a_circuits*, *multiple_outlets*

Admin can add synonyms and groupings that feed search facets (see §1.2.N).

## **1.11.D Onboarding & verification flow**

**Owner tasks**

1067. Create listing (title, description, address, city/geo).
1068. Add **amenities**, **capacity**, **pricing schedules**, **buffers**, **house rules**, and **deposit policy**.
1069. Upload **previews** (scanned; SFW).
1070. Submit **verification**: proof of control/ownership (lease/utility), IDV match to owner (see §1.6), optional insurance cert.

**Admin verification**

- Review docs; optional video call or geo‑code match.
- **Approve** → *verified_studio=true* and studio gets badge; **Reject** → return reasons.
- **Revoke** when reports or insurance lapse; all actions audited in *studio_verification_audit*.

**Publishing gate**

- Cannot publish unless required fields + minimum media count met and **house rules** present. Verification not required to publish, but required for some placements/promotions.

## **1.11.E Pricing & quote engine (deterministic)**

**Inputs**: date/time, duration, studio_id, rate schedule, buffers/cleaning, deposit policy.  
**Steps**

1075. **Resolve rate** by DOW and local time window:

      145. *Hourly*: within a rate window; price = ceil(duration / 60) \* hourly rate.
      146. *Slot*: duration must equal *slot_minutes*; price = slot price.
      147. *Day*: flat day price.

1076. **Apply minimums/maximums**.

1077. **Compute buffers**: ensure surrounding time is free (*buffer_before_min*, *buffer_after_min*, *cleaning_min*).

1078. **Overtime** (if requested or if stop late): price per 30m bucket from *overtime_cents_per_30m*.

1079. **Taxes**: quote service tax by city via adapter (see §1.3.E).

1080. **Deposit**: show **auth amount** (not part of GMV).

1081. **Total** per leg: *subtotal + service tax + platform fee + fee tax* (platform portions from §1.9).

**Edge cases**

- Split windows (e.g., crossing two hourly windows): either disallow or pro‑rate (MVP: disallow).
- Overlapping slot/day with hourly: pick the best matching schedule deterministically.

## **1.11.F Availability, buffers & conflicts**

**Authoritative blocks** are **accepted/confirmed** booking legs + **blackouts**. *availability_json* is a hint for search only.

- On **propose/confirm**, we check for **overlaps + buffers** (before/after + cleaning).
- On **amend/reschedule**, re‑check conflict rules; if conflict, fail with *STUDIO_CONFLICT_BUFFER* or *STUDIO_BLACKOUT*.

**Calendar feeds**

- Generate **read‑only ICS** for owners (includes upcoming bookings + buffers), redacted buyer names.
- Optionally import a Google Calendar read‑only feed for soft conflicts (advisory). Hard conflicts are our DB.

## **1.11.G House rules & compliance docs**

**House rules** live on the **Studio leg doc pack** (see §1.5). Examples: no glitter, no smoke machines, pet policy, quiet hours, cleanup expectations, insurance requirements.

- **Deposit policy** language must match *deposit_required* and *deposit_auth_cents*.
- Any change to house rules that materially affects obligations **invalidates** existing doc packs for future bookings → re‑issue required.

## **1.11.H Images, safety & SEO**

- Previews only; scanned for NSFW/PII per pipeline; Safe‑Mode ON for public; private pages show more but still SFW.
- **Ordering** by *position*; first image becomes listing thumbnail.
- **Alt text** derived from title/amenities for accessibility.
- Optional **virtual tour** (flagged; link rather than storage).

## **1.11.I Search facets (tie‑in to §1.2)**

- **Collection**: *studios_v1* (already defined).
- **Facets**: city, amenities\[\], verifiedStudio (bool), depositRequired (bool), capacity buckets, priceFromCents, ratingAvg, availability day buckets.
- **Sort**: default → text match → verified → rating → price distance from user budget → recency.
- **Safe‑Mode**: block nsfw_band=2 from thumbnails.

## **1.11.J Checkout & deposits (tie‑in to §1.3)**

- Studio leg participates in **atomic LBG confirm**.
- **Deposit auth** handled via **SetupIntent** (separate from GMV).
- **Overtime** & **extras** use the amendment flow (§1.3.K).
- **Deposit claims** handled post‑session with evidence (§1.3.N).
- Cancellation policy bands live in *studio_policy.cancellation_policy*.

## **1.11.K GraphQL API (AppSync) — Studio management & browse**

*\# Types*  
*type Studio {*  
*studioId: ID!*  
*title: String!*  
*slug: String!*  
*description: String!*  
*city: String! region: String! country: String!*  
*geo: Geo!*  
*capacityPeople: Int!*  
*sizeSqft: Int*  
*amenities: \[String!\]!*  
*verifiedStudio: Boolean!*  
*depositRequired: Boolean!*  
*depositAuthCents: Int!*  
*houseRules: \[String!\]!*  
*insuranceConfirmed: Boolean!*  
*priceFromCents: Int!*  
*ratingAvg: Float!*  
*ratingCount: Int!*  
*media: \[Media!\]!*  
*isPublished: Boolean!*  
*}*  
  
*type StudioRate {*  
*rateId: ID!*  
*kind: String!*  
*name: String!*  
*dow: \[Int!\]!*  
*startLocal: String!*  
*endLocal: String!*  
*slotMinutes: Int*  
*priceCents: Int!*  
*overtimeCentsPer30m: Int!*  
*minBookingMinutes: Int!*  
*maxBookingMinutes: Int*  
*taxInclusive: Boolean!*  
*active: Boolean!*  
*}*  
  
*\# Queries*  
*type Query {*  
*studio(slug: String!): Studio!*  
*myStudios: \[Studio!\]!*  
*studioRates(studioId: ID!): \[StudioRate!\]!*  
*studioAvailability(studioId: ID!, from: AWSDateTime!, to: AWSDateTime!): \[DateTimeRange!\]!*  
*}*  
  
*\# Mutations*  
*input StudioInput {*  
*title: String!, description: String!, city: String!, region: String!, country: String!,*  
*lat: Float!, lon: Float!, address: AddressInput!,*  
*amenities: \[String!\]!, capacityPeople: Int!, sizeSqft: Int,*  
*depositRequired: Boolean!, depositAuthCents: Int!, houseRules: \[String!\]!,*  
*insuranceConfirmed: Boolean!*  
*}*  
  
*type Mutation {*  
*createStudio(input: StudioInput!): Studio!*  
*updateStudio(studioId: ID!, input: StudioInput!): Studio!*  
*publishStudio(studioId: ID!): Studio!*  
*unpublishStudio(studioId: ID!): Studio!*  
  
*addStudioRate(studioId: ID!, rate: StudioRateInput!): StudioRate!*  
*updateStudioRate(rateId: ID!, rate: StudioRateInput!): StudioRate!*  
*deleteStudioRate(rateId: ID!): Boolean!*  
  
*addStudioMedia(studioId: ID!, media: MediaInput!): Media!*  
*reorderStudioMedia(studioId: ID!, order: \[ID!\]!): Boolean!*  
*deleteStudioMedia(mediaId: ID!): Boolean!*  
  
*addStudioBlackout(studioId: ID!, range: DateTimeRange!, reason: String): Boolean!*  
*deleteStudioBlackout(blackoutId: ID!): Boolean!*  
  
*submitStudioVerification(studioId: ID!, docs: \[Upload!\]!): Boolean!*  
*}*  

**Guards & rules**

- Publish gate: required fields, minimum media, house rules present.
- Verification submission requires owner IDV passed (from §1.6).
- Media upload uses signed S3 URLs; scans run async; blocked images don’t appear in public.

## **1.11.L Admin console (Studios)**

- **Verification queue**: view submissions, approve/reject/revoke; reasons mandatory; immutable audits.
- **City gate**: gate newly published studios by city (on/off switch).
- **Policy editor**: set default cancellation bands; override per studio.
- **Amenity taxonomy**: add/rename synonyms and groups (publishes to search analyzer).
- **Pricing inspector**: simulate a quote for a date/time to debug owner configs.
- **Owner integrity**: show owner trust badges, dispute/late metrics.

## **1.11.M Error taxonomy (client‑safe)**

- *STUDIO_INCOMPLETE* — cannot publish; missing fields or media.
- *STUDIO_CONFLICT_BUFFER* — requested time conflicts after buffers/cleaning.
- *STUDIO_BLACKOUT* — requested time falls in blackout.
- *STUDIO_RATE_NOT_FOUND* — no applicable rate for requested window.
- *STUDIO_VERIFY_REQUIRED* — action requires verified studio (e.g., promotions).
- *STUDIO_MEDIA_BLOCKED* — preview blocked by safety rules.

Errors return *code*, *message*, *hint*, and a correlation id.

## **1.11.N Telemetry & lineage**

- studio.create\|update\|publish\|unpublish
- studio.rate.add\|update\|delete
- studio.media.add\|blocked\|delete
- studio.verification.submitted\|approved\|rejected\|revoked
- studio.blackout.add\|delete
- *studio.quote.request\|response* (with amounts)
- Correlate with owner *user_id* and booking *leg_id* where relevant.

Dashboards: verified share by city, quote success rate, conflict rates, amenity filter usage, conversion.

## **1.11.O Performance & cost**

- **Search**: small *studios_v1* index; cache results for 60–120s; availability buckets precomputed daily.
- **Storage**: S3 previews only; lifecycle to Intelligent‑Tiering after 30 days; delete orphans after 30 days.
- **Compute**: Lambdas for scans/transforms; quote engine runs in BFF with memoized rate lookups.
- **Maps/geo**: no heavy polygons at MVP; simple radius; pre‑computed city centroids.

## **1.11.P Test plan (CI + sandbox)**

**Onboarding & verification**

1129. Create studio with mandatory fields; cannot publish until media + house rules present.
1130. Submit verification; approve → badge appears; reject → reasons surfaced; revoke path.

**Pricing & quotes**  
3) Hourly/slot/day quotes across DOW windows; min/max duration rules; buffers enforced.  
4) Overtime quote appended via amendment flow.  
5) Tax quote correct per city; deposit auth amount surfaced but not included in GMV.

**Availability & conflicts**  
6) Blackout block; buffer conflicts on adjacent bookings; ICS feed integrity.

**Search & facets**  
7) Amenity filters; deposit required toggle; verified badge facet; ranking respects verified + rating.

**Media & safety**  
8) NSFW scan blocks unsafe previews; blur for band=1; ordering respected.

**Checkout & deposit**  
9) Attach‑in‑flow: atomic confirm (Studio+Talent) succeeds/fails together.  
10) Deposit claim flow: claim within window; capture or deny; receipts updated.

**Admin**  
11) Verification audit trail; policy editor; taxonomy updates push to search analyzer.

**Performance**  
12) Quote engine p95 \< 120 ms; search p95 unchanged with facets; media upload pipeline cost within limits.

## **1.11.Q Work packages (Cursor 4‑agent lanes)**

- **Agent B — Domain/API**  
  WP‑STD‑01: SQL migrations (*studio*, *studio_rate*, *studio_policy*, *studio_blackout*, *studio_media*, *studio_verification_audit*).  
  WP‑STD‑02: GraphQL resolvers for Studio CRUD, rates, media, blackouts, verification.  
  WP‑STD‑03: Quote engine + buffer/conflict checks; ICS feed generator.
- **Agent C — Integrations**  
  WP‑STD‑INT‑01: Media scan + transform Lambdas; NSFW + antivirus; S3 lifecycle.  
  WP‑STD‑INT‑02: Tax quoting for studio services; deposit auth via SetupIntent (already in §1.3).
- **Agent A — Web**  
  WP‑STD‑WEB‑01: Studio create/edit wizard (amenities, pricing, rules, deposit).  
  WP‑STD‑WEB‑02: Public Studio page; search facet UI; attach‑in‑flow picker in checkout.
- **Agent D — Admin & QA**  
  WP‑STD‑ADM‑01: Verification queue; policy editor; taxonomy manager; pricing inspector.  
  WP‑STD‑QA‑01: Full test matrix automation + synthetic data fixtures.

## **1.11.R Acceptance criteria (mark §1.11 FINAL only when ALL true)**

1135. Studio onboarding, publish, and verification operate end‑to‑end with audits.
1136. Quote engine computes hourly/slot/day correctly; buffers/blackouts enforced; taxes and deposit surfaced correctly.
1137. Attach‑in‑flow Studio works with **atomic** LBG confirm; deposit auth is separate and captured only on approved claim.
1138. Search facets (amenities, verified, deposit, capacity, price) function; Safe‑Mode rules hold.
1139. Media pipeline scans/blocks unsafe previews; ordering and thumbnails correct; S3 lifecycle active.
1140. Admin tools (verification, policy editor, taxonomy) function with immutable audits.
1141. Telemetry complete; p95 perf within targets; costs within budget alarms through 48h synthetic run.

# **§1.12 — Platform & Infrastructure (Amplify Gen 2 Foundation, Environments, Security, Cost)**

*(code‑first Amplify, infra topology, CI/CD, auth, data stores, observability, budgets, DR, and developer workflow)*

**Purpose.** Establish a cost‑conscious, elastic, and auditable foundation that can carry us from **build → launch → growth** without re‑platforming. This section guarantees we’re on **Amplify Gen 2 (code‑first/CDK)**—**not** Classic—while wiring AppSync, Cognito, S3/CloudFront, Aurora, DynamoDB, Step Functions, SQS, EventBridge, WAF, and our optional engines (Typesense/OpenSearch). It includes IaC, environments, secrets, runtime limits, budgets, SLOs, admin access controls, and a full test plan.

We will not advance to the next subsection until §1.12 meets your 99.9% bar.

## **1.12.A Canon & invariants**

1142. **Amplify Gen 2 only (code‑first)**: infrastructure expressed in CDK within the repo; no Amplify Classic “console‑first” projects. We add guardrails to prevent accidental Classic usage (see §1.12.D).
1143. **Serverless by default** for elasticity and cost: Aurora Serverless v2 for relational, DynamoDB for hot‑path messaging, Lambda/AppSync for compute, S3/CloudFront for media, Step Functions for sagas.
1144. **One source of truth (IaC)**: every resource is created via CDK/Amplify Gen 2 stacks in Git; no click‑ops in prod.
1145. **Multi‑environment** (dev, stage, prod) with separate AWS accounts, least privilege, and per‑env DNS.
1146. **Security & privacy by design**: KMS, WAF, VPC boundaries, least‑priv IAM, PII minimization, age‑gate/safe‑mode enforcement server‑side.
1147. **Cost controls baked in**: budgets/alerts, right‑sized defaults, lifecycle policies, OCU/RCU caps, and CI step gates when a change increases spend.

## **1.12.B Tech stack & version pins (initial)**

- **Frontend:** Next.js (App Router), React 18, TypeScript 5, Node LTS.
- **Hosting & Edge:** Amplify Hosting + CloudFront; ISR/SSR enabled where needed.
- **BFF/API:** AWS AppSync (GraphQL) + Lambda resolvers (Node 20), with pipeline resolvers for auth, validation, and rate‑limits.
- **Auth:** Amazon Cognito (User Pool + Identity Pool).
- **Relational:** Amazon Aurora PostgreSQL **Serverless v2** (multi‑AZ, autoscaling).
- **NoSQL/Hot path:** DynamoDB (messaging, presence, comms dedupe, ads caches, trust cache).
- **Search:** **Typesense** (MVP) with optional adapter to **OpenSearch Serverless** (feature‑flag).
- **Queues/Orchestration:** SQS + SNS + EventBridge; AWS Step Functions for §1.3 saga.
- **Object storage & CDN:** S3 (private + public buckets) + CloudFront; Lambda@Edge for image transforms; optional MediaConvert (flag).
- **Moderation:** Rekognition/Vision model (NSFW banding); ClamAV Lambda for basic AV.
- **E‑sign:** Dropbox Sign or DocuSign via adapter (flag).
- **Payments/Tax:** Stripe (+ Financial Connections for ACH) and TaxJar/Avalara/Stripe Tax via adapter.

**Suggested modules:** we adopt cost‑efficient open‑source options where safe (e.g., Typesense, MJML for email, image proxy), and keep vendor count minimal (Stripe handles cards + ACH).

## **1.12.C Environments, accounts, and regions**

- **Accounts:** *rastup-dev*, *rastup-stage*, *rastup-prod*.

- **Region:** default **us-east-1** (broadest service coverage, SES deliverability), with room to add read replicas or S3 CRR later.

- DNS:

  - App: *app.dev.rastup.com*, *app.stage.rastup.com*, *app.rastup.com*.
  - Email: *notify.rastup.com* (SES—see §1.10).

- **Secrets & config:** AWS Secrets Manager for secrets; AWS AppConfig for feature flags and city gates.

**Branch mapping (Amplify Hosting):**

- *feature/\** → ephemeral previews (cost-capped; auto‑destroy 48h after last update).
- *main* → **stage**; *release/\** → **prod** via approved promotion.
- *develop* → **dev**.

## **1.12.D Amplify Gen 2 configuration (and “never Classic” guardrails)**

**Repo structure (illustrative):**

*/amplify/*  
*stack.ts \# CDK app entry for Amplify Gen 2*  
*backend/*  
*auth/ (Cognito)*  
*api/ (AppSync schema & functions)*  
*storage/ (S3, Dynamo)*  
*functions/ (Lambdas)*  
*observability/ (CW dashboards, alarms)*  
*search/ (Typesense/OpenSearch stack)*  
*cdk.json*  
*/bin/infra.ts \# CDK app bootstrap for non-Amplify stacks (optionally)*  
*/packages/ (web, bff libs, shared types)*  
*/apps/web (Next.js)*  
*/apps/indexer (indexing worker)*  
*/apps/renderer (docs/pdf)*  

**Guardrails to avoid Classic:**

- CI check: **fail build** if an *amplify/cli.json* or *team-provider-info.json* (Classic) is introduced.
- Only accept PRs that modify CDK stacks under */amplify/backend/\*\**.
- Run *amplify status* (Gen 2) and diff in CI; deny merge if detected drift or unmanaged resources.

**Stacks (high-level CDK):**

- **AuthStack** (Cognito pools, Hosted UI, OAuth providers).
- **ApiStack** (AppSync, GraphQL schema, Lambda functions, role policies).
- **DataStack** (Aurora cluster, Dynamo tables, Secrets, Subnets).
- **SearchStack** (Typesense ECS/Fargate or managed option; or OpenSearch Serverless w/ OCU cap).
- **MediaStack** (S3 buckets, CloudFront, Lambda@Edge image resizer, WAF).
- **WorkflowStack** (SQS, EventBridge, Step Functions).
- **ObservabilityStack** (CloudWatch dashboards, alarms, X‑Ray, logs retention).
- **CommsStack** (SES identities, SNS/SQS for bounces, in‑app store).
- **AdminStack** (Amplify Admin UI access scopes, RBAC seeds).

## **1.12.E Networking & security baseline**

- **VPC** for Aurora + Typesense/OpenSearch; Lambdas in private subnets with NAT **only where needed** (watch NAT cost).
- **Security groups**: least privilege; no public RDS; AppSync → Lambda via VPC endpoints if required.
- **WAF** on CloudFront: bot rate limits, SQLi/XSS rules, country blocks (configurable).
- **TLS**: ACM certs for all domains; enforced HTTPS everywhere.
- **KMS**: CMKs for RDS, Dynamo, S3 buckets (customer-managed where necessary).
- **CORS & CSP**: locked to app domains + Stripe/e‑sign domains.
- **PII partitioning**: sensitive data in Aurora; no PII in search indexes or logs.

## **1.12.F Data stores & retention**

**Aurora (PostgreSQL Serverless v2)**

- **Schemas:** *core* (users, profiles, bookings), *finance*, *docs*, *promo*, *trust*, *studios*, *comms*.
- **Backups:** PITR enabled; snapshots retained 7–30 days in dev/stage, 35–90 days in prod.
- **Migrations:** Sqitch/Prisma/Migrate (choose one; locked in CI).

**DynamoDB**

- Tables: *threads*, *presence*, *comms_tokens*, *comms_dedupe*, *promo_active_by_city*, *trust_cache*.
- **TTL**: presence/typing; dedupe caches; in‑app archivals after 90 days.

**S3**

- Buckets: *public-assets*, *user-previews*, *docs-rendered*, *logs-raw*.
- **Lifecycle:** move to Intelligent‑Tiering after 30 days; cold/archive after 90/180 days where safe.
- **Block public access** by default; use CF OAI/ORI for public access.

**Search**

- **Typesense** single small node (or managed) at launch; replica optional.
- Adapter layer ready to switch to **OpenSearch Serverless** if scale demands; **OCU** cap alarms.

## **1.12.G Identity & access (Cognito)**

- **User Pool** with hosted UI (email, Apple/Google OAuth).
- **Groups/Roles:** *buyer*, *seller*, *studio_owner*, *admin*, *trust*, *support*, *finance*.
- **MFA** optional at signup; required for Admin roles.
- **Age‑gate** attribute on user (*\>18*) linked to IDV status (§1.6).
- **Identity Pool** for S3 direct uploads (scoped IAM policies per bucket/prefix).
- **Session length** tuned per role; refresh token rotation.

## **1.12.H API shape (AppSync)**

- **Schema‑first** in repo; codegen to TS types.

- **Auth modes**: Cognito JWT (primary) + API key (dev only) + IAM (admin tools).

- **Pipeline resolvers** enforce:

  - input validation & normalization
  - rate limits (token bucket per IP/user)
  - role/age gates (e.g., Fan‑sub)

- **Subscriptions** for messaging & notifications.

**Limits**: page sizes capped; cursors opaque; error taxonomy standardized per prior sections.

## **1.12.I CI/CD and migrations**

- **CI (per PR):** typecheck, lint, unit tests, contract tests for GraphQL, build Next.js, synth CDK, **cost‑diff** (cdk‑nag + infracost if configured).

- **DB migrations**: gated step; runs against dev and stage; prod migrations require approval & safe mode (online migrations, lock‑timeout, backfills through batch jobs).

- Deploy:

  - *develop* → dev, auto.
  - *main* → stage, auto with smoke tests.
  - *release/\** → prod, requires approvals; feature flags off by default, enabled progressively.

**Feature flags** via AppConfig: search promotions, LBG, deposits, Fan‑sub, OpenSearch switch, instant payouts, etc.

## **1.12.J Observability**

- **Metrics**: p50/p95/p99 latency, error rates per resolver/function, queue depths, index lag, OCU/RCU/ACU usage, Stripe/tax/e‑sign error rates.
- **Logs**: structured JSON; correlation ids from edge → backend; PII scrubbers.
- **Tracing**: X‑Ray/OpenTelemetry from AppSync → Lambda → DB.
- **Dashboards/Alerts**: SLO burn alerts, 5xx spikes, RDS ACU thrash, Dynamo throttles, WAF blocks, SES bounce/complaint spikes.

## **1.12.K Security posture**

- **Least‑privilege IAM** for each Lambda.
- **Secrets** in Secrets Manager; rotation policies; no secrets in env vars.
- **WAF** with bot control & rate limits (different thresholds for search, auth, checkout).
- **Abuse** mitigations: captcha challenges for signup bursts; email domain denylist; phone verification for payouts.
- **Backups & keys**: scheduled audits for restore drills and KMS key rotations.

## **1.12.L Data privacy & retention**

- **PII catalog** with owners & TTLs; DSAR export tooling (user can request data).
- **Retention**: messages 365 days, in‑app 90 days, proofs 180 days, signed docs 7 years (legal).
- **Redaction**: purge on account deletion (except finance/legal holds).

## **1.12.M Cost guardrails**

- **Budgets & alarms** per account; Slack/email alert on 20%/50%/80% of monthly cap.

- Right‑sizing defaults:

  - Aurora Serverless v2 min ACU 0.5–1.0; autoscale up to 4–8 ACU at launch.
  - Typesense: 1 small node; OpenSearch OCU cap = 2–4 (off by default).
  - Lambda memory set to the cheapest point that meets p95; provisioned concurrency **off** unless needed.
  - S3 lifecycle rules on by default.
  - NAT usage minimized (prefer VPC endpoints; egress audit).

- **CI “cost bump” gate**: if IaC diff raises projected monthly spend over threshold, require finance approval.

## **1.12.N Disaster recovery**

- **RPO**: ≤ 15 minutes for Aurora (PITR).
- **RTO**: ≤ 4 hours (restore + DNS flip) for critical path.
- **Runbook**: documented steps; quarterly drills (stage env); alarms that trigger the runbook.

## **1.12.O Local dev, previews, and seed data**

- **Local mocks:** AppSync local, Dynamo local; Stripe/Tax/e‑sign sandboxes.
- **Seed fixtures** for cities, roles, studios, users, and sample bookings to enable rapid UI work.
- **Ephemeral envs** per PR with auto teardown at 48h.

## **1.12.P Developer experience & governance**

- **Monorepo** with pnpm, turbo, strict TS, ESLint, Prettier.
- **Conventional commits**; PR templates with checklists (security, cost, migrations).
- **CODEOWNERS** for critical paths (finance, trust, infra).
- **Schema/codegen** for GraphQL; shared types for events; golden files for ranking & fee math.
- **ADR** (Architecture Decision Records) in repo for choices like Typesense vs OpenSearch.

## **1.12.Q Work packages (for your 4 Cursor agents)**

**Agent B — Infra/IaC**

- WP‑INF‑01: Amplify Gen 2 CDK stacks (Auth, API, Data, Media, Workflow, Observability).
- WP‑INF‑02: Multi‑account bootstrap, DNS, ACM certs, WAF.
- WP‑INF‑03: Budgets/alerts; cost gate in CI; cdk‑nag rules.

**Agent C — Data/Runtime**

- WP‑DATA‑01: Aurora cluster + migrations framework; Dynamo tables with TTL/RCU/WCU.
- WP‑DATA‑02: Search stack (Typesense baseline + adapter to OpenSearch Serverless).
- WP‑DATA‑03: Step Functions templates & EventBridge buses.

**Agent A — Web/Hosting**

- WP‑WEB‑INF‑01: Amplify Hosting setup w/ branch mapping, ISR/SSR config, edge rewrites.
- WP‑WEB‑INF‑02: Signed S3 uploads with scoped IAM; image proxy/resizer at edge.

**Agent D — SecOps/Observability**

- WP‑SEC‑01: WAF managed rules + custom IP rate limits; Secrets Manager + rotation.
- WP‑OBS‑01: CloudWatch dashboards/alarms; X‑Ray traces; log scrubbing; audit sinks.
- WP‑DR‑01: DR runbook & drill scripts; snapshot retention; restore tests.

## **1.12.R Acceptance criteria (mark §1.12 FINAL only when ALL true)**

1246. **Amplify Gen 2** stacks synth and deploy cleanly; CI fails any PR that introduces Classic artifacts.
1247. **Three environments** live with separate accounts, DNS, certs, and secrets; branch mapping works; previews auto‑expire.
1248. **Security**: WAF enabled, IAM least‑priv, KMS on RDS/DDB/S3, no public RDS, TLS enforced, Secrets Manager used.
1249. **Data**: Aurora + Dynamo tables created; backups & retention policies; migrations framework in place.
1250. **Observability**: dashboards/alerts deployed; traces flow end‑to‑end; PII scrubbing verified.
1251. **Cost**: budgets & alarms active; lifecycle policies in place; OCU/ACU/RCU caps; NAT egress minimal.
1252. **DR**: PITR validated; restore drill passes in stage within RTO.
1253. **DX**: local mocks, seed data, and codegen working; CI green; cost‑diff gate functional.

## **1.12.S Test matrix (CI + stage drills)**

**Infra correctness**

- CDK diff minimal; no drift; destroy/redeploy dev env passes.

**Security**

- Pen test on WAF rules; IAM analyzer finds no broad permissions; secrets never logged.

**Data & migrations**

- Forward/backward migrations with online safety; PITR restore verifies data integrity.

**Observability**

- Synthetic transactions visible across traces; alarms fire on injected faults.

**Cost**

- Synthetic traffic holds within budget; lifecycle transitions verified; search engine OCU alarms quiet.

**DR drill**

- Simulated region issue → restore from snapshot in stage → app healthy within RTO.

# **§1.13 — Data Platform, Analytics & Experimentation**

*(event contracts · ELT (Bronze/Silver/Gold) · near‑real‑time ops views · product analytics · experimentation · data quality & privacy · BI & dashboards · cost controls · tests)*

**Purpose.** Build a privacy‑safe, cost‑conscious analytics stack that powers product decisions, operational visibility (SLOs, reconciliation health), finance reporting, and experimentation—without re‑platforming. This section defines the **event model**, **pipelines**, **storage/layout**, **transformations**, **governance & privacy**, **BI**, **experimentation**, **SLOs & cost**, **admin tools**, and a **full test plan**. We do **not** move on until §1.13 meets your 99.9% bar.

## **1.13.A Canon & invariants**

1260. **Single event canon.** Every user/system action emits an immutable, versioned event to a central bus with stable keys (*user_id*, *anon_id*, *lbg_id*, *leg_id*, etc.).

1261. Bronze → Silver → Gold.

      177. **Bronze**: raw, append‑only JSON in S3 (immutable).
      178. **Silver**: curated, typed Parquet tables (facts/dimensions).
      179. **Gold**: business‑ready marts (dashboards/KPIs).

1262. **Privacy‑by‑design.** No raw PII (email/phone/images) in events or indexes. Emails/phones appear only as **stable hashes** where needed for dedupe.

1263. **Money correctness.** Finance facts derive from source‑of‑record tables in Aurora (§§1.3, 1.9) and from Stripe/tax webhooks; checks ensure sums reconcile (ties into daily close gates).

1264. **Cost‑efficient first.** S3 + Glue Catalog + **Athena** for querying; **QuickSight SPICE** or **Metabase** for BI; optional **Redshift Serverless** only when we outgrow Athena latency.

1265. **Experimentation guardrails.** Sticky bucketing, exposure logging, predefined guardrails (refund/complaint ceilings), and sequential/CUPED‑ready metrics.

## **1.13.B High‑level architecture**

- Ingestion (near real‑time):

  - App & web clients send event envelopes to an authenticated **/collect** endpoint (AppSync → Lambda).
  - Backend services publish **domain events** (the ones we enumerated across §§1.3–1.12) to **EventBridge**.
  - External providers (Stripe, e‑sign, SES) → webhook ingesters → normalized events → EventBridge.

- Transport & storage:

  - **EventBridge → Kinesis Firehose → S3** (partitioned *dt=YYYY‑MM‑DD/hour=HH*).
  - Bronze stored as **newline‑delimited JSON**; compaction jobs produce **Parquet** for Athena.
  - **Glue Catalog** defines tables for Bronze and Silver; partitions registered automatically.

- Transformations:

  - **AWS Glue** (PySpark) or **Athena CTAS** jobs to build Silver/Gold on schedules (NRT 5–15 min for ops, hourly/daily for heavy facts).
  - **dbt‑core on Athena** for modeling, tests, and lineage (optional but recommended).

- Serving & BI:

  - **Athena** for ad‑hoc; **QuickSight** (SPICE) for dashboards; optional **Metabase** (open‑source) on top of Athena/Redshift.
  - **Ops pages** in Admin use **materialized views** (Athena CTAS to Parquet) for low‑latency.

## **1.13.C Event envelope & contracts**

**Envelope (all events)**

*{*  
*"event": "string", // e.g., "checkout.start", "payout.paid"*  
*"v": 1, // schema version*  
*"occurred_at": "2025-11-06T15:24:18Z",*  
*"received_at": "2025-11-06T15:24:19Z",*  
*"user_id": "usr\_...", // optional for anon*  
*"anon_id": "an\_...", // sticky browser/device id when user not logged in*  
*"session_id": "ses\_...", // client session*  
*"city": "houston", // normalized city code when relevant*  
*"device": { "ua": "hash", "os": "iOS", "app_ver": "1.0.3" },*  
*"context": { "role": "buyer\|seller\|studio_owner\|admin" },*  
*"ids": { "lbg_id": "lbg\_...", "leg_id": "leg\_...", "doc_id": "doc\_..." },*  
*"money": { "amount_cents": 12345, "currency": "USD" }, // present when applicable*  
*"payload": { /\* event-specific fields, see below \*/ }*  
*}*  

**Conventions**

- **Amounts** always in integer cents.
- **Durations** in seconds.
- **Booleans** plain; **enums** strict strings.
- **PII** (names, emails, phones, addresses) **never** included—join on ids in Silver when necessary.

**Example families (non‑exhaustive; aligned to earlier sections)**

- **Search (§1.2):** *search.query*, *search.results_view*, *search.card_impression*, *search.card_click*, *search.save*, *search.alert.create\|triggered*.
- **Checkout/Booking (§1.3):** *checkout.start*, *docs.pack.create\|signed*, *payment.intent.created\|succeeded\|failed*, *lbg.confirmed*, *leg.in_progress\|completed*, *amendment.added*, *refund.created\|succeeded*, *payout.queued\|paid\|failed*.
- **Messaging (§1.4):** *thread.create*, *message.send*, *action.create\|state_change*, *deliverable.proof\|final\|approved*.
- **Docs (§1.5):** *doc.pack.issued\|signed*, *doc.pdf.hash_verified*.
- **Trust (§1.6):** *idv.started\|passed\|failed*, *bg.invited\|clear\|consider*, *risk.score.updated*.
- **Promotions (§1.7):** *promo.impression\|click\|invalid_click*, *promo.spend.debit\|credit*, *promo.topup.charge.succeeded*.
- **Reviews (§1.8):** *review.create\|hide\|remove\|restore*, *reputation.recompute*.
- **Comms (§1.10):** *notification.sent*, *email.bounce\|complaint\|unsubscribe*.
- **Studios (§1.11):** *studio.quote.request\|response*, *studio.verification.approved\|revoked*.
- **Infra (§1.12):** *waf.block*, *alarm.triggered*, *deploy.succeeded\|failed* (for internal SRE metrics).

We will ship **JSON Schemas** per event type with unit tests to guarantee backward‑compatible evolution (*v* increments only on breaking changes).

## **1.13.D Bronze → Silver → Gold modeling**

**Bronze (raw):**  
*s3://data/bronze/events/dt=YYYY‑MM‑DD/hour=HH/\*.json*

- Append‑only; immutable.
- Glue Catalog table *bronze_events* with partitions (*dt*, *hour*).

**Silver (typed/curated):** primary tables

- *fact_search_impressions*, *fact_search_clicks* (joinable via *impression_id*).
- *fact_booking_legs* (one row per leg status change with snapshots).
- *fact_payments*, *fact_refunds*, *fact_payouts*, *fact_disputes*.
- *fact_promotions_events* (impressions/clicks/invalids), *fact_promotions_spend*.
- *fact_messages*, *fact_action_cards*, *fact_notifications*.
- *fact_docs*, *fact_idv_bg*, *fact_reviews*.
- **Dimensions**: *dim_user_public* (no PII), *dim_service_profile*, *dim_studio*, *dim_city*, *dim_device*, *dim_campaign*.

**Gold (marts/KPIs):**

- **Marketplace**: *kpi_gmv_daily*, *kpi_take_rate*, *kpi_conversion_funnel* (search→profile→checkout→confirm), *kpi_cancellations*, *kpi_refunds*, *kpi_disputes*.
- **Supply**: *kpi_seller_activation*, *kpi_studio_verification_rate*, *kpi_acceptance_window_hist*.
- **Trust**: *kpi_idv_pass_rate*, *kpi_bg_clear_rate*, *kpi_risk_buckets*.
- **Promotions**: *kpi_promo_ctr*, *kpi_invalid_rate*, *kpi_spend_vs_budget*.
- **Comms**: *kpi_delivery*, *kpi_bounce*, *kpi_complaint*, *kpi_open_click* (non‑sensitive).
- **SRE**: *kpi_api_latency_p95*, *kpi_error_rates*, *kpi_waf_blocks*.

**Build strategy**

- Glue/CTAS jobs materialize Silver to Parquet partitioned by *dt* (and sometimes *city*).
- Gold uses **dbt models** (on Athena) with tests (unique keys, not null, referential integrity), incremental by *dt*.

## **1.13.E Near‑real‑time ops views**

Some ops metrics (recon gates, payout backlogs, dispute queues) require freshness **\<15 min**.

- Create **NRT materialized views** in S3 via Athena CTAS running every **5–10 min**, small partitions only for today’s hours.
- Admin consoles read from these materialized Parquet tables for stable, fast loads.

## **1.13.F Experimentation framework**

**Assignment**

- Sticky bucket per *user_id* (or *anon_id* pre‑login) via salted hash (e.g., *hash(user_id + exp_key) % 100*).
- Variants defined in AppConfig (feature flags). Exposure logged as *exp.exposed* at first checkpoint.

**Metrics & guardrails**

- Primary metrics per experiment pre‑declared; guardrails include: refund rate, complaint rate, SLO latency, bounce for comms.
- **CUPED** or stratified analyses supported by exporting **per‑user aggregates** (pre‑period covariates).
- **Sequential** or fixed horizon; maintain cookbook for analysts.

**Data**

- *dim_exposure* table links *user_id*/*anon_id* to *exp_key*, *variant*, *exposed_at*.
- Gold layer produces per‑variant metric tables with p‑values/CI (analyst notebooks).

## **1.13.G Data quality, validation & lineage**

- **Contract tests**: every event schema tested in CI; unknown event fields flagged but preserved in Bronze.
- **Great Expectations** (or **Deequ**) on Silver/Gold: uniqueness of ids, non‑nulls, ranges (e.g., *rating between 1..5*), monotonicity (e.g., payout queue should drain).
- **Lineage**: dbt docs + event schema registry show upstream/downstream for each mart.
- **Alerts**: failed expectations page Ops; large deltas in GMV/CTR vs 7‑day average trigger review.

## **1.13.H Privacy, governance & retention**

- **Lake Formation** for table/column permissions; analysts get **row‑level filtering** by environment and city if required.

- **Hashing**: *email_sha256*, *phone_sha256* kept only in **Silver private** area (not in Gold); never in events.

- **DSAR/Deletion**: user deletion writes a **tombstone event**; nightly job purges Silver/Gold joins that carry the user’s PII hash; Bronze (raw, immutable) is handled by maintaining a mapping table of redactions and excluding on read.

- **Retention**:

  - Bronze events: 18 months (partition delete after).
  - Silver facts: 24–36 months depending on table.
  - Gold marts: rolling 24 months.

- **Legal holds**: tag partitions; purge blocked until hold cleared.

## **1.13.I BI & dashboards**

- **QuickSight** workspaces per function: **Executive**, **City Ops**, **Trust**, **Finance**, **Support**, **Growth**.
- Use **SPICE** extracts for fast loads; refresh cadences (NRT where appropriate, otherwise daily).
- **Metabase** (optional) for self‑serve exploration; connects to Athena; row‑level guards via Lake Formation.

**Core dashboards** (initial)

- **Executive**: GMV, take rate, bookings, CAC/LTV (when available), city trends, SLO tiles.
- **Operations**: payout backlog, recon variance, cancellation/refund bands, dispute queue.
- **Trust**: IDV/BG funnels, risk bucket movement, dispute outcomes.
- **Growth/Promotions**: impressions/clicks/invalid rate, CPA proxy, campaign pacing.
- **Comms**: delivery vs bounce/complaints, digest suppression, opt‑out flow.
- **Studios**: verification rate, amenity usage, quote success %.

## **1.13.J Cost posture & performance**

- **S3**: Parquet + Snappy compression; partition by date (and city when cardinality helps); lifecycle after 90–180 days to colder storage.
- **Athena**: avoid scanning whole buckets—push **partition filters**; ctables store sorted small files for today’s partitions; limit CTAS output file sizes (256–512 MB).
- **Glue**: small DPU reservations; scale jobs by schedule; stop on idle; reuse code across models.
- **QuickSight**: prefer SPICE extracts (charged per user/capacity) with scheduled refresh; keep visuals focused.
- **Redshift Serverless**: disabled at launch; enable behind a flag if Athena latency becomes a blocker; start at smallest RPU with pause when idle.

## **1.13.K Admin tooling**

- **Schema registry** web UI (read‑only) listing events & versions with examples.
- **Backfill runner** for late events (replay a partition/day without clobbering existing Parquet).
- **Data dictionary** (Gold) with KPI definitions and SQL behind each card (single source of truth).
- **Access audit**: who queried which tables/partitions (CloudTrail/Lake Formation).

## **1.13.L Error taxonomy (data platform)**

- *EVENT_SCHEMA_INVALID* — payload fails JSON Schema.
- *EVENT_REJECTED_RATE_LIMIT* — client flooding; sample/delay.
- *PIPELINE_LAG_EXCEEDED* — Bronze→Silver lag \> SLO.
- *QUALITY_CHECK_FAILED* — Great Expectations failed (which check & partition).
- *DSAR_CONFLICT* — deletion collides with legal hold.
- *BI_REFRESH_FAILED* — SPICE refresh failed.

## **1.13.M SLOs & alerts**

- **Ingestion**: EventBridge→S3 (Bronze) **≤ 60 s p95**.
- **NRT views**: Bronze→Silver (ops views) **≤ 10 min p95**.
- **Daily marts**: complete by **T+6h** local.
- **BI**: Dashboards available by **08:00** local; SPICE refresh success **≥ 99%** rolling 7 days.

Alerts on: ingestion lag beyond SLO, quality failures, unusual GMV deltas, ATHENA_SCANNED_BYTES anomalies (cost), QuickSight refresh failures.

## **1.13.N Test plan (CI + stage)**

**Contracts & ingestion**

1347. Validate JSON Schemas for all events; generate fixtures; reject malformed example.
1348. Simulate Firehose → S3 path; partitions and Glue catalog creation verified.

**Transforms**  
3) Build Silver facts with sample events; ensure referential integrity; Great Expectations pass.  
4) Build Gold marts; compare against golden KPIs.

**Ops freshness**  
5) NRT materialized views update within 10 min under synthetic load.

**Experimentation**  
6) Bucketing sticky across login; exposure logged once; per‑variant metrics computed.

**Privacy & DSAR**  
7) DSAR tombstone leads to exclusion in Silver/Gold; Bronze read‑time exclusion works; legal hold override blocks purge.

**BI**  
8) SPICE extracts refresh; dashboards render within targets.

**Cost**  
9) Athena queries using partition filters; scanned bytes within budget; lifecycle transitions occur.

## **1.13.O Work packages (Cursor agents)**

- **Agent C — Ingestion & Modeling**  
  WP‑DATA‑ING‑01: Event schemas & validation; EventBridge + Firehose S3 pipeline.  
  WP‑DATA‑ING‑02: Bronze→Silver ETL (Glue/Athena CTAS) + dbt project skeleton.
- **Agent B — Quality & Privacy**  
  WP‑DATA‑QTY‑01: Great Expectations suite; alerts; DSAR tombstone flow; Lake Formation grants.
- **Agent A — BI & Experiments**  
  WP‑DATA‑BI‑01: QuickSight datasets & dashboards; SPICE schedules; data dictionary.  
  WP‑EXP‑01: Assignment & exposure logging; guardrail metric jobs; analysis notebooks.
- **Agent D — Ops & Admin**  
  WP‑DATA‑OPS‑01: NRT materialized views (ops); backfill runner; schema registry UI.  
  WP‑COST‑01: Athena scanned‑bytes monitor; lifecycle & partition housekeeping jobs.

## **1.13.P Acceptance criteria (mark §1.13 FINAL only when ALL true)**

1353. Event pipeline ingests and lands Bronze with SLO **≤ 60 s p95**; schemas validated.
1354. Silver facts and dimensions materialize with tests passing; Gold marts compute KPIs correctly.
1355. NRT ops views feed Admin consoles within **≤ 10 min p95**.
1356. Experimentation framework logs exposures, runs metrics with guardrails, and supports CUPED/sequential analysis.
1357. Privacy: no PII in events; DSAR works; Lake Formation permissions enforced; legal holds respected.
1358. BI dashboards live for Executive/City Ops/Trust/Finance/Growth/Comms; SPICE refresh success ≥ 99%.
1359. Cost: Athena scanned bytes within target; lifecycle rules active; no unnecessary compute.
1360. Telemetry & alerts cover pipeline lag, data quality, cost anomalies, and BI refresh health.

# **§1.13 — Data Platform, Analytics & Experimentation (Expanded)**

Below I expand each subsection with **executable‑grade detail**: concrete event schemas, ingestion & storage configs, Athena/CTAS/dbt models, data‑quality suites, DSAR/retention, Lake Formation permissions, NRT ops views, experimentation machinery, BI datasets, and cost/alerting runbooks. You can drop these artifacts into the repo (under */data/* and */amplify/backend/observability/*) and wire them with your Amplify Gen 2 stacks.

## **1.13.C (expanded) — Event Envelope & Contracts**

### **C.1 Canonical envelope (JSON Schema v1)**

*{*  
*"\$id": "*[*https://rastup.com/schemas/event-envelope.v1.json*](https://rastup.com/schemas/event-envelope.v1.json)*",*  
*"\$schema": "*[*https://json-schema.org/draft/2020-12/schema*](https://json-schema.org/draft/2020-12/schema)*",*  
*"type": "object",*  
*"required": \["event", "v", "occurred_at", "received_at", "context", "ids", "payload"\],*  
*"properties": {*  
*"event": { "type": "string", "pattern": "^\[a-z0-9\_.\]+\$" },*  
*"v": { "type": "integer", "enum": \[1\] },*  
*"occurred_at": { "type": "string", "format": "date-time" },*  
*"received_at": { "type": "string", "format": "date-time" },*  
*"user_id": { "type": "string", "pattern": "^usr\_\[A-Za-z0-9\]+\$" },*  
*"anon_id": { "type": "string", "pattern": "^an\_\[A-Za-z0-9\]+\$" },*  
*"session_id": { "type": "string", "pattern": "^ses\_\[A-Za-z0-9\]+\$" },*  
*"city": { "type": "string" },*  
*"device": {*  
*"type": "object",*  
*"properties": {*  
*"ua_hash": { "type": "string" },*  
*"os": { "type": "string" },*  
*"app_ver": { "type": "string" }*  
*},*  
*"additionalProperties": false*  
*},*  
*"context": {*  
*"type": "object",*  
*"required": \["role", "env"\],*  
*"properties": {*  
*"role": { "type": "string", "enum": \["buyer","seller","studio_owner","admin","guest"\] },*  
*"env": { "type": "string", "enum": \["dev","stage","prod"\] }*  
*},*  
*"additionalProperties": true*  
*},*  
*"ids": {*  
*"type": "object",*  
*"properties": {*  
*"lbg_id": { "type": "string", "pattern": "^lbg\_" },*  
*"leg_id": { "type": "string", "pattern": "^leg\_" },*  
*"doc_id": { "type": "string", "pattern": "^doc\_" },*  
*"impression_id": { "type": "string", "pattern": "^imp\_" },*  
*"campaign_id": { "type": "string", "pattern": "^pcmp\_" }*  
*},*  
*"additionalProperties": true*  
*},*  
*"money": {*  
*"type": "object",*  
*"properties": {*  
*"amount_cents": { "type": "integer", "minimum": 0 },*  
*"currency": { "type": "string", "minLength": 3, "maxLength": 3 }*  
*},*  
*"additionalProperties": false*  
*},*  
*"payload": { "type": "object" }*  
*},*  
*"additionalProperties": false*  
*}*  

**PII‑free rule:** No names, emails, phones, exact addresses, or images in events. Join to PII only inside **Silver private** models when absolutely necessary.

### **C.2 Example event schemas (selected)**

- search.card_impression.v1

*{*  
*"\$id": "…/search.card_impression.v1.json",*  
*"type": "object",*  
*"required": \["query_hash","result_pos","target_type","target_id","filters"\],*  
*"properties": {*  
*"query_hash": { "type":"string" },*  
*"result_pos": { "type":"integer", "minimum": 1 },*  
*"target_type": { "type":"string", "enum":\["service_profile","studio"\] },*  
*"target_id": { "type":"string" },*  
*"filters": { "type":"object" }*  
*}*  
*}*  

- lbg.confirmed.v1

*{*  
*"\$id": "…/lbg.confirmed.v1.json",*  
*"type": "object",*  
*"required": \["leg_count","payment_method","total_cents"\],*  
*"properties": {*  
*"leg_count": { "type":"integer","minimum":1 },*  
*"payment_method": { "type":"string","enum":\["card","ach"\] },*  
*"total_cents": { "type":"integer","minimum":0 },*  
*"has_deposit_auth": { "type":"boolean" }*  
*}*  
*}*  

- promo.click.v1

*{*  
*"\$id": "…/promo.click.v1.json",*  
*"type": "object",*  
*"required": \["impression_id","campaign_id","valid"\],*  
*"properties": {*  
*"impression_id": { "type":"string" },*  
*"campaign_id": { "type":"string" },*  
*"valid": { "type":"boolean" },*  
*"invalid_reason": { "type":"string" }*  
*}*  
*}*  

- payout.paid.v1

*{*  
*"\$id":"…/payout.paid.v1.json",*  
*"type":"object",*  
*"required":\["leg_id","amount_cents","provider_ref"\],*  
*"properties":{*  
*"leg_id":{"type":"string"},*  
*"amount_cents":{"type":"integer","minimum":0},*  
*"provider_ref":{"type":"string"}*  
*}*  
*}*  

**Versioning:** Backward‑compatible field additions do not bump *v*; breaking changes → new schema id and *v+1* in envelope.

## **1.13.B & 1.13.E (expanded) — Ingestion, Bronze, and Near‑Real‑Time Views**

### **B.1 Event ingress path**

- **Client events**: App/Web → AppSync mutation *publishEvent* → Lambda *evt_ingest*:

  - Validate against **envelope schema** + **event‑specific schema** (ajv).
  - Add server fields (*received_at*, *context.env*, *ua_hash*).
  - Put onto **EventBridge Bus** (*rastup-events*).

- **Backend events**: services publish directly to EventBridge with the same envelope contract.

- **Provider webhooks** (Stripe, e‑sign, SES): normalized in dedicated Lambdas and published to EventBridge.

### **B.2 EventBridge → Firehose → S3 (Bronze)**

- Kinesis Firehose (Direct PUT from EventBridge)

  - **Buffer size**: 5 MB or **buffer interval** 60 s (whichever first).
  - **Compression**: GZIP.
  - **Dynamic partitioning** via record transformation Lambda to set S3 prefix:

*s3://data/bronze/events/dt=YYYY-MM-DD/hour=HH/env=\${env}/event=\${event}/*  

- - **Backup**: All failures to *s3://data/bronze/\_bad/…* (quarantine) with original payload + error.
- **S3 object key** example:  
  *…/dt=2025-11-06/hour=15/env=prod/event=lbg.confirmed/part-00023-…json.gz*

### **B.3 Glue Catalog & Athena (Bronze table)**

*CREATE EXTERNAL TABLE IF NOT EXISTS bronze_events (*  
*event string,*  
*v int,*  
*occurred_at timestamp,*  
*received_at timestamp,*  
*user_id string,*  
*anon_id string,*  
*session_id string,*  
*city string,*  
*device struct\<ua_hash:string, os:string, app_ver:string\>,*  
*context struct\<role:string, env:string\>,*  
*ids map\<string,string\>,*  
*money struct\<amount_cents:int, currency:string\>,*  
*payload string -- keep raw JSON; parse in Silver*  
*)*  
*PARTITIONED BY (dt string, hour string, env string, event_name string)*  
*ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'*  
*LOCATION 's3://data/bronze/events/'*  
*TBLPROPERTIES ('projection.enabled'='true');*  

**Note:** Use **partition projection** to avoid expensive *MSCK REPAIR*. For Firehose prefixes, set *event_name* from *event* value.

### **E.1 Near‑Real‑Time (NRT) Ops Views**

- Use **Athena CTAS** every 5–10 min to create small **Parquet** materializations for Admin dashboards.

**Example: payout backlog by city (last 24h)**

*CREATE TABLE IF NOT EXISTS ops_payout_backlog*  
*WITH (*  
*format='PARQUET',*  
*parquet_compression='SNAPPY',*  
*partitioned_by=array\['dt'\]*  
*) AS*  
*SELECT*  
*date_format(received_at, '%Y-%m-%d') AS dt,*  
*coalesce(b.payload_json.city, 'unknown') AS city,*  
*count_if(b.event='payout.queued') AS queued,*  
*count_if(b.event='payout.paid') AS paid,*  
*count_if(b.event='payout.failed') AS failed,*  
*(count_if(b.event='payout.queued') - count_if(b.event='payout.paid')) AS backlog*  
*FROM (*  
*SELECT*  
*event,*  
*received_at,*  
*json_parse(payload) AS payload_json*  
*FROM bronze_events*  
*WHERE dt \>= date_format(date_add('day', -1, current_date), '%Y-%m-%d')*  
*AND env='prod'*  
*) b*  
*GROUP BY 1,2;*  

Schedule via **Athena Scheduler** or a small **Step Functions** state machine.

## **1.13.D (expanded) — Silver/Gold Modeling**

### **D.1 CTAS: Silver facts (examples)**

- Search impressions (Silver)

*CREATE TABLE IF NOT EXISTS silver.fact_search_impressions*  
*WITH (format='PARQUET', parquet_compression='SNAPPY', partitioned_by=array\['dt'\]) AS*  
*SELECT*  
*date_format(received_at, '%Y-%m-%d') AS dt,*  
*received_at,*  
*coalesce(user_id, anon_id) AS actor_key,*  
*(payload_json -\>\> 'query_hash') AS query_hash,*  
*(payload_json -\>\> 'result_pos')::int AS result_pos,*  
*(payload_json -\>\> 'target_type') AS target_type,*  
*(payload_json -\>\> 'target_id') AS target_id,*  
*city,*  
*context.role AS role,*  
*ids\['impression_id'\] AS impression_id*  
*FROM (*  
*SELECT event, received_at, user_id, anon_id, city, context, ids,*  
*json_parse(payload) AS payload_json*  
*FROM bronze_events*  
*WHERE event='search.card_impression' AND env='prod'*  
*) b;*  

- **Booking legs snapshot stream (Silver)**  
  (built from *leg.\** status events + finance webhooks)

*CREATE TABLE IF NOT EXISTS silver.fact_booking_legs*  
*WITH (format='PARQUET', parquet_compression='SNAPPY', partitioned_by=array\['dt'\]) AS*  
*SELECT*  
*date_format(received_at, '%Y-%m-%d') AS dt,*  
*ids\['leg_id'\] AS leg_id,*  
*max_by(payload_json, received_at) AS latest_payload, -- snapshot reducer*  
*max(received_at) AS last_event_at*  
*FROM (*  
*SELECT event, received_at, ids, json_parse(payload) AS payload_json*  
*FROM bronze_events*  
*WHERE event LIKE 'leg.%' AND env='prod'*  
*) s*  
*GROUP BY 1, 2;*  

For full fidelity, prefer **dbt** incremental models on Athena to express joins across *leg.\**, *refund.\**, *payout.\**.

### **D.2 dbt project skeleton (Athena adapter)**

*/data/dbt_project.yml*

*name: rastup_analytics*  
*version: 1.0.0*  
*profile: rastup_athena*  
*model-paths: \["models"\]*  
*tests-paths: \["tests"\]*  
*vars:*  
*env: prod*  

*/data/models/silver/fact_promotions_events.sql*

*{{ config(materialized='incremental', unique_key='event_id', partition_by={'field': 'dt'}) }}*  
  
*with base as (*  
*select*  
*md5(concat(event, cast(received_at as varchar), coalesce(ids\['impression_id'\], ''), coalesce(ids\['campaign_id'\], ''))) as event_id,*  
*date_format(received_at, '%Y-%m-%d') as dt,*  
*event,*  
*received_at,*  
*ids\['impression_id'\] as impression_id,*  
*ids\['campaign_id'\] as campaign_id,*  
*city,*  
*context.role as role,*  
*json_extract_scalar(payload, '\$.invalid_reason') as invalid_reason*  
*from {{ ref('bronze_events') }}*  
*where env='{{ var("env") }}'*  
*and event in ('promo.impression','promo.click','promo.invalid_click')*  
*{% if is_incremental() %}*  
*and received_at \> (select coalesce(max(received_at), timestamp '1970-01-01') from {{ this }})*  
*{% endif %}*  
*)*  
*select \* from base;*  

*/data/models/gold/kpi_promo_ctr.sql*

*{{ config(materialized='table', partition_by={'field':'dt'}) }}*  
*select*  
*dt,*  
*campaign_id,*  
*count_if(event='promo.impression') as impressions,*  
*count_if(event='promo.click') as clicks,*  
*(count_if(event='promo.click') / nullif(count_if(event='promo.impression'),0)) as ctr*  
*from {{ ref('fact_promotions_events') }}*  
*group by 1,2;*  

*/data/models/schema.yml* (tests)

*version: 2*  
*models:*  
* - name: fact_promotions_events*  
*columns:*  
* - name: event_id*  
*tests: \[not_null, unique\]*  
* - name: kpi_promo_ctr*  
*columns:*  
* - name: dt*  
*tests: \[not_null\]*  

## **1.13.G (expanded) — Data Quality, Validation & Lineage**

### **G.1 Great Expectations suite (examples)**

*/data/quality/expectations/fact_booking_legs.yml*

*expectations:*  
* - expect_table_columns_to_match_ordered_list:*  
*column_list: \[dt, leg_id, latest_payload, last_event_at\]*  
* - expect_column_values_to_not_be_null:*  
*column: leg_id*  
* - expect_column_values_to_be_between:*  
*column: latest_payload.total_cents*  
*min_value: 0*  
* - expect_compound_columns_to_be_unique:*  
*column_list: \[dt, leg_id\]*  

*/data/quality/expectations/fact_promotions_events.yml*

*expectations:*  
* - expect_column_values_to_be_in_set:*  
*column: event*  
*value_set: \["promo.impression","promo.click","promo.invalid_click"\]*  
* - expect_column_values_to_match_regex:*  
*column: campaign_id*  
*regex: "^pcmp\_.\*"*  

Run suites as part of the CTAS/dbt job tail step; failures → SNS alert + Slack (Ops).

### **G.2 Lineage**

- Maintain a lightweight **schema registry** (static site) auto‑generated from JSON Schemas + dbt docs.
- For every Gold mart, include *meta* fields citing upstream Silver models. dbt renders lineage graph—check into */docs/*.

## **1.13.H (expanded) — Privacy, Governance & Retention**

### **H.1 Lake Formation & permissions**

- **Data lake locations**:

  - *s3://data/bronze* (read: data‑eng only; analysts excluded).
  - *s3://data/silver* (read: data‑eng + analysts; **private PII** columns masked via LF tags).
  - *s3://data/gold* (read: broad analyst/viewers).

- **LF tags**: *pii:yes/no*, *env:dev\|stage\|prod*. Attach to columns (e.g., *email_sha256* is *pii:yes*). Grant principals row‑level + column‑level access via tags.

### **H.2 DSAR (Right to Erasure) workflow**

1378. **User request** creates *dsar.requested* admin ticket and writes a **tombstone event**:  
      *{ event: "dsar.tombstone", v:1, user_id:"usr\_...", occurred_at:… }*.

1379. **Operational stores** (Aurora/Dynamo/S3 app buckets) execute deletion/redaction per policy (already covered in §§1.4–1.12).

1380. Analytics purge:

      10. **Silver/Gold**: nightly job reads tombstones and deletes/overwrites partitions where *user_id=usr\_…* or *actor_key* links; regenerate affected aggregates.
      11. **Bronze**: keep immutable; **exclude on read** by maintaining *dsar_exclusions* table joined in views (regulatory‑approved strategy).

1381. **Verification**: generate a DSAR purge report with table counts before/after; store PDF in legal hold S3.

**Legal hold**: blocked DSARs write *dsar.hold* and the purge job skips those users until hold clears.

### **H.3 Retention**

- **Bronze**: 18 months rolling delete by *dt* partition (S3 lifecycle).
- **Silver**: 24–36 months depending on table; keep finance facts 7 years if required (PII masked).
- **Gold**: 24 months rolling.

## **1.13.F (expanded) — Experimentation Framework**

### **F.1 Assignment & exposure**

- **Assignment function** (deterministic):

*bucket = (fnv1a(hash_key = user_id \|\| anon_id \|\| "EXP_KEY") % 100)*  

- Store assignment in **AppConfig** or a small Dynamo table *exp_assignment* (for overrides).
- Log *exp.exposed* **once** per experiment per user at first exposure checkpoint.

***exp.exposed.v1*** **schema**

*{*  
*"required": \["exp_key","variant","checkpoint"\],*  
*"properties": {*  
*"exp_key": {"type":"string"},*  
*"variant": {"type":"string"},*  
*"checkpoint": {"type":"string","enum":\["search","profile","checkout","postbook"\]}*  
*}*  
*}*  

### **F.2 Guardrails & metrics**

- Guardrails computed **daily**:

  - Refund rate Δ vs control ≤ 0.2 pp
  - Complaint rate ≤ 0.1%
  - API p95 latency ≤ 2 s

- Metrics prepared in **Gold** as per‑variant aggregates with CUPED pre‑period covariates (e.g., prior 28‑day spend or visits).

**Example (Gold) CUPED prep**

*CREATE TABLE gold.exp_metric_checkout_cuped AS*  
*SELECT*  
*e.exp_key, e.variant, e.user_id,*  
*count_if(m.event='checkout.start') AS y_observed,*  
*-- theta estimate computed offline or via regression; simplified here*  
*avg(pre.y_baseline) as theta,*  
*(count_if(m.event='checkout.start') - avg(pre.y_baseline)) as y_cuped*  
*FROM dim_exposure e*  
*LEFT JOIN fact_events m ON e.user_id = m.user_id*  
*LEFT JOIN preperiod_agg pre ON e.user_id = pre.user_id*  
*WHERE e.exp_key='EXP_SEARCH_UI_A'*  
*GROUP BY 1,2,3;*  

## **1.13.I (expanded) — BI Datasets & Dashboards**

### **I.1 Datasets (QuickSight SPICE)**

- ***ds_kpi_marketplace*** (from *gold.kpi\_\**): GMV, bookings, take rate, conversion funnel.
- ***ds_ops_health***: payout backlog, recon variance, dispute queue, acceptance windows.
- ***ds_trust***: IDV/BG funnels, risk buckets, dispute outcomes.
- ***ds_promotions***: impressions, clicks, CTR, invalid rate, spend vs budget.
- ***ds_comms***: delivery, bounces, complaints, opt‑outs, digest suppression.
- ***ds_studios***: verification rate, amenity usage, quote success.

**Row‑level security**: if city‑restricted analyst roles exist, attach a mapping table *analyst_city_scope* and enforce RLS in QuickSight datasets.

### **I.2 Dashboard tiles (definitions)**

- **Executive**:

  - *GMV & Bookings*: *sum(gold.kpi_gmv_daily.gmv_cents)/100* with 7‑day trend.
  - *Take Rate*: *sum(platform_fees)/sum(gmv)*.
  - *Conversion Funnel*: stages from impressions→clicks→profile views→checkout→confirm.

- **Operations**:

  - *Recon variance*: *abs(charges - (payouts + refunds + fees))* with gate alarms.
  - *Payout backlog*: from NRT view *ops_payout_backlog*.

- **Trust**:

  - *IDV pass rate*: *idv.passed / (idv.passed + idv.failed)*.
  - *Risk buckets*: distribution over Watch/Action/Critical.

…(the rest are similar; all pull from Gold/NRT views above)

## **1.13.J (expanded) — Cost Posture & Performance**

- **Firehose**: small buffers to limit latency; GZIP + dynamic partitioning; DLQ for failed records.

- **Athena**:

  - Enforce **workgroup** with **encryption on**, **query bytes cap**, and **results location** per env.
  - Use **CTAS** with *bucketed_by* only if needed (careful with cost).
  - Partition filters **always applied** (*WHERE dt BETWEEN …*); add **city partition** to high‑volume facts (search, promotions) when warranted.

- **Glue**: schedule transforms during off‑peak; use minimal DPUs (e.g., 2–3) and **Athena CTAS** for many transforms to avoid Glue cost.

- **QuickSight**: prefer SPICE; schedule no more than 4–6 daily refreshes; monitor SPICE capacity and prune unused visuals.

**Budget alarms (per env):** S3 storage, Athena scanned bytes, Glue DPU‑hours, QuickSight capacity, Firehose PUTs.

## **1.13.K (expanded) — Admin & Runbooks**

- **Schema registry site** generated from */schemas/\*\*.json* + dbt docs; published to internal Amplify Hosting.

- **Backfill runner**: Step Functions flow

  - pick date range
  - CTAS Bronze→Silver for those partitions
  - rebuild impacted Gold models
  - verify Great Expectations → if fail, auto‑rollback.

- **Incident runbooks**:

  - *Pipeline lag*: pause heavy CTAS, widen Firehose buffers, notify Ops, degrade BI refresh to daily only.
  - *High Athena spend*: identify runaway queries in workgroup metrics; kill/limit; pin dashboards to SPICE only.
  - *Schema break*: move invalid events to *\_bad* quarantine; hotfix schema or add adapter transform.

## **1.13.L/M/N/O (expanded) — Error Taxonomy, SLOs, Tests, Work Packages**

### **L. Error codes (operational)**

- *EVENT_SCHEMA_INVALID*, *EVENT_ENVELOPE_INVALID*, *EVENT_PUT_FAILED*,
- *PIPELINE_LAG_EXCEEDED*, *CTAS_FAILURE*, *QUALITY_CHECK_FAILED*,
- *ATHENA_SCANNED_BYTES_BREACH*, *BI_REFRESH_FAILED*, *DSAR_CONFLICT*.

Each emits a **CloudWatch metric** with labels (*env*, *component*, *severity*) and raises an alarm with runbook link.

### **M. SLOs & Alerts (detail)**

- **Ingestion p95** ≤ 60 s; Alarm at 120 s for 10 min.
- **NRT views** ≤ 10 min; Alarm at 20 min.
- **Daily marts** done by 06:00 local; Alarm at 07:00.
- **Athena scanned bytes**: \< 500 GB/day (stage), \< 2 TB/day (prod) to start; alarms at 80%.
- **BI refresh** success ≥ 99%; alarm on 2 consecutive failures.

### **N. Test matrix (concrete add‑ons)**

- **Contract tests**: CI job enumerates all */schemas/\*.json* and validates synthetic fixtures; fails PR on mismatch.
- **Drill tests**: load a synthetic day, produce Silver/Gold, assert KPIs match golden JSON.
- **Lag tests**: inject 10k events/min for 15 min; verify NRT views within 10 min.
- **DSAR tests**: create user, produce events, issue tombstone, verify exclusion in Silver/Gold, verify Bronze exclusion view.
- **Cost tests**: run representative dashboard queries; ensure scanned bytes under thresholds.

### **O. Work packages (ready to assign to your 4 Cursor agents)**

- Agent C — Ingestion & Schemas

  - WP‑DATA‑ING‑01: EventBridge bus + Firehose + transform Lambda (dynamic partitions).
  - WP‑DATA‑ING‑02: Envelope & event JSON Schemas + ajv validator Lambda.
  - WP‑DATA‑ING‑03: Provider webhook normalizers → EventBridge.

- Agent B — Modeling & Quality

  - WP‑DATA‑MOD‑01: Bronze table, CTAS for *fact_search_impressions*, *fact_promotions_events*, *fact_booking_legs*.
  - WP‑DATA‑QTY‑01: Great Expectations suites + alerts; dbt tests.

- Agent A — BI & Experiments

  - WP‑DATA‑BI‑01: QuickSight datasets & dashboards (Executive/Operations/Growth/Trust).
  - WP‑EXP‑01: Assignment function, *dim_exposure*, guardrails metrics, CUPED pipeline.

- Agent D — Governance & Ops

  - WP‑DATA‑GOV‑01: Lake Formation permissions & LF tags; DSAR tombstone job.
  - WP‑DATA‑OPS‑01: NRT CTAS jobs + payout backlog view; backfill runner; cost monitors.

## **1.13.P (re‑stated) — Final Acceptance Checklist for §1.13**

1423. **Ingestion** to Bronze S3 via EventBridge→Firehose with dynamic partitions; schema validation live; p95 lag ≤ 60 s.
1424. **Silver** facts and **Gold** marts materialize with dbt/CTAS; tests pass; NRT ops views update ≤ 10 min.
1425. **Experimentation** runs (assignment, exposure, metrics with guardrails and CUPED).
1426. **Privacy & governance**: no PII in events; LF column/row permissions; DSAR tombstone flow proven; legal holds respected.
1427. **BI**: QuickSight dashboards up, SPICE refreshed; RLS applied where required.
1428. **Cost & SLOs**: scanned bytes, DPU‑hours, SPICE capacity within budgets; alarms & runbooks configured.
1429. **Runbooks**: backfills, schema breaks, lag, high spend all documented and tested.

# **§1.14 — Fan‑Sub (Paid Content, Requests, Tips & PPV)**

*(roles & gating · subscriptions · paid requests & deliverables · tips & PPV · media pipeline (previews vs finals, watermarking) · safety & age‑gates · payments, taxes & receipts · moderation & DMCA · dashboards · admin · telemetry · tests · cost)*

**Purpose.** Implement a **Fan‑Sub** system that lets fans support creators (talent) via **subscriptions**, **paid custom requests**, **tips**, and **pay‑per‑view (PPV)** content—while enforcing **18+ verification**, safe‑mode rules, privacy, and cost efficiency. Fan‑Sub integrates with messaging (§1.4), docs/e‑sign where required (§1.5), trust gates (§1.6), payments & statements (§1.9), comms (§1.10), studios (§1.11 when relevant), and analytics (§1.13).

We won’t advance until §1.14 meets your 99.9% bar.

## **1.14.A Canon & invariants**

1430. **Age gate & IDV required:** Creators **and** paying fans must be 18+ (verified via §1.6). Creators need **ID Verified** to publish Fan‑Sub.
1431. **Safe‑Mode everywhere:** Public thumbnails are SFW; NSFW bands apply to previews and in‑thread uploads.
1432. **Previews vs finals:** Only **previews** (small images/clips) are stored in our S3. **Final media** is external (Drive/Dropbox/S3 owner) and referenced via **immutable manifests** (checksums), like deliverables in §1.4/§1.3.
1433. **No filter bypass:** Fan‑Sub surfaces honor city gates, age gates, Safe‑Mode, and user preferences.
1434. **Money clarity:** Separate **Marketplace GMV** (requests/PPV) and **Subscription revenue** streams; platform fees & **taxes on fees** follow §1.9.
1435. **Privacy:** No PII in media watermarks; no emails/phones exchanged off‑platform (anticircumvention).
1436. **Auditability:** All paid actions produce immutable records (orders, receipts, approvals), with lineage to users and threads.

## **1.14.B Feature set (MVP + flags)**

- **Subscriptions** (monthly; optional annual flag later).
- **Paid custom requests** (one‑off commissions) with **action cards** in threads (quote → pay → deliverable → approve/revise).
- **Tips** (one‑click).
- **PPV posts** (locked content purchasable without subscribing).
- **Bundles/discounts** (flag‑gated for later).
- **Free trials** (flag‑gated; risk‑aware).
- **Geo/role gates**: creators may limit visibility by city/country if policy demands.

## **1.14.C Data model (Aurora + Dynamo + S3)**

### **C.1 Aurora (source of truth)**

*-- Creator Fan-Sub profile*  
*create table fansub_creator (*  
*creator_id text primary key, -- fsc\_...*  
*user_id text not null unique, -- usr\_...*  
*handle text not null unique, -- vanity*  
*display_name text not null,*  
*city_gate text\[\], -- allowed cities (null = global)*  
*bio text,*  
*price_month_cents int not null, -- subscription price*  
*currency text not null default 'USD',*  
*is_published boolean not null default false,*  
*idv_required_ok boolean not null default false, -- from §1.6*  
*nsfw_ok boolean not null default true, -- creator allows NSFW (still SFW preview rules)*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
  
*-- Subscription & entitlement*  
*create table fansub_subscription (*  
*sub_id text primary key, -- fss\_...*  
*creator_id text not null references fansub_creator(creator_id),*  
*fan_user_id text not null, -- usr\_...*  
*provider text not null, -- 'stripe'*  
*provider_ref text not null, -- subscription id*  
*status text not null check (status in ('active','past_due','paused','canceled','trialing')),*  
*current_period_end timestamptz not null,*  
*renews boolean not null default true,*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now(),*  
*unique (creator_id, fan_user_id)*  
*);*  
  
*-- Tips & PPV & Requests share a common "order" header*  
*create table fansub_order (*  
*order_id text primary key, -- fso\_...*  
*kind text not null check (kind in ('tip','ppv','request')),*  
*creator_id text not null,*  
*buyer_user_id text not null,*  
*amount_cents int not null,*  
*fee_cents int not null default 0, -- platform fee (see §1.9)*  
*fee_tax_cents int not null default 0,*  
*currency text not null default 'USD',*  
*status text not null check (status in ('pending','succeeded','refunded','failed','disputed')),*  
*provider text not null, -- 'stripe'*  
*provider_charge text, -- charge/payment intent id*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
  
*-- PPV posts (locked content)*  
*create table fansub_ppv_post (*  
*ppv_id text primary key, -- fpp\_...*  
*creator_id text not null references fansub_creator(creator_id),*  
*title text not null,*  
*caption text,*  
*price_cents int not null,*  
*preview_media jsonb not null default '\[\]'::jsonb, -- S3 previews (scanned)*  
*final_manifest_id text, -- external manifest id (immutable)*  
*nsfw_band int not null default 0,*  
*is_published boolean not null default false,*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
  
*-- Entitlement when PPV is purchased*  
*create table fansub_ppv_access (*  
*access_id text primary key, -- fpa\_...*  
*ppv_id text not null references fansub_ppv_post(ppv_id),*  
*buyer_user_id text not null,*  
*order_id text not null references fansub_order(order_id),*  
*created_at timestamptz not null default now(),*  
*unique (ppv_id, buyer_user_id)*  
*);*  
  
*-- Custom request lifecycle (threads carry action cards; this table is the money/evidence)*  
*create table fansub_request (*  
*request_id text primary key, -- fsr\_...*  
*thread_id text not null, -- link to §1.4 thread*  
*creator_id text not null,*  
*buyer_user_id text not null,*  
*title text not null,*  
*brief text not null,*  
*quoted_cents int not null,*  
*status text not null check (status in ('quoted','accepted','paid','delivered','approved','revision_requested','refunded','disputed','closed')),*  
*order_id text, -- fansub_order once paid*  
*proof_manifest_id text, -- proofs (external)*  
*final_manifest_id text, -- finals (external)*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  

### **C.2 DynamoDB (hot path caches)**

- *fansub_entitlement_cache*: *PK=USER#usr\_…*, *SK=CREATOR#fsc\_…\|PPV#fpp\_…* → boolean + expiry (for fast gating checks).
- *fansub_rate_limits*: tip/PPV write guardrails per IP/user (abuse mitigation).

### **C.3 S3 buckets (previews only)**

- *fansub-previews* (public via CF; all scanned; Safe‑Mode respected).
- *fansub-quarantine* (flagged previews awaiting T&S).
- Final media **not** stored internally—referenced via manifests, as in §1.4.

## **1.14.D Payment flows (Stripe) & taxes**

- **Subscriptions:** Stripe Billing **subscriptions** (monthly).

  - Create product per creator with *price_month_cents*; or use one product with **price per creator** (more scalable).
  - Webhooks: *invoice.payment_succeeded/failed*, *customer.subscription.updated\|deleted*.
  - We record *fansub_subscription* and entitlement (active period).

- **Tips:** one‑time **PaymentIntent** with **Connect destination** to the creator account (less platform float). Platform fee (if any) handled as application fee on Connect.

- **PPV:** one‑time **PaymentIntent**; after success, create *fansub_ppv_access* row to grant entitlement.

- Requests:

  - Creator issues **quote** (action card in thread).
  - Buyer pays **PaymentIntent**; on success, order → *succeeded*; request status *paid*.
  - Deliverable posted via action card; buyer **approves** or **requests revisions**.
  - Refunds follow §1.3 policy; disputes → §1.9 D.5.

- Taxes:

  - **Subscription/PPV/Requests** are **digital services**; compute **buyer tax** via tax adapter (Stripe Tax/Avalara/TaxJar) using buyer location.
  - We separately compute **platform fee taxes** per §1.9 for any fee we charge.
  - Receipts show line items: content price, tax, platform fee (if present), platform fee tax.

- **Payouts:** per creator via Stripe Connect scheduled payouts; we record *payout.queued\|paid* events into analytics (see §1.13).

## **1.14.E Watermarking, access, and anti‑scrape**

- Previews:

  - Images: server watermark (creator handle + order id) diagonally; max 1600 px; JPEG/WebP.
  - Video snippets: 10–20 s HLS preview; burned watermark.
  - NSFW banding: if *nsfw_band=1*, blur until hovered & age‑gate OK; *=2* blocked on public.

- Finals (external manifests):

  - Manifest includes per‑file SHA‑256, filename, size, URL, optional watermark seed.
  - If using cloud providers that support transforms (e.g., Cloudflare R2/Stream), creators can host DRM; we just store references and checksums.

- Access control:

  - Entitlement check before revealing **final manifest URLs** (fetched on demand and short‑lived).
  - Per‑request signed redirects; **tokenized** fragment in querystring that expires.

- Rate limits & anti‑abuse:

  - Per‑user/view throttles; hotlink protection via CF **signed cookies** if we proxy some assets.
  - Download logs linked to user id for evidence in disputes.

## **1.14.F Messaging integrations (action cards)**

- **Request Quote** → **Pay** → **Deliver** → **Approve/Revise** loops occur in the **thread** using **action cards** defined in §1.4.E (reused with *ACTION_TYPE = FS_REQUEST\_\**).
- **Tip receipt** and **PPV unlocked** post system messages into the thread (optional; user‑toggle).
- **Nudges** (comms §1.10) for unsigned docs if the creator uses any release forms (off by default for Fan‑Sub).

## **1.14.G Safety, policy, and moderation**

- **IDV**: creators and fans must be 18+ verified before accessing Fan‑Sub surfaces.

- **Content rules**:

  - Prohibit illegal content, doxxing, hate, non‑consensual content.
  - For public previews, **SFW only**; NSFW allowed in finals if compliant and user’s Safe‑Mode is OFF.

- **Moderation pipeline**: previews are scanned (image/video); text captions pass toxicity/PII checks; repeat violations trigger T&S review and potential suspension.

- **Anticircumvention**: block emails/phones in captions and messages; nudges and soft blocks escalate on repeat.

- **Reporting**: fans can report content; T&S console handles takedowns and refunds.

- **DMCA**:

  - Inbound claims queue → temporarily hide content; notify creator; counter‑notice process handled via Admin console.
  - Evidence stored (timestamps, hashes from manifest).
  - We do not provide legal advice; the tooling facilitates compliance.

## **1.14.H UX surfaces**

- **Creator page**: hero, SFW gallery, subscription CTA, PPV catalog with locked overlays, request button.
- **Subscribed feed**: latest posts from creators a fan follows; PPV unlock badges.
- **Thread**: request flows, proofs/finals approval, receipts.
- **Wallet/Receipts**: Fan can view purchases, invoices, tax lines.
- **Creator dashboard**: earnings, subscriber counts/churn, top PPV, request backlog.

## **1.14.I GraphQL API (AppSync) — selected**

*type FansubCreator {*  
*creatorId: ID!, handle: String!, displayName: String!,*  
*priceMonthCents: Int!, currency: String!, isPublished: Boolean!,*  
*nsfwOk: Boolean!, idvRequiredOk: Boolean!*  
*}*  
  
*type SubscriptionStatus { status: String!, currentPeriodEnd: AWSDateTime!, renews: Boolean! }*  
  
*type PPVPost {*  
*ppvId: ID!, title: String!, caption: String, priceCents: Int!,*  
*previewMedia: \[Attachment!\]!, nsfwBand: Int!, isPublished: Boolean!*  
*}*  
  
*type Query {*  
*fansubCreator(handle: String!): FansubCreator!*  
*fansubPPV(creatorHandle: String!, cursor: String, limit: Int=12): PPVPage!*  
*mySubscription(creatorId: ID!): SubscriptionStatus*  
*myPPVAccess(ppvId: ID!): Boolean!*  
*}*  
  
*type Mutation {*  
*publishFansubCreator(input: FansubCreatorInput!): FansubCreator!*  
*subscribe(creatorId: ID!): SubscriptionStatus! \# kicks off Stripe flow*  
*cancelSubscription(subId: ID!): Boolean!*  
  
*tip(creatorId: ID!, amountCents: Int!): Boolean!*  
*buyPPV(ppvId: ID!): Boolean!*  
  
*requestQuote(creatorId: ID!, title: String!, brief: String!, priceCents: Int!): ID!*  
*acceptQuote(requestId: ID!): Boolean!*  
*deliverRequest(requestId: ID!, manifestRef: ID!, note: String): Boolean!*  
*approveRequest(requestId: ID!): Boolean!*  
*requestRevision(requestId: ID!, note: String!): Boolean!*  
*}*  

**Server guards**

- All mutations check **IDV age gate** from §1.6.
- Entitlement gating for PPV & subscriber‑only posts.
- Rate limits on tips/requests to prevent abuse.
- Pricing floors/ceilings from AppConfig to avoid outliers.

## **1.14.J Notifications & comms (from §1.10)**

- **Event triggers**: subscription start/renew/fail, PPV unlocked, request quote/paid/delivered, tip received.
- **Channels**: email/push/in‑app; SMS only for critical payment issues (opt‑in).
- **Quiet hours** respected for non‑critical; digest for batch updates.
- **Templates**: *fansub_sub_started*, *fansub_invoice_failed*, *fansub_ppv_unlocked*, *fansub_request_quote*, *fansub_request_delivered*.

## **1.14.K Analytics & experiments (from §1.13)**

- Events: *fansub.subscribe.start\|success\|fail*, *fansub.tip*, *fansub.ppv.buy*, *fansub.request.quote\|paid\|delivered\|approved\|revision*, *fansub.preview.view*, *fansub.final.view*.
- Funnels: profile → subscribe; preview → PPV buy; request quote → paid → approved.
- Guardrails: refund rate, complaint rate, moderation flags.
- Experiments: pricing A/B, preview length, watermark density, digest timing.
- NRT ops: creator earnings today, MTD, subscriber churn, request backlog, invoice failures.

## **1.14.L Admin consoles**

- **Creator eligibility** (IDV status, strikes) and publish toggle.
- **Refund & dispute desk** for tips/PPV/requests (policy simulator).
- **DMCA queue** with evidence viewer and timers.
- **Content moderation** (previews text/media); escalation & suspension controls.
- **Finance**: statements for creators, payout schedule, reserve flags.

All actions audited (actor, reason, before/after), some require dual approval.

## **1.14.M Performance & cost**

- **Storage**: previews only; lifecycle to Intelligent‑Tiering after 30 days.
- **Bandwidth**: HLS previews limited (10–20 s); CloudFront caching; signed cookies for private previews when needed.
- **Compute**: watermarking/transcode via Lambda on demand; no always‑on media servers.
- **Stripe**: use **billing thresholds** & retries for subs; dunning emails via Stripe to reduce send costs.
- **Search**: PPV/creator discovery in Typesense with lean fields (no captions in index).

## **1.14.N Error taxonomy (client‑safe)**

- *FANSUB_IDV_REQUIRED* — user not age‑verified.
- *FANSUB_CREATOR_NOT_PUBLISHED* — creator page not live.
- *FANSUB_PRICE_OUT_OF_RANGE* — violates pricing policy.
- *FANSUB_ENTITLEMENT_REQUIRED* — trying to access locked content.
- *FANSUB_REQUEST_STATE_INVALID* — bad action order.
- *FANSUB_MEDIA_BLOCKED* — preview failed safety checks.
- *PAYMENT_FAILED* — Stripe failure; include retriable hints.

Each error includes *code*, *message*, *hint*, *corrId*.

## **1.14.O Test plan (CI + sandbox)**

**Eligibility & gating**

1503. Creator cannot publish until IDV passed; fan cannot subscribe/buy PPV until age‑verified.

**Subscriptions**  
2) Subscribe success → entitlement; invoice failure → status *past_due*; dunning recovers; cancel resumes access until period end.

**Tips/PPV**  
3) Tip flow success; duplicate/double‑submit idempotent.  
4) PPV buy grants access; re‑buy blocked.

**Requests**  
5) Quote → pay → deliver → approve; revision loop; refund path via policy.  
6) Action cards in thread reflect state; receipts correct.

**Media**  
7) Previews scanned & watermarked; finals referenced via manifest; access tokens expire; rate limits enforced.

**Moderation/DMCA**  
8) Flagged preview hidden; DMCA takedown hides content; counter‑notice restores.

**Analytics**  
9) Events land in Bronze; Silver facts & Gold KPIs update; NRT views show earnings/backlog.

**Performance/cost**  
10) p95 entitlement check ≤ 60 ms (cached); preview loads ≤ 200 ms from CF; Stripe webhooks idempotent; storage/egress within budget alarms.

## **1.14.P Work packages (Cursor 4‑agent lanes)**

- **Agent C — Domain/API**  
  WP‑FS‑01: SQL for *fansub\_\** tables; GraphQL resolvers; entitlement cache.  
  WP‑FS‑02: Action cards for requests; tie‑ins to §1.4 flows; receipts & lineage.
- **Agent B — Payments/Taxes**  
  WP‑FS‑PAY‑01: Stripe Billing subs; PPV/tips PaymentIntents; Connect payouts; tax adapter lines.  
  WP‑FS‑PAY‑02: Webhooks normalization (*invoice.\**, *payment_intent.\**, *charge.\**) + idempotency.
- **Agent A — Web**  
  WP‑FS‑WEB‑01: Creator page, PPV catalog, subscribe/tip/buy flows; thread UI for requests.  
  WP‑FS‑WEB‑02: Watermarked preview renderer; entitlement‑aware media components.
- **Agent D — Safety/Admin/QA**  
  WP‑FS‑SAFE‑01: NSFW scan + watermarking pipeline; anticircumvention in captions.  
  WP‑FS‑ADM‑01: DMCA/moderation/finance consoles; audits.  
  WP‑FS‑QA‑01: Full test matrix automation; synthetic earnings reports.

## **1.14.Q Acceptance criteria (mark §1.14 FINAL only when ALL true)**

1508. Age‑gated eligibility enforced; creators with IDV can publish; fans 18+ can pay.
1509. Subscriptions, tips, PPV, and requests work end‑to‑end with receipts, taxes, and payouts.
1510. Media pipeline (previews vs finals) functions with watermarking, safety scans, and access tokens; no finals stored internally.
1511. Messaging action cards cover the entire request lifecycle; approvals & revisions audited.
1512. Moderation & DMCA tooling live; anticircumvention active; violations audited.
1513. Dashboards & NRT views show earnings/churn/backlog; experiments and guardrails instrumented.
1514. Cost posture holds (previews only, limited HLS, caching); p95 performance targets met.

# **§1.14 — Fan‑Sub (Paid Content, Requests, Tips & PPV) — Expanded Spec**

This augments the earlier §1.14 with **implementation‑grade detail**: exact Stripe object mappings, state machines, watermarking/preview specs, entitlement tokens, manifest contracts, moderation & DMCA flows, tax/fee math, GL entries, comms templates, errors, and runbooks.

## **1.14.1 Roles, gates, and global invariants (recap + expansions)**

- **Eligibility gates** (server‑enforced before any Fan‑Sub surface or API):

  - **Age**: both creator and fan must have *idv_status=passed* and *age_verified=true* (§1.6).
  - **Trust**: creator must be *ID Verified*; **Trusted Pro** badge is **not** required for Fan‑Sub (optional boost).
  - **Policy clean**: creator not suspended; no unresolved DMCA strike blocking publish.

- Safe‑Mode & visibility:

  - Public pages show **SFW previews only**; finals require explicit entitlement + Safe‑Mode OFF (for adult categories).
  - City/region gates respected if configured by creator or policy.

- **Media storage stance**: we **store only previews**; **finals** live off‑platform (creator‑controlled) and are referenced via **immutable manifests** (with file checksums).

- **Money separation**: Marketplace GMV for Fan‑Sub (subs, PPV, requests, tips) is separate from booking GMV. Platform fees are separate revenue per §1.9.

## **1.14.2 Data contracts (DB, cache, storage)**

### **1.14.2.1 SQL (additions & refinements)**

*-- Creator storefront settings & policy*  
*alter table fansub_creator*  
*add column preview_policy jsonb not null default jsonb_build_object(*  
*'image_max_px', 1600, 'video_preview_sec', 15, 'watermark', true, 'nsfw_on_public', false*  
*),*  
*add column payout_schedule text not null default 'standard', -- 'standard' \| 'weekly' (Stripe Connect)*  
*add column tos_accepted_at timestamptz,*  
*add column dmca_contact_email text;*  
  
*-- Subscription invoice snapshots (for statements & taxes)*  
*create table fansub_subscription_invoice (*  
*inv_id text primary key, -- fsi\_...*  
*sub_id text not null references fansub_subscription(sub_id),*  
*provider_invoice text not null, -- Stripe invoice id*  
*period_start timestamptz not null,*  
*period_end timestamptz not null,*  
*amount_cents int not null, -- subtotal (creator portion)*  
*tax_cents int not null,*  
*fee_cents int not null, -- platform fee taken (if any)*  
*fee_tax_cents int not null,*  
*currency text not null default 'USD',*  
*status text not null check (status in ('paid','void','uncollectible')),*  
*created_at timestamptz not null default now()*  
*);*  
  
*-- Creator payout ledger (join to Stripe balance txns)*  
*create table fansub_payout (*  
*payout_id text primary key, -- fpo\_...*  
*creator_id text not null,*  
*provider_transfer text not null, -- Stripe transfer/payout id*  
*amount_cents int not null,*  
*status text not null check (status in ('queued','paid','failed')),*  
*scheduled_for timestamptz,*  
*created_at timestamptz not null default now()*  
*);*  

### **1.14.2.2 DynamoDB (hot‑path caches)**

- ***fansub_entitlement_cache*** item shape:

*{*  
*"pk": "USER#usr_123",*  
*"sk": "CREATOR#fsc_789", // or "PPV#fpp_456"*  
*"entitled": true,*  
*"exp": 1734567890 // TTL (epoch seconds)*  
*}*  

- ***fansub_rate_limits***: keys like *TIP#usr_123#2025-11-06* with counters.

### **1.14.2.3 S3 keys & CF**

- s3://fansub-previews/{creator_id}/ppv\_{ppv_id}/img\_{n}.webp
- s3://fansub-previews/{creator_id}/req\_{request_id}/proof\_{n}.webp
- All served via **CloudFront** with *Cache-Control: public, max-age=86400* and **WAF** throttles.

## **1.14.3 Manifests for final media (off‑platform)**

**Rationale:** Preserve creator control, reduce our media costs/risks, keep **immutable evidence** via hashes.

### **1.14.3.1 Manifest JSON (v1)**

*{*  
*"manifest_version": 1,*  
*"creator_id": "fsc_123",*  
*"kind": "ppv" \| "request",*  
*"entity_id": "fpp_456" \| "fsr_789",*  
*"created_at": "2025-11-06T15:22:10Z",*  
*"files": \[*  
*{*  
*"file_id": "F001",*  
*"name": "set1_001.jpg",*  
*"sha256": "b8f9...e1",*  
*"bytes": 2435612,*  
*"mime": "image/jpeg",*  
*"url": "*[*https://creator-bucket.s3.amazonaws.com/.../set1_001.jpg*](https://creator-bucket.s3.amazonaws.com/.../set1_001.jpg)*"*  
*},*  
*{*  
*"file_id": "V001",*  
*"name": "teaser.mp4",*  
*"sha256": "a3c1...9f",*  
*"bytes": 43293434,*  
*"mime": "video/mp4",*  
*"url": "*[*https://dropbox.com/s/…?dl=1*](https://dropbox.com/s/…?dl=1)*"*  
*}*  
*\],*  
*"signature": {*  
*"algo": "ed25519",*  
*"public_key": "pk\_...",*  
*"sig": "MEYCIQ…"*  
*}*  
*}*  

- **Validation**: we only cache the manifest (and not the files). On access, we **HEAD** each URL to verify availability; for disputes/DMCA, we may pull copies into **evidence vault** with a legal hold (separate S3 WORM bucket).

### **1.14.3.2 Tokenized access (short‑lived)**

- Generate an **entitlement token** per viewer:

*token = base64url(HMAC(k, user_id \| entity_id \| exp_ts \| nonce))*  

- Present token in redirect query: *?e={exp_ts}&t={token}*. Token TTL ~ 5 minutes.
- For creators using their own CDNs, document how to **validate** this token at their edge (optional).

## **1.14.4 Watermarking & previews**

### **1.14.4.1 Image previews**

- **Pipeline**: S3 upload → Lambda trigger:

  - Validate MIME/size → Rekognition NSFW → ClamAV → **Resize** max dimension = *preview_policy.image_max_px* → **Watermark**.

- **Watermark spec**:

  - Content: *@{handle} · {order_or_ppv_id} · {date YYYY‑MM‑DD}*
  - Position: diagonal; **tile** every ~400–600px; 40–55% opacity; font *Inter*/fallback; 14–18px @1x.
  - Color: auto black/white depending on local luminance.

### **1.14.4.2 Video previews**

- **Transcode** to **HLS** with 1 or 2 bitrates (e.g., 540p, 720p); preview length *preview_policy.video_preview_sec* (default 15s).
- **Burned watermark** (same content); or overlay at player with WebVTT if creator demands reversible watermarking (less secure).
- **Segment key rotation** not required for previews (public), but CF signed URLs prevent hotlinking.

## **1.14.5 Stripe object mappings & flows**

### **1.14.5.1 Subscriptions (Stripe Billing + Connect)**

- Create **one Product** “Fan‑Sub Subscription” with **one Price per creator** (*price\_{creator_id}* monthly).

- **Connect mode**:

  - Use **Application Fees** (*application_fee_amount*) to collect platform fees on each invoice (if we charge one), and route the **net** to the creator’s **Connect account** via **transfer_data\[destination\]**.
  - Alternatively, use **Direct charges** on the creator’s account if we want creator seen as MoR for subs. MVP: **Platform is MoR** to centralize tax handling (safer for compliance).

- **Key webhook events**:

  - *invoice.payment_succeeded* → create *fansub_subscription_invoice* row; (entitlement period) = *current_period_end*.
  - *invoice.payment_failed* / *customer.subscription.updated* (status *past_due*) → dunning schedule (below).
  - *customer.subscription.deleted* → mark *status='canceled'* and entitlement ends at period end (no retro refunds unless policy configured).

**Dunning schedule (MVP)**

- Stripe handles retries at 3‑day cadence up to 4 retries; we mirror state changes; optional in‑product reminder at 24h before cancellation.

### **1.14.5.2 PPV, Tips, Requests (PaymentIntents)**

- Create **PaymentIntent** with:

  - *amount = price + tax + (optional platform fee tax) + application_fee_amount* (if platform collects fee).
  - *transfer_data\[destination\]=creator_connect_account* if routing funds immediately; otherwise capture centrally then **Transfer**.

- On *payment_intent.succeeded*:

  - **PPV** → insert *fansub_ppv_access*.
  - **Tip** → just record *fansub_order.status='succeeded'*.
  - **Request** → set *fansub_request.status='paid'*, link *order_id*.

### **1.14.5.3 Refunds & disputes**

- Refunds initiated by support or creator (subject to policy): *refund.created* & *refund.succeeded* webhooks → update *fansub_order.status='refunded'* and revoke entitlements (PPV).

- Chargebacks (*charge.dispute.created*):

  - Set order *status='disputed'*; hide finals; keep previews up; workflow in Admin console (evidence: manifest hashes, comms history).
  - GL expense entry per §1.9.D.5.

## **1.14.6 Tax & fee math (digital goods)**

- **Buyer line items** (per order/invoice):

*subtotal_cents (creator’s content)*  

- content_tax_cents (digital services tax; adapter calculates)
- platform_fee_cents (0 at MVP unless policy says otherwise)
- platform_fee_tax_cents  
  = total_cents (charged)

<!-- -->

- **Platform revenue**: **only** the **platform_fee_cents** (and recognized when **collected**) per §1.9; we are not MoR for creator content unless explicitly configured (default: platform MoR for *platform fee*, not for content price; content is pass‑through).
- **Jurisdictions**: use adapter flags to treat content as **digital service**; store tax summary per invoice/order for audit.

## **1.14.7 Accounting & GL (platform side)**

- **At capture** (order or invoice paid):

*Dr Cash:Stripe total_cents*  
*Cr Liability:CreatorPayable subtotal_cents + content_tax_cents (if pass-through)*  
*Cr Deferred:PlatformFees platform_fee_cents*  
*Cr Liability:TaxPayable:PlatformFeeTax platform_fee_tax_cents*  

- **At payout to creator**:

*Dr Liability:CreatorPayable transfer_amount_cents*  
*Cr Cash:Stripe transfer_amount_cents*  

- **When fee recognized** (immediate on invoice/order paid if we treat fee as earned at sale for Fan‑Sub):

*Dr Deferred:PlatformFees platform_fee_cents*  
*Cr Revenue:PlatformFees platform_fee_cents*  

- **Refunds/Chargebacks** mirror §1.9 logic (reverse earned if applicable).

If we configure **platform fee = 0** at MVP, platform revenue on Fan‑Sub is **\$0** and accounting is simpler; we still incur Stripe fees as expense.

## **1.14.8 State machines**

### **1.14.8.1 Custom Request flow (Step Functions)**

*States:*  
*QuoteIssued -\> (BuyerAccept?) -\> PaymentIntentCreated -\> PaymentSucceeded*  
*-\> CreatorDelivers -\> (BuyerApproves? -\> Closed)*  
*-\> (BuyerRequestsRevision -\> CreatorDelivers) \[loop max N\]*  
*Cancelled/Refunded/Error (terminal)*  
*Guards:*  
* - IDV/age gates checked on every transition*  
* - Max revisions N configurable (default 2)*  
* - Auto-close after 7 days of inactivity post-delivery (no refund)*  

**Transitions (events & actions)**

- *BuyerAccept* → create PI; hold UI until Stripe returns *succeeded*.
- *PaymentSucceeded* → post system message, unlock **proofs**.
- *CreatorDelivers* → proofs posted; buyer can preview (watermarked).
- *BuyerApproves* → finals manifest recorded; receipt issued.
- *BuyerRequestsRevision* → loop with decrementing counter.
- *RefundIssued* → entitlements revoked; status *refunded*.

### **1.14.8.2 Subscription lifecycle**

- *trialing* (if enabled) → *active* on first invoice; *past_due* → *canceled* after dunning; *paused* (manual) halts entitlement updates; *canceled* allows access until *current_period_end*.

## **1.14.9 Moderation, DMCA & safety runbooks**

### **1.14.9.1 Moderation pipeline**

- **Text**: profanity/toxicity + PII regex (emails, phones, socials). Confidence thresholds tuned; soft‑block with inline redaction + appeal path.
- **Media**: Rekognition (nudity/adult), custom NSFW model optional; **band 0/1/2** policy as earlier.
- **Escalation**: 3 strikes in 30 days → auto “under review” (publishing paused) pending T&S decision.

### **1.14.9.2 DMCA flow (Admin console)**

1561. Intake claim → **hide** content (previews & links), notify creator.
1562. Creator may **counter** within window; if no counter, content stays removed; if counter, re‑publish unless legal hold.
1563. Evidence pack: manifest JSON, file SHA‑256, timestamps, access logs; export PDF.

**Timers** and **email templates** pre‑authored (§1.10).

## **1.14.10 Pricing policy, limits & abuse protections**

- **Price ranges** (configurable):

  - Subscriptions: \$2–\$50/month
  - PPV: \$1–\$200
  - Requests: \$5–\$1,000
  - Tips: \$1–\$500 per click (daily cumulative cap per user)

- **Rate limits**:

  - Max 5 PPV purchases/min per user, 20/day; Tips ≤ 10/min; Requests ≤ 3 open per creator per fan.

- **Fraud**: velocity + device/IP risk signals (tie into §1.6 risk score); auto‑pause on thresholds.

## **1.14.11 Notifications & templates (MJML snippets)**

- ***fansub_sub_started***: subject “You’re subscribed to {{creator}}”; body includes period dates, manage link.
- ***fansub_invoice_failed***: “Payment issue for {{creator}}—update your card”.
- ***fansub_ppv_unlocked***: “You unlocked {{title}} by {{creator}}”.
- ***fansub_request_quote***: to buyer with pay CTA; to creator with accepted notice.
- ***fansub_request_delivered***: approve/revise buttons.
- ***fansub_tip_received***: to creator with amount.

All respect quiet hours; security/legal always deliver.

## **1.14.12 GraphQL SDL — extended (selected)**

*enum FansubOrderKind { TIP PPV REQUEST }*  
*enum FansubRequestStatus { QUOTED ACCEPTED PAID DELIVERED APPROVED REVISION_REQUESTED REFUNDED DISPUTED CLOSED }*  
*enum FansubNSFWBand { SAFE BLUR BLOCK }*  
  
*type FansubOrder {*  
*orderId: ID! kind: FansubOrderKind!*  
*amountCents: Int! feeCents: Int! taxCents: Int! currency: String!*  
*status: String! createdAt: AWSDateTime!*  
*}*  
  
*type PPVAccess { ppvId: ID!, purchasedAt: AWSDateTime! }*  
  
*type Mutation {*  
*\# Admin-ish helpers for creators:*  
*setFansubPrices(priceMonthCents: Int!): FansubCreator!*  
*publishPPV(input: PPVInput!): PPVPost!*  
*unpublishPPV(ppvId: ID!): Boolean!*  
  
*\# Purchases:*  
*buyPPV(ppvId: ID!): FansubOrder! \# returns order + client secret if needed*  
*tip(creatorId: ID!, amountCents: Int!): FansubOrder!*  
*subscribe(creatorId: ID!): SubscriptionStatus!*  
  
*\# Requests flow:*  
*requestQuote(creatorId: ID!, title: String!, brief: String!, priceCents: Int!): ID!*  
*acceptQuote(requestId: ID!): FansubOrder!*  
*deliverRequest(requestId: ID!, proofManifest: ManifestInput!): Boolean!*  
*approveRequest(requestId: ID!, finalManifest: ManifestInput!): Boolean!*  
*requestRevision(requestId: ID!, note: String!): Boolean!*  
*}*  

Server injects idempotency keys; returns PaymentIntent client secrets where applicable.

## **1.14.13 Telemetry & ops dashboards (NRT)**

- **NRT views** (≤10 min): creator earnings today/MTD, failed invoices by creator, active subs, churn last 7 days, request backlog.
- **Gold KPIs**: conversion (profile→subscribe), PPV unlock CTR, request completion rate, refund/complaint rate, average tip, ARPU.
- **Alerts**: spike in invoice failures, refund bursts, DMCA volume, NSFW band‑2 misclassifications.

## **1.14.14 Errors & UX copy (client‑safe)**

- *FANSUB_IDV_REQUIRED*: “You must verify you’re 18+ to access Fan‑Sub.”
- *FANSUB_ENTITLEMENT_REQUIRED*: “Unlock this post to view the finals.”
- *FANSUB_PRICE_OUT_OF_RANGE*: “That price is outside allowed limits.”
- *PAYMENT_FAILED_RETRY*: “Payment failed—update your card to continue.”
- *REQUEST_REVISION_LIMIT*: “You’ve reached the maximum revisions for this request.”
- *CONTENT_UNAVAILABLE_DMCA*: “This content is temporarily unavailable.”

All errors include *corrId* and map to telemetry.

## **1.14.15 Performance & cost budgets**

- **Previews only** ensures S3 ≪ cost of finals hosting. Target: ≤ 10 TB/mo egress at launch (cached via CF).
- **Stripe fees** dominate; tune dunning to reduce involuntary churn.
- **Compute**: watermark/transcode Lambdas constrained by concurrency; queue spikes; no provisioned concurrency unless p95 exceeds SLA.

## **1.14.16 Test plan (expanded)**

- **Payments**: simulate happy path & failures (insufficient funds, 3DS challenge, dispute).
- **Entitlements**: PPV & subs access gates; cache TTL; token expiry.
- **Requests loop**: max revisions; inactivity auto‑close.
- **Moderation**: NSFW bands; PII detection; appeals; DMCA hide/restore.
- **Comms**: all templates send with quiet hours; unsubscribe works.
- **Analytics**: events arrive; NRT dashboards update; CUPED/guardrails compute.
- **Cost**: preview bandwidth under budget; Firehose/Athena within thresholds.

## **1.14.17 Work packages (ready to assign)**

- **Agent C — Domain/API**: tables, resolvers, entitlement cache, state machines, receipts.
- **Agent B — Payments/Taxes**: Stripe Billing + Connect flows, tax lines, webhooks, dunning.
- **Agent A — Web**: creator storefront, PPV/subscribe/tip flows, request action cards, entitlement UI.
- **Agent D — Safety/Admin/QA**: preview pipeline (scan/transcode/watermark), DMCA & moderation consoles, test automation + synthetic data.

## **1.14.18 Acceptance criteria — FINAL gate for §1.14**

1596. Age/IDV gates and Safe‑Mode rules enforced across all Fan‑Sub surfaces.
1597. Subscriptions, PPV, tips, and request flows function end‑to‑end with correct receipts, taxes, and payouts.
1598. Previews are watermarked and scanned; finals are referenced via validated manifests; entitlement tokens work; access logs recorded.
1599. Stripe webhooks idempotent; dunning and refunds/chargebacks correctly update state, ledgers, and GL.
1600. Moderation/DMCA tooling in place with audits; anticircumvention enforced in captions/messages.
1601. NRT dashboards and Gold KPIs live; alerts configured for invoice failures, refunds, and DMCA spikes.
1602. Performance and cost within budgets under 48h synthetic load.

# **§1.15 — Support, Disputes & Resolution Center**

*(case taxonomy · refund policies & flows · chargebacks & representment · DMCA & policy violations · data model · evidence & timelines · API & in‑app center · email bridge · automations & macros · payouts/holds · telemetry & SLOs · tests · cost)*

**Purpose.** Provide a unified, auditable system for **customer support**, **refunds**, **booking disputes**, **payments issues**, **chargebacks**, **DMCA**, and **policy‑violation reports**. It connects to booking (§1.3), messaging (§1.4), docs (§1.5), trust (§1.6), promotions (§1.7), reviews (§1.8), finance/GL (§1.9), comms (§1.10), studios (§1.11), infra (§1.12), analytics (§1.13), and Fan‑Sub (§1.14). We’ll implement internal tooling, user‑facing “Support Center,” and operational automations—cost‑consciously and compliant with record‑keeping.

We will not move to §1.16 until §1.15 satisfies your 99.9% bar.

## **1.15.A Canon & invariants**

1603. **Single front door** for all issues (“Support Center”), but **typed cases** with tailored flows.
1604. **Evidence first**: timelines aggregate **messages, deliverables, docs, approvals, geotime metadata**, and **payment records**—no decisions without evidence.
1605. **Refund math is deterministic** (driven by cancellation bands, completion status, and doc acceptance); manual overrides require **reasons + dual approval**.
1606. **Chargebacks ≠ refunds**: separate workflows; chargebacks follow card‑network timelines with **representment** packages.
1607. **Payout safety**: severe open cases place **holds** on affected payouts until resolved.
1608. **DMCA & policy**: legal requirements honored; immutable audits; content can be hidden rapidly but restored with counter‑notice if eligible.
1609. **Cost‑conscious**: in‑house ticketing with SES email bridge; optional external helpdesk later via adapter; storage in S3 with lifecycle policies.
1610. **Privacy**: no raw PII in case summaries beyond what’s necessary; redaction tools for doxxing.
1611. **SLAs by severity**: response and resolution targets with SLO monitoring; breached cases auto‑escalate.

## **1.15.B Case taxonomy (types & subtypes)**

- **Booking issue** (people/studios)

  - *Pre‑event*: reschedule request, venue conflict, wrong filters.
  - *During event*: no‑show, late, unsafe, rules violation.
  - *Post‑event*: quality dispute, late delivery, partial completion, damages (studio).

- Payment & payouts

  - Charge failure, duplicate charge, refund status, **instant payout** delay, verification hold.

- Product/Account

  - Access problems, comms/unsubscribe, trust badge concerns.

- DMCA/IP

  - Infringing media claims (Fan‑Sub or previews), counter‑notice tracking.

- Policy violation

  - Harassment, doxxing, off‑platform solicitation (anticircumvention), hate speech, illegal content.

- Chargeback (card network)

  - Inquiry/notification, evidence packaging, representment, result.

Each maps to a **case flow** with specific states, required fields, and resolution outcomes.

## **1.15.C Refund & dispute policy (deterministic kernels)**

**Bookings (people/studios) — base rules**

- If **buyer cancels** within policy bands (from §1.3 / *studio_policy*): refund = band % of subtotal + service tax; platform fees treated per §1.9 (usually refundable before completion, non‑refundable after; configurable).
- If **seller cancels/no‑show**: full refund; optional credit bonus.
- **Partial completion** (time & materials): proration by time delivered or milestone completion when docs reflect acceptance.
- **Damages (studio)**: deposit capture rules in §1.3.N; evidence required (photos, timestamps, invoices).

**Fan‑Sub (subscriptions, PPV, requests, tips)**

- **Subscriptions**: no retro refunds after period starts unless (a) *involuntary churn* reversal, or (b) service outage; dunning handled via Stripe.
- **PPV**: refundable if content not delivered/unavailable within X days; once **finals accessed**, refund eligibility drops unless quality dispute validated.
- **Requests**: if delivered and **buyer approved**, refund only via goodwill; if *revision loop* exhausted with unresolved defects, partial refund per tariff.
- **Tips**: non‑refundable except fraud.

**Escalation ladder**

1626. Auto‑decision (rules).
1627. Support agent decision with macros + reason codes.
1628. Supervisor dual‑approval when money impact \> threshold.
1629. Legal/T&S in DMCA or policy severe cases.

## **1.15.D State machines (high‑level)**

### **D.1 Generic Support Case**

*OPEN -\> (AwaitingCustomer \| AwaitingSeller \| Investigating)*  
*-\> DecisionPending -\> (Refunded \| Denied \| GoodwillCredit \| Escalated)*  
*-\> Closed*  

- SLA timers on **first response** and **resolution**; pausing allowed when waiting on customer.

### **D.2 Booking dispute (people/studios)**

*Reported -\> EvidenceCollection (pull docs/messages/deliverables)*  
*-\> Adjudication (rules engine + agent)*  
*-\> Outcome: (FullRefund \| PartialRefund \| NoRefund \| DepositCapture \[studio\])*  
*-\> Closed*  

### **D.3 Chargeback**

*Notified -\> EvidenceRequested (deadline T)*  
*-\> Represented (submitted) -\> (Won \| Lost)*  
*-\> (If Lost -\> GL expense; if Won -\> release hold)*  

### **D.4 DMCA**

*ClaimReceived -\> ContentHidden -\> NotifyCreator*  
*-\> (CounterNotice? -\> Review -\> RestoreOrKeepDown)*  
*-\> Closed*  

## **1.15.E Data model (Aurora + S3)**

*create table support_case (*  
*case_id text primary key, -- sca\_...*  
*type text not null check (type in ('booking','payment','product','dmca','policy','chargeback')),*  
*subtype text, -- e.g., 'no_show','quality','duplicate_charge'*  
*status text not null check (status in ('open','awaiting_customer','awaiting_seller','investigating','decision_pending','refunded','denied','goodwill','escalated','closed')),*  
*severity text not null check (severity in ('low','normal','high','urgent')),*  
*opened_by_user text not null, -- usr\_...*  
*owner_user_id text, -- agent assigned*  
*watchers text\[\] not null default '{}',*  
*lbg_id text, -- booking group*  
*leg_id text,*  
*order_id text, -- fansub order (PPV/tip/request)*  
*studio_id text,*  
*creator_id text, -- fansub_creator*  
*payout_id text, -- if payout hold/release*  
*reason_code text, -- normalized reason taxonomy*  
*sla_first_resp_at timestamptz,*  
*sla_due_at timestamptz,*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
  
*create table support_message (*  
*msg_id text primary key, -- smg\_...*  
*case_id text not null references support_case(case_id) on delete cascade,*  
*author_role text not null check (author_role in ('buyer','seller','studio_owner','creator','agent','system')),*  
*author_user_id text,*  
*body_md text not null, -- markdown (sanitized)*  
*attachments_json jsonb not null default '\[\]'::jsonb, -- \[{s3_key, hash, bytes, mime}\]*  
*created_at timestamptz not null default now()*  
*);*  
  
*create table support_event (*  
*evt_id text primary key, -- sev\_...*  
*case_id text not null references support_case(case_id) on delete cascade,*  
*action text not null, -- 'status_change','refund_issued','deposit_captured','evidence_attached','hold_applied','hold_released','chargeback_represented','dmca_hide','dmca_restore'*  
*actor_user_id text,*  
*details_json jsonb not null default '{}'::jsonb,*  
*created_at timestamptz not null default now()*  
*);*  
  
*-- Calculated refund/goodwill outcomes (mirror §1.9 fee/tax logic)*  
*create table support_refund (*  
*refund_id text primary key, -- srf\_...*  
*case_id text not null references support_case(case_id) on delete cascade,*  
*leg_id text,*  
*order_id text,*  
*amount_cents int not null,*  
*platform_fee_cents int not null,*  
*platform_fee_tax_cents int not null,*  
*reason text not null,*  
*processor_ref text, -- refund id on Stripe*  
*status text not null check (status in ('proposed','processing','succeeded','failed')),*  
*created_at timestamptz not null default now()*  
*);*  
  
*-- Payout holds (linked to legs/orders)*  
*create table payout_hold (*  
*hold_id text primary key, -- sph\_...*  
*case_id text not null references support_case(case_id),*  
*leg_id text,*  
*order_id text,*  
*amount_cents int not null, -- up to the payable amount*  
*status text not null check (status in ('applied','released','expired')),*  
*created_at timestamptz not null default now()*  
*);*  

**S3**:

- *support-evidence/* (immutable, WORM‑like via object‑lock if enabled) stores attachments (photos, manifests, logs PDF). Lifecycle → Intelligent‑Tiering @30d; Glacier @180d.

## **1.15.F Evidence & timeline stitching**

When a case opens or moves to **Investigating**, the system auto‑collects:

- **Messages & action cards** (from §1.4) for the thread(s) related to *leg_id* or *request_id*.
- **Docs & signatures** (from §1.5)—hashes and acceptance timestamps.
- **Deliverables & approvals** (proofs/finals manifests).
- **Geo/time** events (check‑ins, scheduled time windows, IP/device changes).
- **Finance**: charge, refund, payout records (§1.9).
- **Comms**: notification delivery (for “no response” claims).
- **Risk**: user risk scores (§1.6.G).

Evidence appears in a **chronological timeline** within the case.

## **1.15.G API (GraphQL) & Support Center (user‑facing)**

*type SupportCase {*  
*caseId: ID!, type: String!, subtype: String, status: String!, severity: String!,*  
*createdAt: AWSDateTime!, updatedAt: AWSDateTime!,*  
*lbgId: ID, legId: ID, orderId: ID, studioId: ID, creatorId: ID,*  
*reasonCode: String, ownerUserId: ID, slaDueAt: AWSDateTime*  
*}*  
*type SupportMessage {*  
*msgId: ID!, authorRole: String!, bodyMd: String!, createdAt: AWSDateTime!*  
*attachments: \[Attachment!\]!*  
*}*  
*type SupportRefund { refundId: ID!, amountCents: Int!, status: String!, createdAt: AWSDateTime! }*  
  
*type Query {*  
*mySupportCases(cursor:String, limit:Int=20): \[SupportCase!\]!*  
*supportCase(caseId: ID!): SupportCase!*  
*supportMessages(caseId: ID!, cursor:String, limit:Int=50): \[SupportMessage!\]!*  
*}*  
  
*input OpenCaseInput {*  
*type: String!, subtype: String, severity: String = "normal",*  
*lbgId: ID, legId: ID, orderId: ID, studioId: ID, creatorId: ID,*  
*reasonCode: String, bodyMd: String!, attachments:\[AttachmentInput!\]*  
*}*  
  
*type Mutation {*  
*openCase(input: OpenCaseInput!): SupportCase!*  
*postSupportMessage(caseId: ID!, bodyMd: String!, attachments:\[AttachmentInput!\]): SupportMessage!*  
*closeCase(caseId: ID!): Boolean!*  
*}*  

**Guards**

- Role‑scoped visibility: buyer sees their cases; seller/creator sees cases naming them; agents see all.
- Attachments scanned (NSFW/AV) as in §1.14.4.
- Rate‑limits on open‑case attempts.

**Support Center UI**

- “Report a problem” flows pre‑filled from booking/order context.
- Case list, case detail with timeline, message composer, attachment upload, status chips.

## **1.15.H Email bridge (SES) & routing**

- **Inbound**: [*case+{case_id}@support.rastup.com*](mailto:case+%7bcase_id%7d@support.rastup.com) → SES inbound rule → Lambda → *support_message* append (author detection via DKIM/DMARC + token).
- **Outbound**: replies include *Message‑ID*/*In‑Reply‑To*; List‑Unsubscribe for marketing categories unaffected.
- **Auto‑ack**: immediate “we received your request” message with case id and SLA.

## **1.15.I Automations, macros, and rules**

- **Macros** (agent shortcuts):

  - Booking no‑show (buyer): checklist + refund logic + canned message + case close.
  - Duplicate charge: verify Stripe balance txns → auto refund/dismiss.
  - Fan‑Sub PPV unavailable: verify manifest access logs → auto refund if within window.

- **Rules engine**:

  - SLA breaches → escalate severity + notify supervisor.
  - Too many simultaneous severe cases for a seller → **auto payout hold** to limit exposure.
  - Policy keywords/NSFW escalation → T&S queue.

## **1.15.J Payout holds & releases**

- **Apply hold** on leg/order payable when: severe open case, chargeback notice, or DMCA that may require refund.
- **Release** on case close or representment win; **expire** after max window (configurable).
- Visible to seller/creator in **Finance console** with reason and expected timeline.

## **1.15.K Chargebacks & representment**

- **Notifications**: case created of type *chargeback* with card‑network reason code and due date.

- **Evidence pack** includes:

  - Signed docs, delivery approvals, message history, IP/device matches, geotime, studio check‑in, manifest checksums, comms delivery.

- **Submission**: representment summary + attachments; track provider ref & due date.

- **Outcomes**:

  - **Won** → release holds; reverse expense.
  - **Lost** → GL *Expense:Chargebacks*, optional risk downgrade (§1.6), optional review of promotions eligibility (§1.7).

## **1.15.L DMCA & policy violations**

- **DMCA intake**: form collects claimant info, URLs, statements under penalty; content hidden immediately; case links to Fan‑Sub/studio media ids.
- **Counter notice**: creator submits; legal review; restore if valid; retain evidence.
- **Policy violations**: T&S adjudication; penalties ladder (warning → temp suspension → permanent removal).
- **Appeals**: one appeal per decision; immutable audit in *support_event*.

## **1.15.M Telemetry, dashboards & SLOs**

**SLOs**

- First response: **≤ 8h** (normal), **≤ 1h** (urgent).
- Resolution: **≤ 72h** average for non‑chargeback; **≤ network deadline** for chargebacks.
- SLA breach rate **\< 5%** rolling 30 days.

**Dashboards**

- Volume by type/subtype & city; backlog aging; SLA breach trend.
- Refund rate by reason; goodwill spend; chargeback **win rate**; DMCA volume/outcomes.
- Payout holds applied/released and exposure at risk.

**Events**

- *support.case.open\|assign\|status_change\|close*, *support.refund.proposed\|succeeded\|failed*,
- *support.hold.apply\|release*, *chargeback.notified\|represented\|won\|lost*,
- *dmca.received\|hidden\|restored*.

## **1.15.N Performance & cost posture**

- **Ticketing** in Aurora (no external SaaS at launch).
- **Email bridge** via SES (inbound + outbound) to avoid Twilio SendGrid costs.
- **Storage**: S3 evidence with lifecycle; avoid storing large videos—store **manifests** and small screenshots.
- **Compute**: Lambda for parsers and automations; Step Functions for chargeback deadlines; no provisioned concurrency unless needed.

## **1.15.O Error taxonomy (client‑safe)**

- *CASE_NOT_FOUND*, *CASE_ACCESS_DENIED*
- *ATTACHMENT_BLOCKED* (malware/NSFW)
- *REFUND_NOT_ELIGIBLE* (policy)
- *PAYOUT_HOLD_APPLY_FAILED* (admin‑only)
- *CHARGEBACK_DEADLINE_PASSED* (admin‑only)  
  Each with *code*, *message*, *hint*, *corrId*.

## **1.15.P Test plan (CI + sandbox)**

**Core flows**

1678. Open case from booking/order context; timeline auto‑stitches evidence.
1679. Deterministic refund outcomes by cancellation bands; manual override requires dual approval.
1680. Payout hold applied & released; finance views update.

**Chargebacks**  
4) Chargeback intake; evidence pack creation; representment submitted; outcome handling (GL + risk).

**DMCA & policy**  
5) DMCA hides content; counter‑notice restores; audits present.  
6) Policy violation escalations; appeals path.

**Email bridge**  
7) Inbound email creates/appends case; spoofing rejected; attachments scanned.  
8) Outbound reply threading correct.

**SLA & automations**  
9) SLA timers escalate; macros apply consistent decisions; rules trigger holds on thresholds.

**Analytics**  
10) Case events land in Bronze → Silver → Gold (§1.13); dashboards show backlog and win rates.

**Performance & cost**  
11) p95 case list fetch ≤ 120 ms; evidence download streams; S3 lifecycle verified.

## **1.15.Q Work packages (Cursor 4‑agent lanes)**

- **Agent C — Domain/API**  
  WP‑SUP‑01: SQL for *support\_\** tables; GraphQL queries/mutations; timeline stitching.  
  WP‑SUP‑02: Refund calculator (ties to §1.3/§1.9); payout hold service.
- **Agent B — Payments/Chargebacks**  
  WP‑SUP‑CB‑01: Chargeback ingest + representment builder; GL side‑effects.  
  WP‑SUP‑DMCA‑01: DMCA intake + hide/restore endpoints; evidence vault.
- **Agent A — Web (Support Center)**  
  WP‑SUP‑WEB‑01: Case list/detail UI, message composer, uploads; booking/order context launchers.  
  WP‑SUP‑WEB‑02: Admin consoles (queues, macros, SLA board, batch actions).
- **Agent D — Comms/QA**  
  WP‑SUP‑COMMS‑01: SES inbound/outbound bridge; templates and quiet hours (hooks §1.10).  
  WP‑SUP‑QA‑01: Test automation for all flows; synthetic chargeback timelines.

## **1.15.R Acceptance criteria (mark §1.15 FINAL only when ALL true)**

1685. Users and agents can create, view, message, and close cases; evidence timelines auto‑assembled.
1686. Refund & goodwill flows compute correct amounts with proper GL entries; overrides require dual approval.
1687. Chargebacks handled end‑to‑end with evidence packs and outcomes; payout holds applied and released correctly.
1688. DMCA intake/hide/restore works with immutable audits; policy violations adjudicated with an appeal path.
1689. Email bridge functional and safe (spoofing resistance, scanning); Support Center UI meets accessibility basics.
1690. Telemetry dashboards live; SLA breach rate within targets for synthetic runs; costs within budget alarms.

# **§1.16 — Growth, Retention & Referrals**

*(saved searches & alerts · weekly city digest · feed & follow · sharecards & link‑in‑bio · “book again” reminders · referrals/credits & anti‑abuse · data models · API · comms · telemetry · cost · tests)*

**What this implements from the non‑technical plan.**  
• **Saved Search → Alert** (ANY/ALL filters, 1/day per search; 30‑day pause toggle) and **Weekly City Digest**.

NonTechBlueprint

• **Feed & Follow** (single unified feed with role tabs; Verified chip; Safe‑Mode SFW previews).

NonTechBlueprint

• **Social share loop**: Sharecard generator + link‑in‑bio minisite with UTM.

NonTechBlueprint

• **Auto “Book Again”** at **7/30/90 days** for recurring packages.

NonTechBlueprint

• **Referrals & Credits (two‑sided)** with monthly caps, ID gate, device/IP fraud checks, and **clawback if first booking is refunded for fraud**.

NonTechBlueprint

• **Global Safe‑Mode** defaults and comms constraints for 18+ material.

NonTechBlueprint

We will not leave §1.16 until the checklist at the end is met.

## **1.16.A Canon & invariants**

1691. **Respect Safe‑Mode & policy** in all growth surfaces (SFW previews publicly; 18+ only in‑app with Safe‑Mode OFF).

NonTechBlueprint

1692. **No spam:** per‑search alert frequency **≤1/day**; weekly digest opt‑in; easy “pause 30 days.”

NonTechBlueprint

1693. **Evidence & attribution:** all growth sends include **UTM** and first‑party click tokens so conversions are attributable in §1.13.

NonTechBlueprint

1694. **Abuse‑resistant referrals:** hard caps, ID checks, same device/IP detection, and **credit clawback** if the first booking is fraudulent/refunded.

NonTechBlueprint

1695. **Cost‑conscious**: serverless jobs (EventBridge Scheduler + Lambda), dedupe in DynamoDB with TTL, SES/SNS for comms (no heavy third‑party tools).

## **1.16.B Data model (Aurora + Dynamo + Typesense)**

### **B.1 Aurora (source of truth)**

*-- Saved searches (people & studios)*  
*create table saved_search (*  
*search_id text primary key, -- ssv\_...*  
*user_id text not null, -- usr\_...*  
*scope text not null check (scope in ('people','studios')),*  
*query_json jsonb not null, -- normalized filters (ANY/ALL groups)*  
*city text not null,*  
*paused_until date, -- 30-day pause*  
*last_alert_dt date, -- last day an alert was sent*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
  
*-- Alert sends (daily dedupe)*  
*create table saved_search_alert (*  
*alert_id text primary key, -- ssa\_...*  
*search_id text not null references saved_search(search_id) on delete cascade,*  
*alert_dt date not null,*  
*match_count int not null,*  
*email_sent boolean not null default false,*  
*inapp_created boolean not null default false,*  
*created_at timestamptz not null default now(),*  
*unique (search_id, alert_dt)*  
*);*  
  
*-- Follow graph (for Feed)*  
*create table follow (*  
*follower_user_id text not null,*  
*target_id text not null, -- usr\_... (people) or fsc\_... (Fan-Sub creator)*  
*target_kind text not null check (target_kind in ('service_profile','fansub_creator')),*  
*created_at timestamptz not null default now(),*  
*primary key (follower_user_id, target_id, target_kind)*  
*);*  
  
*-- Feed posts metadata (case studies, availability cards, touring chips, verified studio slots)*  
*create table feed_post (*  
*feed_id text primary key, -- fdp\_...*  
*author_id text not null, -- usr\_... or fsc\_...*  
*role_tags text\[\] not null, -- \['Model','Photog',...\]*  
*kind text not null check (kind in ('case_study','availability','touring','studio_slot','influence')),*  
*title text not null,*  
*body_md text,*  
*media_preview jsonb not null default '\[\]'::jsonb, -- SFW previews*  
*nsfw_band int not null default 0, -- 0 allow,1 blur,2 block*  
*city text, -- for touring/availability*  
*verified_chip boolean not null default false,*  
*is_published boolean not null default false,*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
  
*-- Referrals & credits (ledger-based)*  
*create table referral_program (*  
*program_id text primary key, -- rpr\_...*  
*kind text not null check (kind in ('provider_invites_provider','buyer_invites_buyer','cross_side')),*  
*reward_bips int not null default 0, -- optional future %*  
*reward_fixed_cents int not null default 0, -- e.g., \$1500 = \$15.00*  
*credit_scope text not null, -- 'buyer_fee_only' etc.*  
*monthly_cap int not null default 5, -- per-user awards cap*  
*active boolean not null default true,*  
*created_at timestamptz not null default now()*  
*);*  
  
*create table referral_invite (*  
*invite_id text primary key, -- rfi\_...*  
*program_id text not null references referral_program(program_id),*  
*inviter_user_id text not null,*  
*invitee_user_id text, -- populated after signup*  
*invitee_email_sha text not null, -- hashed*  
*source text, -- sharecard/linkinbio/…*  
*device_fp text, -- device fingerprint*  
*ip_addr_sha text,*  
*created_at timestamptz not null default now(),*  
*accepted_at timestamptz*  
*);*  
  
*-- Credit ledger entries (immutable)*  
*create table credit_ledger (*  
*entry_id text primary key, -- crl\_...*  
*user_id text not null,*  
*kind text not null check (kind in ('award','clawback','redeem')),*  
*program_id text,*  
*amount_cents int not null,*  
*currency text not null default 'USD',*  
*reason text not null,*  
*related_id text, -- booking_id, invite_id*  
*created_at timestamptz not null default now()*  
*);*  

### **B.2 DynamoDB (hot path)**

- *saved_search_dedupe*: *(PK=search_id, SK=YYYY-MM-DD)* prevents \>1 alert/day; TTL auto‑expires older rows.
- *feed_fanout_cursor*: per follower “last seen” cursor to build incremental feed pages.
- *referral_device_daily*: counters *(device_fp, date)* and *(ip_hash, date)* for rate‑limit and fraud signals.

### **B.3 Search indices (Typesense/OpenSearch)**

- **people_v1** and **studios_v1** already defined; extend with **facets for ANY/ALL** groups and **verified/trusted** flags used in alerts.

NonTechBlueprint

## **1.16.C Saved Searches & Alerts (ANY/ALL + 1/day cap)**

### **C.1 Query model**

- **ANY/ALL**: store filters as *{"any":\[...\],"all":\[...\]}*; search layer builds a boolean query to Typesense/OpenSearch.

NonTechBlueprint

- Safe‑Mode enforced in the query (e.g., hide nudity tiers beyond “Lingerie/Swim” when ON).

NonTechBlueprint

### **C.2 Daily job (EventBridge Scheduler → Lambda)**

1702. For each active *saved_search* not *paused_until \> today*, compute **new matches since** ***last_alert_dt***.

1703. If *match_count\>0* and no *saved_search_alert* exists for *today* (and no Dynamo dedupe row found), create:

      207. an **in‑app digest** item,
      208. an **email** (SES) with at most 20 cards + “View All” deep link,
      209. update *last_alert_dt=today*, write *saved_search_alert*.

1704. **Frequency cap**: exactly **≤1/day/search**.

NonTechBlueprint

1705. **Pause 30 days** toggles *paused_until = today + 30*.

NonTechBlueprint

## **1.16.D Weekly City Digest (opt‑in)**

- Cron weekly per city; content blocks: **featured case studies**, **Verified Studios with open slots**, **Top rising creators** (Rep growth).

NonTechBlueprint

- Safe‑Mode rules for previews; **no 18+** content in email.

NonTechBlueprint

- Unsubscribe per‑digest type; quiet‑hours respected.

## **1.16.E Feed & Follow**

### **E.1 Surfaces (mirrors plan language)**

- **Single unified feed** per user with **role tabs** (Model/Photog/Vid/Creator/Fan‑Sub Creator).

NonTechBlueprint

- Pulls **new case studies**, **availability cards** (“Now booking Saturday”), **touring chips** (e.g., “Visiting Austin 11/20–11/22”), **Verified Studio open slots**, **Verified influence posts** (SFW preview + “Verified” tick).

NonTechBlueprint

- Safe‑Mode default ON for guests/new users; applies to People (18+ gating) but **never hides Studios**.

NonTechBlueprint

### **E.2 Delivery & ranking**

- Build a **fan‑out‑on‑read** feed: query *feed_post* + follows; rank by recency, followed weight, verified chip, and engagement.
- Cursors (time + id) for pagination; **no unbounded fan‑out**.

### **E.3 Authoring**

- Creators/providers publish feed posts tagged by **role(s)**; one post can serve all tabs.

NonTechBlueprint

- Media previews run through the same **NSFW scan** rules as §1.10/§1.14; public views stay SFW.

## **1.16.F Social Share & Link‑in‑Bio**

### **F.1 Sharecard generator**

- **Lambda (headless Chromium)** renders responsive PNG/WebP with: avatar, name, role(s), city, 1–3 images, **QR** to profile/booking link, and **UTM**.

NonTechBlueprint

- Output sizes for IG/TikTok aspect ratios; store in S3 with **year‑long** cache.
- Watermark minimal; Safe‑Mode preview rules apply.

### **F.2 Link‑in‑bio minisite**

- Static microsite auto‑generated per user: **packages**, **availability**, **contact CTA**; includes **UTM** for attribution.

NonTechBlueprint

- Hosted on CloudFront; vanity URL; Safe‑Mode rules for previews.

## **1.16.G “Book Again” reminders (7/30/90)**

- Scheduler picks eligible past bookings tagged as **recurring packages**; sends **“Book Again”** at **7**, **30**, and **90** days post‑completion, pre‑filled with last scope and adjusted dates.

NonTechBlueprint

- Frequency caps by buyer/service‑profile pair; auto‑disables when buyer opts out.
- No 18+ media in comms; deep link to draft checkout.

## **1.16.H Referrals & Credits (two‑sided, abuse‑resistant)**

### **H.1 Programs (as per plan)**

- **Provider invites provider** → both get **+20 DM credits** after invitee **publishes a package** and completes **1 booking**.

NonTechBlueprint

- **Buyer invites buyer** → inviter gets **1 RFP credit** when invitee **posts a brief** and **awards** a booking.

NonTechBlueprint

- **Cross‑side referrals**: provider invites buyer; **\$15 buyer credit** toward next booking (**buyer fee only**). Guardrails below.

NonTechBlueprint

### **H.2 Guardrails (explicit from plan)**

- **Per‑user monthly caps**; **ID required** to redeem; **same device/IP fraud detection**; **clawback** if first booking is **refunded for fraud**.

NonTechBlueprint

### **H.3 Mechanics**

- **Invite flow** issues signed links that encode *program_id* and inviter; capture device/IP on accept.
- **Qualification events**: “package published,” “brief posted,” “booking awarded/completed” feed a small **rules engine**; on pass, write **credit_ledger (award)**.
- **Clawback**: upon fraud/refund adjudication in §1.15/§1.9, write **credit_ledger (clawback)** and revoke unused credits.

## **1.16.I GraphQL API (selected)**

*\# Saved search & alerts*  
*type SavedSearch { searchId: ID!, scope: String!, city: String!, queryJson: AWSJSON!, pausedUntil: AWSDate }*  
*type SavedSearchAlert { alertId: ID!, alertDt: AWSDate!, matchCount: Int!, emailSent: Boolean!, inappCreated: Boolean! }*  
  
*type Query {*  
*mySavedSearches: \[SavedSearch!\]!*  
*myFeed(cursor: String, limit: Int = 25, tab: String): FeedPage!*  
*}*  
  
*input SavedSearchInput { scope: String!, city: String!, queryJson: AWSJSON! }*  
  
*type Mutation {*  
*createSavedSearch(input: SavedSearchInput!): SavedSearch!*  
*pauseSavedSearch(searchId: ID!, days: Int!): SavedSearch! \# 30 days typical*  
*deleteSavedSearch(searchId: ID!): Boolean!*  
  
*follow(targetId: ID!, targetKind: String!): Boolean!*  
*unfollow(targetId: ID!, targetKind: String!): Boolean!*  
  
*sendReferral(programId: ID!, inviteeEmail: String!): Boolean!*  
*redeemCredit(entryId: ID!, amountCents: Int!): Boolean! \# buyer fee only scope validated server-side*  
*}*  

**Server guards**: Safe‑Mode checks in feed; per‑search daily dedupe; per‑user referral caps; ID/age gate for credit redemption where required.

## **1.16.J Comms & templates**

- **Saved search alert** (daily cap)
- **Weekly city digest** (opt‑in)
- Book again 7/30/90
- **Referral invite** and **award** confirmations  
  All templates deliver **SFW** previews only and include **preference links**.

NonTechBlueprint

## **1.16.K Telemetry & experiments (hooked into §1.13)**

- **Events**: *search.saved\|alert.sent\|alert.click*, *feed.post.publish\|impression\|click*, *sharecard.create\|click*, *lib.microsite.visit*, *book_again.sent\|clicked\|converted*, *referral.invite\|accepted\|qualified\|clawback*.
- **Gold KPIs**: alert CTR, digest CTR, follow growth, feed engagement, book‑again conversion, referral qualification rate, fraud/clawback rate.
- **Guardrails**: unsubscribe/complaint rates; Safe‑Mode breaches (should be zero for emails).
- **NRT** ops tiles: today’s alerts/digests volume, referral awards vs caps, clawbacks.

## **1.16.L Performance & cost**

- **Schedulers**: EventBridge scheduled Lambdas (cron & daily); no long‑running workers.
- **Search**: pre‑compute **match hashes** to reduce index scans for alerts; use Typesense filters efficiently.
- **Storage**: S3 for sharecards, lifecycle → Intelligent‑Tiering @30d; CloudFront cache hits ≥95%.
- **Email**: SES shared IPs; digest batches to keep costs low.
- **Dynamo**: TTL‑based dedupe tables; RCU/WCU caps.
- **Budgets**: alarms on SES sends/day, Lambda duration, Dynamo capacity.

## **1.16.M Error taxonomy (client‑safe)**

- *ALERT_FREQUENCY_LIMIT* — already sent today for this search.
- *DIGEST_OPTOUT* — user unsubscribed.
- *SAFE_MODE_BLOCKED* — attempting to include 18+ in email.
- *REFERRAL_CAP_EXCEEDED* — monthly cap reached.
- *CREDIT_SCOPE_VIOLATION* — tried to apply buyer credit to non‑fee items.
- Each error returns *code*, *message*, *hint*, and *corrId*.

## **1.16.N Test plan (CI + sandbox)**

**Saved searches & alerts**

1751. ANY/ALL correctness; Safe‑Mode gates; 1/day frequency; 30‑day pause respected; alert contains only *new* matches.

NonTechBlueprint

NonTechBlueprint

**Weekly digest**  
2) Opt‑in/out; city content blocks; no 18+ previews in email.

NonTechBlueprint

NonTechBlueprint

**Feed & follow**  
3) Unified feed with role tabs; Verified chip; SFW previews on public; pagination stable.

NonTechBlueprint

**Sharecards & link‑in‑bio**  
4) Image renders for IG/TT; QR & UTM present; attribution shows in §1.13 marts.

NonTechBlueprint

**Book again**  
5) 7/30/90 schedule; prefill scope; opt‑out honored; conversions attributed.

NonTechBlueprint

**Referrals & credits**  
6) Program qualifications (publish package / post brief / award + complete); monthly caps; device/IP checks; clawback on fraud/refund.

NonTechBlueprint

**Telemetry & cost**  
7) Events land Bronze→Silver→Gold; dashboards populate; SES/Lambda/Dynamo within budgets.

## **1.16.O Work packages (Cursor 4‑agent lanes)**

- **Agent B — Domain/API**: Saved Search, Feed, Referrals SQL + resolvers; daily/weekly schedulers; credit ledger; book‑again job.
- **Agent C — Search/Index**: ANY/ALL query builder; match hash generation; Verified/Trusted facets.
- **Agent A — Web**: Saved Search UI (ANY/ALL builder), Feed with role tabs & Verified chip, link‑in‑bio page, sharecard UI.
- **Agent D — Comms/QA**: MJML templates (alerts/digest/book‑again/referrals), SES setup, test automation for dedupe and caps.

## **1.16.P Acceptance criteria (mark §1.16 FINAL only when ALL true)**

1756. Saved Searches support ANY/ALL, Safe‑Mode filters, and **≤1/day** alerts with 30‑day pause.

NonTechBlueprint

NonTechBlueprint

1757. Weekly City Digest ships, opt‑in/out respected, **SFW only** in email.

NonTechBlueprint

NonTechBlueprint

1758. Unified Feed delivers case studies, availability, touring chips, verified studio slots, influence posts with role tabs and Verified chip; Safe‑Mode enforced.

NonTechBlueprint

1759. Sharecards and link‑in‑bio microsite generate correctly with UTM and QR, and conversions are attributable.

NonTechBlueprint

1760. “Book Again” at 7/30/90 runs with prefilled scope; frequency caps and opt‑outs enforced.

NonTechBlueprint

1761. Referrals/credits hit qualification rules, enforce monthly caps/ID/device/IP rules, and **claw back** on fraud/refund.

NonTechBlueprint

1762. Telemetry, dashboards, budgets, and alarms are live; cost and SLO targets met on a 48‑hour synthetic run.

# **§1.16 — Artifacts (inline, text‑only)**

**How to paste into your doc:** Keep the headings and the “Recommended filename/path” comments so your team can find each artifact later.

## **1.16‑A. SQL — Growth & Referrals schema (Aurora PostgreSQL)**

**Recommended filename/path:** *db/migrations/016_growth_referrals.sql*

*-- 016_growth_referrals.sql*  
*-- Saved searches (ANY/ALL filters), alert sends, follow graph, feed posts,*  
*-- referrals & credits (ledger), with sensible indexes.*  
  
*begin;*  
  
*create table if not exists saved_search (*  
*search_id text primary key, -- ssv\_...*  
*user_id text not null, -- usr\_...*  
*scope text not null check (scope in ('people','studios')),*  
*query_json jsonb not null, -- normalized ANY/ALL filters*  
*city text not null,*  
*paused_until date,*  
*last_alert_dt date,*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
*create index if not exists idx_saved_search_user on saved_search(user_id);*  
*create index if not exists idx_saved_search_city on saved_search(city);*  
  
*create table if not exists saved_search_alert (*  
*alert_id text primary key, -- ssa\_...*  
*search_id text not null references saved_search(search_id) on delete cascade,*  
*alert_dt date not null,*  
*match_count int not null,*  
*email_sent boolean not null default false,*  
*inapp_created boolean not null default false,*  
*created_at timestamptz not null default now(),*  
*unique (search_id, alert_dt)*  
*);*  
  
*create table if not exists follow (*  
*follower_user_id text not null, -- usr\_...*  
*target_id text not null, -- usr\_... \| fsc\_...*  
*target_kind text not null check (target_kind in ('service_profile','fansub_creator')),*  
*created_at timestamptz not null default now(),*  
*primary key (follower_user_id, target_id, target_kind)*  
*);*  
  
*create table if not exists feed_post (*  
*feed_id text primary key, -- fdp\_...*  
*author_id text not null,*  
*role_tags text\[\] not null,*  
*kind text not null check (kind in ('case_study','availability','touring','studio_slot','influence')),*  
*title text not null,*  
*body_md text,*  
*media_preview jsonb not null default '\[\]'::jsonb, -- SFW previews only*  
*nsfw_band int not null default 0, -- 0 allow,1 blur,2 block*  
*city text,*  
*verified_chip boolean not null default false,*  
*is_published boolean not null default false,*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
*create index if not exists idx_feed_post_pub on feed_post(is_published, created_at desc);*  
*create index if not exists idx_feed_post_city on feed_post(city);*  
  
*create table if not exists referral_program (*  
*program_id text primary key, -- rpr\_...*  
*kind text not null check (kind in ('provider_invites_provider','buyer_invites_buyer','cross_side')),*  
*reward_bips int not null default 0,*  
*reward_fixed_cents int not null default 0,*  
*credit_scope text not null, -- e.g., 'buyer_fee_only'*  
*monthly_cap int not null default 5,*  
*active boolean not null default true,*  
*created_at timestamptz not null default now()*  
*);*  
  
*create table if not exists referral_invite (*  
*invite_id text primary key, -- rfi\_...*  
*program_id text not null references referral_program(program_id),*  
*inviter_user_id text not null,*  
*invitee_user_id text,*  
*invitee_email_sha text not null,*  
*source text, -- 'sharecard','linkinbio', etc.*  
*device_fp text,*  
*ip_addr_sha text,*  
*created_at timestamptz not null default now(),*  
*accepted_at timestamptz*  
*);*  
*create index if not exists idx_rfi_inviter on referral_invite(inviter_user_id, created_at desc);*  
*create index if not exists idx_rfi_email on referral_invite(invitee_email_sha);*  
  
*create table if not exists credit_ledger (*  
*entry_id text primary key, -- crl\_...*  
*user_id text not null,*  
*kind text not null check (kind in ('award','clawback','redeem')),*  
*program_id text,*  
*amount_cents int not null,*  
*currency text not null default 'USD',*  
*reason text not null,*  
*related_id text,*  
*created_at timestamptz not null default now()*  
*);*  
*create index if not exists idx_credit_user on credit_ledger(user_id, created_at desc);*  
  
*commit;*  

## **1.16‑B. DynamoDB — hot‑path/TTL tables**

**Recommended filename/path:** *infra/dynamodb/016_growth_ttl_tables.md* *(doc note for infra CDK)*

*Table: saved_search_dedupe*  
*Key: PK = search_id, SK = alert_date (YYYY-MM-DD)*  
*Attributes: ttl_epoch (Number)*  
*Purpose: ensure ≤1 alert/day/search; items auto-expire via TTL.*  
  
*Table: feed_fanout_cursor*  
*Key: PK = user_id, SK = 'cursor'*  
*Attributes: last_seen_created_at (ISO), last_seen_id*  
*Purpose: incremental paging for unified feed.*  
  
*Table: referral_device_daily*  
*Key: PK = device_fp#YYYY-MM-DD, SK = program_id*  
*Attributes: ip_hash, count*  
*TTL: next day*  
*Purpose: rate-limit & fraud signal for invites/accepts.*  

## **1.16‑C. GraphQL SDL — Saved Search, Feed, Referrals**

**Recommended filename/path:** *api/schema/growth.graphql*

*\# growth.graphql*  
  
*scalar AWSJSON*  
*scalar AWSDate*  
*scalar AWSDateTime*  
  
*type SavedSearch {*  
*searchId: ID!*  
*scope: String!*  
*city: String!*  
*queryJson: AWSJSON!*  
*pausedUntil: AWSDate*  
*lastAlertDt: AWSDate*  
*createdAt: AWSDateTime!*  
*updatedAt: AWSDateTime!*  
*}*  
  
*type SavedSearchAlert {*  
*alertId: ID!*  
*searchId: ID!*  
*alertDt: AWSDate!*  
*matchCount: Int!*  
*emailSent: Boolean!*  
*inappCreated: Boolean!*  
*createdAt: AWSDateTime!*  
*}*  
  
*type FeedCard {*  
*feedId: ID!*  
*authorId: ID!*  
*roleTags: \[String!\]!*  
*kind: String!*  
*title: String!*  
*bodyMd: String*  
*mediaPreview: AWSJSON!*  
*city: String*  
*verifiedChip: Boolean!*  
*createdAt: AWSDateTime!*  
*}*  
  
*type FeedPage { items: \[FeedCard!\]!, cursor: String }*  
  
*type ReferralInvite { inviteId: ID!, programId: ID!, inviterUserId: ID!, acceptedAt: AWSDateTime }*  
*type CreditLedger { entryId: ID!, userId: ID!, kind: String!, amountCents: Int!, reason: String!, createdAt: AWSDateTime! }*  
  
*input SavedSearchInput { scope: String!, city: String!, queryJson: AWSJSON! }*  
  
*type Query {*  
*mySavedSearches: \[SavedSearch!\]!*  
*myFeed(cursor: String, limit: Int = 25, tab: String): FeedPage!*  
*myCredits: \[CreditLedger!\]!*  
*}*  
  
*type Mutation {*  
*createSavedSearch(input: SavedSearchInput!): SavedSearch!*  
*pauseSavedSearch(searchId: ID!, days: Int!): SavedSearch!*  
*deleteSavedSearch(searchId: ID!): Boolean!*  
  
*follow(targetId: ID!, targetKind: String!): Boolean!*  
*unfollow(targetId: ID!, targetKind: String!): Boolean!*  
  
*sendReferral(programId: ID!, inviteeEmail: String!): Boolean!*  
*redeemCredit(entryId: ID!, amountCents: Int!): Boolean!*  
*}*  

## **1.16‑D. EventBridge schedules (cron) — Alerts/Digests/Book‑Again**

**Recommended filename/path:** *infra/schedules/growth-schedules.yml*

*\# growth-schedules.yml (declarative intent; implemented via CDK/Amplify Gen 2)*  
*schedules:*  
* - name: saved-search-alerts-daily*  
*cron: "cron(5 13 \* \* ? \*)" \# 13:05 UTC daily*  
*targetLambda: growthSavedSearchAlerts*  
* - name: weekly-city-digest*  
*cron: "cron(15 14 ? \* MON \*)" \# Mondays 14:15 UTC*  
*targetLambda: growthWeeklyDigest*  
* - name: book-again-7d*  
*cron: "cron(0 12 \* \* ? \*)"*  
*targetLambda: growthBookAgain7*  
* - name: book-again-30d*  
*cron: "cron(5 12 \* \* ? \*)"*  
*targetLambda: growthBookAgain30*  
* - name: book-again-90d*  
*cron: "cron(10 12 \* \* ? \*)"*  
*targetLambda: growthBookAgain90*  

## **1.16‑E. Lambda handler skeleton — Saved Search Alerts**

**Recommended filename/path:** *apps/functions/growthSavedSearchAlerts.ts*

*// growthSavedSearchAlerts.ts*  
*// Pseudocode: load eligible searches, query index, dedupe (Dynamo), send in-app + email via SES.*  
  
*import { queryPeople, queryStudios } from '../lib/search';*  
*import { getEligibleSavedSearches, markAlertSent } from '../lib/savedSearchRepo';*  
*import { dynamoDedupeHit } from '../lib/dedupe';*  
*import { sendEmail } from '../lib/ses';*  
*import { createInAppDigest } from '../lib/inapp';*  
  
*export const handler = async () =\> {*  
*const searches = await getEligibleSavedSearches();*  
*for (const s of searches) {*  
*const alreadySent = await dynamoDedupeHit(s.searchId);*  
*if (alreadySent) continue;*  
  
*const matches = s.scope === 'people'*  
*? await queryPeople(s.query_json, s.city)*  
*: await queryStudios(s.query_json, s.city);*  
  
*if (matches.length === 0) continue;*  
  
*await createInAppDigest(s.user_id, s.search_id, matches.slice(0, 20));*  
*await sendEmail({*  
*toUserId: s.user_id,*  
*template: 'saved_search_alert',*  
*vars: { city: s.city, count: matches.length, cards: matches.slice(0, 20) }*  
*});*  
  
*await markAlertSent(s.search_id, matches.length);*  
*}*  
*};*  

## **1.16‑F. MJML template — Saved Search Alert (SFW‑only)**

**Recommended filename/path:** *comms/templates/saved_search_alert.mjml*

*\<mjml\>*  
*\<mj-head\>*  
*\<mj-title\>New matches in {{city}}\</mj-title\>*  
*\<mj-attributes\>*  
*\<mj-text font-size="14px" line-height="20px" /\>*  
*\</mj-attributes\>*  
*\</mj-head\>*  
*\<mj-body\>*  
*\<mj-section\>*  
*\<mj-column\>*  
*\<mj-text font-size="18px"\>\<strong\>{{count}}\</strong\> new match{{#plural count}}es{{/plural}} in {{city}}\</mj-text\>*  
*\<mj-text\>We’ve found new profiles that match your saved search. Previews are SFW.\</mj-text\>*  
*\</mj-column\>*  
*\</mj-section\>*  
  
*{{#each cards}}*  
*\<mj-section\>*  
*\<mj-column\>*  
*\<mj-image src="{{this.previewUrl}}" alt="{{this.title}} — SFW preview" /\>*  
*\<mj-text\>\<strong\>{{this.title}}\</strong\>\<br/\>{{this.subtitle}}\</mj-text\>*  
*\<mj-button href="{{this.deepLink}}"\>View profile\</mj-button\>*  
*\</mj-column\>*  
*\</mj-section\>*  
*{{/each}}*  
  
*\<mj-section\>*  
*\<mj-column\>*  
*\<mj-text\>If you’d like to pause alerts for 30 days, \<a href="{{pauseLink}}"\>click here\</a\>.\</mj-text\>*  
*\<mj-text font-size="12px" color="#666"\>No 18+ content is included in this email. To change preferences, visit Settings.\</mj-text\>*  
*\</mj-column\>*  
*\</mj-section\>*  
*\</mj-body\>*  
*\</mjml\>*  

## **1.16‑G. JSON Schemas — Key Growth Events**

**Recommended filename/path:** *data/schemas/growth-events/*

*// search.saved.v1.json*  
*{*  
*"\$id": "*[*https://rastup/schemas/search.saved.v1.json*](https://rastup/schemas/search.saved.v1.json)*",*  
*"\$schema": "*[*https://json-schema.org/draft/2020-12/schema*](https://json-schema.org/draft/2020-12/schema)*",*  
*"type": "object",*  
*"required": \["scope","city","query_hash"\],*  
*"properties": {*  
*"scope": { "type": "string", "enum": \["people","studios"\] },*  
*"city": { "type": "string" },*  
*"query_hash": { "type": "string" }*  
*},*  
*"additionalProperties": false*  
*}*  

*// alert.sent.v1.json*  
*{*  
*"\$id": "*[*https://rastup/schemas/alert.sent.v1.json*](https://rastup/schemas/alert.sent.v1.json)*",*  
*"\$schema": "*[*https://json-schema.org/draft/2020-12/schema*](https://json-schema.org/draft/2020-12/schema)*",*  
*"type": "object",*  
*"required": \["search_id","count","channel"\],*  
*"properties": {*  
*"search_id": { "type": "string" },*  
*"count": { "type": "integer", "minimum": 1 },*  
*"channel": { "type": "string", "enum": \["email","inapp"\] }*  
*},*  
*"additionalProperties": false*  
*}*  

*// referral.invite.v1.json*  
*{*  
*"\$id": "*[*https://rastup/schemas/referral.invite.v1.json*](https://rastup/schemas/referral.invite.v1.json)*",*  
*"\$schema": "*[*https://json-schema.org/draft/2020-12/schema*](https://json-schema.org/draft/2020-12/schema)*",*  
*"type": "object",*  
*"required": \["program_id","inviter_user_id","invitee_email_sha"\],*  
*"properties": {*  
*"program_id": { "type": "string" },*  
*"inviter_user_id": { "type": "string" },*  
*"invitee_email_sha": { "type": "string" },*  
*"source": { "type": "string" }*  
*},*  
*"additionalProperties": false*  
*}*  

## **1.16‑H. Cost guardrails (observability notes)**

**Recommended filename/path:** *observability/budgets/growth-guards.md*

*Metrics & alarms:*  
*- SES sends/day: warn at 80% of daily cap; hard stop at 120% (switch to in-app only).*  
*- Lambda duration: P95 \> 750ms sustained 10m → investigate search query shapes.*  
*- Dynamo RCU/WCU: consume \> 80% for 15m → auto scale + alert.*  
*- Typesense/OpenSearch: QPS spikes \> 3x baseline → enable precomputed match hashes for saved-search batch.*  

# **§1.16 — Artifacts (inline, text-only) — Continuation**

Below are the remaining **copy-pasteable** blocks for the project plan. Each includes a **Recommended filename/path** label so your builders can later lift them into a repo if you choose. These are all text for your single Word doc.

## **1.16-I. MJML — Weekly City Digest (SFW-only, opt-in)**

**Recommended filename/path:** *comms/templates/weekly_city_digest.mjml*

*\<mjml\>*  
*\<mj-head\>*  
*\<mj-title\>Your {{city}} weekly creative digest\</mj-title\>*  
*\<mj-attributes\>*  
*\<mj-all font-family="Inter, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif" /\>*  
*\<mj-text font-size="14px" line-height="20px" /\>*  
*\<mj-section padding="0" /\>*  
*\<mj-column padding="0" /\>*  
*\</mj-attributes\>*  
*\<mj-style\>*  
*.chip { background:#F2F4F7; border-radius:16px; padding:4px 10px; font-size:12px; }*  
*\</mj-style\>*  
*\</mj-head\>*  
  
*\<mj-body background-color="#ffffff"\>*  
  
*\<!-- Header --\>*  
*\<mj-section padding="16px 24px"\>*  
*\<mj-column\>*  
*\<mj-text font-size="20px" font-weight="600"\>This week in {{city}}\</mj-text\>*  
*\<mj-text color="#667085"\>SFW previews only. Update preferences anytime.\</mj-text\>*  
*\</mj-column\>*  
*\</mj-section\>*  
  
*\<!-- Featured case studies --\>*  
*{{#if caseStudies.length}}*  
*\<mj-section padding="8px 24px"\>*  
*\<mj-column\>*  
*\<mj-text font-size="16px" font-weight="600"\>Featured case studies\</mj-text\>*  
*\</mj-column\>*  
*\</mj-section\>*  
*{{#each caseStudies}}*  
*\<mj-section padding="0 24px 12px"\>*  
*\<mj-column\>*  
*\<mj-image src="{{this.preview}}" alt="{{this.title}} — SFW preview" padding-bottom="8px" /\>*  
*\<mj-text\>\<strong\>{{this.title}}\</strong\>\<br/\>{{this.subtitle}}\</mj-text\>*  
*\<mj-text\>\<span class="chip"\>{{this.role}}\</span\> \<span class="chip"\>{{this.neighborhood}}\</span\>\</mj-text\>*  
*\<mj-button href="{{this.link}}"\>See the full breakdown\</mj-button\>*  
*\</mj-column\>*  
*\</mj-section\>*  
*{{/each}}*  
*{{/if}}*  
  
*\<!-- Verified Studios with open slots --\>*  
*{{#if studios.length}}*  
*\<mj-section padding="8px 24px"\>*  
*\<mj-column\>*  
*\<mj-text font-size="16px" font-weight="600"\>Verified Studios — open slots\</mj-text\>*  
*\</mj-column\>*  
*\</mj-section\>*  
*{{#each studios}}*  
*\<mj-section padding="0 24px 12px"\>*  
*\<mj-column\>*  
*\<mj-image src="{{this.preview}}" alt="{{this.name}} — SFW preview" padding-bottom="8px" /\>*  
*\<mj-text\>\<strong\>{{this.name}}\</strong\>\<br/\>{{this.amenities}}\</mj-text\>*  
*\<mj-text\>\<span class="chip"\>From {{this.price}}\</span\> \<span class="chip"\>{{this.slotDates}}\</span\>\</mj-text\>*  
*\<mj-button href="{{this.link}}"\>View studio\</mj-button\>*  
*\</mj-column\>*  
*\</mj-section\>*  
*{{/each}}*  
*{{/if}}*  
  
*\<!-- Rising creators --\>*  
*{{#if rising.length}}*  
*\<mj-section padding="8px 24px"\>*  
*\<mj-column\>*  
*\<mj-text font-size="16px" font-weight="600"\>Rising creators\</mj-text\>*  
*\</mj-column\>*  
*\</mj-section\>*  
*{{#each rising}}*  
*\<mj-section padding="0 24px 12px"\>*  
*\<mj-column\>*  
*\<mj-image src="{{this.preview}}" alt="{{this.handle}} — SFW preview" padding-bottom="8px" /\>*  
*\<mj-text\>\<strong\>{{this.handle}}\</strong\>\<br/\>{{this.roles}}\</mj-text\>*  
*\<mj-text\>\<span class="chip"\>Verified\</span\> \<span class="chip"\>{{this.cityArea}}\</span\>\</mj-text\>*  
*\<mj-button href="{{this.link}}"\>View profile\</mj-button\>*  
*\</mj-column\>*  
*\</mj-section\>*  
*{{/each}}*  
*{{/if}}*  
  
*\<!-- Footer --\>*  
*\<mj-section padding="24px"\>*  
*\<mj-column\>*  
*\<mj-text font-size="12px" color="#667085"\>*  
*You’re receiving this because you opted into the {{city}} weekly digest.*  
*SFW only; no 18+ content is emailed. \<a href="{{unsubLink}}"\>Unsubscribe\</a\> ·*  
*\<a href="{{prefsLink}}"\>Manage preferences\</a\>*  
*\</mj-text\>*  
*\</mj-column\>*  
*\</mj-section\>*  
  
*\</mj-body\>*  
*\</mjml\>*  

## **1.16-J. MJML — “Book Again” (7/30/90 variants)**

**Recommended filename/path:** *comms/templates/book_again_7d.mjml* (copy & tweak for *30d*/*90d*)

*\<mjml\>*  
*\<mj-head\>*  
*\<mj-title\>Ready to book {{spName}} again?\</mj-title\>*  
*\<mj-attributes\>*  
*\<mj-text font-size="14px" line-height="20px" /\>*  
*\</mj-attributes\>*  
*\</mj-head\>*  
*\<mj-body\>*  
*\<mj-section padding="16px 24px"\>*  
*\<mj-column\>*  
*\<mj-text font-size="20px" font-weight="600"\>Re-book {{spName}}\</mj-text\>*  
*\<mj-text\>We pre-filled your last package and scope. Pick a date, and you’re done.\</mj-text\>*  
*\</mj-column\>*  
*\</mj-section\>*  
  
*\<mj-section padding="0 24px 12px"\>*  
*\<mj-column\>*  
*\<mj-image src="{{previewUrl}}" alt="{{spName}} — SFW preview" /\>*  
*\<mj-text\>\<strong\>Last package:\</strong\> {{packageName}} — {{packagePrice}}\</mj-text\>*  
*\<mj-button href="{{draftCheckoutLink}}"\>Open draft checkout\</mj-button\>*  
*\</mj-column\>*  
*\</mj-section\>*  
  
*\<mj-section padding="16px 24px"\>*  
*\<mj-column\>*  
*\<mj-text font-size="12px" color="#667085"\>*  
*To stop these reminders for this provider, \<a href="{{stopLink}}"\>click here\</a\>.*  
*\</mj-text\>*  
*\</mj-column\>*  
*\</mj-section\>*  
*\</mj-body\>*  
*\</mjml\>*  

## **1.16-K. HTML/CSS — Link-in-Bio microsite (SFW previews)**

**Recommended filename/path:** *web/linkinbio/template.html*

*\<!doctype html\>*  
*\<html lang="en"\>*  
*\<head\>*  
*\<meta charset="utf-8" /\>*  
*\<meta name="viewport" content="width=device-width, initial-scale=1" /\>*  
*\<title\>{{handle}} — Link-in-Bio\</title\>*  
*\<style\>*  
*:root{ --bg:#0e1116; --card:#151a21; --text:#e7edf5; --muted:#9aa6b2; --brand:#ECC540; }*  
*body{ margin:0; background:var(--bg); color:var(--text); font: 16px/1.5 Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; }*  
*.wrap{ max-width:780px; margin:0 auto; padding:28px 16px; }*  
*.profile{ display:flex; gap:16px; align-items:center; }*  
*.avatar{ width:72px; height:72px; border-radius:999px; object-fit:cover; border:2px solid var(--brand); }*  
*.handle{ font-size:20px; font-weight:600; }*  
*.chip{ display:inline-block; background:#212833; border:1px solid \#2a3442; padding:4px 10px; border-radius:999px; font-size:12px; margin-right:6px; }*  
*.grid{ display:grid; gap:12px; grid-template-columns: repeat(auto-fit, minmax(220px,1fr)); margin-top:16px; }*  
*.card{ background:var(--card); border:1px solid \#222b36; border-radius:16px; padding:12px; }*  
*.card img{ width:100%; height:160px; object-fit:cover; border-radius:12px; }*  
*.btn{ display:inline-block; background:var(--brand); color:#111; padding:10px 14px; border-radius:12px; font-weight:600; text-decoration:none; }*  
*.muted{ color:var(--muted); font-size:13px; }*  
*\</style\>*  
*\</head\>*  
*\<body\>*  
*\<main class="wrap"\>*  
*\<section class="profile"\>*  
*\<img class="avatar" src="{{avatarUrl}}" alt="{{handle}}" /\>*  
*\<div\>*  
*\<div class="handle"\>@{{handle}}\</div\>*  
*\<div class="muted"\>{{city}}\</div\>*  
*{{#if verified}}\<span class="chip"\>Verified\</span\>{{/if}}*  
*{{#each roles}}\<span class="chip"\>{{this}}\</span\>{{/each}}*  
*\</div\>*  
*\</section\>*  
  
*\<section class="grid"\>*  
*\<!-- Packages --\>*  
*{{#each packages}}*  
*\<div class="card"\>*  
*\<img src="{{this.previewUrl}}" alt="SFW preview for {{this.name}}"\>*  
*\<h4\>{{this.name}}\</h4\>*  
*\<p class="muted"\>{{this.description}}\</p\>*  
*\<a class="btn" href="{{this.checkoutLink}}?utm_source=lib&utm_medium=link&utm_campaign=pkg"\>Book {{this.price}}\</a\>*  
*\</div\>*  
*{{/each}}*  
  
*\<!-- Availability --\>*  
*{{#each availability}}*  
*\<div class="card"\>*  
*\<h4\>Availability: {{this.date}}\</h4\>*  
*\<p class="muted"\>{{this.window}}\</p\>*  
*\<a class="btn" href="{{this.bookLink}}?utm_source=lib&utm_medium=link&utm_campaign=avail"\>Request\</a\>*  
*\</div\>*  
*{{/each}}*  
*\</section\>*  
  
*\<p class="muted" style="margin-top:16px"\>*  
*Previews are SFW. For 18+ material, Safe-Mode must be OFF and age-verified in app.*  
*\</p\>*  
*\</main\>*  
*\</body\>*  
*\</html\>*  

## **1.16-L. ANY/ALL Query Builder — Typesense/OpenSearch spec**

**Recommended filename/path:** *search/spec/any_all_query_builder.md*

*Goal*  
*Support saved searches with (ANY OR ALL) filter groups over people/studios while enforcing Safe-Mode.*  
  
*Input*  
*queryJson:*  
*{*  
*"any": \[*  
*{"field":"roleFields.genres","op":"in","value":\["fashion","editorial"\]},*  
*{"field":"verification.id","op":"eq","value":true}*  
*\],*  
*"all": \[*  
*{"field":"city","op":"eq","value":"Houston"},*  
*{"field":"priceFromCents","op":"between","value":\[10000,30000\]}*  
*\]*  
*}*  
  
*Algorithm (Typesense flavor)*  
* - Base filters: city:={{city}} AND isPublished:=true AND safeModeBandMax:\<= {{safeMode?1:2}}*  
* - Build ANY clause:*  
* - Map each criterion to Typesense filter expression:*  
*\* in: field:=\[v1, v2, ...\]*  
*\* eq: field:=value*  
*\* between: field:\>={{lo}} && field:\<={{hi}}*  
* - ANY -\> join with " \|\| "*  
* - Build ALL clause: same mapping, join with " && "*  
* - Combined: base && ( (ANY) \|\| true_if_any_empty ) && (ALL)*  
* - Sorting: text match score, geo distance, repScore, verifyBoost, priceFit*  
* - Pagination: cursor API; record query_hash for analytics and dedupe.*  
  
*OpenSearch variant*  
* - Translate to bool query:*  
*{*  
*"bool": {*  
*"filter": \[*  
*{"term":{"city":"houston"}},*  
*{"term":{"isPublished":true}},*  
*{"range":{"safeModeBandMax":{"lte": safeMode?1:2}}}*  
*\],*  
*"must": \[ ...ALL... \],*  
*"should": \[ ...ANY... \],*  
*"minimum_should_match": {{ANY? 1 : 0}}*  
*}*  
*}*  

## **1.16-M. UTM & Attribution Rules**

**Recommended filename/path:** *growth/utm_attribution_rules.md*

*UTM structure*  
*utm_source = one of: lib (link-in-bio), sharecard, digest, alert*  
*utm_medium = email \| inapp \| web*  
*utm_campaign = pkg \| avail \| city_digest \| book_again_7 \| book_again_30 \| book_again_90 \| referral*  
  
*Click tokens*  
*token = HMAC(k, user_id \| ts \| target) \# 5-minute TTL*  
*Store click event -\> attribute conversion to last non-expired click within 7 days.*  
  
*Attribution in §1.13*  
* - fact_clicks (Silver) join to fact_conversions (checkout.confirmed) by user_id within window.*  
* - Gold KPI: by (utm_source, utm_campaign), city, role.*  

## **1.16-N. Lambda Skeleton — Weekly Digest**

**Recommended filename/path:** *apps/functions/growthWeeklyDigest.ts*

*// growthWeeklyDigest.ts*  
*import { pickDigestBlocks } from '../lib/digestBlocks';*  
*import { sendEmail } from '../lib/ses';*  
*import { createInApp } from '../lib/inapp';*  
*import { getOptedInUsersByCity } from '../lib/digestRepo';*  
  
*export const handler = async () =\> {*  
*const cities = await getDigestCities();*  
*for (const city of cities) {*  
*const users = await getOptedInUsersByCity(city);*  
*const blocks = await pickDigestBlocks(city); // { caseStudies, studios, rising }*  
*for (const u of users) {*  
*await createInApp(u.userId, 'weekly_digest', { city, blocks });*  
*await sendEmail({*  
*toUserId: u.userId,*  
*template: 'weekly_city_digest',*  
*vars: { city, ...blocks }*  
*});*  
*}*  
*}*  
*};*  

## **1.16-O. Lambda Skeleton — Book Again (7/30/90)**

**Recommended filename/path:** *apps/functions/growthBookAgain7.ts* (copy for 30/90)

*// growthBookAgain7.ts*  
*import { findEligibleRebooks } from '../lib/rebookRepo';*  
*import { sendEmail } from '../lib/ses';*  
  
*export const handler = async () =\> {*  
*const reb = await findEligibleRebooks({ daysAgo: 7 });*  
*for (const r of reb) {*  
*await sendEmail({*  
*toUserId: r.buyerId,*  
*template: 'book_again_7d',*  
*vars: {*  
*spName: r.spName,*  
*packageName: r.packageName,*  
*packagePrice: r.packagePriceFmt,*  
*previewUrl: r.previewUrl,*  
*draftCheckoutLink: r.draftCheckoutLink,*  
*stopLink: r.stopLink*  
*}*  
*});*  
*}*  
*};*  

## **1.16-P. Cost & SLO Guardrails (growth jobs)**

**Recommended filename/path:** *observability/slo/growth-jobs.md*

*SLOs*  
* - Saved-search alert job completes \< 10 min p95; per-user dedupe strictly 1/day/search.*  
* - Weekly digest job \< 20 min p95 per city cohort.*  
* - Book-again jobs \< 5 min p95 each run.*  
  
*Alarms*  
* - SES bounce/complaint spikes \> 0.3% rolling 24h -\> pause digest/alerts, in-app only.*  
* - Lambda errors \> 1% or duration p95 \> SLO -\> investigate search query shapes or batch sizes.*  
* - Dynamo TTL dead-letter \> 100/day -\> inspect dedupe miswrites.*  
  
*Cost*  
* - Prefer in-app notifications when SES threshold near daily cap.*  
* - Batch Typesense/OpenSearch queries for alerts by grouping identical filters.*

# **§1.17 — SEO, Web Performance & Content Discovery**

*(URL topology · metadata & canonicalization · JSON‑LD · robots/noindex & Safe‑Mode · sitemaps · hreflang · ISR/SSR caching · Core Web Vitals budgets · a11y synergy · admin content ops · telemetry · tests · cost)*

**Purpose.** Make the marketplace discoverable while keeping costs down and content safe. This section defines *exactly* how we structure URLs, metadata, structured data, crawlers access, internationalization signals, build & caching strategy, performance budgets, admin workflows, and monitoring—plus copy‑pasteable artifacts for your Word plan.

## **1.17.A Canon & invariants**

1763. **SFW on the open web.** Public pages show *SFW previews only*. Age‑gated/18+ content never leaves the app; no email with 18+ previews.
1764. **Single canonical per concept.** Every profile, studio, case study, and city page has one canonical URL; alternates (share/UTM/tracking) 301 to the canonical.
1765. **Server‑rendered entry, cached at the edge.** We use Next.js **ISR/SSR** with CloudFront caching and smart revalidation (low cost).
1766. **Robots are guests, not owners.** We invite indexing of SFW listings and guides; we set *noindex* on anything gated, duplicated, or ephemeral (drafts, filters, session pages).
1767. **Accessibility improves SEO.** Headings, landmarks, alt text, and readable copy are mandatory—no image‑only text.

## **1.17.B URL topology (stable, human‑readable)**

**People (Service Profiles)**

- */p/{handle}* (canonical)
- */p/{handle}/packages/{slug}* (canonical for package detail)
- */p/{handle}?utm\_\** → 301 → */p/{handle}*

**Studios**

- */s/{slug}* (studio listing)
- */s/{slug}/rates* (rate table, SFW)

**Cities & discovery**

- */city/{city-slug}* — city hub (SFW)
- */city/{city-slug}/people* — SFW grid (server‑filtered)
- */city/{city-slug}/studios* — SFW studios list
- */stories/{slug}* — case studies/guides (SFW hero)

**System**

- */robots.txt*, */sitemap.xml* (+ segmented sitemaps)
- */legal/{tos\|privacy\|dmca}* (indexable)
- */help/\** (indexable FAQ)
- Anything transactional (*/checkout*, */messages*, */admin*) → *noindex, nofollow*.

## **1.17.C Metadata & canonicalization**

- **Required** ***\<head\>*** **tags per page:**

  - *\<title\>* unique, ≤60 chars; *\<meta name="description"\>* ≤160 chars.
  - \<link rel="canonical" href="…"\>
  - OpenGraph (*og:title*, *og:description*, *og:image* SFW, *og:url*, *og:type*)
  - Twitter Card (*summary_large_image*)
  - Preconnect only to first‑party + Stripe (at checkout), never to ad CDNs.

- **Tracking query params** (*utm\_\**, *ref*) are stripped by a Next.js middleware and 301 to canonical (no duplicate content).

- **Case studies** use Article OG tags (*article:published_time*, *article:tag*).

## **1.17.D JSON‑LD structured data (copy‑paste)**

**Recommended path:** *web/seo/snippets.md* *(inline in the plan; later lift to helper functions)*

### **D.1 Service Profile as** ***Person***** +** ***Product*** **(package)**

*\<script type="application/ld+json"\>*  
*{*  
*"@context": "*[*https://schema.org*](https://schema.org)*",*  
*"@type": "Person",*  
*"name": "{{displayName}}",*  
*"url": "*[*https://rastup.com/p/{{handle*](https://rastup.com/p/%7b%7bhandle)*}}",*  
*"jobTitle": "{{primaryRole}}",*  
*"image": "{{sfwAvatarUrl}}",*  
*"knowsAbout": {{json roles}},*  
*"address": { "@type": "PostalAddress", "addressLocality": "{{city}}", "addressRegion": "{{region}}", "addressCountry": "{{country}}" }*  
*}*  
*\</script\>*  
  
*\<script type="application/ld+json"\>*  
*{*  
*"*[*@context":"https://schema.org*]()*",*  
*"@type":"Product",*  
*"name":"{{packageName}}",*  
*"image":\["{{sfwPackagePreview1}}","{{sfwPackagePreview2}}"\],*  
*"description":"{{sfwShortDesc}}",*  
*"brand":{"@type":"Brand","name":"{{displayName}}"},*  
*"offers":{*  
*"@type":"Offer",*  
*"priceCurrency":"{{currency}}",*  
*"price":"{{priceDecimal}}",*  
*"availability":"https://schema.org/InStock",*  
*"url":"https://rastup.com/p/{{handle}}/packages/{{slug}}"*  
*}*  
*}*  
*\</script\>*  

### **D.2 Studio as** ***LocalBusiness***

*\<script type="application/ld+json"\>*  
*{*  
*"*[*@context":"https://schema.org*]()*",*  
*"@type":"LocalBusiness",*  
*"name":"{{studioName}}",*  
*"url":"https://rastup.com/s/{{slug}}",*  
*"image":\["{{sfwPreview1}}","{{sfwPreview2}}"\],*  
*"address":{"@type":"PostalAddress","streetAddress":"{{shortAddr}}","addressLocality":"{{city}}","addressRegion":"{{region}}","postalCode":"{{zip}}","addressCountry":"{{country}}"},*  
*"amenityFeature":\[*  
*{"@type":"LocationFeatureSpecification","name":"Natural light","value":{{hasNaturalLight}}},*  
*{"@type":"LocationFeatureSpecification","name":"Cyc wall","value":{{hasCycWall}}}*  
*\],*  
*"priceRange":"{{priceHint}}"*  
*}*  
*\</script\>*  

### **D.3 Guides/Case Studies as** ***Article***

*\<script type="application/ld+json"\>*  
*{*  
*"*[*@context":"https://schema.org*]()*",*  
*"@type":"Article",*  
*"headline":"{{title}}",*  
*"image":\["{{sfwHero}}"\],*  
*"datePublished":"{{publishedISO}}",*  
*"author":{"@type":"Organization","name":"RastUp"},*  
*"mainEntityOfPage":"https://rastup.com/stories/{{slug}}"*  
*}*  
*\</script\>*  

**Rule:** JSON‑LD images must be **SFW previews** only.

## **1.17.E Robots, Safe‑Mode, and** ***noindex*** **policy**

**robots.txt (template)**  
**Recommended path:** *web/public/robots.txt*

*User-agent: \**  
*Disallow: /admin/*  
*Disallow: /messages/*  
*Disallow: /checkout/*  
*Disallow: /\_next/*  
*Disallow: /\*?\**  
*Allow: /\$*   
*Allow: /city/*  
*Allow: /p/*  
*Allow: /s/*  
*Sitemap:* [*https://rastup.com/sitemap.xml*](https://rastup.com/sitemap.xml)

**X‑Robots‑Tag headers**

- Add *x-robots-tag: noindex, nofollow* to: drafts, preview routes, filtered result pages with query params, any page with *nsfw_band \>= 2* assets, and takedowns (DMCA).
- When Safe‑Mode is ON for a user, we still index the public SFW page; no 18+ assets are exposed in HTML/JSON‑LD.

## **1.17.F Sitemaps (segmented, auto‑rotating)**

**Recommended path:** *web/pages/sitemap.xml.ts* *(ISR function)*

- **Sitemap Index** */sitemap.xml* lists child maps:

  - */sitemaps/people-0.xml*, */sitemaps/people-1.xml*, … (sharded by hash)
  - */sitemaps/studios-0.xml*, …
  - */sitemaps/cities.xml*, */sitemaps/stories.xml*

- **lastmod** from *updated_at*; **changefreq** = *weekly* for people/studios, *daily* for cities during launch, *monthly* later.

- Exclude de‑published, unverified, or NSFW‑blocked pages.

**Example child sitemap XML**

*\<?xml version="1.0" encoding="UTF-8"?\>*  
*\<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\>*  
*\<url\>*  
*\<loc\>https://rastup.com/p/{{handle}}\</loc\>*  
*\<lastmod\>{{updatedISO}}\</lastmod\>*  
*\<changefreq\>weekly\</changefreq\>*  
*\<priority\>0.8\</priority\>*  
*\</url\>*  
*\</urlset\>*  

## **1.17.G Hreflang & locale routing**

- Default locale *en-US*. Add hreflang alternates when we add translations:

  - *\<link rel="alternate" hreflang="en" href="…"\>*, *\<link rel="alternate" hreflang="es" href="…"\>*, plus *x-default*.

- URL policy: keep canonical paths without locale prefix; inject *hreflang* only (simplifies link sharing).

- Next.js middleware detects *Accept‑Language*, sets *lang* and *dir* on *\<html\>*, and formats dates/currency per locale.

**Snippet (Next.js, concept)**  
**Recommended path:** *web/middleware.ts* *(doc block)*

*export function middleware(req: NextRequest) {*  
*const locale = negotiateLocale(req.headers.get('accept-language'));*  
*const res = NextResponse.next();*  
*res.headers.set('x-lang', locale.lang);*  
*res.headers.set('x-dir', locale.dir); // ltr/rtl*  
*return res;*  
*}*  

## **1.17.H Rendering strategy & caching (ISR/SSR + CDN)**

- **People/Studios pages**: ISR with *revalidate: 86400* (24h) on low‑change fields; **on‑demand revalidation** when profile edits publish.
- **City pages**: ISR, *revalidate: 21600* (6h) at launch → 24h later.
- **Stories**: static at publish; republish on edit.
- **Edge cache**: CloudFront cache policy keyed by *Accept‑Language* and *Cookie* *only for Safe‑Mode* flag (avoid leaking modes).
- **Stale‑while‑revalidate** for instant TTFB.
- **ETag** for JSON APIs used by static props.

## **1.17.I Core Web Vitals & performance budgets**

**Targets (P75 on mobile):**

- **LCP ≤ 2.5s**, **CLS ≤ 0.10**, **INP ≤ 200ms**, **TTFB ≤ 800ms**.

**Levers:**

- Use Next/Image for responsive SFW previews; WebP/AVIF; lazy + priority on hero.
- Inline **critical CSS** for above‑the‑fold; remove unused CSS via CSS‑in‑JS extraction.
- Code‑split heavy modules (editor, charts) behind dynamic import.
- Preconnect to our CDN and Stripe (checkout pages only).
- Ship system fonts or 1 local WOFF2 with *font-display: swap*.
- Avoid blocking analytics; send beacons via *navigator.sendBeacon* to our */collect* endpoint.
- Only 1 external script allowed on public pages: the consented analytics shim (first‑party). No ad trackers.

**Lighthouse CI budget (inline)**  
**Recommended path:** *observability/budgets/lighthouse-budget.json*

*{*  
*"resourceSizes": \[*  
*{"resourceType": "script", "budget": 160},*  
*{"resourceType": "total", "budget": 900}*  
*\],*  
*"resourceCounts": \[*  
*{"resourceType": "third-party", "budget": 2},*  
*{"resourceType": "total", "budget": 90}*  
*\],*  
*"timings": \[*  
*{"metric": "interactive", "budget": 3500},*  
*{"metric": "first-contentful-paint", "budget": 1800}*  
*\]*  
*}*  

## **1.17.J Accessibility synergy (SEO + a11y)**

- Semantic headings (*h1* unique), landmarks (*header/main/nav/footer*), and visible skip‑links.
- All images have **alt**; decorative images *alt=""*.
- Focus outlines enabled; keyboard navigation through interactive components; ARIA on custom controls (carousels/cards).
- Color contrast ≥ 4.5:1 for text, 3:1 for large text/icons.
- Descriptive link text (“View studio details”), not “click here”.
- Media captions for videos; transcripts for long videos in stories.

## **1.17.K Admin content ops & safeguards**

- **Publish workflow**: drafts → preview (noindex) → publish (indexable).
- **Link checker**: nightly job crawls published stories, flags 404s/5xx.
- **Search Console & Bing Webmaster**: XML verification, sitemaps auto‑submit at deploy.
- **DMCA integration**: hidden content adds *x-robots-tag: noindex* and is removed from sitemaps on next run.
- **Sharecard sanity**: ensure OG images are SFW versions only.

## **1.17.L Telemetry & dashboards**

- **Core Web Vitals (field)**: RUM beacon reports LCP/CLS/INP by route, device, city; dashboard in QuickSight.
- **Crawl health**: sitemap submission status, indexed pages over time, top coverage errors (ingested via Search Console API exporter).
- **SEO funnel**: impressions → clicks → profile views → checkout start → confirmation (hooked into §1.13).
- **Alerting**: LCP regression \> 10% WoW on top city pages, spike in non‑200 response ratio, robots blocking anomalies.

## **1.17.M Test plan (CI + stage)**

1821. **Lighthouse CI** on PRs for */*, */city/{city}*, */p/{handle}*, */s/{slug}*, */stories/{slug}*; budgets enforced.
1822. **Structured data** validates (Person/Product/LocalBusiness/Article) with schema validator; image URLs SFW.
1823. **Canonical/redirects**: UTM/ref variants 301 to canonical; no duplicate indexation.
1824. **Robots/noindex**: drafts, filters, admin, checkout and DMCA pages return *x-robots-tag: noindex*.
1825. **Sitemaps**: contain only published SFW pages; child sitemaps \< 50k URLs; index lists all children.
1826. **Hreflang** (when enabled): alternates present and correct.
1827. **A11y**: axe/Pa11y suite passes; keyboard nav end‑to‑end on public pages.
1828. **Perf**: p75 CWV targets met under synthetic 3G.

## **1.17.N Cost posture**

- **Edge caching** with ISR keeps SSR compute near‑zero for stable pages.
- **Static image transforms** for SFW previews; avoid runtime transformations for public pages when possible.
- **No third‑party SEO SaaS** at launch; rely on Search Console/Bing free tools; Lighthouse CI self‑hosted runner.
- **Sharecard worker** concurrency capped; aggressively cache results.

## **1.17.O Inline artifacts block**

**O.1 robots.txt** (see §1.17.E)  
**O.2 sitemap child template** (see §1.17.F)  
**O.3 JSON‑LD snippets** (see §1.17.D)  
**O.4 Lighthouse budget JSON** (see §1.17.I)  
**O.5 Next.js middleware snippet** (see §1.17.G)

Copy these directly into your Word doc under an “Artifacts” subheading.

## **1.17.P Acceptance criteria — mark §1.17 FINAL only when ALL true**

1833. Canonical URL policy implemented; UTM/ref routes 301 correctly.
1834. JSON‑LD present on People, Packages, Studios, and Stories with SFW images only.
1835. robots/noindex enforced for drafts, gated/NSFW, filters, admin, and checkout routes.
1836. Segmented sitemaps generate & auto‑submit; include only indexable pages; refresh cadence set.
1837. Hreflang in place when we enable additional locales; default *en* with *x-default*.
1838. ISR/SSR caching + CloudFront policies deliver p75 **LCP ≤ 2.5s**, **CLS ≤ 0.10**, **INP ≤ 200ms** on top routes.
1839. a11y checks pass (axe/Pa11y) on public routes; alt text coverage ≥ 99%.
1840. Dashboards show CWV trends, crawl health, and the SEO funnel; alerts configured for regressions.
1841. Costs stay within budgets (no third‑party bloat; edge cache hit ratio ≥ 90%).

# **§1.17 — SEO & On‑Site Optimization Deep‑Dive (Expanded)**

## **1.17.1 Crawl & Indexation Control (robots, meta, headers)**

**Goals:** Maximize crawl efficiency on **indexable SFW pages**, prevent indexing of **gated/duplicate/thin** pages, and make crawler behavior cheap.

**Policies**

- **Indexable:** Home, City & Role hubs, Search (unfiltered landing variants only), Service Profiles (non‑adult), Studios, Case Studies/Guides, Legal/Help.
- **Noindex:** age‑gated or login‑required pages; any URL with tracking params; filter‑heavy result pages; drafts/preview; checkout/messages/admin; duplicate “print/share” variants.
- **Disallow (robots.txt):** */admin/*, */messages/*, */checkout/*, internal asset routes, *\_next/*.

**Artifacts**

**A) robots.txt (inline)**  
*Recommended path:* *web/public/robots.txt*

*User-agent: \**  
*Disallow: /admin/*  
*Disallow: /messages/*  
*Disallow: /checkout/*  
*Disallow: /\_next/*  
*Disallow: /\*?\* \# parameters not for indexing*  
*Allow: /\$*  
*Allow: /city/*  
*Allow: /studios*  
*Allow: /studio/*  
*Allow: /models*  
*Allow: /photographers*  
*Allow: /videographers*  
*Allow: /creators*  
*Sitemap:* [*https://rastup.com/sitemap.xml*](https://rastup.com/sitemap.xml)

**B) X‑Robots‑Tag header policy (server)**  
*Recommended path:* *web/lib/robots.ts* (pseudocode)

*export function robotsHeaderFor(req, page) {*  
*if (page.isAdult \|\| page.requiresLogin \|\| page.isPreview) return "noindex, nofollow, noarchive";*  
*if (req.url.includes("?")) return "noindex, follow"; // filter/param variants are non-canonical*  
*return "index, follow";*  
*}*  

**C)** ***\<meta name="robots"\>*** **fallback (HTML)**  
Add a server‑generated *\<meta name="robots" content="..."\>* mirroring the header on all public templates.

## **1.17.2 Canonicalization & URL Normalization**

**Rules**

- **Single canonical per entity** (profile */p/{handle}*, studio */s/{slug}*, package */p/{handle}/packages/{slug}*).
- Strip ***utm\_\******,** ***ref*****, session and cache‑busting** params via 301 to canonical.
- Normalize: lowercase paths, **no trailing slash** (choose one; below assumes none), collapse multiple slashes, decode percent‑encoding.
- City context for hubs: canonical as **query param** (*/models?city=houston*), not path segments—prevents duplicate city pages.

**Artifacts**

**A) Canonical redirect middleware (Next/Edge pseudocode)**  
*Recommended path:* *web/middleware.ts*

*const CANON_QP_BLOCKLIST = \["utm_source","utm_medium","utm_campaign","utm_term","utm_content","ref","gclid","fbclid"\];*  
*export function middleware(req) {*  
*const url = new URL(req.nextUrl);*  
*// Normalize case and trailing slash*  
*url.pathname = url.pathname.toLowerCase().replace(/\\+\$/,'').replace(/\\{2,}/g,'/');*  
*// Strip tracking params*  
*for (const p of CANON_QP_BLOCKLIST) url.searchParams.delete(p);*  
*// If changed, 301 to canonical*  
*if (url.toString() !== req.nextUrl.toString()) return Response.redirect(url, 301);*  
*return;*  
*}*  

**B) Canonical link builder (server)**  
*Recommended path:* *web/lib/canonical.ts*

*export const canonicalFor = (entity) =\>*  
*entity.kind === "person" ? \`https://rastup.com/\${entity.role}/\${entity.slug}\` :*  
*entity.kind === "studio" ? \`https://rastup.com/studio/\${entity.slug}\` :*  
*entity.kind === "package" ? \`https://rastup.com/\${entity.role}/\${entity.slug}/packages/\${entity.pkgSlug}\` :*  
*\`https://rastup.com/\`;*  

## **1.17.3 Faceted Navigation, Pagination & Filters**

**Objective:** Let users filter richly **without** creating an indexation explosion.

**Approach**

- **Indexable landing** per role/city **without filters** (e.g., */models?city=houston*).
- **Non‑indexable** filter combinations (e.g., price/amenities) → keep crawlable links but serve *noindex, follow* and **self‑canonical** to the landing variant.
- Pagination: *?page=2* allowed but **noindex**; canonical to page 1 landing. Avoid *rel=prev/next* (deprecated); use strong internal links instead.

**Artifact — filter allowlist**  
*Recommended path:* *search/spec/filter-allowlist.md*

*Indexable: (role + city) only*  
*Non-indexable: any additional filters (price, amenity, availability, verification, rating, etc.) =\> meta robots noindex, self-canonical to landing*  
*Pagination: ?page=N =\> meta robots noindex, canonical to page=1*  

## **1.17.4 Structured Data (JSON‑LD) — Full Coverage**

**Entity → schema.org type map**

- **People (Service Profiles)**: *Person* + *Offer*(s) for packages; optional *AggregateRating* when policy allows.
- **Studios**: *LocalBusiness* with *amenityFeature*; optional *AggregateRating*.
- **Case Studies/Guides**: *Article*/*CreativeWork*.
- **Breadcrumbs**: *BreadcrumbList* on all public pages.
- **Search results** (optional enhancement): *ItemList* on landing pages.

**Artifacts**

**A) BreadcrumbList**  
*Recommended path:* *web/lib/ldjson/breadcrumb.ts*

*export const breadcrumbLd = (trail) =\> ({*  
*"@context": "*[*https://schema.org*](https://schema.org)*",*  
*"@type": "BreadcrumbList",*  
*"itemListElement": trail.map((item, i) =\> ({*  
*"@type": "ListItem", "position": i+1, "name": item.name, "item": item.url*  
*}))*  
*});*  

**B) Service Profile with Offers & rating**  
*Recommended path:* *web/lib/ldjson/personOffers.ts*

*export const personWithOffersLd = (p) =\> ({*  
*"@context": "*[*https://schema.org*](https://schema.org)*",*  
*"@type": "Person",*  
*"name": p.displayName,*  
*"image": p.og_image_sfw_url,*  
*"url": \`https://rastup.com/\${p.role}/\${p.slug}\`,*  
*"jobTitle": p.roleTitle,*  
*"address": {"@type":"PostalAddress","addressLocality": p.city},*  
*"makesOffer": p.packages.map(pkg =\> ({*  
*"@type":"Offer",*  
*"priceCurrency": pkg.currency,*  
*"price": (pkg.priceCents/100).toFixed(2),*  
*"url": \`https://rastup.com/\${p.role}/\${p.slug}/packages/\${pkg.slug}\`,*  
*"availability":"https://schema.org/InStock"*  
*})),*  
*...(p.ratingCount \>= 5 ? {*  
*"aggregateRating": {*  
*"@type":"AggregateRating",*  
*"ratingValue": p.rating.toFixed(1),*  
*"reviewCount": p.ratingCount*  
*}*  
*} : {})*  
*});*  

**C) Studio with amenity features**  
*(already covered earlier—kept here for completeness; ensure SFW images)*

## **1.17.5 Content Templates & On‑Page Optimization**

**Title & Description formulas**  
*Recommended path:* *web/seo/title-desc-formulas.md*

*Service Profile (People):*  
*\<title\> {DisplayName} — {RoleTitle} in {City} \| RastUp \</title\>*  
*\<meta name="description" content="{Short role tagline}. Packages, availability, reviews, and verified badges." /\>*  
  
*Studio:*  
*\<title\> {StudioName} — {City} Studio Rental (Amenities & Rates) \| RastUp \</title\>*  
*\<meta name="description" content="{Short studio pitch}. Amenities: {Top 3}. From {Price}/hr." /\>*  
  
*City/Role landing:*  
*\<title\> {RolePlural} in {City} — Verified & Bookable \| RastUp \</title\>*  
*\<meta name="description" content="Explore {City} {rolePlural}. Verified portfolios, packages, and studios." /\>*  

**Heading & module order (to reduce CLS + maximize relevance)**  
*Recommended path:* *web/seo/page-templates.md*

*Service Profile:*  
*H1: {DisplayName} — {RoleTitle} in {City}*  
*Intro block (50–80 words, SFW)*  
*Modules (in order): Packages → Portfolio (SFW grid) → Availability → Reviews → Badges/Verification → Location (city-only hint) → FAQs*  
*Internal links: "Similar {rolePlural} in {City}" (3–8 cards), "Studios with {top amenity}" (2–4 cards)*  
  
*Studio Detail:*  
*H1: {StudioName} — {City}*  
*Intro (amenity-rich; SFW)*  
*Modules: Gallery (SFW) → Rates & Rules → Amenities → Availability/Slots → Host → Location (area only) → FAQs*  
*Internal links: "People recently booked here" cards*  
  
*City/Role Landing:*  
*H1: {RolePlural} in {City}*  
*Intro paragraph (~120–160 words, unique)*  
*Modules: Top Verified → New this week → Budget filters → Case Studies carousel (SFW)*  

**Internal linking rules**

- Every profile and studio page should expose **two blocks** of curated internal links: “Similar in {City}” and a cross‑entity block (People↔Studios).
- Keep links **crawlable** (no *nofollow*), descriptive anchor text, and **stable** across rebuilds (deterministic selection).

## **1.17.6 Image & Video SEO (SFW‑only)**

**Images**

- Filenames: kebab‑case with role/city cues, e.g., *houston-photographer-jane-doe-portrait-01.webp*.
- Always set *width*/*height* to prevent CLS; use *srcset*/*sizes*; serve AVIF/WebP with JPEG fallback.
- *alt* text: short literal description; **no keyword stuffing**; for decorative images, *alt=""*.
- Lazy‑load below‑the‑fold; **preload** the hero (LCP) image.

**Videos** (case studies, studio tours)

- Use ***VideoObject*** JSON‑LD with SFW poster frames; duration and upload date.
- Provide **captions**; avoid auto‑play with sound (INP risk).

**Artifact — VideoObject JSON‑LD**  
*Recommended path:* *web/lib/ldjson/video.ts*

*export const videoLd = (v) =\> ({*  
*"@context": "*[*https://schema.org*](https://schema.org)*",*  
*"@type": "VideoObject",*  
*"name": v.title,*  
*"description": v.desc,*  
*"thumbnailUrl": \[v.posterSfw\],*  
*"uploadDate": v.publishedISO,*  
*"duration": \`PT\${v.durationSeconds}S\`,*  
*"contentUrl": v.hlsPublicPreview*  
*});*  

## **1.17.7 Performance for SEO (CWV‑first Build)**

**Budgets (mobile P75):** LCP ≤ 2.5s, CLS ≤ 0.10, INP ≤ 200ms, TTFB ≤ 800ms.

**Tactics**

- Pick an **LCP element** (hero image) per template; preload it with *as=image* and *fetchpriority="high"*.
- Inline **critical CSS**; defer the rest; no blocking fonts (local WOFF2 + *font-display: swap*).
- **Code‑split** heavy widgets; ship minimal JS on public pages.
- Preconnect only to **our CDN** and **Stripe** (checkout only).
- Serve **stale‑while‑revalidate** via ISR + CloudFront.
- Use **first‑party analytics** via *sendBeacon* (no third‑party bloat).

**Artifact — Lighthouse CI budget**  
*Recommended path:* *observability/budgets/lighthouse.json*

*{*  
*"resourceSizes": \[*  
*{"resourceType":"total", "budget": 900},*  
*{"resourceType":"script", "budget": 160}*  
*\],*  
*"timings": \[*  
*{"metric": "interactive", "budget": 3500},*  
*{"metric": "first-contentful-paint", "budget": 1800}*  
*\]*  
*}*  

## **1.17.8 Internationalization (hreflang) & Localization**

- Launch locale: **en‑US**; all public pages must set *\<html lang="en"\>*.
- **Hreflang scaffolding** in head for future locales; keep canonical **without** locale in path; add *\<link rel="alternate" hreflang="…"\>* once translations ship.
- Localize **currency/date/number** rendering server‑side for public pages; keep URLs stable.

**Artifact — hreflang helper**  
*Recommended path:* *web/lib/hreflang.ts*

*export const hreflangLinks = (canonical, alts) =\>*  
*alts.map(a =\> \`\<link rel="alternate" hreflang="\${a.lang}" href="\${a.href}"\>\`).join("\n")*  
* + \`\n\<link rel="alternate" hreflang="x-default" href="\${canonical}"\>\`;*  

## **1.17.9 Accessibility (A11y) Synergy for SEO**

- Semantic structure (landmarks, headings) and **visible focus**.
- Keyboard‑reachable filters/maps; ARIA for tabs/carousels.
- Image **alt** as above; captions/transcripts on videos.
- Error pages with clear next actions; readable contrast (≥4.5:1 body text).

## **1.17.10 Sitemaps (Web, Image, Video)**

**Strategy**

- **Index file** */sitemap.xml* linking to segmented sitemaps (People A‑Z, Studios by city, Case Studies, Cities).
- **Image sitemaps** for people/studios (SFW thumbnails only).
- **Video sitemap** for case studies with videos.

**Artifact — Image sitemap entry (template)**  
*Recommended path:* *web/sitemaps/templates/image-url.xml*

*\<url\>*  
*\<loc\>https://rastup.com/studio/{{slug}}\</loc\>*  
*\<image:image\>*  
*\<image:loc\>https://cdn.rastup.com/sfw/{{imageFile}}\</image:loc\>*  
*\<image:title\>{{imageTitle}}\</image:title\>*  
*\<image:caption\>{{imageCaption}}\</image:caption\>*  
*\</image:image\>*  
*\</url\>*  

## **1.17.11 Internal Linking & Breadcrumbs**

- **Breadcrumbs** everywhere (Home → City → Role → Entity).

- In‑content cross‑links:

  - On profiles: “Similar in {City}”, “Studios with {Amenity}”
  - On studios: “People recently booked here”

- Avoid link farms; keep blocks 3–8 items; **deterministic** selection.

## **1.17.12 Log‑File Analysis & Search Console Ingestion**

- Export **edge logs** (CloudFront) + **app access logs** to S3; model into Athena (§1.13).
- Build **crawl dashboard**: hits by bot UA, 200/3xx/4xx, coverage of sitemaps, crawl waste on non‑indexable pages.
- Ingest **GSC** performance/coverage via API to the lake; build SEO funnel (impressions→clicks→profile views→checkout).

**Artifact — Athena table (simplified)**  
*Recommended path:* *data/sql/cf_logs.sql*

*CREATE EXTERNAL TABLE IF NOT EXISTS cf_logs (*  
*dt string, time string, x_edge_location string, sc_status int, cs_method string,*  
*cs_uri_stem string, cs_uri_query string, cs_user_agent string, cs_referer string*  
*)*  
*PARTITIONED BY (date string)*  
*ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'*  
*LOCATION 's3://logs/cloudfront/';*  

## **1.17.13 SEO‑Safe Experimentation**

- **No client‑side cloaking**: bots must see a stable, indexable version (avoid A/B that changes indexable content for bots only).
- Keep experiments **server‑side** (SSR/ISR) or **non‑indexable** UI variations.
- For content experiments (titles, descriptions), roll out by **entity cohorts**; revalidate ISR pages on change.

## **1.17.14 Risk Register & Mitigations**

- **Duplicate content** via tracking params → mitigated by canonical middleware + 301.
- **Faceted crawl bloat** → *noindex, follow* + allowlist + self‑canonical.
- **Accidental 18+ leakage** → centralized SFW image service for OG/JSON‑LD; tests in CI.
- **Thin pages** (empty profiles) → hold *noindex* until profile meets completeness threshold.
- **CLS regressions** → enforce width/height on images; block unstyled font flashes.

## **1.17.15 QA Checklists (Pre‑launch & Ongoing)**

**Pre‑launch**

- Canonical/robots tags verified on top templates.
- Sitemaps (web/image/video) present and validate; robots.txt references index.
- JSON‑LD validates on 25 sample pages across types.
- Lighthouse p75 budgets met on emulated mobile.
- All OG images SFW; email templates tested for SFW previews.

**Ongoing**

- Weekly crawl dashboard reviewed; non‑indexable hit rate trending down.
- GSC: errors addressed; CTR and position monitored for top city/role pages.
- Uptime for ISR revalidation hooks; cache hit ratio ≥95% for public pages.

## **1.17.16 Work Packages (Cursor 4‑agent lanes)**

- **Agent A — Web:** canonical middleware, meta/LD‑JSON injectors, templates (title/desc/headers), image/video sitemaps, breadcrumb component.
- **Agent B — API:** SEO resolvers, slug service, ISR revalidation hooks, Search Console export cron.
- **Agent C — Ops:** CloudFront behaviors, logs→S3→Athena pipeline, robots/noindex header policy, cache keys.
- **Agent D — QA/Perf:** Lighthouse CI, JSON‑LD tests, SFW OG guard, crawl dashboards, a11y audits.

## **1.17.17 Acceptance Criteria (mark §1.17 FINAL only when ALL true)**

1907. Canonical URLs, robots **headers + meta**, and parameter stripping are live; filter/pagination pages are **noindex** and self‑canonical.
1908. City/role landings exist and are indexable; hubs and detail pages have **SFW OG** images; age‑gated items are **noindex**.
1909. JSON‑LD present and valid for Person(+Offers), LocalBusiness, Article, BreadcrumbList, and (where applicable) VideoObject.
1910. Segmented **web + image + video sitemaps** generate correctly and reference only indexable content; robots.txt points to the index.
1911. CWV budgets met (p75 mobile) on Home, City/Role landing, Service Profile, Studio Detail, and a Case Study page.
1912. A11y checks pass (axe/Pa11y) on public pages; images have alt; keyboard navigation functional.
1913. CloudFront logs + GSC are ingested; crawl waste \<10% of bot hits after 30 days; cache hit ratio ≥95%.
1914. SEO‑safe experimentation policy enforced; no client‑side cloaking or bot‑variant divergence.

# **§1.18 — Security, Compliance & DevSecOps**

*(zero‑trust architecture · IAM boundaries · authN/authZ for AppSync · secrets & key mgmt · encryption in transit/at rest · data classification & PII minimization · logging/audit & tamper‑evidence · WAF/bot/DDOS protections · vulnerability mgmt & CI/CD hardening · incident response & DR · compliance scaffolding · telemetry, SLOs, tests, costs)*

**Purpose.** Define the end‑to‑end security & compliance posture for the marketplace (web/app, Amplify/AppSync/Lambda/Aurora/DynamoDB/S3/CF, Stripe/IDV/esign providers), with **implementation‑grade** controls and inline artifacts you can paste into the plan. This section will not advance until it satisfies the **≥99.9%** bar.

## **1.18.A Security canon & threat model**

1915. **Least privilege & zero trust.** Every call is authenticated and authorized; no “trusted subnet.”
1916. **Default‑deny at edges.** WAF blocks obvious bad traffic; API throttles by identity.
1917. **PII minimization.** Only store what we must; tokenize or hash where possible; keep PII out of logs.
1918. **Compartmentalization.** Separate AWS accounts per env (dev/stage/prod) and per blast radius (prod‑data, prod‑ops).
1919. **Tamper‑evident audit.** Immutable trails for money/IDV/policy actions.
1920. **Idempotence everywhere.** All webhooks & money operations idempotent (no double charges).
1921. **Cost aware.** Prefer managed services (Amplify, Cognito, AppSync, WAF, Security Hub) over self‑hosted appliances.

## **1.18.B Identity & access management (IAM) boundaries**

**Recommended path:** *security/policies/iam-boundaries.md*

- Accounts & org

  - AWS **Organizations** with SCPs: deny *\*:\** at root, deny public S3 unless explicitly allowed, deny KMS key deletion.
  - Separate accounts: *rastup-dev*, *rastup-stage*, *rastup-prod*, plus *rastup-shared* (log archive) and *rastup-security*.

- Roles

  - **Workload roles**: per Lambda/service with minimal permissions (AppSync resolver roles; S3 prefixes; DynamoDB tables).
  - **Human roles**: *AdminLimited* (break‑glass), *OpsReadOnly*, *Analyst*, *SecurityEngineer*. MFA enforced; session limits (1–4h).
  - **JIT elevation** via IAM Identity Center (formerly SSO) with approval; all admin actions audited.

**Inline artifact — example least‑priv Dynamo policy**  
**Path:** *security/iam/policies/dynamo-least-priv.json*

*{*  
*"Version":"2012-10-17",*  
*"Statement":\[*  
*{"Effect":"Allow","Action":\["dynamodb:PutItem","dynamodb:GetItem","dynamodb:UpdateItem"\],*  
*"Resource":"arn:aws:dynamodb:us-east-1:{{account}}:table/fansub_entitlement_cache",*  
*"Condition":{"ForAllValues:StringEquals":{"dynamodb:LeadingKeys":\["USER#"\]}}}*  
*\]*  
*}*  

## **1.18.C Authentication & authorization (Amplify/AppSync/Cognito)**

**AuthN**

- **Cognito User Pool** for end‑users (buyers/sellers/creators/studio owners) with email+password and optional social IdPs (Apple/Google).
- **Cognito Identity Pool** for federated access to limited S3 (signed uploads of previews only).
- **Admin/agent** access via **OIDC** (IdP such as Google Workspace/Okta) → separate AppSync auth mode.

**AuthZ (AppSync multi‑auth)**

- **Cognito JWT** for user operations; **IAM** for server‑to‑server; **OIDC** for internal tooling.
- Use **@auth** rules + VTL/JS resolvers to enforce **row‑level** constraints (e.g., user can access only their threads, creator their own Fan‑Sub pages, admin by role claims).
- **Fine‑grained**: deny by default; allow by ownership (*ownerId == \$ctx.identity.sub*), role claim (*has("admin")*), or entitlement check (Dynamo cache read).

**Inline artifact — AppSync auth modes**  
**Path:** *security/appsync/multi-auth.md*

*- Default Authorization: AMAZON_COGNITO_USER_POOLS*  
*- Additional:*  
* - AWS_IAM (trusted Lambdas + batch jobs)*  
* - OPENID_CONNECT (Admin console only)*  
*- API Key: \*\*disabled\*\* in prod*  

## **1.18.D Secrets & key management**

- **AWS Secrets Manager**: Stripe keys, Plaid (if adopted), e‑sign provider tokens, SMTP creds (if not SES), third‑party API tokens.
- **SSM Parameter Store**: non‑secret config (feature flags, limits).
- **KMS**: dedicated CMKs per data domain (*pii*, *finance*, *legal*) with **key policies** bound to minimal roles; automatic rotation enabled.

**Inline artifact — Secrets naming convention**  
**Path:** *security/secrets/naming.md*

*/prod/stripe/secret_key*  
*/prod/stripe/webhook_secret*  
*/prod/plaid/client_id*  
*/prod/plaid/secret*  
*/prod/esign/api_key*  
*/stage/...*  

## **1.18.E Encryption (in transit & at rest)**

- **TLS 1.2+** everywhere (CloudFront, ALB, AppSync). HSTS on apex.
- **At rest**: S3 SSE‑KMS; DynamoDB SSE‑KMS; Aurora **encrypted**; CloudWatch Logs encrypted; Athena workgroup encryption enforced.
- **Field‑level**: hash emails (*sha256(email.lower().trim())*), store last‑4 only for phone if needed; avoid plaintext PII in events.
- **Tokenization**: use surrogate keys (*usr\_*, *sp\_*, *fsc\_*) across domains.

## **1.18.F Network & edge protections**

- **CloudFront + WAF**:

  - Managed rule sets (AWS Core, Bot Control), plus custom: block obvious scanners, rate‑limit */graphql* and POSTs.
  - Allowlist Stripe & provider IPs for webhook ingress (alternate: use API Gateway with a shared secret HMAC).

- **AWS Shield Standard** (at least) enabled on CF/ALB.

- **Lambdas**: in VPC only if they need RDS; otherwise public (reduces cold‑start & cost). Use **VPC endpoints** for S3/Secrets if inside VPC.

**Inline artifact — WAF rate rule example**  
**Path:** *security/waf/rate-limit-graphql.json*

*{ "Name":"GraphQLRateLimit","RateLimit":2000,"ScopeDownStatement":*  
*{"ByteMatchStatement":{"SearchString":"/graphql","FieldToMatch":{"UriPath":{}},"TextTransformations":\[{"Priority":0,"Type":"NONE"}\],"PositionalConstraint":"CONTAINS"}}*  
*}*  

## **1.18.G Data classification & handling**

**Recommended path:** *security/policies/data-classification.md*

- **Public**: marketing copy, SFW previews.
- **Internal**: ops dashboards, aggregate metrics.
- **Confidential PII**: names, emails, phone (minimize; never in logs).
- **Highly Sensitive**: government IDs, IDV artifacts, payment tokens (never store raw PAN).  
  **Rules**
- PII only in **Aurora/Dynamo “private”** schemas; analytics **events are PII‑free** (link via surrogate keys).
- **DSAR** tombstone events (see §1.13) applied to Silver/Gold; Bronze excluded on read.
- **Retention**: per §1.13 — Bronze 18 mo, Silver 24–36 mo, Gold 24 mo; finance facts 7 years.

## **1.18.H Logging, audit, and tamper‑evidence**

- **CloudTrail** to dedicated **log‑archive account** (S3 with **Object Lock** + Glacier).
- **App logs**: JSON, structured, **no PII**. Correlation IDs propagate (*x‑corr‑id*).
- **Admin actions** (refunds, holds, DMCA, representment) write to an **immutable audit table** (Aurora) and **append‑only** S3 log (WORM).
- **Webhook idempotency**: record *event_id* + response; on duplicate → 200 OK no‑op.

**Inline artifact — audit event shape**  
**Path:** *security/audit/event-envelope.json*

*{*  
*"ts":"2025-11-06T12:34:56Z",*  
*"actor":"usr_abc \| sys_lambda \| admin@rastup",*  
*"action":"refund.issued \| payout.hold.apply \| dmca.hide",*  
*"target":"leg\_... \| order\_... \| content\_...",*  
*"details":{ "reason":"...", "amount_cents":1234 },*  
*"corrId":"abc123"*  
*}*  

## **1.18.I Vulnerability management & CI/CD hardening**

- **Dependency hygiene**: lockfiles checked‑in; Renovate/Dependabot weekly PRs; third‑party package allowlist.
- **SAST**: GitHub CodeQL (or equivalent) on PR; custom regex rules for secrets.
- **Secrets scanning**: pre‑receive hooks + CI step; block merges on positive.
- **Container/Lambda layers**: ECR image scan or *npm audit* gates; Lambda base runtime kept current.
- **IaC**: CDK/Terraform scanned with **Checkov**/cfn‑nag.
- **CI**: OIDC‑based deploy roles (no long‑lived keys); branch protections; required reviews; signed tags for releases.
- **SBOM**: generate CycloneDX on release; archive to S3.

**Inline artifact — CI policy checklist**  
**Path:** *security/ci/policy.md*

*- Require PR reviews (2 for prod)*  
*- Status checks: build, test, lint, SAST, IaC scan, license scan*  
*- Protected branches: no force-push, linear history*  
*- OIDC deploy to AWS; no PAT/keys stored*  
*- Secrets only in GitHub OIDC to AWS + Secrets Manager at runtime*  

## **1.18.J Incident response (IR) & disaster recovery (DR)**

- **IR team & runbooks**: security@ group, Slack \#secur‑incidents (private), paging via SNS.

- **Playbooks**: credential leak, PII exposure, DDOS, data corruption, provider breach.

- **Forensics**: isolate role credentials; retrieve CloudTrail & app logs; snapshot affected S3 prefixes with Write Once retention.

- **DR**:

  - **Backups**: Aurora PITR, daily snapshots; Dynamo PITR; S3 versioning + Object Lock for evidence.
  - **RPO/RTO**: core web ≤ 15m RPO / ≤ 60m RTO; payments webhooks ≤ 5m / 15m.
  - **Regional**: consider cross‑region S3 replication for evidence vault; Aurora global DB if required later.

**Inline artifact — IR ticket template**  
**Path:** *security/ir/ticket-template.md*

*- Summary:*  
*- Detected by:*  
*- Impacted data/classes:*  
*- Timeline:*  
*- Containment:*  
*- Eradication:*  
*- Recovery:*  
*- Customer comms needed? Y/N*  
*- Follow-up CAPA items:*  

## **1.18.K Compliance scaffolding (SOC 2‑ready baseline)**

- **Policies**: access control, change mgmt, incident response, vendor risk, data retention, acceptable use (templates in */security/policies/\**).
- **Evidence**: automated exports (CloudTrail sampling, IAM user/role diffs, Security Hub findings, backup status, vulnerability scans).
- **Vendor management**: Stripe/IDV/esign risk rating, DPAs stored; review annually.
- **Training**: annual security awareness for staff; onboarding/offboarding checklist.

## **1.18.L Monitoring & detection**

- **GuardDuty**: enabled in all accounts; alerts → Security account SNS.

- **Security Hub**: aggregates findings; CIS benchmark checks.

- **Access Analyzer**: detect public/broad‑trust resources.

- **CloudWatch/SNS** alerts:

  - WAF blocks spike, 4xx/5xx spikes, AppSync throttles, Lambda DLQ growth, KMS key errors, Secrets rotation failure.

- **SIEM (lightweight)**: centralize key logs in S3 + Athena queries; optional OpenSearch later.

## **1.18.M SLOs, budgets & costs**

**SLOs**

- **Auth availability** ≥ 99.9% monthly.
- **Webhook idempotency** 100% (no double side‑effects).
- **P0 IR response** ≤ 15 min; **P1** ≤ 1 hour.
- **Secrets rotation** success 100% monthly cadence.

**Budgets**

- WAF: managed rules only at start; add Bot Control if abuse appears.
- Security Hub/GuardDuty: monitor costs; scope to prod + stage at launch.
- Logs: 30–90d hot retention; archive to Glacier Instant Retrieval thereafter.

## **1.18.N Test plan (security)**

1978. **AuthZ tests**: attempts to access other users’ resources denied; @auth rules covered.
1979. **Webhook replay**: replay Stripe/IDV webhooks; verify idempotent outcomes.
1980. **Secrets rotation**: rotate Stripe/SES/… in stage; production dry‑run window; alarms on failures.
1981. **WAF**: simulate bursts; ensure rate rules and managed sets engage; false positives monitored.
1982. **SAST/IaC**: seed a vulnerable branch; CI blocks merge.
1983. **DR**: restore Aurora snapshot into a staging clone; validate integrity.
1984. **PII logging**: send synthetic PII; verify logs redaction and alerts.
1985. **Break‑glass**: test JIT admin; ensure revocation and audit entries present.

## **1.18.O Work packages (Cursor 4‑agent lanes)**

- **Agent A — Auth & AppSync**: Cognito pools/claims, multi‑auth rules, entitlement resolvers, admin OIDC, JWT claims mapping.
- **Agent B — Edge & WAF**: CloudFront behaviors, WAF rules & rate limits, webhook ingress gateway, Shield enrollment.
- **Agent C — Secrets/KMS/Logs**: Secrets Manager structure, KMS CMKs & policies, CloudTrail to log‑archive, immutable audit append.
- **Agent D — CI/CD & Detection**: CodeQL/Checkov gates, OIDC deploy roles, Security Hub/GuardDuty, IR runbooks, DR backup policies.

## **1.18.P Acceptance criteria (mark §1.18 FINAL only when ALL true)**

1990. Multi‑auth implemented (Cognito + IAM + OIDC) with least‑privilege resolvers; API key **off** in prod.
1991. Secrets stored in Secrets Manager; KMS keys per domain; rotation policy in place and tested.
1992. S3/Dynamo/Aurora encrypted; TLS enforced; PII redaction in logs verified.
1993. WAF deployed with managed rules + GraphQL rate limits; webhooks protected (HMAC or allowlist).
1994. Immutable audit for admin actions present; CloudTrail centralization to log‑archive with Object Lock.
1995. CI/CD has SAST/IaC gates; OIDC deployments; SBOM archived.
1996. IR/DR runbooks executed in stage; RPO/RTO met; backup health dashboard up.
1997. Security Hub/GuardDuty/Access Analyzer findings triaged; alerts wired.
1998. Costs within initial budgets; no paid security appliances required at launch.

# **§1.18 — DevSecOps Addendum (Deep Completeness)**

Everything below is **text‑only artifacts** for your Word doc (each includes a *Recommended filename/path* to lift later if you choose).

## **1.18.A Threat Model (assets, trust boundaries, controls)**

**Recommended path:** *security/threat-model/overview.md*

*Assets*  
*- A1: Money flows (Stripe Connect, payouts, refunds)*  
*- A2: PII (names, emails, phones), IDV artifacts (age/18+ evidence), studio contracts*  
*- A3: Content previews (SFW only), deliverable manifests (hashes + URLs)*  
*- A4: Auth & session tokens (Cognito JWTs, admin OIDC)*  
*- A5: Audit trails & evidence vault (DMCA, chargebacks)*  
*- A6: Secrets & keys (Stripe, KMS, Secrets Manager)*  
  
*Trust Boundaries*  
*- Edge (CloudFront/WAF) → App (Next.js/AppSync/Lambdas)*  
*- App → Data (Aurora/Dynamo/S3/Glue/Athena)*  
*- Providers (Stripe/IDV/e‑sign/SES) via webhooks*  
*- Admin/OIDC → AppSync Admin mode*  
  
*Primary Risks & Controls*  
*- Injection/XXE/SSRF → parameterized queries, SSRF‑blocked by VPC egress policy, S3 Access Points*  
*- AuthZ bypass → AppSync @auth rules + resolver checks + test matrix*  
*- Webhook replay → idempotency store + HMAC verification*  
*- PII leakage/logging → structured logs with redaction + log scans*  
*- DoS/Bot → WAF rate rules + GraphQL complexity limits + per‑actor quotas*  
*- Content abuse → NSFW scanning + Safe‑Mode + DMCA pipeline*  

## **1.18.B Security Headers (CSP, Referrer, Permissions)**

**Recommended path:** *security/headers/response-headers.json*

*{*  
*"Content-Security-Policy": "default-src 'self'; img-src 'self'* [*https://cdn.rastup.com*](https://cdn.rastup.com) *data:; media-src 'self'* [*https://cdn.rastup.com*](https://cdn.rastup.com)*; script-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self' data:; connect-src 'self'* [*https://api.rastup.com*](https://api.rastup.com)*; frame-ancestors 'none'; base-uri 'self'; form-action 'self'",*  
*"Referrer-Policy": "strict-origin-when-cross-origin",*  
*"Permissions-Policy": "camera=(), microphone=(), geolocation=()",*  
*"Strict-Transport-Security": "max-age=63072000; includeSubDomains; preload",*  
*"X-Content-Type-Options": "nosniff",*  
*"X-Frame-Options": "DENY",*  
*"X-XSS-Protection": "0"*  
*}*  

Apply via **CloudFront Response Headers Policy**; for checkout pages add Stripe to *connect-src*/*frame-src*.

## **1.18.C GraphQL Complexity/Depth Limits + Rate Quotas**

**Recommended path:** *security/graphql/limits.md*

*GraphQL Limits*  
*- Max depth: 8*  
*- Max cost: 2,000 per query (field weights; nested lists penalized)*  
*- Max input payload: 256 KB*  
*- Introspection: enabled in dev/stage; disabled in prod except for whitelisted admin IPs*  
  
*Rate Quotas (per 5 minutes)*  
*- Anonymous: 120 requests*  
*- Authenticated user: 900 requests*  
*- Admin OIDC: 1,200 requests*  
*- Burst: 20 requests/second/user*  
*Enforced by WAF + AppSync throttling + identity-aware API Gateway usage plans (if used).*  

**Resolver guard (pseudocode)**  
**Path:** *security/graphql/cost-limiter.ts*

*export function enforceLimits(ctx) {*  
*if (ctx.depth \> 8 \|\| ctx.cost \> 2000) throw new Error("QUERY_LIMIT_EXCEEDED");*  
*if (ctx.inputSize \> 256\*1024) throw new Error("INPUT_TOO_LARGE");*  
*}*  

## **1.18.D Cookie & Session Policy**

**Recommended path:** *security/cookies/policy.md*

*Cookies*  
*- \_\_Host-rastup: session JWT reference; SameSite=Lax; Secure; HttpOnly; Path=/; Domain=\<none\>; Prefix=\_\_Host*  
*- consent: preference state; SameSite=Lax; Secure; HttpOnly=false*  
*- cfduid/edge: none (avoid third-party identifiers)*  
  
*Rules*  
*- No third-party trackers on public pages.*  
*- Analytics via first-party beacon only; respect consent.*  
*- JWTs not stored in localStorage; refresh via secure cookie.*  

## **1.18.E Webhook HMAC Verification (Stripe/Plaid)**

**Recommended path:** *security/webhooks/verify.ts*

*import crypto from 'crypto';*  
  
*export function verifyStripe(rawBody: Buffer, sigHeader: string, secret: string) {*  
*// Prefer Stripe SDK constructEvent; fallback HMAC check:*  
*const \[tPart, v1Part\] = sigHeader.split(',').map(s =\> s.trim());*  
*const t = tPart.split('=')\[1\]; const v1 = v1Part.split('=')\[1\];*  
*const payload = \`\${t}.\${rawBody.toString()}\`;*  
*const hmac = crypto.createHmac('sha256', secret).update(payload).digest('hex');*  
*if (!crypto.timingSafeEqual(Buffer.from(hmac), Buffer.from(v1))) throw new Error('INVALID_SIGNATURE');*  
*}*  

Store last **event_id** in an idempotency table; on duplicate, return 200 OK without re‑execution.

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

## **1.18.G Pre‑Signed Uploads (size/type guard)**

**Recommended path:** *security/s3/presign.ts*

*export function presignPreviewUpload({ userId, mime, bytes }) {*  
*if (!/^image\\(jpe?g\|png\|webp)\$/.test(mime)) throw new Error('UNSUPPORTED_TYPE');*  
*if (bytes \> 10 \* 1024 \* 1024) throw new Error('FILE_TOO_LARGE');*  
*// key scoped to user prefix, random suffix*  
*const key = \`previews/\${userId}/\${Date.now()}\_\${Math.random().toString(36).slice(2)}.webp\`;*  
*return s3.getSignedUrl('putObject', { Bucket: 'fansub-previews', Key: key, ContentType: mime, Expires: 300 });*  
*}*  

## **1.18.H Break‑Glass & JIT Admin Access**

**Recommended path:** *security/admin/break-glass.md*

*- No standing Admin in prod. Use Identity Center JIT with 1-hour session TTL.*  
*- Break-glass triggers:*  
*\* Widespread outage, data corruption, compromised credentials.*  
*- Procedure:*  
* 1) PagerDuty page; open IR ticket.*  
*2) Two-person approval; one requests JIT role; one approves.*  
*3) All actions in console shell are screen-recorded; correlation ID must be attached to commands.*  
*4) Revoke access at TTL; post-mortem includes access diff from CloudTrail.*  

## **1.18.I Secrets Rotation Runbook (Stripe, SES, KMS)**

**Recommended path:** *security/secrets/rotation-runbook.md*

*Cadence*  
*- Stripe API/Webhook: 90 days*  
*- SES SMTP creds: 180 days*  
*- KMS key rotation: yearly (auto)*  
  
*Steps (Stripe)*  
*1) Create new restricted key (write: charges, read: events).*  
*2) Deploy to stage via Secrets Manager (/stage/stripe/secret_key).*  
*3) Run stage smoke tests (webhooks).*  
*4) In prod, add new key alongside old; rotate webhooks secret.*  
*5) Flip AppSync/Lambdas to new secret; verify live.*  
*6) Disable old key; update runbook timestamps.*  
  
*Verification*  
*- CloudWatch alarm if Stripe auth errors \> 0.1% after rotation.*  

## **1.18.J Vendor Risk Management**

**Recommended path:** *security/vendors/register.md*

*- Stripe (Processor): DPA, SOC1/2 bridge, data location (US), breach SLA in vendor contract.*  
*- IDV provider: ID docs storage duration & encryption; data deletion API tested quarterly.*  
*- E-sign: signature evidence retention; tamper-evident hashes.*  
*- Email (SES): region & sending limits; bounce/complaint handling verified.*  
*- CDN/DNS: CloudFront/Route53; no third-party DNS at launch.*  
*- Annually review DPAs and security reports; track in vendor register with risk scores.*  

## **1.18.K Pen‑Test Scope & Safe Harbor**

**Recommended path:** *security/testing/pentest-scope.md*

*- In-scope: public web, AppSync API, mobile clients, preview upload endpoints.*  
*- Out-of-scope: providers (Stripe, IDV), employee-only VPN resources.*  
*- Constraints: no volumetric DoS, no social engineering.*  
*- Data: use synthetic accounts in stage; limited prod tests under supervision.*  
*- Safe harbor: good-faith testing protected; report via security@ with proof-of-concept only.*  

## **1.18.L OWASP ASVS Mapping (excerpt)**

**Recommended path:** *security/standards/asvs-mapping.md*

*- V1 Architecture: Zero-trust, least privilege (covered §1.18.B/C)*  
*- V2 Auth: Cognito/OIDC with MFA for admin; session cookie flags (§1.18.D)*  
*- V4 Access Control: AppSync @auth + resolver checks (tests in §1.18.N)*  
*- V5 Validation: JSON Schemas, event validation (see §1.13)*  
*- V9 Data Protection: TLS/HSTS/KMS; PII minimization (this section)*  
*- V14 Config: CSP, headers, secrets management (this section)*  

## **1.18.M DR Drill & Severity Matrix**

**Recommended path:** *security/ir/severity-matrix.md*

*Severities*  
*- P0: data exfiltration confirmed; payments outage \> 30 min*  
*- P1: partial outage; suspected credential leak*  
*- P2: localized bug with security impact; WAF false positive spike*  
  
*DR Drill (quarterly)*  
*- Restore Aurora snapshot to stage clone; switch read traffic for an hour; verify parity.*  
*- Simulate region impairment: serve static from CF + cached ISR; payments degraded mode on.*  
*- Outcome recorded; gaps turned into CAPA tickets.*  

## **1.18.N SIEM/Athena Queries (suspicious patterns)**

**Recommended path:** *security/siem/queries.sql*

*-- Excessive GraphQL POSTs per IP in 5 min*  
*SELECT ip, count(\*) AS c*  
*FROM cf_logs*  
*WHERE cs_method='POST' AND cs_uri_stem LIKE '%/graphql%' AND date=CAST(current_date AS varchar)*  
*GROUP BY ip HAVING count(\*) \> 500;*  
  
*-- Admin OIDC logins outside office hours*  
*SELECT user, ts FROM admin_auth_logs*  
*WHERE hour(ts) NOT BETWEEN 8 AND 20 AND result='SUCCESS';*  

## **1.18.O Access Recertification Schedule**

**Recommended path:** *security/governance/access-recert.yml*

*recertification:*  
*cadence: quarterly*  
*scopes:*  
* - human_roles: \[AdminLimited, OpsReadOnly, Analyst, SecurityEngineer\]*  
* - workload_roles: all Lambdas/AppSync roles*  
*approvers:*  
* - security_lead*  
* - domain_owner*  
*evidence:*  
* - IAM role membership diff*  
* - Access Analyzer public findings = 0*  

### **§1.18 Determination (post‑addendum)**

With this addendum, **§1.18 Security, Compliance & DevSecOps** covers the full scope to **≥99.9%**. It includes: identity boundaries, authN/Z details for AppSync, secrets/KMS, encryption, WAF/bot/DDOS, webhooks + idempotency, cookie/session policy, CSP/headers, S3/CloudFront hardening, rate limits & GraphQL complexity, audit, vendor risk, pen‑test scope, OWASP mapping, incident/DR, SIEM queries, access recertification, SLOs, budgets, tests, and runbooks — all as **inline artifacts** ready for your Word doc. I am **100% confident** we can proceed.

# **§1.19 — Internationalization (I18n), Localization (L10n) & Accessibility (A11y) —** ***Begin***

We will build a fully localized and accessible experience across public pages (SEO‑sensitive), app flows (checkout, messaging, Fan‑Sub), and admin tooling—without inflating costs. This section will be exhaustive and artifact‑rich; I’ll keep expanding it across replies until it meets the 99.9% bar.

## **1.19.A Canon & invariants**

- **Locale‑agnostic URLs** (canonical without locale; hreflang alternates in head).
- **Server‑rendered locale content** for SEO; dynamic strings pulled from versioned catalogs.
- **Currency, date, number** formats localized server‑side.
- **Right‑to‑left (RTL)** support from day one (dir=rtl).
- **Accessibility first**: WCAG 2.2 AA; keyboard‑first nav; SFW previews always carry alt text.
- **Cost**: use message catalogs + ICU; avoid heavy third‑party i18n SaaS; translations stored in S3/JSON and cached.

## **1.19.B Locale catalog & message format**

**Recommended path:** *i18n/catalog/en-US.json* (example)

*{*  
*"nav.home": "Home",*  
*"nav.city": "{city} creatives",*  
*"profile.title": "{displayName} — {role} in {city}",*  
*"studio.amenities": "Amenities",*  
*"checkout.pay": "Pay {amount, number, ::currency/USD}",*  
*"a11y.skip": "Skip to main content"*  
*}*  

**Loader (pseudocode)**  
**Path:** *i18n/loader.ts*

*export async function loadLocale(lang: string) {*  
*const res = await fetch(\`https://cdn.rastup.com/i18n/\${lang}.json\`, { cache: 'force-cache' });*  
*return res.json();*  
*}*  

## **1.19.C Hreflang & negotiation**

**Recommended path:** *web/lib/hreflang.ts* (complements §1.17)

*export const locales = \["en-US","es-ES","fr-FR","ar","de-DE"\];*  
*export function linksFor(canonical: string, map: Record\<string,string\>) {*  
*return Object.entries(map).map((\[lang, href\]) =\> \`\<link rel="alternate" hreflang="\${lang}" href="\${href}"\>\`).join("\n")*  
* + \`\n\<link rel="alternate" hreflang="x-default" href="\${canonical}"\>\`;*  
*}*  

# **§1.19 — Internationalization (I18n), Localization (L10n) & Accessibility (A11y) — Full Spec**

**Goal:** Ship a multilingual, accessible marketplace that preserves SEO, Safe‑Mode rules, and performance budgets. Everything below is **text‑only** for your Word doc and includes **Recommended filename/path** tags for later lift into the repo. We keep costs low (no heavy SaaS): JSON catalogs in S3, *Intl.\** APIs server/client, and automated extraction/QA.

## **1.19.1 Canon & invariants**

2005. **Locale‑agnostic canonicals.** Canonical URLs **don’t** contain locale; we add *hreflang* alternates (ties to §1.17).
2006. **Server‑rendered locale content** for public/SEO pages; client hydration matches server strings.
2007. **ICU MessageFormat** everywhere (plural, select, number/currency, dates).
2008. **RTL** supported from day one (Arabic/Hebrew): directional CSS, logical properties, bidi‑safe UI.
2009. **WCAG 2.2 AA**: keyboard, contrast, focus, forms, motion.
2010. **Cost**: catalogs in S3 (versioned), CDN‑cached; no per‑string paid APIs.
2011. **Safe‑Mode** rules: no 18+ previews in public pages/emails; localized strings **must not** bypass gating.

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

## **1.19.3 Locale catalogs & loading**

**Catalog structure (ICU MessageFormat)**  
**Recommended path:** *i18n/catalogs/en-US.json*

*{*  
*"nav.home": "Home",*  
*"nav.city": "{city} creatives",*  
*"cta.book": "Book now",*  
*"price.perHour": "{amount, number, ::currency/USD} per hour",*  
*"availability.slots": "{count, plural, one {# slot} other {# slots}} available",*  
*"a11y.skip": "Skip to main content",*  
*"safeMode.disclaimer": "Public previews are SFW. Some content requires Safe-Mode OFF and age verification."*  
*}*  

**Other locales** (create *es-ES.json*, *fr-FR.json*, *ar.json*, etc.) with identical keys; avoid string concatenation—always parametrize.

**Loader (server & client)**  
**Recommended path:** *i18n/loader.ts*

*export async function loadLocaleCatalog(lang: string) {*  
*const url = \`https://cdn.rastup.com/i18n/\${lang}.json\`;*  
*const res = await fetch(url, { cache: "force-cache" });*  
*if (!res.ok) throw new Error("CATALOG_MISSING");*  
*return res.json();*  
*}*  

**Extraction config**  
**Recommended path:** *i18n/extract.config.json*

*{*  
*"src": \["web/\*\*/\*.{ts,tsx}","apps/\*\*/\*.{ts,tsx}"\],*  
*"funcs": \["t","fmt.t","i18n.t"\],*  
*"output": "i18n/messages.pot"*  
*}*  

## **1.19.4 Locale detection & routing (no auto‑redirect loop)**

**Middleware (concept)**  
**Recommended path:** *web/middleware.locale.ts*

*import { NextRequest, NextResponse } from "next/server";*  
*import Negotiator from "negotiator";*  
*const SUPPORTED = \["en-US","es-ES","fr-FR","ar","de-DE"\];*  
  
*export function middleware(req: NextRequest) {*  
*const res = NextResponse.next();*  
*// Honor explicit choice in cookie first*  
*const chosen = req.cookies.get("locale")?.value;*  
*const lang = chosen \|\| new Negotiator({ headers: { "accept-language": req.headers.get("accept-language") \|\| "" } }).language(SUPPORTED) \|\| "en-US";*  
*res.headers.set("x-lang", lang);*  
*res.headers.set("x-dir", lang.startsWith("ar") ? "rtl" : "ltr");*  
*return res;*  
*}*  

**UX:** always offer a visible language switcher; **do not** force redirects based on IP.

## **1.19.5 Numbers, currency, dates & time zones**

**Utility**  
**Recommended path:** *i18n/format.ts*

*export function money(amountCents: number, currency: string, locale: string) {*  
*return new Intl.NumberFormat(locale, { style: "currency", currency }).format(amountCents / 100);*  
*}*  
*export function dateFmt(dtISO: string, locale: string, tz: string) {*  
*return new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short", timeZone: tz }).format(new Date(dtISO));*  
*}*  

**Rules:**

- Always format **server‑side** for SEO pages.
- Respect *prefers_24h* and *timezone*.
- For booking availability, display both **provider local time** and **viewer time** when they differ.

## **1.19.6 RTL support & logical CSS**

**Base CSS logical props**  
**Recommended path:** *web/styles/rtl.css*

*html\[dir="rtl"\] { direction: rtl; }*  
*.card { padding-inline: 16px; margin-inline: 8px; }*  
*.icon-chevron { transform: scaleX(var(--dir-mult, 1)); }*  
*html\[dir="rtl"\] .icon-chevron { --dir-mult: -1; }*  

**Mirroring images/icons:** use bidirectional icons or auto‑mirrored SVG; avoid text baked into images.

## **1.19.7 Accessible components (WCAG 2.2 AA)**

**Skip link & landmarks**  
**Recommended path:** *web/components/SkipLink.tsx*

*export const SkipLink = () =\> (*  
*\<a href="#main" className="sr-only focus:not-sr-only focus:fixed focus:top-2 focus:left-2 bg-yellow-300 p-2 rounded"\>*  
*{t("a11y.skip")}*  
*\</a\>*  
*);*  

**Accessible modal (focus trap, aria)**  
**Recommended path:** *web/components/Modal.tsx*

*export function Modal({ open, titleId, children, onClose }) {*  
*// trap focus, ESC to close, role="dialog" aria-modal="true" aria-labelledby={titleId}*  
*/\* ...focus management code... \*/*  
*}*  

**Combobox (search) ARIA**  
**Recommended path:** *web/components/Combobox.tsx*

*/\* role="combobox" aria-expanded aria-controls listbox; options role="option"; keyboard arrows, Enter, Esc; announces via aria-live \*/*  

**Color/contrast:** enforce ≥ 4.5:1; expose *high_contrast* toggle that upgrades token set.

**Reduced motion:** respect *prefers-reduced-motion* and user pref; disable parallax/animated transitions.

## **1.19.8 Form localization & validation**

- **Names:** do not force first/last in all locales; offer single “full name” with optional structured fields.
- **Addresses:** use country‑specific layouts (state/province, postal code).
- **Phones:** use libphonenumber server‑side and client hints; store E.164 format.
- **Error messages:** localized, short, plain language; associate with fields via *aria-describedby*.
- **Date pickers:** local week start; localized month/day names; keyboard accessible.

**Validation messages catalog**  
**Recommended path:** *i18n/validation/en-US.json*

*{*  
*"required": "This field is required.",*  
*"email": "Enter a valid email address.",*  
*"minLength": "Use at least {min} characters.",*  
*"invalidPhone": "Enter a valid phone number."*  
*}*  

## **1.19.9 Public SEO pages: localized metadata & JSON‑LD**

**Head helper**  
**Recommended path:** *web/seo/meta.tsx*

*export function PageMeta({ titleKey, descKey, params }) {*  
*const title = t(titleKey, params);*  
*const desc = t(descKey, params);*  
*return (*  
*\<\>*  
*\<title\>{title}\</title\>*  
*\<meta name="description" content={desc} /\>*  
*{/\* SFW OG image per §1.17 \*/}*  
*\</\>*  
*);*  
*}*  

**Localized JSON‑LD:** translate *headline*, *description*, *addressLocality* etc., but **never** substitute 18+ images.

## **1.19.10 Emails & notifications localization (MJML)**

**Template with locale switch**  
**Recommended path:** *comms/templates/\_partials/strings.json*

*{*  
*"en-US": { "cta.viewProfile": "View profile", "digest.header": "This week in {city}" },*  
*"es-ES": { "cta.viewProfile": "Ver perfil", "digest.header": "Esta semana en {city}" }*  
*}*  

**Sender policy:** *From* name localized; subject lines localized; quiet hours per **recipient timezone**.

## **1.19.11 Translation workflow, QA & pseudolocalization**

**Workflow**

2020. Devs mark strings with *t('key')*.
2021. Extract → *messages.pot* (CI).
2022. Translate in Git (JSON catalogs), not in CMS; PR review by language owners.
2023. **Pseudolocalization** stage (*\[!! Ŧêxţ ẽłôñĝąţęđ !!\]*) to catch truncation/overflow.
2024. Screenshot diff QA for top pages per locale (Crowd‑shots optional later).
2025. Version catalogs; invalidate CDN on merge.

**Pseudolocalizer script**  
**Recommended path:** *i18n/tools/pseudo.ts*

*export function pseudo(s: string){ return s.replace(/\[aAeEiIoOuUc\]/g, m =\> ({a:"á",e:"ë",i:"ï",o:"ø",u:"ü",c:"ç"}\[m.toLowerCase()\] \|\| m)).replace(/(\[a-z\])/gi,"\$1\u0301"); }*  

## **1.19.12 A11y testing (automated + manual)**

**Automated (CI):** axe + pa11y on */*, */city/{city}*, */p/{handle}*, */s/{slug}*, */checkout*.  
**Manual matrix:** keyboard‑only; screen readers (NVDA/Windows, VoiceOver/macOS), zoom 200%, high‑contrast mode, reduced‑motion, RTL reading order.  
**Defect SLAs:** A11y blockers = P1 (fix before release to prod); contrast/label issues = P2 (fix within 2 sprints).

## **1.19.13 Performance & bundle budgets for i18n**

- **Do not** ship all catalogs to every user: load on demand from CDN.
- Tree‑shake i18n runtime; rely on browser *Intl*; **Node with full‑icu** in SSR.
- Pre‑render top locales for city/role pages to hit SEO.

**Bundle budget (public pages)**  
**Recommended path:** *observability/budgets/i18n-budget.json*

*{ "resourceSizes":\[{"resourceType":"script","budget":150},{"resourceType":"total","budget":850}\] }*  

## **1.19.14 Governance: language coverage & content policy**

- Launch locales: *en-US*; “Phase 2”: *es-ES*; “Phase 3”: *fr-FR*, *de-DE*, *ar*.
- **Gate publishing** of a locale until: 100% key coverage, pseudolocalization pass, a11y pass, SEO checks (hreflang).
- Maintain a **glossary** per role/feature to keep translations consistent.

## **1.19.15 Work packages (Cursor 4‑agent lanes)**

- **Agent A — Web/App:** i18n provider, locale switcher, RTL styles, A11y components (Modal, Combobox, SkipLink), head meta helper.
- **Agent B — API/SSR:** user prefs fields/resolvers, server formatting helpers, Node full‑icu build, JSON‑LD localization.
- **Agent C — Comms/SEO:** localized MJML templates, subject/From localization, hreflang tags, sitemap alternates.
- **Agent D — QA/Tooling:** extractor/pseudolocalizer, axe/pa11y CI, screenshot diff, catalogs versioning/CDN invalidation.

## **1.19.16 Acceptance criteria — mark §1.19 FINAL only when ALL true**

2036. Locale selection persists; server adds *lang* & *dir* correctly; **no auto‑redirect loops**; hreflang alternates present on SEO pages.
2037. ICU MessageFormat is used across web/app/emails; prices/dates/numbers localized; dual‑timezone display where relevant.
2038. RTL renders correctly: layout mirrored, icons swapped, reading order valid; no clipped/truncated text.
2039. A11y: WCAG 2.2 AA checks pass (axe/pa11y + manual SR runs); keyboard navigation works across all interactive components.
2040. Public pages (SEO) pre‑render localized titles/descriptions/JSON‑LD with **SFW images** only; Safe‑Mode rules respected.
2041. Catalogs load per‑locale (no shipping all); bundle budgets met; Node SSR has full‑icu.
2042. Translation workflow operational: extraction → PR review → pseudolocalized QA → deploy; glossary maintained.
2043. Emails localized, with quiet hours by timezone; no 18+ previews in emails.
2044. Costs controlled: catalogs on S3/CDN; no paid localization SaaS at launch.

# **§1.20 — Mobile (PWA + Optional Native Shells), Push, and Device Capabilities**

*(app architecture · PWA config & offline · optional RN/Expo shells · deep links & routing · auth/session on device · push notifications (APNs/FCM/Pinpoint) · file uploads from camera · Safe‑Mode & age‑gated UX · performance budgets · a11y on mobile · CI/CD & releases · telemetry · tests · cost posture)*

**Purpose.** Specify the complete mobile experience: a first‑class **Progressive Web App (PWA)** that covers the entire user journey (discovery → messages → booking → delivery), with an optional **React Native (Expo) shell** for app store presence when/if desired. This section defines how we implement offline, push, deep‑links, device uploads, Safe‑Mode gating, performance, a11y, telemetry, CI/CD, and costs. All artifacts are **inline text** for your Word doc with “Recommended filename/path” tags so your builders can later lift them into the repo.

## **1.20.A Canon & invariants**

2045. **PWA‑first**: one codebase (Next.js) with service worker, install prompt, offline for core routes, and background sync for drafts/uploads.
2046. **Optional native shells** (React Native + Expo) wrap the web for store distribution and system‑level push; both shells and PWA use the same AppSync APIs.
2047. **Safe‑Mode on mobile**: defaults ON for guests/new installs; SFW previews only; 18+ features gated behind age verification and explicit user choice, never emailed or pushed with previews.
2048. **Cost‑conscious:** APNs/FCM via Amazon **Pinpoint/SNS**, no extra third‑party SDK bloat; media uploads are direct‑to‑S3 presigned, resized on device.
2049. **Accessibility**: WCAG mobile patterns, large tap targets, VoiceOver/TalkBack tested, motion‑safe animations.
2050. **Privacy**: no background location; images EXIF stripped on upload (unless user opts in for studio proofs).

## **1.20.B Client architecture**

- **PWA shell** (Next.js): app‑router, service worker, manifest, edge caching; GraphQL via AppSync (JWT auth).

- **Native shells** (optional):

  - **React Native** + **Expo** (managed workflow) for iOS/Android.
  - Uses a small native bridge for push tokens, file pickers, camera, and device storage; renders either RN screens or a WebView wrapper for certain flows if we choose a hybrid approach.

- **Shared modules**: auth/session, GraphQL client, feature flags, Safe‑Mode, formatting (ICU), and analytics events shared across PWA and RN.

## **1.20.C PWA configuration (manifest, SW, caching, offline)**

**Recommended path:** *web/public/manifest.webmanifest*

*{*  
*"name": "RastUp",*  
*"short_name": "RastUp",*  
*"start_url": "/?source=pwa",*  
*"display": "standalone",*  
*"background_color": "#0e1116",*  
*"theme_color": "#0e1116",*  
*"icons": \[*  
*{"src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},*  
*{"src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png"}*  
*\]*  
*}*  

**Service Worker** (Workbox‑style pseudocode)  
**Recommended path:** *web/public/sw.js*

*self.addEventListener('install', e =\> {*  
*e.waitUntil(caches.open('rastup-precache-v1').then(c =\> c.addAll(\[*  
*'/', '/city', '/styles.css', '/manifest.webmanifest'*  
*\])));*  
*});*  
*self.addEventListener('fetch', e =\> {*  
*const url = new URL(e.request.url);*  
*// HTML: NetworkFirst with fallback to cache*  
*if (e.request.mode === 'navigate') {*  
*e.respondWith(fetch(e.request).then(r =\> {*  
*const copy = r.clone(); caches.open('rastup-pages').then(c =\> c.put(e.request, copy));*  
*return r;*  
*}).catch(() =\> caches.match(e.request) \|\| caches.match('/')));*  
*return;*  
*}*  
*// Images: Stale-While-Revalidate*  
*if (url.pathname.startsWith('/\_next/image') \|\| url.pathname.startsWith('/images/')) {*  
*e.respondWith(caches.open('img').then(async c =\> {*  
*const cached = await c.match(e.request);*  
*const fresh = fetch(e.request).then(r =\> { c.put(e.request, r.clone()); return r; });*  
*return cached \|\| fresh;*  
*}));*  
*}*  
*});*  

**Offline scope:** home, city pages, profile/studio detail (last viewed), messages list (last page cached), compose drafts.

## **1.20.D Optional native shells (React Native + Expo)**

**Project layout**  
**Recommended path:** *apps/mobile/App.tsx*

*export default function App() {*  
*return (*  
*\<SafeAreaProvider\>*  
*\<NavigationContainer linking={linking}\>*  
*\<Stack.Navigator\>*  
*\<Stack.Screen name="Home" component={HomeScreen}/\>*  
*\<Stack.Screen name="Messages" component={MessagesScreen}/\>*  
*\<Stack.Screen name="Booking" component={BookingScreen}/\>*  
*\<Stack.Screen name="Web" component={WebViewScreen}/\> {/\* for hybrid routes if needed \*/}*  
*\</Stack.Navigator\>*  
*\</NavigationContainer\>*  
*\</SafeAreaProvider\>*  
*);*  
*}*  

**Deep link config**  
**Recommended path:** *apps/mobile/linking.ts*

*export default {*  
*prefixes: \['rastup://','https://rastup.com'\],*  
*config: { screens: {*  
*Home: '',*  
*Messages: 'messages',*  
*Booking: 'checkout/:id',*  
*Profile: 'p/:handle',*  
*Studio: 's/:slug'*  
*}}*  
*};*  

**Platform considerations (high‑level policy):** at launch, **PWA can be primary**. If/when we publish native apps, limit the initial native scope to discovery, booking, messages, and studios; keep **Fan‑Sub paid content flows** in the web experience until we explicitly decide to support native in‑app purchase workflows.

## **1.20.E Auth & session on device**

- **Cognito** hosted UI or embedded flows; JWTs stored in **HttpOnly Secure** cookies for Web/PWA; in RN, keep tokens in **secure storage** (Keychain/Keystore).
- **Session refresh** via refresh‑token rotation; background refresh guarded by app state.
- **Device trust**: bind push tokens and device fingerprints to user id for security & rate‑limits (§1.18).

## **1.20.F Messaging UX on mobile**

- **Thread list** with last message preview, unread counts, typing indicators; **thread view** with infinite scroll and media bubbles (SFW thumbnails).
- **Composer**: text, camera/gallery picker, quick templates.
- **Offline**: queue outgoing messages; retry with backoff; show pending state.
- **Abuse controls**: block/report from header; Safe‑Mode hides 18+ previews.

## **1.20.G Push notifications (APNs/FCM via Pinpoint/SNS)**

**Token registration**  
**Recommended path:** *apps/mobile/push/register.ts*

*export async function registerPushToken(userId: string, token: string, platform: 'ios'\|'android'\|'web') {*  
*await gql.mutate('savePushToken', { userId, token, platform, tz: Intl.DateTimeFormat().resolvedOptions().timeZone });*  
*}*  

**Server routing**

- Use Pinpoint/SNS topics per **city** and per **user** for rate‑efficient broadcasts and 1:1 messages.
- **Quiet hours** enforce local‑time windows; **daily caps** per category (alerts/digests vs direct messages).
- Templates mirror §1.16 MJML text (title/body only; no 18+ previews).

## **1.20.H File uploads from camera/gallery**

- **Direct‑to‑S3 presigned PUT** (see §1.18.G) with client‑side resize (e.g., target ≤ 2048px longest).
- **EXIF strip** by default; user can opt‑in to keep GPS/time for studio evidence flows.
- **Progress & background**: show %; resume after app pause.
- **Virus/NSFW scan** on ingest (already defined in §1.14 and §1.10).

**Recommended path:** *apps/mobile/upload.ts*

*export async function uploadImage(fileUri: string, mime: string) {*  
*const { url, fields, key } = await gql.mutate('getPresignedUrl', { mime, purpose: 'preview' });*  
*const body = await buildMultipart(fileUri, fields); // RN: fetch blob/file*  
*const res = await fetch(url, { method: 'POST', body });*  
*if (!res.ok) throw new Error('UPLOAD_FAILED');*  
*return { key };*  
*}*  

## **1.20.I Safe‑Mode & age gating UX**

- **First‑run:** Safe‑Mode ON; explain what it does; clear toggle path in **Settings**.
- **Age verification** (when required): IDV web flow in secure webview; store only verdict and event id, not raw images (§1.18 data minimization).
- **Surface rules:** No push/email with 18+ previews; PWA and RN show SFW placeholders until Safe‑Mode OFF + verified.

## **1.20.J Performance budgets (mobile)**

**Targets (mobile P75):** LCP ≤ 2.5s (PWA), INP ≤ 200ms, TTI ≤ 3.5s, bundle ≤ 900KB total on first load (GZIP).

**Tactics:**

- Code‑split heavy editors/maps; prefetch next screens on tap‑down; image lazy‑load with low‑quality placeholders; *fetchpriority="high"* for LCP hero; local fonts with *font-display: swap*.
- For RN: Hermes engine, RAM bundles, Flipper disabled in prod, animation worklets only where needed.

**Budget file**  
**Recommended path:** *observability/budgets/mobile.json*

*{ "pwaFirstLoadKB": 900, "pwaScriptKB": 160, "pwaImgPolicy": "webp/avif", "rnBundleKB": 420 }*  

## **1.20.K Accessibility (mobile a11y)**

- **VoiceOver/TalkBack** labels on all controls; proper roles for tabs/lists; visible focus on PWA.
- **Touch targets ≥ 44px**; dynamic type support; prefers‑reduced‑motion disables parallax and spinners.
- Color contrast tokens switchable to high‑contrast palette (user pref from §1.19).

## **1.20.L Deep links & universal links**

- **iOS** *apple‑app‑site‑association* and **Android** Asset Links hosted under */.well-known/*.
- Universal link handling maps to Profile/Studio/Checkout/Message screens; unknown routes open in in‑app webview.

**Recommended path:** *web/public/.well-known/apple-app-site-association*

*{"applinks":{"apps":\[\],"details":\[{"appID":"TEAMID.com.rastup.app","paths":\["/p/\*","/s/\*","/checkout/\*","/messages\*"\]}\]}}*  

## **1.20.M CI/CD & releases (PWA + RN shells)**

- **PWA**: GitHub Actions build → deploy to Amplify Hosting/CloudFront; invalidation of changed paths; Lighthouse CI budget gate.
- **RN shells** *(optional)*: Expo EAS build & submit; internal test tracks (Play) and TestFlight; codepush‑style OTA (for JS only, not for policy‑sensitive features).
- **Signing & secrets** in GitHub OIDC + Secrets Manager; no long‑lived signing keys in repo (§1.18).

## **1.20.N Telemetry & crash reporting**

- PWA: first‑party analytics via *navigator.sendBeacon*; CWV field data per route; soft‑error logging.
- RN: minimal crash reporter (e.g., Sentry‑like equivalent can be added later) but keep SDKs lean; at launch, start with OS crash logs + our event pipeline.
- **Mobile event taxonomy** aligns with §1.13 (e.g., *app.install*, *pwa.install_prompt*, *push.opt_in*, *message.send*, *upload.start/success*, *booking.start/complete*).

## **1.20.O Error taxonomy (client‑safe)**

- *UPLOAD_FAILED*, *UNSUPPORTED_TYPE*, *FILE_TOO_LARGE*, *PUSH_DENIED*, *SAFE_MODE_BLOCKED*, *AUTH_EXPIRED*, *OFFLINE_RETRYING*.
- Each error includes user‑friendly copy and retry guidance.

## **1.20.P Test plan (device & CI)**

2086. **Installability** (PWA): manifest audit, offline home/city, revalidation behavior.
2087. **Messaging**: send/receive, offline queue, image upload retry.
2088. **Booking**: flow from profile → package → checkout; date/timezones; Apple/Google Pay via web Stripe (where applicable).
2089. **Push**: token registration; quiet hours; category caps; deep link opens correct screen.
2090. **Safe‑Mode**: previews stay SFW with Safe‑Mode ON; age‑gated features blocked until verified.
2091. **A11y**: VoiceOver/TalkBack; high‑contrast; reduced‑motion.
2092. **Performance**: p75 budgets met on mid‑range Android (Moto G‑class).
2093. **RN shells** (if used): deep links, file uploads, push, fallback to webview for long‑tail routes.

## **1.20.Q Work packages (Cursor 4‑agent lanes)**

- **Agent A — PWA/UX**: service worker, manifest, offline scopes, Safe‑Mode toggles, upload UI.
- **Agent B — RN Shells** (optional): Expo app, push bridge, deep links, secure storage, hybrid webview wrappers.
- **Agent C — Backend/Comms**: Pinpoint/SNS setup, push templates, quiet hours & caps, presigned uploads, AppSync mutations.
- **Agent D — QA/Perf**: device matrix, Lighthouse CI, CWV field beacons, a11y runs, perf tuning.

## **1.20.R Acceptance criteria — mark §1.20 FINAL only when ALL true**

2098. PWA installable; offline works for defined scopes; background retry for uploads/messages.
2099. Push notifications delivered via Pinpoint/SNS to Web/iOS/Android with quiet hours & caps; deep links open the correct screen.
2100. Camera/gallery uploads succeed with on‑device resize, EXIF strip by default, S3 presigned PUT, and server‑side scans.
2101. Safe‑Mode and age gating enforced consistently; no 18+ previews in notifications or public pages.
2102. Mobile performance budgets met; a11y checks pass on PWA and RN shells (if used).
2103. CI/CD pipelines in place for PWA (Amplify/CloudFront) and, if used, RN shells (EAS/TestFlight/Play internal).
2104. Telemetry and crash/error reporting active; event taxonomy integrated with §1.13.

# **§1.21 — Search, Discovery & Ranking Engine (Re‑issued in full, sequential order)**

*This is the same complete §1.21 I produced earlier, re‑posted here to maintain strict numeric order in your master Word document. Everything is text‑only and copy‑pasteable, with “Recommended filename/path” markers for later lift‑and‑shift.*

## **1.21.A Index documents & schemas**

We maintain two primary collections: *people_v1* and *studios_v1*. All public fields are **SFW‑only** (no 18+ media or attributes). Private/sensitive fields never enter search docs.

**Recommended path:** *search/schemas/typesense.json*

*{*  
*"collections": \[*  
*{*  
*"name": "people_v1",*  
*"fields": \[*  
*{"name":"id","type":"string"},*  
*{"name":"handle","type":"string"},*  
*{"name":"displayName","type":"string"},*  
*{"name":"roles","type":"string\[\]","facet":true},*  
*{"name":"genres","type":"string\[\]","facet":true},*  
*{"name":"city","type":"string","facet":true},*  
*{"name":"region","type":"string","facet":true},*  
*{"name":"country","type":"string","facet":true},*  
*{"name":"lat","type":"float"},*  
*{"name":"lon","type":"float"},*  
*{"name":"verified","type":"bool","facet":true},*  
*{"name":"trusted","type":"bool","facet":true},*  
*{"name":"nsfw_band","type":"int32","facet":true},*  
*{"name":"priceFromCents","type":"int64","facet":true},*  
*{"name":"priceToCents","type":"int64","facet":true},*  
*{"name":"amenities","type":"string\[\]","facet":true},*  
*{"name":"packagesCount","type":"int32"},*  
*{"name":"repScore","type":"float"},*  
*{"name":"recencyScore","type":"float"},*  
*{"name":"engagementScore","type":"float"},*  
*{"name":"availabilityScore","type":"float"},*  
*{"name":"completenessScore","type":"float"},*  
*{"name":"updatedAt","type":"int64"},*  
*{"name":"createdAt","type":"int64"}*  
*\],*  
*"default_sorting_field": "updatedAt"*  
*},*  
*{*  
*"name":"studios_v1",*  
*"fields":\[*  
*{"name":"id","type":"string"},*  
*{"name":"slug","type":"string"},*  
*{"name":"name","type":"string"},*  
*{"name":"city","type":"string","facet":true},*  
*{"name":"region","type":"string","facet":true},*  
*{"name":"country","type":"string","facet":true},*  
*{"name":"lat","type":"float"},*  
*{"name":"lon","type":"float"},*  
*{"name":"verified","type":"bool","facet":true},*  
*{"name":"nsfw_band","type":"int32","facet":true},*  
*{"name":"amenities","type":"string\[\]","facet":true},*  
*{"name":"priceFromCents","type":"int64","facet":true},*  
*{"name":"priceToCents","type":"int64","facet":true},*  
*{"name":"sizeSqFt","type":"int32","facet":true},*  
*{"name":"recencyScore","type":"float"},*  
*{"name":"engagementScore","type":"float"},*  
*{"name":"bookingScore","type":"float"},*  
*{"name":"updatedAt","type":"int64"},*  
*{"name":"createdAt","type":"int64"}*  
*\],*  
*"default_sorting_field": "updatedAt"*  
*}*  
*\]*  
*}*  

## **1.21.B Ingest & indexing pipeline**

**Sources:** Aurora (entities), S3 (SFW previews/derived tags), computed‑signals service.

**Flow:** publish/edit/booking → **Kinesis change topic** → **Indexer Lambda** → Typesense *upsert*.

**Recommended path:** *search/events/entity-change.json*

*{ "kind":"entity.updated", "entity":"person\|studio", "id":"sp\_...\|st\_...", "reason":"publish\|edit\|review\|booking\|availability", "ts":"2025-11-06T15:10:01Z" }*  

**Recommended path:** *search/indexer/indexer.ts*

*for (const evt of stream) {*  
*const base = await loadEntity(evt.entity, evt.id);*  
*const signals = await computeSignals(evt.entity, evt.id);*  
*const doc = toSearchDocument(base, signals); // SFW-only*  
*await typesense.collections(coll(evt.entity)).documents().upsert(doc, { 'dirty_values':'coerce_or_drop' });*  
*}*  

**Reindex runbook** (alias flip, dual‑write, shadow compare): *search/runbooks/reindex.md*.

## **1.21.C Query model (ANY/ALL, Safe‑Mode, geo/price)**

Input mirrors §1.16’s saved‑search format:

*{*  
*"scope":"people\|studios",*  
*"city":"houston",*  
*"any":\[{"field":"genres","op":"in","value":\["fashion","editorial"\]}\],*  
*"all":\[{"field":"priceFromCents","op":"between","value":\[10000,30000\]},{"field":"verified","op":"eq","value":true}\],*  
*"safeMode":true,*  
*"sort":"best\|new\|distance\|price_low\|price_high",*  
*"origin":{"lat":29.7604,"lon":-95.3698}*  
*}*  

- **Safe‑Mode ON:** filter *nsfw_band \<= 1*.
- **Distance:** add *\_distance(lat,lon)* for sort and expose *distanceKm* in results.
- **Price:** hard filter via ranges; soft fitness in ranking (below).

## **1.21.D Autocomplete & suggestions**

2108. **Prefix autocomplete** across *displayName/handle/genres/city* with typo tolerance.
2109. **Query suggestions** materialized from analytics (last 30 days), ranked by CTR and deduped; cached.

**Recommended path:** *search/api/autocomplete.ts*

*export async function autocomplete({ q, scope, city }) {*  
*const params = {*  
*q,*  
*query_by: scope==='people' ? 'displayName,handle,genres,city' : 'name,amenities,city',*  
*filter_by: \[\`city:=\${city}\`, 'nsfw_band:\<=1'\].join(' && '),*  
*per_page: 8,*  
*prefix: true,*  
*num_typos: 2*  
*};*  
*return typesense.collections(coll(scope)).documents().search(params);*  
*}*  

**Materialization SQL:** *search/suggestions/materialize.sql* (CTR@30d, thresholds, limit 2k).

## **1.21.E Ranking & boosts (default “best” sort)**

**People**

*score = 0.25\*rep + 0.20\*recency + 0.15\*engagement + 0.15\*availability*  
* + 0.10\*verifiedBoost + 0.05\*trustedBoost + 0.05\*priceFitness*  
* - 0.10\*distancePenalty*  

**Studios**

*score = 0.30\*booking + 0.20\*recency + 0.15\*engagement*  
* + 0.15\*verifiedBoost + 0.10\*amenityFitness*  
* - 0.10\*distancePenalty*  

Signals are normalized to \[0,1\]. Boosts are **bounded** to avoid overwhelming organic signals; tie‑breakers: recency, id.

**Spec:** *search/signals/compute.md* (sigmoid/exp‑decay/gaussian/Jaccard formulas).

## **1.21.F Synonyms, stemming & typo tolerance**

- Domain synonyms (e.g., *“cyclorama” ⇄ “cyc wall”*), city nicknames (*“NYC” ⇄ “New York City”*).
- Typos: **2** for terms \>5 chars, **1** for 3–5 chars, exact for ≤2 chars.
- **Recommended path:** *search/schemas/synonyms.json*.

## **1.21.G Safe‑Mode, policy & exclusion**

- Safe‑Mode ON excludes *nsfw_band \>= 2*.
- Policy: DMCA/policy cases remove entities from index; reinstate when cleared.
- Thin profiles (completeness \< threshold) are not searchable until improved.

## **1.21.H Caching, throughput & cost**

- Edge‑cache **query suggestions** (1–5 min TTL).
- Short server‑side memoization for hot city/role landings (30–60s).
- Alert/scheduler batch queries off‑peak.
- Cluster sizing targets 95p latency \< 120 ms at launch; monitor and scale.

## **1.21.I Admin & curation tools**

- **Pins** per city/query; TTL; stored in *search_curation* (DDL below).
- **Synonym editor** (admin UI) persisted in Aurora and synced to Typesense.
- **Bad queries** dashboard for zero‑results & low CTR.

**Recommended path:** *db/migrations/021_search_curations.sql*

*create table if not exists search_curation (*  
*cur_id text primary key, -- scu\_...*  
*scope text not null check (scope in ('people','studios')),*  
*city text not null,*  
*query text,*  
*pin_ids text\[\] not null,*  
*expires_at timestamptz,*  
*created_at timestamptz not null default now()*  
*);*  

## **1.21.J Telemetry, evaluation & experimentation**

- **Events:** *search.query\|results\|click\|zero_results*, *search.autocomplete.select*, *search.suggest.click*.
- **Quality:** CTR@k, save rate@k, message‑start/booking start&complete@k, zero‑results rate.
- **Offline eval:** compute **NDCG@10** weekly from interaction labels; compare weight variants; guardrails for result diversity.

**NDCG SQL (simplified):** *search/eval/ndcg.sql*.

## **1.21.K API (GraphQL)**

**Recommended path:** *api/schema/search.graphql*

*type SearchResult {*  
*id: ID!*  
*kind: String!*  
*score: Float!*  
*distanceKm: Float*  
*priceFromCents: Int*  
*priceToCents: Int*  
*city: String!*  
*displayName: String*  
*name: String*  
*verified: Boolean!*  
*trusted: Boolean*  
*preview: AWSJSON*  
*}*  
  
*type SearchPage { items: \[SearchResult!\]!, total: Int!, nextCursor: String }*  
  
*input SearchFilter {*  
*scope: String!, city: String!,*  
*any: AWSJSON, all: AWSJSON,*  
*safeMode: Boolean = true,*  
*originLat: Float, originLon: Float,*  
*sort: String = "best", pageSize: Int = 24, cursor: String*  
*}*  
  
*type Query {*  
*search(input: SearchFilter!): SearchPage!*  
*autocomplete(q: String!, scope: String!, city: String!): \[String!\]!*  
*}*  

## **1.21.L Test plan**

2126. Indexing correctness & reindex safety; DMCA hide works.
2127. ANY/ALL logic; Safe‑Mode; distance/price sorts; synonyms; typos; autocomplete.
2128. Ranking weights & bounded boosts; diversity guardrails.
2129. Zero‑results suggestions & logging.
2130. Load: 95p \< 120 ms for 95% queries; bursts handled.
2131. Security: WAF throttles; no PII in docs; admin curation role‑gated.
2132. Cost: alert jobs complete within budget.

## **1.21.M Acceptance criteria — mark §1.21 FINAL only when ALL true**

2133. *people_v1*/*studios_v1* live with SFW‑only docs; ingest pipeline + reindex runbook in place.
2134. Query model supports ANY/ALL, Safe‑Mode, geo origin, standard sorts; autocomplete & suggestions operational.
2135. Ranking implemented with bounded boosts, price/amenity fitness, distance penalty; diversity guardrails active.
2136. Synonyms/typos configured; city nicknames resolved; zero‑results rate below target.
2137. Admin pinning & synonym tools available; analytics dashboards show CTR@k, save rate@k, booking conversions, NDCG@10.
2138. Latency & throughput SLOs met; costs within launch budget; WAF & policy gates enforced.

# **§1.22 — Payments, Payouts, Refunds & Financial Reconciliation — Full Spec**

*(platform fees & pricing model · Stripe Connect architecture · payment methods & flows · holds/capture/escrow posture · refunds, disputes & evidence · credits/vouchers & taxes · payouts & compliance (KYC/1099‑K) · ledgers & reconciliation (Bronze/Silver/Gold) · webhooks & idempotency · fraud controls & risk flags · admin tooling · telemetry, tests, SLOs, costs)*

**Purpose.** Define the money stack for bookings across People and Studios: checkout, fees, credits, payouts, refunds/disputes, and accounting. All artifacts below are **text‑only** for your master Word plan, with **Recommended filename/path** markers for later repo lift‑and‑shift.

## **1.22.1 Canon & invariants**

2139. **Processor:** **Stripe Connect (Express)** for providers/studios. Buyers pay through **PaymentIntents**; platform fees via application fee or separate charges+transfers.
2140. **Bank linking:** default to **Stripe Financial Connections** for ACH; consider **Plaid** only if we need features FinConn/Link don’t cover (e.g., specific institutions, account switch UX constraints).
2141. **Escrow posture:** no true escrow at launch. We either **capture immediately** and **transfer post‑completion** or **authorize then capture** for short holds.
2142. **Idempotency everywhere:** client and server actions that move money must be idempotent.
2143. **Compliance:** Stripe handles KYC for connected accounts and 1099‑K. We never store PAN; only tokens/ids.
2144. **Credits scope:** referral/promo credits reduce **platform fees only** unless a promo explicitly subsidizes subtotal.
2145. **Cost posture:** launch with **cards + Apple/Google Pay**; add ACH when volume justifies ops overhead and delayed funding.

## **1.22.2 Pricing & fee model (baseline)**

- **Buyer pays:** *subtotal* (package + add‑ons) + *buyer_fee* (platform) + taxes (if applicable).
- **Provider receives:** *subtotal* minus Stripe processing (from provider’s share) minus optional **provider take** if we ever use it.
- **Platform receives:** *buyer_fee* (+ optional provider take).
- **Refund/chargeback policy** controls who eats which fees.

**Artifact — fee policy matrix**  
**Recommended path:** *payments/policy/fee-matrix.md*

*- Buyer cancels before provider accepts: Full refund; all fees returned.*  
*- Buyer cancels \>48h after accept: Refund subtotal minus cancellation fee to provider; platform fee refunded.*  
*- No-show: Provider receives minimum guarantee; platform may refund buyer fee at discretion.*  
*- Dispute lost: Full refund; provider payout clawback; platform fee refunded unless provider fraud is proven.*  

## **1.22.3 Data model (Aurora) — orders, intents, transfers, refunds**

**Recommended path:** *db/migrations/022_payments_core.sql*

*begin;*  
  
*create table "order" (*  
*order_id text primary key, -- ord\_...*  
*buyer_user_id text not null,*  
*provider_user_id text not null, -- seller*  
*service_profile_id text not null, -- sp\_...*  
*studio_id text, -- optional, st\_...*  
*currency text not null default 'USD',*  
*subtotal_cents int not null,*  
*buyer_fee_cents int not null, -- platform fee charged to buyer*  
*tax_cents int not null default 0,*  
*credit_applied_cents int not null default 0, -- credits applied to buyer_fee*  
*status text not null check (status in ('draft','authorized','captured','completed','refunded','voided','disputed')),*  
*booking_dt timestamptz,*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
  
*create table payment_intent (*  
*pi_id text primary key, -- pi\_...*  
*order_id text not null references "order"(order_id),*  
*stripe_pi text not null, -- PaymentIntent id*  
*client_secret text not null,*  
*method text not null, -- 'card','ach','wallet'*  
*capture_method text not null check (capture_method in ('automatic','manual')) default 'automatic',*  
*amount_cents int not null,*  
*currency text not null,*  
*status text not null, -- 'requires_payment_method','succeeded','requires_capture','canceled'*  
*last_error text,*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now(),*  
*unique (order_id, stripe_pi)*  
*);*  
  
*create table transfer_ledger (*  
*xfer_id text primary key, -- xfr\_...*  
*order_id text not null references "order"(order_id),*  
*provider_account text not null, -- acct\_... (Stripe Connect)*  
*amount_cents int not null,*  
*currency text not null,*  
*stripe_transfer text, -- tr\_...*  
*status text not null check (status in ('pending','paid','reversed','canceled')),*  
*created_at timestamptz not null default now()*  
*);*  
  
*create table refund_ledger (*  
*refund_id text primary key, -- rfd\_...*  
*order_id text not null,*  
*stripe_refund text,*  
*amount_cents int not null,*  
*reason text not null,*  
*initiator text not null, -- 'buyer','provider','platform','dispute'*  
*created_at timestamptz not null default now()*  
*);*  
  
*commit;*  

Separate from the **credit_ledger** in §1.16 (promos/referrals). Card numbers are never stored—only Stripe ids.

## **1.22.4 Checkout & payment flows**

### **A) Card (default) — immediate capture**

2150. Create **Order (draft)** → compute totals (apply credit to buyer_fee before tax).
2151. Create **PaymentIntent** for *amount = subtotal + buyer_fee + tax − credit_applied*.
2152. Confirm PI (Stripe SDK or server) → on success, **capture now**; set order = *captured*.
2153. **Transfers** occur after completion (e.g., T+24h) or as per policy; platform fee retained.

### **B) Manual capture (short hold)**

- Use *capture_method='manual'* for time‑sensitive bookings. **Authorize now**, **capture on completion** (within Stripe’s hold window). If completion exceeds hold window, re‑authorize or charge immediately with a delayed transfer.

### **C) ACH (Phase 2) — Financial Connections**

- *payment_method_types=\['us_bank_account'\]*; confirm with bank link; longer settlement; transfer **after funds clear**.

**Artifact — GraphQL mutations**  
**Recommended path:** *api/schema/payments.graphql*

*type Order { orderId: ID!, status: String!, amountCents: Int!, currency: String!, clientSecret: String }*  
*input OrderInput { serviceProfileId: ID!, studioId: ID, packageId: ID!, date: AWSDateTime!, addons: \[ID!\], currency: String! }*  
  
*type Mutation {*  
*createOrder(input: OrderInput!): Order!*  
*applyCredit(orderId: ID!, amountCents: Int!): Order!*  
*createPaymentIntent(orderId: ID!, method: String!, capture: String): Order!*  
*confirmOrder(orderId: ID!): Order!*  
*cancelOrder(orderId: ID!, reason: String!): Order!*  
*}*  

## **1.22.5 Stripe Connect onboarding (providers)**

- **Type:** **Express** accounts; Stripe‑hosted onboarding/updates.
- Enable capabilities for payments/transfers; Stripe handles KYC; we reflect verification status in UI (*account.updated* webhooks).
- **Payout schedule:** weekly by default; consider T+1/T+7 policy gates (see §1.22.11).

**Artifact — onboarding link resolver**  
**Recommended path:** *api/resolvers/payments/onboarding.ts*

*export async function createOnboardingLink(userId: string) {*  
*const acct = await lookupOrCreateStripeAccount(userId); // acct\_...*  
*const link = await stripe.accountLinks.create({*  
*account: acct,*  
*refresh_url: \`\${HOST}/onboarding/refresh\`,*  
*return_url: \`\${HOST}/onboarding/return\`,*  
*type: 'account_onboarding'*  
*});*  
*return link.url;*  
*}*  

## **1.22.6 Charges & transfers pattern**

Choose **one** per order for simplicity:

- Destination charge

  - Charge on connected account; include *application_fee_amount*.
  - **Pros:** Simple split; Stripe handles fee. **Cons:** Fewer methods; less transfer timing control.

- **Separate charges & transfers** (recommended)

  - Charge on platform; attach *transfer_group=order_id*; create **Transfer** to provider on completion.
  - **Pros:** Full payout timing control; clean refunds. **Cons:** Platform temporarily carries liability.

## **1.22.7 Webhooks, idempotency & order state machine**

**Listen to:**  
*payment_intent.succeeded*, *payment_intent.payment_failed*, *charge.refunded*, *charge.dispute.created\|closed*, *account.updated*, *transfer.paid\|reversed*, *payout.paid\|failed*.

**Order states:** *draft → authorized? → captured → completed → (refunded\|disputed)*.

**Artifact — webhook handler skeleton**  
**Recommended path:** *apps/functions/stripeWebhook.ts*

*import { verifyStripe } from '../../security/webhooks/verify'; // §1.18.E*  
  
*export const handler = async (evt) =\> {*  
*const sig = evt.headers\['stripe-signature'\];*  
*const raw = Buffer.from(evt.body, 'utf8');*  
*const event = stripe.webhooks.constructEvent(raw, sig, process.env.STRIPE_WEBHOOK_SECRET);*  
  
*switch (event.type) {*  
*case 'payment_intent.succeeded': await onPiSucceeded(event.data.object); break;*  
*case 'payment_intent.payment_failed': await onPiFailed(event.data.object); break;*  
*case 'charge.refunded': await onRefund(event.data.object); break;*  
*case 'charge.dispute.created': await onDispute(event.data.object); break;*  
*case 'charge.dispute.closed': await onDisputeClosed(event.data.object); break;*  
*case 'transfer.paid': await onTransferPaid(event.data.object); break;*  
*}*  
*return { statusCode: 200, body: '{}' };*  
*};*  

**Idempotency store:** record processed *event.id* in Dynamo with TTL; duplicates are no‑ops.

## **1.22.8 Refunds, cancellations & disputes**

- **Refunds**: compute per policy; create Stripe Refunds; write *refund_ledger*. Partial refunds supported.

- **Disputes**: on *charge.dispute.created* → **pause transfer** if pending; if already paid, prepare potential clawback.

  - Evidence pack = messages, deliverables, ToS acceptance, studio confirmations; submit via API or dashboard.
  - On closure: if **lost**, finalize refund ledger; claw back provider payout; if **won**, release reserve/hold.

**Artifact — refund policy JSON (for UI)**  
**Recommended path:** *payments/policy/refund-policy.json*

*{*  
*"before_accept": {"buyer":"100%", "provider":"0%"},*  
*"accepted_gt_48h": {"buyer":"subtotal - cancel_fee", "provider":"cancel_fee"},*  
*"accepted_lt_48h": {"buyer":"partial at platform discretion", "provider":"minimum_guarantee"}*  
*}*  

## **1.22.9 Credits, vouchers & taxes**

- **Credits (referral/promos)** reduce **platform fee** (buyer_fee) only unless promo explicitly subsidizes subtotal.
- If a promo reduces **subtotal**, it’s platform‑funded; treat as **negative revenue** in analytics.
- **Tax** on platform fees depends on jurisdiction; at launch either (a) enable **Stripe Tax** for the fee component, or (b) restrict to jurisdictions where fees are non‑taxable. Provider service tax remains provider’s responsibility at launch; we show guidance.

**Artifact — platform invoice MJML (fee line item)**  
**Recommended path:** *comms/templates/invoice_platform_fee.mjml*  
*(Structure mirrors §1.16 MJML; includes order id, buyer fee, tax (if any), and payment method.)*

## **1.22.10 Payout scheduling & reserves**

- Default **T+1** transfer after completion; **T+7** for new providers until reaching a reputation threshold.
- **Rolling reserve** (e.g., 10% for 30 days) for high‑risk providers (dispute/cancellation rates).
- Manual **hold/release** flags for risk (see §1.22.12); all changes are audited.

**Artifact — payout policy**  
**Recommended path:** *payments/policy/payout-schedule.md*

*- New providers (\<5 completed bookings): T+7*  
*- Verified/Trusted Pro: T+1*  
*- Reserve triggers: dispute rate \>1%, abnormal cancellations, risk flags*  

## **1.22.11 Fraud controls & risk flags (tied to §1.18 / §1.15)**

- Signals: rapid multi‑card attempts, device fingerprint mismatch, same IP across multiple buyers, new provider with unusually high prices, excessive outbound messages/spam.
- Actions: enforce **3DS** on high‑risk cards, **manual review** holds, increase **reserve**, delay transfer until IDV passes.
- Every decision is written to the **immutable audit** trail (see §1.18.H).

## **1.22.12 Reconciliation — ledgers & analytics lake**

**Bronze**: raw webhook dumps + Stripe balance transactions → S3.  
**Silver**: normalized facts: *fact_payments*, *fact_transfers*, *fact_refunds*, *fact_payouts* joined by *order_id*/*transfer_group*.  
**Gold**: revenue dashboards (by city/role), take‑rate, dispute rate, net provider earnings.

**Artifact — reconciliation SQL (Silver build)**  
**Recommended path:** *data/sql/recon_build.sql*

*CREATE OR REPLACE TABLE fact_payments AS*  
*SELECT o.order_id, p.stripe_pi, bt.id as balance_tx, bt.amount, bt.fee, bt.net, bt.created*  
*FROM stripe_balance_tx bt*  
*JOIN payment_intent p ON bt.source = p.stripe_pi*  
*JOIN "order" o ON o.order_id = p.order_id;*  
  
*CREATE OR REPLACE TABLE fact_transfers AS*  
*SELECT t.order_id, t.stripe_transfer, bt.amount, bt.fee, bt.net, bt.created*  
*FROM stripe_balance_tx bt*  
*JOIN transfer_ledger t ON bt.source = t.stripe_transfer;*  

**Dashboards:** revenue by city/role, average booking value, platform take‑rate, refunds %, disputes %, payout SLA compliance.

## **1.22.13 Admin finance console**

- Search orders by id/email; view PI/charge; see transfers; issue refunds; apply holds/releases; apply credits; upload dispute evidence.
- **Audit trail** for every action (immutable table; see §1.18.H).
- **Access:** OIDC Admin role only; irreversible actions require two‑step confirmation.

**Artifact — admin GraphQL**  
**Recommended path:** *api/schema/payments.admin.graphql*

*type PaymentAdmin {*  
*orderId: ID!, stripePi: String, amountCents: Int!, currency: String!,*  
*status: String!, providerAccount: String, transfers: \[Transfer!\]!, refunds: \[Refund!\]!*  
*}*  
*type Transfer { xferId: ID!, stripeTransfer: String, amountCents: Int!, status: String! }*  
*type Refund { refundId: ID!, stripeRefund: String, amountCents: Int!, reason: String! }*  
  
*extend type Query {*  
*adminGetOrder(orderId: ID!): PaymentAdmin! @auth(role: "admin")*  
*}*  
*extend type Mutation {*  
*adminRefund(orderId: ID!, amountCents: Int!, reason: String!): Boolean! @auth(role: "admin")*  
*adminHoldPayout(orderId: ID!, reason: String!): Boolean! @auth(role: "admin")*  
*adminReleasePayout(orderId: ID!): Boolean! @auth(role: "admin")*  
*}*  

## **1.22.14 Telemetry, SLOs & cost**

- **Events:** *checkout.start\|confirm\|success\|fail*, *refund.create*, *dispute.open\|won\|lost*, *transfer.create\|paid*, *payout.paid\|failed*.
- **KPIs:** checkout conversion, authorization/capture rates, refund %, dispute %, T+N transfer SLA, webhook latency.
- **SLOs:** payment success p50 ≥ **96% (cards)**; webhook processing p95 ≤ **2s**; transfer execution after completion p95 ≤ **15m**; D+1 reconciliation completeness by **08:00 UTC**.
- **Cost posture:** Stripe only at launch; **ACH** only when volume justifies; no third‑party fraud SaaS initially—rely on Stripe Radar + our risk flags; serverless webhooks & nightly reconciliation to keep compute low.

## **1.22.15 Test plan**

2179. Card happy path (with/without credits), receipts.
2180. Manual capture (authorize, capture/void) path.
2181. Refunds (full/partial) per policy; credits re‑application logic.
2182. Disputes lifecycle (open → evidence → closed win/loss) and payout clawback/release.
2183. ACH flow (when enabled): settlement timing; transfer after funds clear.
2184. Webhooks idempotency: replay same *event.id* → no duplicate effects.
2185. Reconciliation: balance transactions vs ledgers; variance ≤ \$0.01 per order.
2186. Risk: forced 3DS; rate‑limit card attempts; apply reserve.

## **1.22.16 Work packages (Cursor 4‑agent lanes)**

- **Agent A — Buyer Checkout & Credits:** PI creation/confirm, credits application, receipts, error handling.
- **Agent B — Provider Onboarding & Payouts:** Connect Express flow, payout schedule/reserves, transfer logic, statements.
- **Agent C — Webhooks & Reconciliation:** webhook lambdas + idempotency, ledgers, daily Stripe exports, Silver model & dashboards.
- **Agent D — Admin & Risk:** finance console, refunds/holds/releases, dispute evidence packs, risk flagging & decisions.

## **1.22.17 Acceptance criteria — mark §1.22 FINAL only when ALL true**

2191. Checkout supports cards (Apple/Google Pay where available); credits apply to **buyer_fee** only; orders reach *captured*.
2192. Provider onboarding via Connect Express; payouts scheduled per policy; reserves supported.
2193. Webhooks idempotent; state machine transitions correct; clawbacks/holds work.
2194. Refunds/disputes complete end‑to‑end with accurate ledger entries and communications.
2195. **Separate charges & transfers** implemented with controllable transfer timing; reconciliation (Silver) runs without variances.
2196. Admin console (role‑gated) supports refund/hold/release & evidence; all actions audited.
2197. KPIs/SLOs measured with alerts; D+1 reconciliation completes by **08:00 UTC**.
2198. Costs within launch budgets; ACH deferred until justified.

# **§1.23 — Messaging, Inbox & Collaboration (Technical Spec)**

**Scope:** This section implements the non‑technical “SubSection 1.4 — Messaging, Inbox & Collaboration UX” in full technical detail (objects, flows, folders, filters, credits, action cards, safety controls). The non‑technical goals include role‑aware & booking‑aware threads, a single source of truth for chat + project context, respectful fast communication (receipts, templates), and strong safety/anti‑circumvention tooling, including report/block and rate limits.

NonTechBlueprint

In addition, Trust & Safety requires Safe‑Mode behavior on previews, reporting flows, escalation, and harassment/doXXing protections that also apply inside messaging.

NonTechBlueprint_Part3

## **1.23.1 Canon & Invariants**

- **Role‑aware, Booking‑aware:** Every thread is anchored to a **Role Context** (service profile) and, when applicable, a **Booking**. This mirrors the non‑tech “Roleaware & Bookingaware” principle.

NonTechBlueprint

- **Single source of truth:** Messages + structured **Project Panel** context (package, schedule, call sheet, contracts, deliverables, extras, payments) co‑exist in the thread.

NonTechBlueprint

- **Structured “Action Cards”:** time proposals/reschedules, add‑ons, overtime, proofs/finals, approvals, expense receipts, mark‑completed, open dispute, share location, safety flag—sent as typed, machine‑readable cards.

NonTechBlueprint

- **Message Requests & Credits:** First‑time contacts land in **Requests**; users can **Accept/Decline/Block**. New conversation **credits** throttle cold outreach; replies and booking‑thread messaging remain unlimited. Contact filters (ID‑verified only, budget disclosed, date provided) are enforced before a message can be sent.

NonTechBlueprint

- **Safety & Policy:** Prominent **Report/Block**, rate limits, spam detection, and PII redaction tools for support are required. Messaging must respect Safe‑Mode on previews and use the policy escalation flows.

NonTechBlueprint_Part3

- **Privacy:** No sensitive EXIF by default on uploads; redactable message copies for legal/dispute workflows.
- **Cost posture:** Serverless realtime (AppSync + DynamoDB + S3 + Lambda) with pay‑per‑use; Typesense (shared) for message search snippets.

## **1.23.2 Data Model**

We follow the non‑tech “Objects (data model at a glance)”—**Thread**, **Message**, **Attachment**, and **Project**—while adding normalized/denormalized details to meet performance and safety requirements.

NonTechBlueprint

### **1.23.2.1 DynamoDB (primary, realtime path)**

**Table:** ***msg_threads*** **(PK =** ***threadId*****, SK = constant)**  
Attributes:

- *threadId* (string, *th\_…*) **PK**
- *type* (enum: *INQUIRY\|INVITE\|BOOKING\|DISPUTE\|SYSTEM*) — non‑tech “Type” list.

NonTechBlueprint

- *roleContext* (string enum: *Model\|Photographer\|Videographer\|Creator* etc.) — as per service profile role.

NonTechBlueprint

- *participants* (\[userId\])
- *bookingId* (nullable)
- *status* (enum: *OPEN\|AWAITING_REPLY\|PENDING_DECISION\|CONFIRMED\|COMPLETED\|DISPUTED\|ARCHIVED*) — mirrors non‑tech.

NonTechBlueprint

- *lastMessageAt* (epoch ms), *unreadCountByUser* (map), *lastSenderId*
- *requestState* (enum: *REQUESTS\|ACCEPTED\|DECLINED*)
- *safetyFlags* ({blockedUserIds:\[\], mutedUserIds:\[\], tnsFlags:\[\]})
- *projectSnapshot* (summary subset for right‑pane Project Panel—see below)

**Table:** ***msg_messages*** **(PK =** ***threadId*****, SK =** ***ts#\<epoch\>#\<rand\>*** **for ordering)**  
Attributes:

- *threadId* (string) **PK**, *msgKey* (string) **SK**
- *messageId* (*m\_…*), *senderId*, *ts* (epoch ms)
- *kind* (enum: *TEXT\|ATTACHMENT\|ACTION\|SYSTEM\|STATE*)
- *content* (JSON; text markdown subset for *TEXT*)
- *attachments* (\[{*key*,*mime*,*bytes*,*hash*,*thumbKey*}\]) — presigned S3 keys
- *action* (nullable Action Card payload; see §1.23.6)
- *stateChange* ({*type*: *READ\|DELIVERED\|TYPING_ON\|TYPING_OFF*, *targets*:\[userId\]})
- *safeModeBand* (int *0\|1\|2* for preview gating)
- *spamScore* (float), *policyTags* (\[*HARASSMENT\|DOXXING\|NSFW*…\]) — for triage routing.

NonTechBlueprint_Part3

- GSIs:

  - *gsiUserThreads* (PK=*userId*, SK=*lastMessageAt* desc) for inbox list
  - *gsiSearch* (PK=*threadId*, SK=*textIndex*) optional if we keep Typesense as the search frontend

### **1.23.2.2 Aurora (relational join & analytics)**

**Tables:**

- thread_index(thread_id pk, booking_id, role_context, created_at)
- message_audit(message_id pk, thread_id fk, sender_id, ts, kind, safe_band, policy_tags)
- *message_credit_ledger(user_id, period, granted, spent, carryover)* — supports “New conversation credits (monthly) … Unlimited replies in existing threads.”

NonTechBlueprint

Rationale: DynamoDB handles hot paths (inbox reads, message fan‑out). Aurora preserves joins with bookings/contracts and provides durable audit/reporting.

## **1.23.3 GraphQL Schema (AppSync)**

**Recommended path:** *api/schema/messaging.graphql*

*enum ThreadType { INQUIRY INVITE BOOKING DISPUTE SYSTEM }*  
*enum ThreadStatus { OPEN AWAITING_REPLY PENDING_DECISION CONFIRMED COMPLETED DISPUTED ARCHIVED }*  
*enum MessageKind { TEXT ATTACHMENT ACTION SYSTEM STATE }*  
  
*type Thread {*  
*threadId: ID!*  
*type: ThreadType!*  
*roleContext: String!*  
*participants: \[ID!\]!*  
*bookingId: ID*  
*status: ThreadStatus!*  
*lastMessageAt: AWSDateTime!*  
*unreadCount: Int!*  
*project: ProjectPanel*  
*requestState: String*  
*}*  
  
*type Message {*  
*messageId: ID!*  
*threadId: ID!*  
*senderId: ID!*  
*ts: AWSDateTime!*  
*kind: MessageKind!*  
*text: String*  
*attachments: \[Attachment!\]*  
*action: ActionCard*  
*}*  
  
*type Attachment { key: String!, mime: String!, bytes: Int!, thumbKey: String }*  
*type ProjectPanel {*  
*packageId: ID*  
*schedule: AWSJSON*  
*location: AWSJSON*  
*callSheet: AWSJSON*  
*contracts: \[ID!\]*  
*deliverables: AWSJSON*  
*payments: AWSJSON*  
*}*  
  
*union ActionCard = ProposeTime \| Reschedule \| AddExtras \| Overtime \| UploadProofs \| RequestApproval \| ExpenseReceipt \| MarkCompleted \| OpenDispute \| ShareLocation \| SafetyFlag*  
*type ProposeTime { start: AWSDateTime!, end: AWSDateTime!, timezone: String! }*  
*type Reschedule { reason: String!, options: \[ProposeTime!\]! }*  
*type AddExtras { items: \[ExtraInput!\]! }*  
*input ExtraInput { sku: ID!, qty: Int! }*  
*type Overtime { minutes: Int!, rateCents: Int! }*  
*type UploadProofs { files: \[Attachment!\]! }*  
*type RequestApproval { assetIds: \[ID!\]!, due: AWSDateTime }*  
*type ExpenseReceipt { amountCents: Int!, memo: String!, attachment: Attachment }*  
*type MarkCompleted { note: String }*  
*type OpenDispute { reason: String!, detail: String }*  
*type ShareLocation { lat: Float!, lon: Float!, until: AWSDateTime }*  
*type SafetyFlag { category: String!, note: String }*  
  
*type Query {*  
*inbox(folder: String, after: String, limit: Int = 30): \[Thread!\]!*  
*thread(threadId: ID!): Thread!*  
*messages(threadId: ID!, after: String, limit: Int = 50): \[Message!\]!*  
*}*  
  
*type Mutation {*  
*startConversation(toUserId: ID!, roleContext: String!, bookingId: ID, firstMessage: String!): Thread!*  
*sendMessage(threadId: ID!, kind: MessageKind!, text: String, attachments: \[AttachmentInput!\], action: AWSJSON): Message!*  
*setTyping(threadId: ID!, on: Boolean!): Boolean!*  
*markRead(threadId: ID!, upToTs: AWSDateTime!): Boolean!*  
*acceptRequest(threadId: ID!): Boolean!*  
*declineRequest(threadId: ID!, reason: String): Boolean!*  
*blockUser(userId: ID!, reason: String): Boolean!*  
*reportMessage(messageId: ID!, reason: String!, detail: String): Boolean!*  
*}*  
  
*input AttachmentInput { key: String!, mime: String!, bytes: Int!, thumbKey: String }*  
*type Subscription {*  
*onThreadEvent(threadId: ID!): Message! @aws_subscribe(mutations: \["sendMessage"\])*  
*}*  

**Mapping:** Types, statuses, and action cards mirror the non‑tech definitions and project panel contents.

NonTechBlueprint

## **1.23.4 Realtime Delivery, Receipts & Typing**

- **Transport:** AppSync subscriptions (WebSocket).
- **Delivery states:** server writes *DELIVERED* state‑messages for recipients online; **read‑receipts** are explicit *markRead()* mutations that upsert *STATE* messages for *READ*. This maps to “sent ✓, delivered ✓✓, read ✓✓ filled.”

NonTechBlueprint

- **Typing:** ephemeral *STATE TYPING_ON/OFF* messages with TTL (15s), not persisted in Aurora.

**Lambda fan‑out:** Kinesis stream from *msg_messages* → Lambda → push (Pinpoint) when user offline; quiet hours respected (§1.20).

## **1.23.5 Message Requests, Credits & Contact Filters**

- **Requests:** First‑time contacts to a user route to *REQUESTS* until accepted; the inbox shows a separate **Requests** folder. Accept moves to normal inbox; Decline keeps a passive block entry.

NonTechBlueprint

- Credits:

  - Ledger *message_credit_ledger* grants **monthly “new conversation” credits** (amount configurable). Spending 1 credit allows *startConversation*. **Replies** do not consume credits; **booking threads** are exempt (unlimited).

NonTechBlueprint

- **Contact filters:** Enforce per recipient settings: **ID‑verified only**, **budget disclosed**, **date provided**. If unmet, present an **Action Card** form to collect missing fields before allowing send.

NonTechBlueprint

## **1.23.6 Action Cards (Structured Forms in Chat)**

Implements the non‑tech Action Cards list and ensures cards trigger the right domain workflows (booking update, add‑on, dispute, etc.).

NonTechBlueprint

- **ProposeTime/Reschedule:** writes a pending booking change request; recipient can **Accept/Counter/Decline** → updates booking schedule.
- **AddExtras/Overtime:** creates draft **order adjustments** (subtotal delta) and posts a summary; acceptance updates the order and, if needed, collects additional payment (ties to §1.22).
- **UploadProofs/RequestApproval:** uploads to S3 proofs bucket; approval marks deliverables accepted; denial loops with comments.
- **ExpenseReceipt:** attaches expense and moves to project finance view.
- **MarkCompleted:** flips booking state and triggers transfer scheduling (per §1.22).
- **OpenDispute:** creates a **DISPUTE** thread subtype and generates a finance hold.
- **ShareLocation:** ephemeral card visible until *until* timestamp.
- **SafetyFlag:** routes to T&S queue with policy tags.

**Validation:** JSON Schemas per card under *messaging/action-cards/\*.schema.json*.

## **1.23.7 Attachments & Previews (S3 + Safe‑Mode)**

- **Direct‑to‑S3** presigned PUTs; client‑side resize; max size/polices from §1.18.G.
- **Virus/NSFW scans** on ingest; thumbnails stored; raw files retained per user choice (privacy).
- **Safe‑Mode:** previews in **inbox list** and **message bubbles** are SFW thumbnails when Safe‑Mode is ON; full‑res only after user opts into Safe‑Mode OFF + verified age. This follows public‑surface policy but applies to messaging previews too.

NonTechBlueprint_Part3

## **1.23.8 Inbox Folders, Filters & Search**

- **Folders:** All, Unread, Starred, Inquiries, Invites, **Bookings**, **Disputes**, Archived, Spam—exactly as in non‑tech.

NonTechBlueprint

- **Filters:** by Role, Status (Awaiting reply, Payment pending), City/Date, Has files—mirror non‑tech.

NonTechBlueprint

- **Thread bundles:** group by counterparty with role‑scoped subthreads—matches “bundles” description.

NonTechBlueprint

- **Search:** Typesense index of message excerpts + thread metadata; respect Safe‑Mode; exclude blocked users’ content unless searching within the thread.

## **1.23.9 Spam Controls, Rate Limits & Safety**

- **Rate limits:** per‑user token bucket: new‑conversation starts (credits + per‑hour cap), per‑thread send QPS, attachment size caps; Requests folder protected by stricter per‑sender gates.
- **Spam detection:** rules + lightweight ML: rapid multi‑thread outreach, repeated phrases/links, reputation signals.
- **Report/Block:** one‑tap from thread header; **block** stops delivery both ways; **report** files a T&S case with evidence bundles and policy tags (harassment, doxxing, illegal).

NonTechBlueprint_Part3

- **PII redaction (support‑side tool):** hide phone/email/addresses from public copies when necessary.

NonTechBlueprint_Part3

- **Enforcement:** auto‑muting, temporary holds, escalation to T&S lead for severe harms with legal hand‑off.

NonTechBlueprint_Part3

## **1.23.10 Notifications (Email/Push) & Quiet Hours**

- **Triggers:** new message, acceptance from Requests, action‑card responses, approvals, dispute events.
- **Channel policy:** no 18+ previews; **quiet hours** by recipient timezone; daily caps for non‑booking messages.
- **Unsubscribe controls:** per thread & per category.

## **1.23.11 Project Panel (Right‑Pane) Data**

- **Snapshot** of package/extras, schedule, location, participants, moodboard, shot list, call sheet, contracts, deliverables, milestones, expenses, payments, travel, notes—surfaced read‑only in the message view; edits flow through the appropriate action cards or project screens.

NonTechBlueprint

## **1.23.12 Error Taxonomy (client‑safe)**

- *REQUESTS_REQUIRED*, *CREDITS_EXHAUSTED*, *CONTACT_FILTER_UNMET*, *SAFE_MODE_BLOCKED*, *ATTACHMENT_TOO_LARGE*, *UNSUPPORTED_TYPE*, *RATE_LIMITED*, *OFFLINE_RETRYING*.

## **1.23.13 Observability & Telemetry**

- **Events:** *msg.thread.open*, *msg.start*, *msg.send*, *msg.delivered*, *msg.read*, *msg.attachment.upload*, *msg.action.submit/accept/decline*, *msg.report*, *msg.block*.
- **KPIs:** response time, response rate, request acceptance rate, booking conversion from thread, dispute rate, spam flag rate, reversal rate after appeal.
- **SLOs:** p95 send‑to‑deliver \< 600 ms; p95 initial inbox load \< 300 ms; push delivery \< 10 s.

## **1.23.14 Cost & Scale Posture**

- **DynamoDB** on‑demand at launch; auto‑scales; write units sized from expected messages/day.
- **AppSync** pay‑per‑connection; set connection idle timeouts; compress payloads.
- **S3** for attachments; lifecycle transition to IA after 30–90 days; delete thumbnails if threads archived (configurable).
- **Typesense** reuse cluster (shared with search) for message snippets; cap stored fields.

## **1.23.15 Security, Privacy & Retention**

- **Privacy by default:** EXIF stripped unless opted‑in for studio proofs.
- **Retention:** operational retention 18 months; **legal hold** for disputes; aggregated analytics retained indefinitely.
- **Access controls:** only participants + admins (read‑only, case‑based) can view thread content; all admin views are audited.

## **1.23.16 Test Plan**

2270. **Requests flow:** first‑time contact → Request → Accept/Decline/Block; credits decremented only on start.
2271. **Contact filters:** enforce ID‑verified only / budget / date gates; action card collection when missing.

NonTechBlueprint

2272. **Realtime:** send/deliver/read receipts & typing; offline → push → deep link opens thread.
2273. **Action cards:** each card validates, triggers domain updates (booking, billing), and shows consistent state.

NonTechBlueprint

2274. **Attachments:** upload (size/type), virus/NSFW scan, Safe‑Mode previews.

NonTechBlueprint_Part3

2275. **Spam/rate limits:** token bucket & ML thresholds; false‑positive appeal flows.

NonTechBlueprint_Part3

2276. **Search:** snippets return; Safe‑Mode respected; blocked users excluded.
2277. **A11y & i18n:** keyboard navigation, screen reader labels, RTL layouts; localized time/number formatting (§1.19).
2278. **Perf:** inbox P95 \< 300 ms; thread open P95 \< 400 ms; send‑to‑deliver P95 \< 600 ms.

## **1.23.17 Work Packages (Cursor 4‑agent lanes)**

- **Agent A — Backend & Realtime:** AppSync schema/resolvers, Dynamo tables/GSIs, Kinesis fan‑out, receipts/typing, idempotency.
- **Agent B — Web/App UI:** Inbox folders & filters, thread view, Project Panel (read‑only), Requests gate, credits UX, attachments.
- **Agent C — Action Cards & Booking/Billing Bridges:** card schemas, mutations → booking & payments, approvals, disputes, expense receipts.
- **Agent D — Safety & Observability:** report/block tooling, spam/rate rules, Safe‑Mode previews, audit logs, metrics/KPIs dashboards.

## **1.23.18 Acceptance Criteria — mark §1.23 FINAL only when ALL true**

2283. Threads are **role‑aware** and **booking‑aware**; Requests/Accept/Decline/Block work; credits apply only to **new** conversations; replies/booking threads unrestricted.

NonTechBlueprint

NonTechBlueprint

2284. Action Cards (time, reschedule, add‑ons, overtime, proofs/approvals, expense, mark‑completed, dispute, share location, safety flag) function end‑to‑end and update bookings/orders where applicable.

NonTechBlueprint

2285. Realtime delivery, receipts, and typing work; offline users receive push within SLO; deep links open the right thread.
2286. Attachments upload/scan successfully; Safe‑Mode previews are enforced in inbox and bubbles; no 18+ in notifications.

NonTechBlueprint_Part3

2287. Inbox folders/filters/bundles and search behave as specified; blocked users are hidden; Safe‑Mode is respected.

NonTechBlueprint

2288. Spam/rate limits and report/block flows operate with audit trails; T&S escalation pipeline functions.

NonTechBlueprint_Part3

2289. Perf SLOs met; costs within budget; retention and privacy rules active.

# **§1.24 — Studios & Spaces (Listings, Booking Widget, Host Ops, Reviews) — Full Technical Spec**

*(implements the non‑technical “Studios/Spaces” blueprint: Quick Facts, Amenities, Rules & Policies, Availability & Pricing, Booking Widget, Reviews & Reputation, Host Create/Edit Wizard, Host Dashboard & Operations, ICS export, privacy of address, and “Pair with Talent” cross‑module links).*

NonTechBlueprint

NonTechBlueprint

**What this delivers:** A complete “space marketplace” that lets hosts list studios/locations, buyers browse and book time‑based slots with min‑hours/buffers, handle deposits/house rules, coordinate in Messaging, and leave verified reviews. Address privacy and door‑code sharing are respected; the widget can link into a people‑booking flow (Linked Booking Group).

NonTechBlueprint

## **1.24.1 Objectives & Scope**

- **Public listing pages** showing: **Quick Facts** (size, ceiling height, daylight orientation, power), **Amenities** chips, **Rules & Policies**, **Availability** (hourly slots with min hours and buffers), **Pricing** (per‑hour, cleaning fee, examples), **Host** stats, **Location** (approximate map only, exact address released post‑booking), and **Reviews**.

NonTechBlueprint

- **Booking Widget** that enforces min hours/buffers, collects crew size, attaches Smart Docs (Property/Space Release + House Rules) to checkout, supports **deposit holds**, and differentiates **Instant Book** vs **Request to book**.

NonTechBlueprint

- **Host Create/Edit Wizard & Dashboard**: content, amenities, rules, pricing/schedule, IB toggle, deposit settings, verification, calendar ops, ICS export, and post‑booking adjustments (overtime/crew overage/violations).

NonTechBlueprint

- **Reviews & Reputation (space‑scoped)** with owner reply, filters, and reputation breakdowns; signals flow to Search (§1.21).

NonTechBlueprint

- **Cross‑module links**: “**Pair with Talent**” chips prefilter People search for the same date/city (deep‑link).

NonTechBlueprint

## **1.24.2 Architecture (cost‑savvy, elastic)**

- **Frontend (web + RN):** Next.js + Amplify Gen 2 (SSR for listing pages for SEO), React Native screens for mobile booking & host ops.
- **API layer:** AppSync GraphQL.
- **Canonical data store:** **Aurora PostgreSQL** for listings, rules, pricing tiers, schedules, and reviews (we need rich filtering/sorting and transactional edits).
- **Search:** **Typesense** index (title, neighborhood, amenity facets, price ranges, availability summaries, rating).
- **Media:** S3 + CloudFront; image transforms via Lambda (thumbs), with guidelines for minimum gallery set.

NonTechBlueprint

- **Availability & booking:** use the same booking/order pipeline defined in §1.12/§1.13 and payments in §1.22; widget emits a **space‑line item** with min‑hours and fee components.
- **Docs:** Smart Docs service (Property/Space Release, House Rules) injected at checkout and stored with the order.

NonTechBlueprint

- **Deposit holds:** Stripe authorization only, as labeled in the widget; captured only if a post‑booking violation is logged.

NonTechBlueprint

- **Location:** AWS Location Service for geocoding + approximate map render; precise address gated to post‑booking.

NonTechBlueprint

- **Calendars:** ICS export for host calendars; inbound full two‑way sync is Phase 2 (optional).

NonTechBlueprint

## **1.24.3 Data Model (Aurora PostgreSQL + S3)**

**Tables (schema** ***spaces*****)**

- *space* (pk *space_id*, owned by *host_user_id*): *title*, *neighborhood*, *lat_approx*, *lon_approx*, *capacity*, *size_sqft*, *ceiling_height_ft*, *daylight_orientation*, *power_notes*, *status*, *published_at*. **Quick Facts** fields mirror the non‑tech spec.

NonTechBlueprint

- *space_media* (*space_id*, *media_id*, *type*, *s3_key*, *ordinal*) — **min 6** with recommended shots list (exterior, cyc, makeup/dressing, load‑in path, restrooms).

NonTechBlueprint

- *space_amenity* (*space_id*, *amenity_code*, *detail_json*) — amenity chips + details (e.g., cyc dimensions).

NonTechBlueprint

- *space_rule* (*space_id*, *rule_code*, *value_bool*, *value_text*) — noise, shoes, pets, food, **surveillance disclosure (required)**, crew limits, hazard toggles (strobe/haze/open flame/ladder).

NonTechBlueprint

- *space_pricing* (*space_id*, *currency*, *price_per_hour_cents*, *min_hours*, *cleaning_fee_cents*, *buffer_before_min*, *buffer_after_min*) — widget computes example totals; buffers enforced.

NonTechBlueprint

- *space_availability_slot* (*space_id*, *weekday*, *start_minute*, *end_minute*, *effective_from*, *effective_to*, *is_blocked*) — **hourly slots** with min hours and buffers.

NonTechBlueprint

- *space_deposit_policy* (*space_id*, *hold_cents*, *hold_currency*) — “authorization only” label in widget.

NonTechBlueprint

- *space_verification_lite* (*space_id*, *status*, *evidence_doc_s3*, *ocr_json*, *place_match_score*, *badge_visible*) — **Studio Lite** verification; on pass, badge available and can gate IB if policy requires.

NonTechBlueprint

- *space_review* (*review_id pk*, *space_id*, *author_user_id*, *rating_int*, *body*, *has_photos*, *created_at*, *is_verified_booking*) — verified booking reviews labeled; owner **one reply** allowed.

NonTechBlueprint

- *space_reputation* (*space_id*, *score_float*, *volume*, *reliability*, *responsiveness*, *verification*, *recency*) — breakdown as described.

NonTechBlueprint

- *space_listing_link* (*space_id*, *linked_people_profile_id*) — supports “**Pair with Talent**” deep‑linking.

NonTechBlueprint

- *space_booking_policy* (*space_id*, *instant_book_enabled_bool*, *ib_guardrail_reason*) — IB guardrails per city/feature flags as needed (ties to §3.9 ops).

NonTechBlueprint

**S3 prefixes**

- *spaces/{spaceId}/media/…* (images/video), *spaces/{spaceId}/docs/…* (rules PDF snapshot, verification docs), *spaces/{spaceId}/doorcode.txt* (encrypted at rest, shared only post‑booking).

**Typesense collection** *spaces_public*  
Fields: *title*, *city*, *neighborhood*, amenity facets, price/hour (ranges), rating, **availability summaries** for a look‑ahead window.

## **1.24.4 GraphQL Schema (selected)**

*(file: api/schema/spaces.graphql)*

*type Space {*  
*id: ID!*  
*title: String!*  
*neighborhood: String*  
*quickFacts: QuickFacts!*  
*amenities: \[Amenity!\]!*  
*rules: \[Rule!\]!*  
*pricing: Pricing!*  
*availability: \[AvailabilityWindow!\]!*  
*media: \[Media!\]!*  
*reputation: Reputation*  
*host: HostSummary!*  
*locationPreview: LocationPreview! \# approximate map only*  
*reviews(page: Int = 1): \[SpaceReview!\]!*  
*linkedTalent: \[ID!\] \# people profile ids*  
*instantBookEnabled: Boolean!*  
*}*  
  
*type QuickFacts { sizeSqft: Int, ceilingHeightFt: Float, daylightOrientation: String, powerNotes: String }*  
*type Amenity { code: String!, detail: AWSJSON }*  
*type Rule { code: String!, valueBool: Boolean, valueText: String }*  
*type Pricing { currency: String!, pricePerHourCents: Int!, minHours: Int!, cleaningFeeCents: Int, bufferBeforeMin: Int, bufferAfterMin: Int }*  
*type AvailabilityWindow { weekday: Int!, startMinute: Int!, endMinute: Int!, effectiveFrom: AWSDate, effectiveTo: AWSDate, blocked: Boolean! }*  
*type Media { id: ID!, type: String!, url: AWSURL!, thumbUrl: AWSURL! }*  
*type Reputation { score: Float!, volume: Int!, reliability: Float, responsiveness: Float, verification: Float, recency: Float }*  
*type HostSummary { userId: ID!, avatarUrl: AWSURL, responseStats: AWSJSON, otherListings: Int! }*  
*type LocationPreview { latApprox: Float!, lonApprox: Float! }*  
  
*type SpaceReview { id: ID!, authorUserId: ID!, rating: Int!, body: String!, hasPhotos: Boolean!, createdAt: AWSDateTime!, verifiedBooking: Boolean!, ownerReply: String }*  
  
*input SpaceFilter {*  
*city: String, neighborhood: String, priceMin: Int, priceMax: Int, amenityCodes: \[String!\], minCeilingFt: Float*  
*availableOn: AWSDateTime, durationHours: Int*  
*}*  
  
*type Query {*  
*searchSpaces(filter: SpaceFilter!, page: Int = 1): \[Space!\]!*  
*space(id: ID!): Space!*  
*}*  
  
*input SpaceDraftInput { ... } \# wizard fields (title, media, amenities, rules, pricing, availability)*  
*input BookingWidgetInput { spaceId: ID!, start: AWSDateTime!, durationHours: Int!, crewSize: Int!, acceptDocs: Boolean!, requestInstant: Boolean }*  
  
*type Mutation {*  
*createSpaceDraft(input: SpaceDraftInput!): ID! \# returns spaceId*  
*publishSpace(spaceId: ID!): Boolean!*  
*updateSpace(spaceId: ID!, patch: AWSJSON!): Boolean!*  
*setInstantBook(spaceId: ID!, enabled: Boolean!): Boolean!*  
*makeBookingForSpace(input: BookingWidgetInput!): ID! \# returns bookingId; enforces min hours/buffers and deposit hold*  
*leaveSpaceReview(spaceId: ID!, rating: Int!, body: String!, photos: \[ID!\]): Boolean!*  
*ownerReplyToReview(reviewId: ID!, body: String!): Boolean!*  
*}*  

**Notes:**

- *makeBookingForSpace* creates a **space line item** and injects **Property/Space Release + House Rules** into checkout. Deposit hold metadata is included in the payment intent (Stripe auth‑only).

NonTechBlueprint

- Address secrecy: only *LocationPreview* is public; the exact address and door code are revealed in the **booking detail** after confirmation.

NonTechBlueprint

## **1.24.5 Booking Widget (UI & validation)**

- **Inputs:** date/time, duration (≥ min hours; fit within available slots after **buffer hints**), crew size (drives overage tiers), optional cleaning fee toggle (auto‑applied when required).

NonTechBlueprint

- **Docs preview badges:** clearly show **House Rules** and **Property/Space Release** (“signed at checkout”).

NonTechBlueprint

- **Deposit hold:** label as **authorization only** with exact amount prior to submit.

NonTechBlueprint

- **IB vs Request:** if IB → immediate booking; else **host must accept within SLA** (configurable ops flag).

NonTechBlueprint

- **Linked Booking Group:** if user arrived from talent checkout, show “This studio will be added to your shoot checkout.”

NonTechBlueprint

## **1.24.6 Reviews & Reputation (space‑scoped)**

- **Verified booking reviews** are labeled; **owner** may reply once; filters: Most recent / Highest / Lowest / **With photos**.

NonTechBlueprint

- **Reputation score** shows breakdown (volume/reviews, reliability, responsiveness, verification, recency). Signals flow to Search ranking (§1.21).

NonTechBlueprint

- **Anti‑gaming:** content policy filters and appeals follow §1.19/§T&S.

NonTechBlueprint

## **1.24.7 Host Create/Edit Wizard (end‑to‑end)**

- Basics → Media → Amenities → Rules → Pricing & Schedule → Deposits & Docs → Verification Lite → Review & Publish.
- **Verification Lite**: upload lease/utility/biz doc → OCR (Textract) + geocode/place match; on pass, **Verified Studio** badge; **IB** may require this badge per ops policy.

NonTechBlueprint

- Post‑publish checklist: **Add slots**, **Pass Studio Lite**, **Link to People profile(s)**, **Add Case Study**.

NonTechBlueprint

## **1.24.8 Host Dashboard & Operations**

- **Calendar:** hourly grid; block/unblock, view IB windows; **ICS export**.

NonTechBlueprint

- **Bookings list:** upcoming/past; status; **check‑in/out**; overtime flags.

NonTechBlueprint

- **Booking detail:** timeline, messages, docs, **share access (door code)**, **Post‑Booking Adjustments** (overtime/crew overage/violation) → creates order deltas and can capture deposit.

NonTechBlueprint

## **1.24.9 Search & “Pair with Talent” Links**

- Studio listing pages show “**Pair with Talent**” chips that open a People search prefiltered for the same **date/city** (deep link carrying the availability window).

NonTechBlueprint

- Typesense facets: amenity codes, price bands, min ceiling height, city, rating; availability pseudo‑facet generated daily.

## **1.24.10 Privacy, Policy & Safety**

- **Approximate map** only; release exact address post‑booking.

NonTechBlueprint

- **Rules & hazards** (strobe/haze/open flame/ladder) flagged and visible.

NonTechBlueprint

- **House Rules** & **Release** are signed in checkout; violations enable **deposit capture** with evidence.

NonTechBlueprint

- **Content moderation:** listing media expectations (min set, recommended shots) and public‑surface policy (Safe‑Mode as applicable) follow §T&S.

NonTechBlueprint_Part3

## **1.24.11 Notifications & ICS**

- **Host notifications:** new booking request, IB confirmation, schedule change, deposit capture, review posted, verification decision; **ICS export** for schedule.

NonTechBlueprint

- **Buyer notifications:** request accepted/declined, pre‑shoot reminders (parking/load‑in hints), post‑shoot review prompt.

## **1.24.12 Observability & KPIs**

- **Events:** *space.publish\|update*, *availability.update*, *widget.quote\|submit*, *booking.request\|ib*, *deposit.auth\|capture\|release*, *review.create\|reply*, *verification.pass\|fail*.
- **KPIs:** request→accept rate, IB share, min‑hours compliance, deposit capture rate, review completion rate, search→book conversion.

## **1.24.13 Test Plan**

2344. **Listing page** renders all Quick Facts/Amenities/Rules; min 6 media enforced; approximate map only.

NonTechBlueprint

NonTechBlueprint

2345. **Widget** enforces min hours/buffers; shows fee breakdown; attaches docs; shows auth‑only deposit; IB vs Request flows.

NonTechBlueprint

2346. **Host wizard** round‑trips all fields; Verification Lite passes with plausible docs; badge shows; IB gate honors badge.

NonTechBlueprint

2347. **Dashboard** blocks/unblocks slots; ICS export works; booking detail shows door code and supports post‑booking adjustments.

NonTechBlueprint

2348. **Reviews**: verified badge, owner one‑reply, filters, reputation breakdown; signals appear in Search.

NonTechBlueprint

2349. **Pair with Talent** deep link prefilters People search (date/city retained).

NonTechBlueprint

2350. **Policy**: surveillance disclosure required; hazard toggles saved; address remains private until booking.

NonTechBlueprint

## **1.24.14 Cost & Scale**

- **Aurora Postgres** (serverless v2) autoscaling; keep read replicas off at launch; aggressive connection pooling via Data API.
- **Typesense**: shared cluster (same as §1.21) with capped fields; background reindex on publish/update.
- **S3/CloudFront** for gallery assets; image transforms cached; lifecycle to IA after 90 days.
- **Stripe** deposit holds auth‑only (no capture unless violation).
- **AppSync** on‑demand; resolvers primarily Data API + Lambda; no long‑polling jobs.

## **1.24.15 Work Packages (Cursor 4‑agent lanes)**

- **Agent A — Data & API:** Aurora schema, GraphQL resolvers, deposit/IB rules, Linked Booking Group.
- **Agent B — UI (Web/RN):** Listing pages (SSR), Widget, Wizard, Dashboard (calendar, bookings, ICS).
- **Agent C — Media & Search:** S3 pipelines, image transforms, Typesense indexing & search, amenity facets.
- **Agent D — Policy & Ops:** Verification Lite (OCR+geocode), surveillance disclosure enforcement, hazards, post‑booking adjustments & deposit capture, notifications.

## **1.24.16 Acceptance Criteria — mark §1.24 FINAL only when ALL true**

2360. Public listing pages show **Quick Facts/Amenities/Rules/Availability/Pricing/Host/Location (approximate)/Reviews** per spec; minimum media set enforced.

NonTechBlueprint

2361. **Booking Widget** enforces min‑hours, buffers, fees, **auth‑only deposit**, IB vs Request, and injects **House Rules + Property/Space Release** at checkout.

NonTechBlueprint

2362. **Host Wizard & Dashboard** perform full CRUD, show **Verified Studio** when passed, support **ICS export**, and handle **post‑booking adjustments**.

NonTechBlueprint

2363. **Reviews & Reputation** behave as specified; signals propagate to Search ranking.

NonTechBlueprint

2364. **Pair with Talent** links open a prefiltered People search for same date/city.

NonTechBlueprint

2365. Address privacy, surveillance disclosure, and hazard flags are enforced; moderation policies respected.

NonTechBlueprint

NonTechBlueprint_Part3

2366. SLOs & cost caps configured; analytics dashboards show the KPIs above.

# **§1.24 — Studios & Spaces — Addendum (Final Completeness)**

All items are **text‑only artifacts** for your Word doc with **Recommended filename/path** markers.

### **A) Insurance / COI Requirements (optional but supported at launch)**

**Recommended path:** *spaces/policy/insurance-coi.md*

*- Host can mark "COI Required" and set minimum coverage (e.g., \$1M).*  
*- Checkout requires COI upload or provider selection by buyer (PDF/IMG).*  
*- Validation: file type = pdf/jpg/png \<= 10MB; name must include policyholder.*  
*- Storage: S3 /spaces/{spaceId}/coi/{orderId}.pdf (encrypted, 1y retention).*  
*- Display: "COI on file" badge in booking detail for host and buyer.*  
*- Enforcement: booking cannot "Start" until COI is approved by host or auto-approved if policy flag allows.*  

**Schema additions (Aurora)** — *db/migrations/024_spaces_coi.sql*

*alter table spaces.space add column coi_required boolean not null default false;*  
*create table spaces.space_coi (*  
*id text primary key, order_id text not null, space_id text not null,*  
*s3_key text not null, status text not null check (status in ('pending','approved','rejected')),*  
*created_at timestamptz default now()*  
*);*  

### **B) Pricing Tiers, Overtime & Crew‑size Multipliers**

**Recommended path:** *spaces/pricing/tiers.md*

*- Base price_per_hour + min_hours; optional tiers:*  
* - peak_multiplier (Fri 18:00–Sun 23:59) e.g., 1.20x*  
* - offpeak_multiplier e.g., 0.85x*  
* - crew_size_tiers: \[{max:5, mult:1.0},{max:10, mult:1.15},{max:20, mult:1.30}\]*  
*- Overtime: charged per 30-min block at overtime_rate (default same as hourly).*  
*- Cleaning fee: fixed; refunds only if host marks "waived" post‑inspection.*  

**DDL** — *db/migrations/025_spaces_pricing_tiers.sql*

*alter table spaces.space_pricing add column peak_multiplier numeric;*  
*alter table spaces.space_pricing add column offpeak_multiplier numeric;*  
*create table spaces.space_crew_tier (*  
*space_id text not null, max_people int not null, multiplier numeric not null, primary key (space_id, max_people)*  
*);*  
*alter table spaces.space_pricing add column overtime_rate_cents int;*  

**Widget math note (server‑side):** compute effective hourly = base × (peak/offpeak) × crew multiplier; then add cleaning fee and deposit auth if configured.

### **C) ADA / Accessibility Quick‑Facts (public & filterable)**

**Recommended path:** *spaces/policy/accessibility.md*

*- Fields: step-free access (Y/N), elevator (Y/N), restroom accessible (Y/N), doorway width (in), parking accessibility (Y/N).*  
*- Display: "Accessibility" section on listings; facets available in search.*  

**DDL** — *db/migrations/026_spaces_accessibility.sql*

*alter table spaces.space add column accessible_step_free boolean default false;*  
*alter table spaces.space add column accessible_elevator boolean default false;*  
*alter table spaces.space add column accessible_restroom boolean default false;*  
*alter table spaces.space add column accessible_door_width_in int;*  
*alter table spaces.space add column accessible_parking boolean default false;*  

### **D) Host Cancellation Penalties & Reputation Impact**

**Recommended path:** *spaces/policy/host-cancel.md*

*- Penalty triggers: host-initiated cancellation after acceptance.*  
*- Actions: automatic buyer refund; host reputation decrease; platform fee waived; optional host fee penalty (% of subtotal) after N cancellations per quarter.*  
*- Search impact: temporary down-rank in Studios index; badge removed if cancellations persist.*  

**DDL note:** add *host_cancel_count_qtr* to *space_reputation* and a history table *space_host_cancellation*.

### **E) Evidence & Deposit Capture Rules (post‑booking)**

**Recommended path:** *spaces/policy/deposit-evidence.md*

*- Violations: overtime, crew overage, damage, cleaning breach, rule breach (smoking, open flame, etc.).*  
*- Evidence: photos/videos, timestamp, note; optional third-party invoice upload.*  
*- Workflow: host files adjustment → buyer has 72h to accept/contest → if unresponsive or rejected, T&S mediates; deposit capture only after mediation outcome = "approve capture".*  
*- Stripe integration: if deposit hold still valid, capture up to hold amount; else create additional charge with buyer consent or case-based platform escalation.*  

### **F) Response SLA / Autocancel for Requests (not IB)**

**Recommended path:** *spaces/policy/response-sla.md*

*- Host must respond within 24h (configurable). If no action:*  
* - Auto-expire request → buyer notified and offered alternatives.*  
* - Host responsiveness score decreases; repeated timeouts hide "Request" for future windows until recovered.*  

**Events:** *request.auto_expire*, *host.responsiveness.dec*.

### **G) Availability Blackouts & Holidays**

**Recommended path:** *spaces/availability/blackouts.md*

*- Hosts can define blackout dates or repeated holiday rules.*  
*- Booking widget blocks those windows; ICS export includes "blocked" events.*  

**DDL** — *db/migrations/027_spaces_blackouts.sql*

*create table spaces.space_blackout (*  
*id text primary key, space_id text not null, start_ts timestamptz not null, end_ts timestamptz not null,*  
*reason text, created_at timestamptz default now()*  
*);*  

### **H) SEO JSON‑LD for Studio Listings (SFW‑only)**

**Recommended path:** *web/seo/spaces-jsonld.tsx*

*export function SpaceJsonLd({ space }) {*  
*const data = {*  
*"@context": "*[*https://schema.org*](https://schema.org)*",*  
*"@type": "Place",*  
*"name": space.title,*  
*"address": { "@type": "PostalAddress", "addressLocality": space.city, "addressRegion": space.region, "addressCountry": space.country },*  
*"geo": { "@type": "GeoCoordinates", "latitude": space.latApprox, "longitude": space.lonApprox },*  
*"aggregateRating": space.reputation ? { "@type": "AggregateRating", "ratingValue": space.reputation.score, "reviewCount": space.reputation.volume } : undefined*  
*};*  
*return \<script type="application/ld+json" dangerouslySetInnerHTML={{\_\_html: JSON.stringify(data)}} /\>;*  
*}*  

Never embed exact address or NSFW images in JSON‑LD.

### **I) Approximate Location Policy (geohash precision)**

**Recommended path:** *spaces/policy/location-privacy.md*

*- Public maps show geohash precision ~ 7 (≈150m) jittered; exact address revealed only post‑booking.*  
*- Share Window: address visible from T-24h to T+4h by default, adjustable in ops flags.*  

### **J) House‑Rules & Releases — Template Library & Versioning**

**Recommended path:** *spaces/docs/templates.md*

*- Templates: House Rules + Property/Space Release; locale-aware; versioned.*  
*- Drafting: admin can update templates; change log kept; new orders freeze current version.*  
*- Checkout: shows summary + "View full PDF"; after purchase, signed copies stored per order.*  

### **K) Calendar Sync Posture (Phase 2 two‑way)**

**Recommended path:** *spaces/calendar/sync.md*

*- Launch: ICS export only (read-only).*  
*- Phase 2: inbound sync from Google/Microsoft via OAuth; conflict resolution: platform source of truth; external holds create "blocked" slots.*  
*- Security: per-host token stored in Secrets Manager; least-priv scopes.*  

### **L) Expanded Tests (add to §1.24.13)**

**Recommended path:** *spaces/tests/additional.md*

*- COI required → checkout upload → host approve/reject workflow.*  
*- Pricing tiers: peak/weekend multipliers + crew-size multipliers + overtime blocks.*  
*- Accessibility facets appear and filter in search.*  
*- Host-cancel penalties applied; reputation & ranking impact observable.*  
*- Deposit evidence workflow; capture only after mediation approve.*  
*- Response SLA: request auto-expire if no action; buyer alternatives suggested.*  
*- Blackouts/holidays enforce; ICS export shows blocked events.*  
*- JSON-LD present; geohash policy respected; no exact address before booking.*  

### **M) Work‑packages delta (Cursor 4‑agent lanes)**

- **Agent A — Data & Policy:** COI tables & flows, host-cancel penalties, blackouts/holidays, deposit evidence policy.
- **Agent B — Pricing & Widget:** tier math, crew multipliers, overtime calculation, UI labels for auth-only deposit.
- **Agent C — SEO/Privacy/Docs:** JSON‑LD, geohash map, house‑rules templates & versioning.
- **Agent D — Ops & Calendars:** response‑SLA/autocancel engine, ICS export polish, Phase‑2 calendar sync scaffolding.

# **§1.26 — Admin Console, Ops & Support (Back‑Office) — Full Technical Spec**

*(RBAC & SSO · immutable audit · user/listing moderation · Trust & Safety casework (reports, DMCA, disputes) · Finance ops & reconciliation views · Search curation tools · Smart Docs admin · feature flags & config · content ops (help/announcements) · rate‑limit & risk tuning · observability & SLAs · tests · acceptance)*

**Purpose.** Provide the operational tooling your team needs to run the marketplace safely and efficiently—from handling reports/disputes and financial operations to managing templates, search curation, and configuration. Everything below is **text‑only** for your Word plan and includes **Recommended filename/path** markers for later lift‑and‑shift.

## **1.26.1 Canon & invariants**

2371. **Least privilege + JIT access.** Role‑based access (RBAC), per‑action checks, and **just‑in‑time case access** for message/content review.
2372. **Immutable audit.** Every admin action writes to an append‑only audit table and an object‑locked S3 stream (see §1.18).
2373. **Separation of duties.** Finance permissions are distinct from Trust & Safety (T&S) and Content Ops.
2374. **Privacy.** Admins view PII only when case‑bound and time‑boxed; all access is logged.
2375. **Cost.** One lightweight **Admin Next.js app** behind CloudFront + IP allowlist + SSO; serverless APIs (AppSync/Lambda), pay‑per‑use data access.

## **1.26.2 Roles & permissions (RBAC)**

**Roles (initial set)**

- *super_admin* (break‑glass; very limited holders)
- *trust_safety* (reports, DMCA, disputes, suspensions)
- *finance_ops* (refunds, holds, releases, reconciliation views)
- *support* (account lookups, resend emails, reset MFA, limited credits)
- *content_ops* (help/announcements/city content; SEO snippets)
- *search_curator* (pins, synonyms; §1.21)
- *docs_admin* (templates/versioning; §1.25)
- *engineering* (feature flags, config, read‑only observability)

**Recommended path:** *admin/rbac/policy.json*

*{*  
*"trust_safety": \["case:\*", "user:suspend", "listing:unpublish", "message:read_case_bound", "audit:read"\],*  
*"finance_ops": \["payment:refund", "payout:hold\|release", "order:view", "recon:view", "audit:read"\],*  
*"support": \["user:view", "user:resend_email", "mfa:reset", "credits:grant_limited", "audit:read_own"\],*  
*"content_ops": \["cms:\*", "announcement:\*", "seo:snippet_edit"\],*  
*"search_curator": \["search:pin", "search:synonym"\],*  
*"docs_admin": \["docs:template_crud", "docs:envelope_view"\],*  
*"engineering": \["flag:\*", "config:\*", "observability:\*"\]*  
*}*  

**SSO.** OIDC (Google Workspace / Okta) with group→role mapping. Session lifetime short; re‑auth for destructive actions.

## **1.26.3 App shell & security**

- **Admin app**: Next.js, SSR disabled (pure client + APIs) to minimize PII leakage.
- **Network**: CloudFront → WAF (bot/rate rules) → Admin API Gateway (JWT from SSO).
- **IP allowlist** for office/VPN; optional hardware key (WebAuthn) step‑up for finance/disputes.
- **Break‑glass**: short‑lived *super_admin* elevations require a ticket id + reason; auto‑revoked after TTL.

## **1.26.4 Data model (Aurora) — cases, actions, audit**

**Recommended path:** *db/migrations/026_admin_core.sql*

*begin;*  
  
*create table admin_case (*  
*case_id text primary key, -- cas\_...*  
*kind text not null check (kind in ('report','dmca','dispute','appeal','fraud')),*  
*status text not null check (status in ('new','triage','investigating','awaiting_user','resolved','closed')),*  
*priority int not null default 3, -- 1 .. 5*  
*opened_by text not null, -- usr\_... or system*  
*subject_user text, -- user primarily involved*  
*order_id text, -- optional link*  
*thread_id text, -- optional link*  
*listing_id text, -- person/studio id*  
*summary text not null,*  
*sla_due_at timestamptz,*  
*created_at timestamptz default now(),*  
*updated_at timestamptz default now()*  
*);*  
  
*create table admin_action (*  
*action_id text primary key, -- act\_...*  
*case_id text references admin_case(case_id) on delete cascade,*  
*actor_admin text not null, -- admin user id (oidc subject)*  
*action text not null, -- 'suspend','refund','request_evidence','note','close',...*  
*payload jsonb,*  
*created_at timestamptz default now()*  
*);*  
  
*create table admin_audit (*  
*audit_id text primary key, -- aud\_...*  
*actor_admin text not null,*  
*resource text not null, -- 'user:usr\_...','order:ord\_...'*  
*action text not null,*  
*payload jsonb,*  
*ip inet,*  
*user_agent text,*  
*created_at timestamptz default now()*  
*);*  
  
*commit;*  

**Immutable stream.** All *admin_audit* rows also appended to S3 with **Object Lock** (WORM).

## **1.26.5 Modules & screens**

### **A) User management**

- Search by email/id; view profile, verification (IDV/payment/connected acct), recent orders/threads.
- Actions: **suspend / reinstate**, reset MFA, force logout, grant limited credits (support goodwill), toggle **Safe‑Mode default**.
- Hard deletes disabled; DSAR export (bundle profile + docs + orders) and deletion request workflow.

### **B) Listing management**

- People and Studios: publish/unpublish, verification badges (Trusted/Verified Studio Lite), hazard flags, surveillance disclosure check, COI required flag.
- Media moderation: replace/remove, mark reason; thumbnail regeneration job trigger.
- Address privacy: preview public (approx geohash) vs internal exact address.

### **C) Trust & Safety casework**

- Queues: **Reports**, **DMCA**, **Disputes**, **Appeals**, **Fraud investigations**.
- Case view: timeline (events, messages, evidence), linked order/thread/listing, SLA timer, canned responses.
- Actions: request evidence (auto‑asks parties), temporary **mute**, **block**, **shadow‑ban**, **suspend**.
- Messaging access is **case‑bound**: open a thread in read‑only or limited reply mode; every view is audited.

### **D) Finance Ops**

- Cohesive view of **orders**, **transfers**, **refunds**, **payouts** (joins §1.22 ledgers).
- Actions: issue refund (full/partial), hold/release payout, deposit capture after mediation, adjust payout schedule/reserve.
- Reconciliation viewer (Silver models): detect variances, export CSV.

### **E) Search curation (§1.21)**

- Pin/unpin entities per city/query with TTL; synonym CRUD; zero‑results dashboard.

### **F) Smart Docs admin (§1.25)**

- Templates (versioned & localized) CRUD; preview in context; envelope monitor (status, re‑send, void).

### **G) Content Ops (CMS)**

- **Help Center** articles; **Announcements** (sitewide banner/city‑specific); **City page snippets** for SEO.
- Scheduled publish; localization keys; image library with S3.

### **H) Flags & configuration**

- Feature flags (IB eligibility, Safe‑Mode defaults, response SLA, deposit capture rules).
- Risk/rate‑limit knobs (token buckets for messaging, signup throttles, 3DS enforcement thresholds).
- City activation toggles.

## **1.26.6 Admin API (GraphQL)**

**Recommended path:** *api/schema/admin.graphql*

*enum CaseKind { REPORT DMCA DISPUTE APPEAL FRAUD }*  
*enum CaseStatus { NEW TRIAGE INVESTIGATING AWAITING_USER RESOLVED CLOSED }*  
  
*type AdminCase {*  
*caseId: ID!, kind: CaseKind!, status: CaseStatus!, priority: Int!,*  
*subjectUser: ID, orderId: ID, threadId: ID, listingId: ID,*  
*summary: String!, slaDueAt: AWSDateTime, timeline: \[AdminAction!\]!*  
*}*  
*type AdminAction { actionId: ID!, actorAdmin: ID!, action: String!, payload: AWSJSON, createdAt: AWSDateTime! }*  
  
*type Query {*  
*adminSearchUsers(q: String!, limit: Int = 25): \[AWSJSON!\]! @auth(role: "support")*  
*adminGetCase(caseId: ID!): AdminCase! @auth(role: "trust_safety")*  
*adminListCases(kind: CaseKind, status: CaseStatus, page: Int = 1): \[AdminCase!\]! @auth(role: "trust_safety")*  
*adminRecon(orderId: ID!): AWSJSON! @auth(role: "finance_ops")*  
*}*  
  
*type Mutation {*  
*adminCreateCase(kind: CaseKind!, summary: String!, subjectUser: ID, orderId: ID, threadId: ID, listingId: ID): ID! @auth(role: "trust_safety")*  
*adminAddAction(caseId: ID!, action: String!, payload: AWSJSON): Boolean! @auth(role: "trust_safety")*  
*adminSuspendUser(userId: ID!, reason: String!): Boolean! @auth(role: "trust_safety")*  
*adminReinstateUser(userId: ID!): Boolean! @auth(role: "trust_safety")*  
*adminRefund(orderId: ID!, amountCents: Int!, reason: String!): Boolean! @auth(role: "finance_ops")*  
*adminHoldPayout(orderId: ID!, reason: String!): Boolean! @auth(role: "finance_ops")*  
*adminReleasePayout(orderId: ID!): Boolean! @auth(role: "finance_ops")*  
*adminSearchPin(scope: String!, city: String!, query: String, pinIds: \[ID!\]!, ttlHours: Int): Boolean! @auth(role: "search_curator")*  
*adminSynonymUpsert(id: String!, words: \[String!\]!): Boolean! @auth(role: "search_curator")*  
*adminTemplatePublish(templateId: String!, version: String!, locale: String!): Boolean! @auth(role: "docs_admin")*  
*adminFlagSet(key: String!, value: AWSJSON!): Boolean! @auth(role: "engineering")*  
*}*  

## **1.26.7 JIT access & privacy guardrails**

- **Case‑bound scopes**: to open any message or attachment, an admin must attach it to an **open case**; access grants are time‑boxed (e.g., 2 hours) and **auto‑revoked** when case status changes.
- View/download of sensitive artifacts (IDs, invoices, door codes) uses **signed, single‑use URLs** with short TTL.
- All views generate *admin_audit* entries with IP/UA and the case id.

## **1.26.8 Observability & SLAs**

- **Event taxonomy:** *admin.login*, *admin.case.create\|act\|close*, *admin.user.suspend\|reinstate*, *admin.refund\|hold\|release*, *admin.template.publish*, *admin.search.pin*, *admin.synonym.upsert*, *admin.flag.set*, *admin.audit.view*.

- **Dashboards:** case backlog & aging, time‑to‑first‑response, time‑to‑resolution, dispute outcomes, refund rate, appeal win rate, moderator workload, finance queue length, search pin performance.

- SLOs:

  - Reports triaged p95 ≤ 4h (business hours)
  - Disputes resolved p95 ≤ 5 days
  - Finance webhook→action p95 ≤ 15m
  - Audit write availability 99.99%

## **1.26.9 Content & SEO operations (light CMS)**

- Admin UI to author **help articles** (Markdown→HTML), **announcements**, and **city snippets** (meta description/intro copy).
- All content is versioned, localized (ties to §1.19), and pre‑rendered for SEO; Safe‑Mode always respected on public surfaces.

## **1.26.10 Rate‑limit & risk tuning**

- Sliders/toggles for **message starts/hour**, **signup/IP/day**, **search API burst**, **payments 3DS threshold**.
- Changes require two‑person approval (4‑eyes) for high‑impact risk knobs; change‑log recorded in audit.

## **1.26.11 Feature flags & config**

- Flags: **Instant Book eligibility**, **response SLA**, **deposit capture policy**, **city activation**, **Studio Lite requirement for IB**, **Saved‑search digests cadence**.
- Backed by DynamoDB table with typed schema, exposed read‑only to clients via CDN JSON for fast boot (signed, cache‑controlled).

## **1.26.12 CI/CD & access controls**

- Admin app deploys to a separate Amplify environment / CloudFront distribution.
- SSO required for any access; WAF blocks public traffic; IP allowlist; rate‑limits.
- Secrets in AWS Secrets Manager; no admin credentials in code.

## **1.26.13 Test plan**

2423. **RBAC**: each role’s allowed/denied actions enforced; step‑up auth for finance/disputes.
2424. **Cases**: create/triage/resolve; SLA timers and notifications.
2425. **User**: suspend/reinstate; DSAR export; deletion request workflow.
2426. **Listings**: publish/unpublish; hazard/surveillance flags; COI required.
2427. **Finance**: refund/hold/release; reconciliation viewer; audit entries present.
2428. **Search curation**: pins & synonyms appear in search; TTL expiry works.
2429. **Docs admin**: template publish; envelope monitor; evidence view.
2430. **CMS**: help/announcement create & publish; localization; SEO pre‑render.
2431. **JIT access**: cannot open messages without case; time‑boxed access revokes properly.
2432. **Audit**: 100% of admin actions write to *admin_audit* and S3 WORM stream.

## **1.26.14 Work packages (Cursor 4‑agent lanes)**

- **Agent A — RBAC, Cases & Audit:** schema, resolvers, case flows, immutable audit, JIT access.
- **Agent B — Ops UIs:** user/listing management, T&S workbench, finance console, curation tools, CMS screens.
- **Agent C — Flags & Risk:** feature flags backend, risk knobs, rate‑limits, city activation controls.
- **Agent D — Observability & SSO:** SSO/OIDC integration, step‑up auth, dashboards, alerts, WAF/IP allowlist.

## **1.26.15 Acceptance criteria — mark §1.26 FINAL only when ALL true**

2437. RBAC & SSO enforced; destructive actions require step‑up; least privilege verified.
2438. Cases (reports/DMCA/disputes/fraud) run end‑to‑end with SLA timers, evidence capture, and outcome recording.
2439. Finance console performs refunds, holds, releases; reconciliation viewers work; audit exists.
2440. Listing and user moderation tools operate with privacy safeguards; messaging access is case‑bound and time‑boxed.
2441. Search curation and Smart Docs admin functions are live; CMS can publish localized help/announcements/city snippets.
2442. Feature flags & risk knobs adjustable with audit trails and (for high‑impact) 4‑eyes approval.
2443. Observability dashboards and SLO alerts are active; audit stream is immutable (S3 Object Lock).
2444. Costs and security controls match launch posture (serverless, CloudFront+WAF, IP allowlist).

# **§1.27 — SEO & On‑Site Optimization — Full Technical Spec**

*(crawl control · SSR/ISR build strategy · canonical/robots/sitemaps · structured data · pagination & faceted navigation · Safe‑Mode & SFW indexing · media/OG tags · Core Web Vitals budgets · internal linking · error/redirect policy · analytics & monitoring · tests · acceptance)*

**Purpose.** Implement an SEO system that safely exposes only SFW content, scales city/role/studio listings without creating crawl traps, and drives qualified discovery for People and Studios. This fills the non‑technical gap you flagged and ties into earlier sections (Search §1.21, Studios §1.24, Messaging §1.23, Payments §1.22, Admin §1.26).

## **1.27.1 Canon & invariants**

2445. **SFW‑only indexing.** Public pages (profiles, studios, city pages) must render SFW previews and **noindex** any page that would expose 18+ content or paid assets. Safe‑Mode OFF areas are never indexed.
2446. **Stable URLs & canonical rules.** We allow a small, controlled set of query params to be indexed; everything else is **canonicalized** to a base URL to avoid duplicate content and crawl traps.
2447. **SSR/ISR.** City & directory pages use **Next.js SSR + Incremental Static Regeneration (ISR)** for speed and freshness; profiles/studios use SSR with short revalidation.
2448. **Lightweight structured data.** We publish JSON‑LD for **Person** (People profiles), **Place** (Studios), and **BreadcrumbList** on directories; never include exact addresses on public Studio pages (privacy).
2449. **Crawl budget control.** We pre‑render and surface only “thin‑spine” pages (Cities × Roles/Genres), not combinatorial facets.
2450. **Performance first.** Core Web Vitals (CWV) budgets are enforced at build and runtime (LCP, INP, CLS).

## **1.27.2 URL design & routing**

**Pages (examples):**

- City directory: */tx/houston/models* (*/state/city/role*)
- Genre slice: */tx/houston/models/editorial*
- Studio directory: */tx/houston/studios*
- Profile: */p/{handle}* (SFW profile)
- Studio: */s/{slug}* (SFW listing; exact address hidden)
- Content hubs / guides (optional): */guides/houston-photography-studios*

**Canonical param whitelist:** *?page=*, *?sort=* limited to *best\|new\|price_low\|price_high\|distance* when an origin exists. All other params are dropped in canonicals. Deep facet queries (ANY/ALL filters) **do not** get indexable canonicals.

## **1.27.3 Canonical, robots, and meta tags**

**Recommended path:** *web/lib/seo/canonical.ts*

*export function canonicalFor(url: URL) {*  
*const allowed = new Set(\['page','sort'\]);*  
*const kept = \[...url.searchParams.entries()\].filter((\[k\]) =\> allowed.has(k));*  
*const params = new URLSearchParams(kept);*  
*url.search = params.toString();*  
*return url.toString();*  
*}*  

**robots meta logic:**

- Public directories, SFW profiles/studios: *\<meta name="robots" content="index,follow"\>*
- Any page where Safe‑Mode OFF or NSFW band \>= 2 would appear: *\<meta name="robots" content="noindex,nofollow"\>*
- Paid content pages (Fan‑Sub): always *noindex,nofollow*.

**Recommended path:** *web/pages/\_app.tsx* (excerpt)

*const robots = isIndexable(routeCtx) ? "index,follow" : "noindex,nofollow";*  
*\<head\>\<meta name="robots" content={robots} /\>\</head\>*  

## **1.27.4 robots.txt and crawl allowances**

**Recommended path:** *web/public/robots.txt*

*User-agent: \**  
*Disallow: /api/*  
*Disallow: /checkout/*  
*Disallow: /messages*  
*Disallow: /fan/*  
*Disallow: /\*?\*safeMode=false*  
*Disallow: /\*?\*any=\**  
*Disallow: /\*?\*all=\**  
*Allow: /tx/*  
*Sitemap:* [*https://rastup.com/sitemap.xml*](https://rastup.com/sitemap.xml)

We explicitly disallow combinatorial filters and Safe‑Mode‑off queries.

## **1.27.5 Sitemap strategy (index + modular feeds)**

- **Sitemap index**: */sitemap.xml* → links to:

  - */sitemaps/cities.xml* (city directories)
  - */sitemaps/people-{A..Z}.xml* (profiles by initial)
  - /sitemaps/studios-{A..Z}.xml
  - */sitemaps/guides.xml* (content hubs)

**Generation:** nightly job (Lambda) using Aurora queries and Typesense to fetch only **indexable** (SFW & published) slugs.  
**Changefreq/priority:** profiles/studios *weekly*, directories *daily* while active.

**Recommended path:** *web/pages/sitemap.xml.ts*

*export async function GET() {*  
*const xml = await buildSitemapIndex();*  
*return new Response(xml, { headers: {'Content-Type':'application/xml'}});*  
*}*  

## **1.27.6 Structured data (JSON‑LD)**

### **A) Person (SFW profile)**

**Recommended path:** *web/seo/jsonld-person.tsx*

*export function PersonJsonLd({ p }) {*  
*const data = {*  
*"*[*@context":"https://schema.org*]()*",*  
*"@type":"Person",*  
*"name": p.displayName,*  
*"jobTitle": p.primaryRole, // "Model" \| "Photographer" ...*  
*"knowsAbout": p.genres.slice(0,8),*  
*"image": p.sfwAvatarUrl, // SFW only*  
*"url": \`https://rastup.com/p/\${p.handle}\`,*  
*"address": { "@type":"PostalAddress", "addressLocality": p.city, "addressRegion": p.region, "addressCountry": p.country }*  
*};*  
*return \<script type="application/ld+json" dangerouslySetInnerHTML={{\_\_html: JSON.stringify(data)}} /\>;*  
*}*  

### **B) Place (Studio listing, approximate coordinates only)**

**Recommended path:** *web/seo/jsonld-place.tsx*  
*(uses approx lat/lon; never exact street address pre‑booking; see §1.24)*

### **C) BreadcrumbList for directories**

**Recommended path:** *web/seo/jsonld-breadcrumbs.tsx*

## **1.27.7 SSR/ISR build plan**

- **Directories (City/Role/Genre):** ISR with *revalidate: 300–900s* depending on city activity; pre‑render top 200 city/role combos.
- **Profiles/Studios:** SSR with *revalidate: 300s*; if completeness \< threshold or NSFW band \>= 2, render **SFW gate + noindex**.
- **Guides:** pure static builds, trigger rebuild on edit (CMS).

**Fallbacks:** bots see server‑rendered paginated HTML (not infinite scroll) with *rel="next/prev"* pagination links.

## **1.27.8 Pagination & faceted navigation**

- **Pagination:** use *?page=n*; include *rel="next"*/*rel="prev"*; noindex pages beyond a reasonable depth (e.g., *page \> 20* → *noindex,follow*).
- **Facets:** for UX we keep ANY/ALL filters (genres, amenities, price) but we **noindex** any URL with *any=*/*all=*; canonical points to base listing with the same city/role.
- **Sorts:** *sort* is canonically preserved; others are stripped.

## **1.27.9 Internal linking & content hubs**

- **City pages** surface top roles/genres and **editorial guides** (“Best natural light studios in Houston”).
- **Profile cross‑links:** “Works with” chips link to complementary roles in the same city (controlled set only).
- **Studios:** “Pair with Talent” links (already in §1.24) deep‑link into People search with date/city preserved.

## **1.27.10 Media, OpenGraph & Twitter cards**

- **Profile OG image:** server‑side composited SFW headshot + name + city.
- **Studio OG image:** first SFW gallery image + title + city.
- **Guides OG:** hero image + title.
- All OG images render via an edge image function (Next Image Response) and cached.

**Recommended path:** *web/app/(public)/p/\[handle\]/opengraph-image.tsx*

## **1.27.11 Core Web Vitals budgets & enforcements**

**Budgets (mobile P75):** LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1.  
**Build gate:** Lighthouse CI must pass budgets on key templates (home, city listing, profile, studio).  
**Runtime beacons:** send CWV field data via *web-vitals* to our analytics (§1.13).  
**Tactics:**

- Preconnect DNS for Typesense/AppSync endpoints; lazyload below‑fold images; use *fetchpriority="high"* for LCP media; defer non‑critical JS; no third‑party tag bloat.

**Recommended path:** *observability/budgets/web.json*

*{"lcpMs": 2500, "inpMs": 200, "cls": 0.1, "maxScriptKb": 160, "maxFirstLoadKb": 900}*  

## **1.27.12 Error & redirect policy**

- **4xx:** custom 404 with search module; return *404* (not soft).

- **5xx:** friendly error page; *Retry-After* when under maintenance.

- Redirects:

  - Legacy slugs preserved via *301*; maintain a *slug_redirects* table (source → target).
  - Force canonical host (*www* vs apex) and HTTPS.
  - Trailing slashes normalized.

**Recommended path:** *web/next.config.mjs* (excerpt)

*async redirects() { return \[*  
*{ source: '/profile/:handle', destination: '/p/:handle', permanent: true },*  
*{ source: '/studio/:slug', destination: '/s/:slug', permanent: true }*  
*\];}*  

## **1.27.13 Safe‑Mode & SFW gating (SEO)**

- **Indexable pages must be Safe‑Mode clean**: if any visible component would render NSFW previews, return *noindex,nofollow*.
- **Profile/studio completeness:** below threshold → **noindex** to avoid thin content.
- **Fan‑Sub (paid)**: *noindex* on all paid content and collection pages; preview pages (teasers) are SFW.

## **1.27.14 Analytics & monitoring**

- **GSC** integration per environment (prod only).
- **Event taxonomy:** *seo.published*, *seo.noindex_applied*, *seo.sitemap.emit*, *seo.redirect.hit*, *seo.ogimage.render*.
- **Dashboards:** impressions/clicks by city/role, CTR by directory, profile/studio coverage (% indexable), sitemap submission health, crawl errors over time.
- **Alarms:** surge in 5xx, sitemap job failures, spike in *noindex_applied* beyond baseline (could indicate Safe‑Mode flagging).

## **1.27.15 Cost posture**

- **Serverless build & serve**: ISR caches on CloudFront; minimal SSR compute.
- **OG image render**: edge function cached with low TTL; invalidate only on profile/studio image change.
- **No third‑party SEO SaaS** required at launch; GSC + internal logs suffice.

## **1.27.16 Artifacts (copy‑pasteable)**

- *web/public/robots.txt* (above)
- *web/pages/sitemap.xml.ts* (index builder) + *web/pages/sitemaps/\*.ts* (modular feeds)
- *web/lib/seo/canonical.ts* (canonical builder)
- *web/seo/jsonld-person.tsx*, *web/seo/jsonld-place.tsx*, *web/seo/jsonld-breadcrumbs.tsx*
- *web/app/(public)/.../opengraph-image.tsx* (dynamic OG images)
- *observability/budgets/web.json* (CWV budgets)
- *web/next.config.mjs* redirects (legacy → canonical)

## **1.27.17 Test plan**

2495. **Indexability matrix:** verify *index,follow* on city listings, SFW profiles/studios; verify *noindex,nofollow* on any page with NSFW risks, Safe‑Mode OFF, or paid content.
2496. **Canonicals:** for facet URLs, canonical points to base; for allowed sorts/pagination, canonical preserves them; prev/next present for paginated listings.
2497. **Sitemaps:** validate XML; GSC fetch succeeds; sitemaps list only indexable URLs; updated on publish/unpublish.
2498. **JSON‑LD:** Person/Place/Breadcrumb validate in Rich Results; studios never leak exact address pre‑booking.
2499. **OG/Twitter:** correct images and titles; images update on asset change; cached at edge.
2500. **CWV:** Lighthouse CI passes budgets on templates; field beacons report within targets after deploy.
2501. **Redirects:** legacy slugs 301 to current; no redirect loops; canonical host enforced.
2502. **Error handling:** 404 returns hard 404; maintenance returns Retry‑After; robots obeys disallows.
2503. **Security:** no PII or paid asset URLs in page source; signed URLs never appear in HTML.

## **1.27.18 Acceptance criteria — mark §1.27 FINAL only when ALL true**

2504. Robots, canonicals, and sitemaps are live; only SFW, complete pages are indexable; combinatorial facets are non‑indexable.
2505. Profiles (Person) and Studios (Place) emit valid JSON‑LD; city/role directories emit BreadcrumbList; no exact studio address is exposed.
2506. SSR/ISR strategy implemented; paginated HTML for bots; prev/next and canonical tags correct.
2507. OG/Twitter images render with correct caching; redirect rules cover legacy paths.
2508. Core Web Vitals budgets enforced (build & field); dashboards and alerts wired; GSC is clean of soft‑404 or duplicate‑content warnings.
2509. Costs remain within launch budgets; no third‑party SEO tool lock‑ins.

# **§1.28 — Admin Console, Ops & Support (Back‑Office) — Full Technical Spec**

*(RBAC & SSO · immutable audit/WORM · user/listing moderation · Trust & Safety casework (reports, DMCA, disputes) · finance ops & reconciliation · search curation tools · Smart Docs admin · CMS (help/announcements) · feature flags & risk knobs · observability & SLAs · tests · acceptance)*

**Purpose.** Provide safe, efficient operational tooling to run the marketplace—moderate users/listings, handle reports/DMCA/disputes, operate refunds/payouts, curate search, manage Smart Docs templates, publish help/announcements, tune risk/rate‑limits, and observe SLOs—while enforcing least‑privilege, case‑bound access, and immutable audit.

## **1.28.1 Canon & invariants**

2510. **Least privilege + JIT access.** Roles narrowly scoped; message/media viewing requires **case‑bound** time‑boxed access.
2511. **Immutable audit.** Every admin action is recorded in Aurora **and** appended to S3 with **Object Lock (WORM)**.
2512. **Separation of duties.** Finance vs Trust & Safety (T&S) vs Support vs Content Ops vs Search Curation vs Docs Admin.
2513. **Privacy by design.** Sensitive artifacts only via short‑TTL, single‑use signed URLs; all access audited.
2514. **Cost posture.** One Next.js Admin app behind CloudFront + WAF + IP allowlist; serverless APIs (AppSync/Lambda/Data API).

## **1.28.2 Roles & permissions (RBAC)**

**Initial roles**

- *super_admin* (break‑glass, time‑boxed)
- *trust_safety* (reports, DMCA, disputes, suspensions)
- *finance_ops* (refunds, payout hold/release, reconciliation views)
- *support* (account lookup, resend emails, reset MFA, grant limited credits)
- *content_ops* (help/announcements/city SEO snippets)
- *search_curator* (pins, synonyms)
- *docs_admin* (template/versioning & envelope monitor)
- *engineering* (feature flags, config, observability read)

**Recommended path:** *admin/rbac/policy.json*

*{*  
*"trust_safety": \["case:\*","user:suspend","listing:unpublish","message:read_case_bound","audit:read"\],*  
*"finance_ops": \["payment:refund","payout:hold\|release","order:view","recon:view","audit:read"\],*  
*"support": \["user:view","user:resend_email","mfa:reset","credits:grant_limited","audit:read_own"\],*  
*"content_ops": \["cms:\*","announcement:\*","seo:snippet_edit"\],*  
*"search_curator": \["search:pin","search:synonym"\],*  
*"docs_admin": \["docs:template_crud","docs:envelope_view"\],*  
*"engineering": \["flag:\*","config:\*","observability:\*"\]*  
*}*  

**SSO & step‑up:** OIDC (Google/Okta) group→role mapping; **WebAuthn** step‑up for finance/disputes; short admin session TTL; re‑auth for destructive actions.

## **1.28.3 App shell & perimeter security**

- **Network:** CloudFront → WAF (bot/rate) → Admin API Gateway (JWT from SSO) → AppSync/Lambda.
- **IP allowlist** for office/VPN subnets; break‑glass path requires ticket id + reason and auto‑revokes after TTL.
- **No SSR** for admin pages (client‑side only) to minimize accidental PII caching.

## **1.28.4 Data model (cases, actions, audit)**

**Recommended path:** *db/migrations/028_admin_core.sql*

*begin;*  
  
*create table admin_case (*  
*case_id text primary key, -- cas\_...*  
*kind text not null check (kind in ('report','dmca','dispute','appeal','fraud')),*  
*status text not null check (status in ('new','triage','investigating','awaiting_user','resolved','closed')),*  
*priority int not null default 3, -- 1..5*  
*opened_by text not null, -- usr\_... or system*  
*subject_user text,*  
*order_id text,*  
*thread_id text,*  
*listing_id text,*  
*summary text not null,*  
*sla_due_at timestamptz,*  
*created_at timestamptz default now(),*  
*updated_at timestamptz default now()*  
*);*  
  
*create table admin_action (*  
*action_id text primary key, -- act\_...*  
*case_id text references admin_case(case_id) on delete cascade,*  
*actor_admin text not null, -- OIDC subject*  
*action text not null, -- 'suspend','refund','request_evidence','note','close',...*  
*payload jsonb,*  
*created_at timestamptz default now()*  
*);*  
  
*create table admin_audit (*  
*audit_id text primary key, -- aud\_...*  
*actor_admin text not null,*  
*resource text not null, -- 'user:usr\_...','order:ord\_...','doc:doc\_...'*  
*action text not null,*  
*payload jsonb,*  
*ip inet,*  
*user_agent text,*  
*created_at timestamptz default now()*  
*);*  
  
*commit;*  

**Immutable stream:** all *admin_audit* rows mirrored to S3 bucket with **Object Lock (WORM)**; lifecycle and retention per §1.18.

## **1.28.5 Modules & screens**

### **A) User management**

- Search by email/id; profile verification status; recent orders/threads; Safe‑Mode default.
- Actions: **suspend/reinstate**, reset MFA, force logout, grant goodwill **credits** (amount‑limited), DSAR export & deletion request workflow (with legal holds).

### **B) Listing management (People & Studios)**

- Publish/unpublish; verification badges (Trusted Pro / Verified Studio Lite); hazard & surveillance disclosure flags; **COI required** toggle (ties to §1.24 addendum).
- Media moderation (remove/replace/regen thumbs) with reason codes; public preview vs internal exact address check.

### **C) Trust & Safety casework**

- Queues: **Reports**, **DMCA**, **Disputes**, **Appeals**, **Fraud**.
- Case view: timeline of events, linked order/thread/listing, SLA timer, canned responses.
- Actions: request evidence (auto‑asks parties), temporary **mute**, **block**, **shadow‑ban**, **suspend**.
- **Case‑bound message access:** open thread in read‑only or limited reply; every view/action audited.

### **D) Finance operations**

- Unified view of **orders/transfers/refunds/payouts** (joins §1.22 ledgers and Stripe data).
- Actions: refund (full/partial), **payout hold/release**, deposit capture (post‑mediation), adjust payout schedule/reserve.
- Reconciliation viewer (Silver models) with export/variance flags.

### **E) Search curation (ties §1.21)**

- Pin/unpin results per city/query with TTL; synonyms CRUD; zero‑results dashboard with suggestions to Content Ops.

### **F) Smart Docs admin (ties §1.26)**

- Template library (versioned & localized), preview in context; envelope monitor (status/resend/void); policy knobs (expiry, reminder cadence).

### **G) Content Ops (light CMS)**

- Help Center articles (Markdown→HTML), **Announcements** (global or city‑scoped banners), **City page snippets** for SEO.
- Schedule publish; localization keys; S3 media library; all content versioned.

### **H) Feature flags & risk knobs**

- Flags: Instant Book eligibility, response SLA/autocancel, deposit capture policy, Studio Lite requirement, city activation.
- Risk knobs: message starts/hour, signup ip/day, 3DS enforcement threshold; **4‑eyes approval** for high‑impact changes.

## **1.28.6 Admin API (GraphQL)**

**Recommended path:** *api/schema/admin.graphql*

*enum CaseKind { REPORT DMCA DISPUTE APPEAL FRAUD }*  
*enum CaseStatus { NEW TRIAGE INVESTIGATING AWAITING_USER RESOLVED CLOSED }*  
  
*type AdminCase {*  
*caseId: ID!, kind: CaseKind!, status: CaseStatus!, priority: Int!,*  
*subjectUser: ID, orderId: ID, threadId: ID, listingId: ID,*  
*summary: String!, slaDueAt: AWSDateTime, timeline: \[AdminAction!\]!*  
*}*  
*type AdminAction { actionId: ID!, actorAdmin: ID!, action: String!, payload: AWSJSON, createdAt: AWSDateTime! }*  
  
*type Query {*  
*adminSearchUsers(q: String!, limit: Int = 25): \[AWSJSON!\]! @auth(role: "support")*  
*adminGetCase(caseId: ID!): AdminCase! @auth(role: "trust_safety")*  
*adminListCases(kind: CaseKind, status: CaseStatus, page: Int = 1): \[AdminCase!\]! @auth(role: "trust_safety")*  
*adminRecon(orderId: ID!): AWSJSON! @auth(role: "finance_ops")*  
*}*  
  
*type Mutation {*  
*adminCreateCase(kind: CaseKind!, summary: String!, subjectUser: ID, orderId: ID, threadId: ID, listingId: ID): ID! @auth(role: "trust_safety")*  
*adminAddAction(caseId: ID!, action: String!, payload: AWSJSON): Boolean! @auth(role: "trust_safety")*  
*adminSuspendUser(userId: ID!, reason: String!): Boolean! @auth(role: "trust_safety")*  
*adminReinstateUser(userId: ID!): Boolean! @auth(role: "trust_safety")*  
*adminRefund(orderId: ID!, amountCents: Int!, reason: String!): Boolean! @auth(role: "finance_ops")*  
*adminHoldPayout(orderId: ID!, reason: String!): Boolean! @auth(role: "finance_ops")*  
*adminReleasePayout(orderId: ID!): Boolean! @auth(role: "finance_ops")*  
*adminSearchPin(scope: String!, city: String!, query: String, pinIds: \[ID!\]!, ttlHours: Int): Boolean! @auth(role: "search_curator")*  
*adminSynonymUpsert(id: String!, words: \[String!\]!): Boolean! @auth(role: "search_curator")*  
*adminTemplatePublish(templateId: String!, version: String!, locale: String!): Boolean! @auth(role: "docs_admin")*  
*adminFlagSet(key: String!, value: AWSJSON!): Boolean! @auth(role: "engineering")*  
*}*  

## **1.28.7 JIT access & privacy guardrails**

- Case‑bound scopes grant temporary read (and limited reply where policy allows) to specific threads/media.
- Sensitive artifacts (IDs, invoices, door codes) are served only by short‑TTL, single‑use signed URLs; downloads counted and audited.
- All access writes an *admin_audit* record with case id, IP, UA, and reason.

## **1.28.8 Observability & SLAs**

- **Events:** *admin.login*, *admin.case.create\|act\|close*, *admin.user.suspend\|reinstate*, *admin.refund\|hold\|release*, *admin.search.pin*, *admin.synonym.upsert*, *admin.template.publish*, *admin.flag.set*, *admin.audit.view*.

- **Dashboards:** case backlog/aging, time‑to‑first‑response, time‑to‑resolution, dispute outcomes, refund rate, moderator workload, finance queue length, pin performance.

- SLOs:

  - Report triage p95 ≤ **4h** (business hours)
  - Dispute resolution p95 ≤ **5 days**
  - Finance webhook→action p95 ≤ **15m**
  - Audit write availability **99.99%**

## **1.28.9 CMS & SEO ops (public content)**

- Markdown editor with preview; scheduled publish/unpublish; locale keys; image handling (alt text required); SEO pre‑render.
- Safe‑Mode enforced on public surfaces; no NSFW in help/announcements.

## **1.28.10 Rate‑limit & risk tuning**

- Token buckets for message starts/hour, signup/IP/day; 3DS enforcement threshold sliders.
- High‑impact changes require **two‑person approval**; changes are audited with before/after values.

## **1.28.11 Feature flags & configuration**

- Flags stored in DynamoDB with typed schema; read‑only, signed JSON snapshot exposed via CDN to clients for fast boot.
- Secrets stored in AWS Secrets Manager; no keys in code.

## **1.28.12 CI/CD & access controls**

- Admin app deployed to a dedicated Amplify/CloudFront stack; WAF and IP allowlist required.
- SSO enforced for all routes; break‑glass elevation requires ticket id; logs routed to centralized logging with retention.

## **1.28.13 Test plan**

2557. **RBAC matrix** enforced; step‑up auth for finance/disputes.
2558. **Cases**: create/triage/resolve; SLA timers and notifications; evidence upload/review.
2559. **User moderation**: suspend/reinstate; DSAR export/deletion flow with legal hold exceptions.
2560. **Listing moderation**: publish/unpublish; hazard & surveillance flags; COI required.
2561. **Finance ops**: refund/hold/release; reconciliation viewer; audit entries present.
2562. **Search curation**: pins/synonyms propagate; TTL expiry works; zero‑results insights populated.
2563. **Docs admin**: template publish; envelope status monitor; resend/void; expiry knobs apply.
2564. **CMS**: help/announcement creation; localization; SEO pre‑render.
2565. **JIT access**: cannot open messages without an open case; grants auto‑expire.
2566. **Audit/WORM**: 100% of actions mirrored to S3 Object Lock; tamper attempts rejected.

## **1.28.14 Work packages (Cursor 4‑agent lanes)**

- **Agent A — RBAC, Cases & Audit:** schema, resolvers, case queues, immutable audit, JIT access.
- **Agent B — Ops UIs:** user/listing mgmt, T&S workbench, finance console, curation tools, CMS.
- **Agent C — Flags & Risk:** flag backend, risk knobs, 4‑eyes workflow, city activation controls.
- **Agent D — SSO/Observability:** OIDC groups/roles, WebAuthn step‑up, dashboards, alerts, WAF/IP allowlist.

## **1.28.15 Acceptance criteria — mark §1.28 FINAL only when ALL true**

2571. RBAC & SSO enforced; destructive/financial actions require step‑up; least‑privilege verified.
2572. Casework (reports/DMCA/disputes/fraud) runs end‑to‑end with SLA timers, evidence capture, and outcomes recorded.
2573. Finance console performs refunds, payout holds/releases; reconciliation viewers operate; all actions audited.
2574. Listing & user moderation tools function with privacy safeguards; message/media access is case‑bound and time‑boxed.
2575. Search curation and Smart Docs admin are operational; CMS publishes localized help/announcements/city snippets.
2576. Feature flags & risk knobs adjustable with 4‑eyes approval; complete audit trail.
2577. Observability dashboards live; SLO alerts wired; audit stream is immutable (S3 Object Lock).
2578. Costs/security match launch posture (serverless, CloudFront+WAF, IP allowlist).

# **§1.29 — Case Studies, Portfolios & Boards — Full Technical Spec**

**Purpose.** Showcase real work (case studies, portfolio sets) on role profiles to increase buyer trust and conversion; allow collaborators to be tagged and approve credits; let buyers and producers collect favorites on **Boards** and launch “**Request a similar shoot**” flows. All public surfaces must remain **SFW** with Safe‑Mode gating, collaborator approvals, and DMCA/abuse handling. This section implements the non‑technical acceptance: portfolio tab on profiles; tagging & approvals; collaborator links to profiles; “Add to Board”; Safe‑Mode/SFW only; and editor tools in the owner dashboard.

NonTechBlueprint

## **1.29.1 Scope (from non‑technical plan → technical)**

- **Portfolio tab on public role profiles** with SFW media, grids/galleries, and case‑study stories. Owner dashboard includes a **Portfolio** editor.

NonTechBlueprint

- **Tag collaborators** on portfolio items; collaborators must **approve** or **decline** the credit before their avatar/name appears; collaborator chips **open profiles**.

NonTechBlueprint

- **Boards** (collections) across People, Studios, and Portfolio items; **Add to Board** from any eligible card; event telemetry *board.add*.

NonTechBlueprint

- **Studio linking**: portfolio items can show the **studio used** and link to that studio page; role profiles can show “Has/Owns Studio” chips; telemetry *studio.link.click*.

NonTechBlueprint

- **Safe‑Mode**: public surfaces remain **SFW**; anything beyond permitted tiers is hidden or “blurred with label” per policy when Safe‑Mode is ON.

NonTechBlueprint

## **1.29.2 Architecture (cost‑conscious, elastic)**

- **Frontend:** Next.js (web) SSR for profile tabs; React Native (mobile) with identical data shape.
- **API:** AppSync GraphQL with Lambda resolvers.
- **Storage:** S3 (versioned) for images/video; CloudFront delivery; optional **on‑upload transforms** (thumbs, web‑optimized).
- **Search/Discovery:** Typesense collections for light faceting (“genres”, “city”, “role”), plus profile ranking signals.
- **Moderation & policy:** Safe‑Mode renderer + optional Rekognition moderation check; DMCA/T&S flows via Admin (§1.28).
- **Cost posture:** No external DAM/SaaS. S3 lifecycle → IA/Glacier; CloudFront caching; transforms cached.

## **1.29.3 Data model (Aurora PostgreSQL + S3)**

**Tables (schema** ***portfolio*****)**

- portfolio_item

  - *item_id pk*, *owner_user_id*, *role_profile_id*, *title*, *slug*, *city*, *shoot_date*, *genres text\[\]*,  
    *cover_media_id*, *sfw_band smallint*, *status enum('draft','pending','published','archived','blocked')*,  
    *verified_booking_order_id nullable*, *studio_id nullable*, *created_at*, *updated_at*.
  - Notes: *sfw_band* drives Safe‑Mode visibility; *verified_booking_order_id* shows a “Verified booking” badge when present. **All public media must be SFW.**

NonTechBlueprint

- portfolio_media

  - *media_id pk*, *item_id fk*, *kind enum('image','video')*, *s3_key_original*, *s3_key_web*, *width*, *height*, *duration_sec nullable*, *ordinal*, *alt_text*.

- *portfolio_case_study* (optional, attached to *item_id*)

  - *client_type*, *summary*, *deliverables text\[\]*, *results text*, *budget_range_low_cents*, *budget_range_high_cents*.

- portfolio_collab_tag

  - *item_id fk*, *collaborator_user_id*, *role_code*, *status enum('pending','approved','declined')*, *note*, *evidence_order_id nullable*, *created_at*.
  - Drives **tagging & approvals**; only **approved** collaborators render as chips that **open profiles**.

NonTechBlueprint

- board

  - *board_id pk*, *owner_user_id*, *title*, *visibility enum('private','unlisted','public')*, *city nullable*, *created_at*.

- board_item

  - *board_id fk*, *entity_type enum('person','studio','portfolio_item')*, *entity_id*, *note nullable*, *ordinal*.

**S3 prefixes**

- *portfolio/{ownerUserId}/{itemId}/media/\** (original & web)
- *boards/{ownerUserId}/{boardId}/share/\** (share images, optional)

## **1.29.4 GraphQL schema (selected)**

*(file: api/schema/portfolio.graphql)*

*type PortfolioItem {*  
*id: ID!, title: String!, slug: String!, ownerUserId: ID!, roleProfileId: ID!,*  
*city: String, shootDate: AWSDate, genres: \[String!\]!,*  
*cover: Media!, media: \[Media!\]!, caseStudy: CaseStudy,*  
*studioUsedId: ID, verifiedBooking: Boolean!, sfwBand: Int!, status: String!,*  
*collaborators: \[CollabTag!\]!*  
*}*  
  
*type Media { id: ID!, kind: String!, url: AWSURL!, width: Int, height: Int, durationSec: Int, altText: String }*  
*type CaseStudy { clientType: String, summary: String, deliverables: \[String!\], results: String, budgetLowCents: Int, budgetHighCents: Int }*  
*type CollabTag { userId: ID!, roleCode: String!, status: String!, note: String }*  
  
*type Board { id: ID!, title: String!, visibility: String!, items: \[BoardItem!\]! }*  
*type BoardItem { entityType: String!, entityId: ID!, note: String, ordinal: Int }*  
  
*input PortfolioDraftInput { title: String!, roleProfileId: ID!, city: String, shootDate: AWSDate, genres: \[String!\]! }*  
*input PortfolioPublishInput { id: ID!, caseStudy: AWSJSON, studioUsedId: ID, coverMediaId: ID! }*  
*input CollabRequestInput { itemId: ID!, collaboratorUserId: ID!, roleCode: String!, note: String }*  
*input CollabRespondInput { itemId: ID!, status: String!, note: String }*  
*input BoardCreateInput { title: String!, visibility: String! }*  
*input BoardAddInput { boardId: ID!, entityType: String!, entityId: ID!, note: String }*  
  
*type Query {*  
*portfolioItem(slug: String!): PortfolioItem*  
*profilePortfolio(roleProfileId: ID!, page: Int = 1): \[PortfolioItem!\]!*  
*boards(ownerUserId: ID!): \[Board!\]!*  
*}*  
  
*type Mutation {*  
*createPortfolioDraft(input: PortfolioDraftInput!): ID!*  
*uploadPortfolioMedia(itemId: ID!, mediaKind: String!, fileName: String!): AWSJSON! \# presigned URL*  
*requestCollaboratorTag(input: CollabRequestInput!): Boolean!*  
*respondToCollaboratorTag(input: CollabRespondInput!): Boolean! \# approve/decline*  
*publishPortfolio(input: PortfolioPublishInput!): Boolean!*  
*archivePortfolioItem(id: ID!): Boolean!*  
  
*createBoard(input: BoardCreateInput!): ID!*  
*addToBoard(input: BoardAddInput!): Boolean!*  
*removeFromBoard(boardId: ID!, entityType: String!, entityId: ID!): Boolean!*  
*reorderBoardItem(boardId: ID!, entityType: String!, entityId: ID!, ordinal: Int!): Boolean!*  
  
*dmcaReport(entityType: String!, entityId: ID!, reason: String!, evidence: AWSJSON): ID! \# routes to Admin/T&S*  
*}*  

## **1.29.5 Public UI (web) & owner/editor flows**

**Profile → Portfolio tab (public):**

- Grid (masonry) of **Portfolio Items**; hover shows title, city, genres; Safe‑Mode ensures **SFW only** on public surfaces.

NonTechBlueprint

- Case‑study page (optional route */p/{handle}/work/{slug}*) with hero media, story, deliverables, “**Request a similar shoot**” CTA, collaborators row (only **approved** chips click to profiles), and “**Studio used**” chip linking to the studio page.

NonTechBlueprint

**Owner editor (dashboard):**

- Sections: **Portfolio** (media upload, order, cover pick), **Case Study** (story/results/deliverables), **Collaborators** (invite → pending → approve/decline UI), **Studio used** (search/link). These tools are called out in the non‑technical owner editor scope.

NonTechBlueprint

**Boards (public/private):**

- From any People/Studio/Portfolio card: **Add to Board** → picker (create new or choose existing); fires *board.add* telemetry.

NonTechBlueprint

- Board page lists items (mixed types) with notes; can be **private** (default), **unlisted** (share link), or **public** (SEO‑light; SFW only).

**“Request a similar shoot”**

- On case‑study pages and Board pages, a CTA opens a **pre‑filled RFP** (city, genres, budget band from case study). On submit, it creates an inquiry thread to the owner (or a marketplace RFP if configured).

## **1.29.6 Safe‑Mode & policy**

- **SFW enforcement** on all public portfolio/board surfaces; beyond permitted tiers are **not rendered** (or shown as blurred blocks with “Hidden in Safe‑Mode” label) and pages remain indexable only when SFW.

NonTechBlueprint

- **Collaborator consent**: only approved tags render; pending/declined never show publicly.

NonTechBlueprint

- **DMCA/T&S:** one‑click report from item menu routes to Admin casework (§1.28) for takedown review; item can be blocked system‑wide during review.
- **Watermarks** (optional): on public previews only; originals retained in S3 and not publicly accessible.

## **1.29.7 Media pipeline**

- **Upload** via presigned S3; client sends *x-amz-meta-sfw-band*.
- **Lambda transform**: generate web‑optimized images (e.g., 1920/1280/640 px) + poster for video; strip EXIF; enforce max duration/size.
- **Moderation check (optional)**: Rekognition Moderation; if score \> threshold, set *status='pending'* and send to T&S queue.
- **Caching**: CloudFront with aggressive caching; image URLs include content hash to bust on update.

## **1.29.8 Discovery & SEO**

- **JSON‑LD:** *CreativeWork* (case study pages) or *ImageGallery* (portfolio grids) for **SFW‑only** items; profile/studio JSON‑LD stays as Person/Place (§1.27/§1.24).
- **Internal linking:** collaborator chips → profiles; studio chip → studio page; related items carousel on case‑study pages.
- **Sitemaps:** include only SFW case‑study routes; omit private/unlisted boards.
- **Telemetry:** *board.add*, *portfolio.tag.approve*, *portfolio.tag.decline*, *studio.link.click*, *profile.view*, *cta.click.book/message*.

NonTechBlueprint

## **1.29.9 Analytics & KPIs**

- **Portfolio coverage** (% of active profiles with ≥3 items), **collab approval rate**, **case‑study view → message/book CTR**, **boards created per visitor**, **RFPs initiated from case studies**, **studio‑from‑portfolio clicks**.
- Event names follow the non‑technical telemetry list (see above).

NonTechBlueprint

## **1.29.10 Cost & scale**

- S3 + CloudFront only (no DAM SaaS). Lifecycle: originals to IA after 30 days; web renditions after 90 days.
- Rekognition moderation optional toggle by environment.
- Typesense fields: title, city, genres, role, recency; small documents (no full captions indexing at launch).

## **1.29.11 Artifacts (copy‑pasteable into your Word plan)**

- *db/migrations/029_portfolio.sql* — tables above.
- *api/schema/portfolio.graphql* — schema above.
- *web/seo/jsonld-creativework.tsx* — JSON‑LD helper.
- *web/components/PortfolioItemCard.tsx* — SFW card UI (title, city, genres, Safe‑Mode label).
- *web/components/AddToBoardDialog.tsx* — create/select + add.
- *web/app/(public)/p/\[handle\]/work/\[slug\]/page.tsx* — case‑study route.
- *lambdas/portfolio-transform/index.ts* — image/video transforms + EXIF strip.

*(All artifacts are text here for your single project doc.)*

## **1.29.12 Test plan**

2628. **Owner editor**: upload, reorder, set cover, write case‑study, publish → renders on profile.
2629. **Collaborator tags**: request → collaborator approves/declines → public chips render only on approve; decline hides.

NonTechBlueprint

2630. **Safe‑Mode**: with Safe‑Mode ON, any beyond‑allowed tier media is hidden/blurred; public page remains SFW.

NonTechBlueprint

2631. **Boards**: add/remove/reorder across mixed entities; private vs unlisted vs public behaviors; telemetry *board.add* fires.

NonTechBlueprint

2632. **Studio chip**: link on case study opens the studio page; telemetry *studio.link.click* fires.

NonTechBlueprint

2633. **Request similar shoot**: CTA pre‑fills RFP and creates thread/RFP; edge cases (missing city/budget).
2634. **DMCA**: report → Admin case created → item blocked → unblock on resolution.
2635. **SEO**: JSON‑LD validates; only SFW case‑study URLs appear in sitemaps.
2636. **Perf**: LCP/INP within budgets on portfolio and case‑study templates (ties to §1.27 CWV budgets).

## **1.29.13 Work packages (Cursor 4‑agent lanes)**

- **Agent A — Data & API:** migrations, GraphQL, presigned upload, moderation hooks, DMCA endpoint.
- **Agent B — Web/RN UI:** Portfolio grid, case‑study page, collaborator dialog, Safe‑Mode rendering, Add‑to‑Board dialog.
- **Agent C — Media pipeline & SEO:** Lambda transforms, EXIF strip, JSON‑LD helpers, sitemap emitters.
- **Agent D — Discovery & RFP:** studio chip linking, “Request similar shoot” pre‑fill flow, Typesense indexing, telemetry.

## **1.29.14 Acceptance criteria — mark §1.29 FINAL only when ALL true**

2641. Portfolio tab is live with SFW grids; owner can create/edit/publish items and case studies.

NonTechBlueprint

2642. Collaborator tagging works with **approval/decline**; only approved credits render; collaborator chips open profiles.

NonTechBlueprint

2643. Boards can collect People/Studios/Portfolio items; **Add to Board** is available and tracked.

NonTechBlueprint

2644. Case‑study pages support **Request similar shoot** pre‑fill; studio chip links to the studio page.

NonTechBlueprint

2645. Safe‑Mode strictly enforces **SFW** on public surfaces; anything beyond allowed tiers is hidden/blurred; pages remain indexable only when SFW.

NonTechBlueprint

2646. DMCA/report routes to Admin casework; items can be blocked/unblocked via T&S.
2647. Telemetry events exist per plan (*board.add*, *portfolio.tag.approve/decline*, *studio.link.click*, etc.).

NonTechBlueprint

2648. Performance/SEO budgets pass; cost posture (S3/CloudFront/lifecycle) configured.

# **§1.3 — Booking, Payments & Disputes — Full Technical Spec**

**Purpose.** Implement fast, trustworthy booking with Instant Book (IB) and Request‑to‑Book (RTB), private **Smart Invite** to multiple profiles, escrowed payments, transparent cancellation, and a fair, auditable dispute process. This section translates your non‑technical scope (Service Profile, Packages, Extras, Usage License, IB/Smart Invite, checkout contracts, escrow, payout timing, and disputes) into build‑ready detail.

NonTechBlueprint

## **1.3.1 Scope confirmation (from non‑technical → technical)**

- **Key concepts & objects**: Service Profile (SP), Packages, Extras, Usage License, Instant Book, Smart Invite, Auto‑accept rules.

NonTechBlueprint

- **Booking modes**: Instant Book; Request‑to‑Book (+ Accept / Decline / Counter); Smart Invite (multi‑recipient private brief; buyer can award one or more hires).

NonTechBlueprint

- **Checkout & payment flow**: select package/extras/license; pick date/time & location; dynamic travel fees; **contract pack auto‑attached** (Booking Agreement, Usage License, Model Release for model hires, Content Promotion Terms for creators); e‑sign at checkout; escrow notice; pay & confirm; calendars block; chat opens.

NonTechBlueprint

- **Escrow & payout**: charge buyer → hold funds (“escrow”) → completion signals (time‑based vs deliverable‑based) → grace/review window → auto‑release if no dispute; new‑provider risk delays first payouts; ACH & card support; tipping after completion.

NonTechBlueprint

## **1.3.2 Architecture & cost posture**

- **Frontend**: Next.js web (SSR for booking; ISR for directory), React Native apps.
- **API**: AppSync GraphQL → Lambda resolvers → Aurora Postgres (core booking) + DynamoDB (idempotent event log) + S3 (contracts/attachments).
- **Payments**: **Stripe Connect** (Standard/Express) + **PaymentIntents** for cards and **Financial Connections** (ACH). Funds are captured immediately to platform balance and **transferred** to providers on completion (acts as “escrow” without relying on card auth holds that expire). *No extra PSP at launch to control cost and complexity.*
- **Compliance**: Stripe KYC/KYB for providers, 3DS when required, PCI burden offloaded to Stripe.
- **Cost**: Pure serverless, small Aurora Serverless v2 floor, aggressive CloudFront caching, no paid DAM or workflow SaaS.

## **1.3.3 Data model (Aurora, schema** ***booking*****)**

**Recommended path:** *db/migrations/013_booking_core.sql*

*begin;*  
  
*create type booking_mode as enum ('IB','RTB','INVITE');*  
*create type booking_status as enum (*  
*'initiated','pending_accept','countered','accepted','declined',*  
*'confirmed','in_progress','delivered','completed',*  
*'cancelled_buyer','cancelled_provider','disputed','resolved'*  
*);*  
  
*-- Core order*  
*create table booking.order (*  
*order_id text primary key, -- ord\_...*  
*buyer_user_id text not null,*  
*provider_user_id text not null, -- owner of Service Profile*  
*service_profile_id text not null,*  
*package_id text, -- null when base rate*  
*mode booking_mode not null,*  
*status booking_status not null default 'initiated',*  
*city text, -- normalized city for search/seo*  
*start_ts timestamptz not null,*  
*end_ts timestamptz not null,*  
*location_kind text not null check (location_kind in ('buyer','provider_studio','rented_studio','remote')),*  
*location_address text, -- revealed to parties post-confirm*  
*travel_miles numeric, -- for travel fee calc*  
*license_tier text, -- 'commercial','ads','exclusive','buyout'...*  
*subtotal_cents int not null default 0,*  
*platform_fee_cents int not null default 0,*  
*tax_cents int not null default 0,*  
*tip_cents int not null default 0,*  
*total_cents int not null default 0, -- money charged to buyer*  
*currency text not null default 'usd',*  
*stripe_payment_intent_id text,*  
*connect_transfer_group text,*  
*chat_thread_id text, -- opens on confirm*  
*created_at timestamptz default now(),*  
*updated_at timestamptz default now()*  
*);*  
  
*-- Line items (packages, extras, travel, license)*  
*create table booking.line_item (*  
*id text primary key,*  
*order_id text references booking.order(order_id) on delete cascade,*  
*kind text not null check (kind in ('package','extra','travel','license','adjustment','refund')),*  
*title text not null,*  
*qty numeric not null default 1,*  
*unit_cents int not null,*  
*total_cents int not null*  
*);*  
  
*-- Auto-accept rules (owned by provider)*  
*create table booking.autoaccept_rule (*  
*rule_id text primary key,*  
*service_profile_id text not null,*  
*min_price_cents int,*  
*weekday_mask int, -- bitmask; e.g., Mon..Sun*  
*max_distance_mi numeric,*  
*allow_ib boolean not null default false*  
*);*  
  
*-- Request → Accept / Decline / Counter (Custom Offer)*  
*create table booking.request (*  
*request_id text primary key, -- req\_...*  
*mode booking_mode not null,*  
*order_id text not null, -- binds to a draft order*  
*buyer_user_id text not null,*  
*provider_user_id text not null,*  
*status text not null check (status in ('pending','accepted','declined','countered','expired')),*  
*message text,*  
*expires_at timestamptz,*  
*created_at timestamptz default now()*  
*);*  
  
*-- Smart Invite fan-out recipients*  
*create table booking.invite_recipient (*  
*invite_id text,*  
*recipient_user_id text,*  
*status text not null check (status in ('new','responded','awarded','not_awarded')),*  
*primary key (invite_id, recipient_user_id)*  
*);*  
  
*-- Milestones (deliverable-based jobs)*  
*create table booking.milestone (*  
*milestone_id text primary key,*  
*order_id text not null,*  
*title text not null,*  
*due_ts timestamptz,*  
*amount_cents int not null, -- portion of subtotal*  
*status text not null check (status in ('open','delivered','approved','disputed','refunded'))*  
*);*  
  
*-- Disputes*  
*create table booking.dispute (*  
*dispute_id text primary key, -- dsp\_...*  
*order_id text not null,*  
*opened_by text not null, -- buyer or provider*  
*reason text not null,*  
*description text,*  
*status text not null check (status in ('open','awaiting_evidence','under_review','resolved_buyer','resolved_provider','split','chargeback')),*  
*created_at timestamptz default now(),*  
*updated_at timestamptz default now()*  
*);*  
  
*commit;*  

**Studio damage deposits** (auth‑only holds) live in §1.24 schema; talent bookings do not use deposit holds at launch. (Cross‑ref only; no duplication here.)

## **1.3.4 GraphQL API (AppSync)**

**Recommended path:** *api/schema/booking.graphql*

*enum BookingMode { IB RTB INVITE }*  
*enum BookingStatus {*  
*INITIATED PENDING_ACCEPT COUNTERED ACCEPTED DECLINED*  
*CONFIRMED IN_PROGRESS DELIVERED COMPLETED*  
*CANCELLED_BUYER CANCELLED_PROVIDER DISPUTED RESOLVED*  
*}*  
  
*type LineItem { id: ID!, kind: String!, title: String!, qty: Float!, unitCents: Int!, totalCents: Int! }*  
*type Milestone { id: ID!, title: String!, dueTs: AWSDateTime, amountCents: Int!, status: String! }*  
  
*type Order {*  
*id: ID!, buyerId: ID!, providerId: ID!, serviceProfileId: ID!,*  
*mode: BookingMode!, status: BookingStatus!,*  
*startTs: AWSDateTime!, endTs: AWSDateTime!,*  
*locationKind: String!, city: String,*  
*licenseTier: String, subtotalCents: Int!, platformFeeCents: Int!, taxCents: Int!, tipCents: Int!, totalCents: Int!,*  
*lineItems: \[LineItem!\]!, milestones: \[Milestone!\]!,*  
*chatThreadId: ID*  
*}*  
  
*input StartOrderInput {*  
*serviceProfileId: ID!, mode: BookingMode!, packageId: ID,*  
*startTs: AWSDateTime!, endTs: AWSDateTime!, city: String, locationKind: String!,*  
*extras: \[ID!\], licenseTier: String, travelMiles: Float*  
*}*  
*input CounterOfferInput { orderId: ID!, newStartTs: AWSDateTime, newEndTs: AWSDateTime, lineItemChanges: AWSJSON }*  
*input AcceptInput { requestId: ID! }*  
*input DeclineInput { requestId: ID!, reason: String }*  
*input ConfirmIBInput { orderId: ID! } \# IB fast path*  
*input CreateInviteInput { brief: String!, recipients: \[ID!\]!, startTs: AWSDateTime!, endTs: AWSDateTime!, packageId: ID, budgetCents: Int }*  
*input AwardInviteInput { inviteId: ID!, recipientId: ID! }*  
*input CompleteInput { orderId: ID!, milestoneId: ID } \# time- or deliverable-based*  
*input DisputeInput { orderId: ID!, reason: String!, description: String }*  
  
*type Query {*  
*order(id: ID!): Order*  
*myOrders(page: Int = 1): \[Order!\]!*  
*myRequests(page: Int = 1): \[AWSJSON!\]!*  
*}*  
  
*type Mutation {*  
*startOrder(input: StartOrderInput!): ID! @auth(role: "user")*  
*sendRequest(orderId: ID!, message: String): ID! @auth(role: "user")*  
*confirmInstantBook(input: ConfirmIBInput!): Boolean! @auth(role: "user")*  
*counterOffer(input: CounterOfferInput!): Boolean! @auth(role: "user")*  
*acceptRequest(input: AcceptInput!): Boolean! @auth(role: "user")*  
*declineRequest(input: DeclineInput!): Boolean! @auth(role: "user")*  
  
*createInvite(input: CreateInviteInput!): ID! @auth(role: "user")*  
*awardInvite(input: AwardInviteInput!): Boolean! @auth(role: "user")*  
  
*completeWork(input: CompleteInput!): Boolean! @auth(role: "user")*  
*openDispute(input: DisputeInput!): ID! @auth(role: "user")*  
*}*  

## **1.3.5 Booking modes & flows**

### **A) Instant Book (IB) (opt‑in per provider)**

- IB badge in search when **allow_ib** rule is active; buyer selects date/time, package, extras, license, location; payment → **confirmed immediately** if within rules; calendars block; chat opens.

NonTechBlueprint

- **Server logic**: evaluate *autoaccept_rule* (weekday mask, min price, distance) before confirming; else fallback to RTB.

NonTechBlueprint

### **B) Request‑to‑Book (RTB)**

- Buyer configures the same elements and sends a request. Provider can **Accept / Decline / Counter** (custom offer). On **Accept**, we charge (if not already) and mark **confirmed**. Unanswered requests **auto‑expire** (e.g., 24–48h).

NonTechBlueprint

### **C) Smart Invite (private, multi‑recipient)**

- Buyer selects up to *N* profiles, writes **one brief**, and sends private invites. Buyer can **award** one or multiple hires. No public job board.

NonTechBlueprint

## **1.3.6 Checkout, contracts & e‑sign**

- **Contract pack auto‑attached** at checkout:

  - **Booking Agreement** (scope, deliverables, schedule, payment terms, cancellation, safety rules)
  - **Usage License** (commercial/ads/exclusive/buyout tiers with price adders)
  - **Model Release** (if booking a model)
  - **Content Promotion Terms** (for creators’ posting timelines/crediting)  
    Parties **e‑sign at checkout**; docs are stored with the booking and visible in thread.

NonTechBlueprint

- **Travel fees**: if provider configured per‑mile pricing and locationKind=buyer, compute line item dynamically.

NonTechBlueprint

## **1.3.7 Money movement (“escrow”), release & payouts**

- **Charge & hold semantics**: capture funds to platform balance at confirm (IB) or on provider accept (RTB). This behaves as “escrow” without relying on card authorizations that time‑out.

NonTechBlueprint

- **Completion signals**:

  - **Time‑based jobs** (e.g., model for 3 hours): provider taps **Completed** after session → buyer has **24–48h** to confirm or dispute.
  - **Deliverable‑based jobs** (e.g., photo/video/creator posts): provider marks **Delivered** per milestone; buyer review window per milestone. **Auto‑release** after window if no dispute.

NonTechBlueprint

- **Payout timing**: standard release **~48h** after completion/expiry; **new‑provider risk policy**: first **X** payouts delayed up to **7 days** to reduce chargeback/fraud risk (configurable; relax with reputation). **ACH** primary; PayPal etc. optional later. Tips after completion.

NonTechBlueprint

## **1.3.8 Fees, tax, currencies**

- **Platform fee** line item shown in **Summary & Fees** section of checkout (plus taxes if applicable).

NonTechBlueprint

- **Taxes**: optional Stripe Tax at launch; if disabled, show “taxes may apply” for certain jurisdictions and keep it off the critical path.
- **Currencies**: *currency* stored per order; start with *usd*.

## **1.3.9 Cancellations, reschedules & no‑shows (policy engine)**

**Policy matrix (configurable in Admin; defaults below):**

- **Flexible**:

  - Buyer cancels ≥72h: full refund minus platform fee.
  - 72–24h: 50% of subtotal (provider) + platform fee not refunded.
  - \<24h: no refund (provider keeps subtotal) unless provider rebooks slot.

- **Standard**: 7d/48h/24h thresholds with 100%/50%/0% similar to above.

- **Strict**: 14d/7d/48h thresholds with 75%/50%/0%.

**Reschedule**: buyer can request reschedule ≥48h without fees; provider must accept; otherwise treat as cancellation.  
**Provider cancel**: automatic buyer refund; provider reputation hit; optional monetary penalty after repeated cancels (Admin configurable).  
**No‑show**: treat per policy; talent no‑show → refund; buyer no‑show → no refund.

Studio‑specific overtime/cleaning/deposit rules live in §1.24.

## **1.3.10 Disputes & chargebacks**

- **In‑app disputes**: buyer/provider can open a dispute within the review window. System creates *booking.dispute* and routes a **T&S case** to Admin (§1.26). Evidence collection (photos, deliverables, chat history) with timestamps. Outcomes: *resolved_buyer* (refund), *resolved_provider* (payout), or *split* (partial).
- **Stripe chargebacks**: listen to *charge.dispute.\** webhooks; auto‑attach internal evidence pack (contracts, deliverables, chat logs) and submit via Stripe’s API; mark dispute status *chargeback*.
- **Deposit capture** (studios only): governed by §1.24 policy; not part of talent bookings.

## **1.3.11 Events, webhooks & idempotency**

**Event taxonomy (emits to Kinesis/SNS):**

- booking.request.sent\|accepted\|declined\|countered\|expired
- booking.confirmed\|calendar.blocked\|chat.opened
- booking.milestone.delivered\|approved
- booking.completed\|payout.scheduled\|payout.released
- booking.cancelled.buyer\|provider
- booking.dispute.opened\|resolved

**Webhooks (Stripe Connect):**

- *payment_intent.succeeded*, *payment_intent.payment_failed*, *charge.refunded*, *charge.dispute.created\|closed*, *transfer.created\|paid\|reversed*.

**Idempotency**: all webhook handlers accept *event.id* and store in DynamoDB to prevent duplicate processing.

## **1.3.12 Messaging & calendar integration**

- **Chat thread** opens on confirm; pre‑loads contract summaries; safety tools (report/block) available.
- **Calendar blocks** for both parties; ICS export enabled; holds auto‑expire if request expires; reschedules update blocks.

## **1.3.13 Security, privacy, and Safe‑Mode**

- Contract PDFs and evidence stored in S3 with **pre‑signed short‑TTL** URLs; audit views via Admin.
- Public pages remain **SFW**; checkout surfaces never expose unsafe previews.
- PII (exact addresses/door codes) revealed only post‑confirm and time‑boxed around event.

## **1.3.14 Cost controls**

- One PSP (Stripe) at launch; **no Plaid** needed because **Stripe Financial Connections** covers ACH with lower integration surface and fewer vendors (cheaper to operate). If later needed for broader bank coverage, we can add Plaid behind a feature flag.
- Off‑peak Lambdas (webhooks, transforms) scale to zero; Aurora min ACUs tuned; CloudFront caches static and semi‑static pages.

## **1.3.15 Artifacts (text‑only, paste into your doc)**

- *db/migrations/013_booking_core.sql* — schema above.
- *api/schema/booking.graphql* — GraphQL schema above.
- *ops/runbooks/booking-dispute.md* — step‑by‑step dispute flow and evidence checklist (ties to Admin).
- *ops/policies/cancellation-matrix.md* — default thresholds & examples.
- *api/webhooks/stripe-handlers.md* — event mapping, idempotency, retries.
- *product/acceptance/booking-scenarios.md* — enumerated scenarios (below).

## **1.3.16 Test plan (representative, not exhaustive)**

2696. **IB happy path**: rule allows → confirm → charge → calendar block → chat opens → complete → payout after window.

NonTechBlueprint

2697. **RTB**: request → provider accepts → charge → confirm; request auto‑expires if no response within SLA.

NonTechBlueprint

2698. **Counter‑offer**: provider counters → buyer accepts; totals recalc; prior request invalidated.
2699. **Smart Invite**: 1 brief → N recipients; award one or multiple; non‑awarded invites close.

NonTechBlueprint

2700. **Contracts**: pack generated, e‑signed, stored; visible in thread and Admin.

NonTechBlueprint

2701. **Completion**: time‑based vs milestone‑based; auto‑release after window if no dispute.

NonTechBlueprint

2702. **Cancellation matrix**: refunds computed per thresholds; provider cancel penalty applied; reschedule allowed before window.
2703. **Disputes**: open → evidence → Admin resolution; outcomes map to partial/full refund or payout.
2704. **Stripe webhooks**: success/failure, dispute created/closed, refund; idempotency proven.
2705. **Risk**: new provider payouts delayed; 3DS enforced where required; ACH pending state handled.
2706. **SEO/privacy**: no sensitive data indexed; SFW surfaces only.

## **1.3.17 Acceptance criteria — mark §1.3 FINAL only when ALL true**

2707. IB, RTB, and Smart Invite flows work end‑to‑end with calendar blocks and chat threads.

NonTechBlueprint

2708. Checkout attaches and signs the correct **contract pack**; documents are retained with the order.

NonTechBlueprint

2709. Funds are charged and held on platform balance; **release/payout** logic respects completion + review windows; tipping supported.

NonTechBlueprint

2710. Cancellation & reschedule policies compute correct refunds/penalties; provider cancellations penalize reputation and (if repeated) fees.
2711. Disputes route to Admin casework with evidence; outcomes apply refunds/payouts; Stripe chargebacks are tracked.
2712. Webhooks are idempotent; retries safe; audit trails complete.
2713. Costs remain within launch posture (single PSP; serverless infra; no third‑party workflow SaaS).

# **§1.3 — Booking, Payments & Disputes — Full Technical Spec**

**Purpose.** Implement fast, trustworthy booking with Instant Book (IB) and Request‑to‑Book (RTB), private **Smart Invite** to multiple profiles, escrowed payments, transparent cancellation, and a fair, auditable dispute process. This section translates your non‑technical scope (Service Profile, Packages, Extras, Usage License, IB/Smart Invite, checkout contracts, escrow, payout timing, and disputes) into build‑ready detail.

NonTechBlueprint

## **1.3.1 Scope confirmation (from non‑technical → technical)**

- **Key concepts & objects**: Service Profile (SP), Packages, Extras, Usage License, Instant Book, Smart Invite, Auto‑accept rules.

NonTechBlueprint

- **Booking modes**: Instant Book; Request‑to‑Book (+ Accept / Decline / Counter); Smart Invite (multi‑recipient private brief; buyer can award one or more hires).

NonTechBlueprint

- **Checkout & payment flow**: select package/extras/license; pick date/time & location; dynamic travel fees; **contract pack auto‑attached** (Booking Agreement, Usage License, Model Release for model hires, Content Promotion Terms for creators); e‑sign at checkout; escrow notice; pay & confirm; calendars block; chat opens.

NonTechBlueprint

- **Escrow & payout**: charge buyer → hold funds (“escrow”) → completion signals (time‑based vs deliverable‑based) → grace/review window → auto‑release if no dispute; new‑provider risk delays first payouts; ACH & card support; tipping after completion.

NonTechBlueprint

## **1.3.2 Architecture & cost posture**

- **Frontend**: Next.js web (SSR for booking; ISR for directory), React Native apps.
- **API**: AppSync GraphQL → Lambda resolvers → Aurora Postgres (core booking) + DynamoDB (idempotent event log) + S3 (contracts/attachments).
- **Payments**: **Stripe Connect** (Standard/Express) + **PaymentIntents** for cards and **Financial Connections** (ACH). Funds are captured immediately to platform balance and **transferred** to providers on completion (acts as “escrow” without relying on card auth holds that expire). *No extra PSP at launch to control cost and complexity.*
- **Compliance**: Stripe KYC/KYB for providers, 3DS when required, PCI burden offloaded to Stripe.
- **Cost**: Pure serverless, small Aurora Serverless v2 floor, aggressive CloudFront caching, no paid DAM or workflow SaaS.

## **1.3.3 Data model (Aurora, schema** ***booking*****)**

**Recommended path:** *db/migrations/013_booking_core.sql*

*begin;*  
  
*create type booking_mode as enum ('IB','RTB','INVITE');*  
*create type booking_status as enum (*  
*'initiated','pending_accept','countered','accepted','declined',*  
*'confirmed','in_progress','delivered','completed',*  
*'cancelled_buyer','cancelled_provider','disputed','resolved'*  
*);*  
  
*-- Core order*  
*create table booking.order (*  
*order_id text primary key, -- ord\_...*  
*buyer_user_id text not null,*  
*provider_user_id text not null, -- owner of Service Profile*  
*service_profile_id text not null,*  
*package_id text, -- null when base rate*  
*mode booking_mode not null,*  
*status booking_status not null default 'initiated',*  
*city text, -- normalized city for search/seo*  
*start_ts timestamptz not null,*  
*end_ts timestamptz not null,*  
*location_kind text not null check (location_kind in ('buyer','provider_studio','rented_studio','remote')),*  
*location_address text, -- revealed to parties post-confirm*  
*travel_miles numeric, -- for travel fee calc*  
*license_tier text, -- 'commercial','ads','exclusive','buyout'...*  
*subtotal_cents int not null default 0,*  
*platform_fee_cents int not null default 0,*  
*tax_cents int not null default 0,*  
*tip_cents int not null default 0,*  
*total_cents int not null default 0, -- money charged to buyer*  
*currency text not null default 'usd',*  
*stripe_payment_intent_id text,*  
*connect_transfer_group text,*  
*chat_thread_id text, -- opens on confirm*  
*created_at timestamptz default now(),*  
*updated_at timestamptz default now()*  
*);*  
  
*-- Line items (packages, extras, travel, license)*  
*create table booking.line_item (*  
*id text primary key,*  
*order_id text references booking.order(order_id) on delete cascade,*  
*kind text not null check (kind in ('package','extra','travel','license','adjustment','refund')),*  
*title text not null,*  
*qty numeric not null default 1,*  
*unit_cents int not null,*  
*total_cents int not null*  
*);*  
  
*-- Auto-accept rules (owned by provider)*  
*create table booking.autoaccept_rule (*  
*rule_id text primary key,*  
*service_profile_id text not null,*  
*min_price_cents int,*  
*weekday_mask int, -- bitmask; e.g., Mon..Sun*  
*max_distance_mi numeric,*  
*allow_ib boolean not null default false*  
*);*  
  
*-- Request → Accept / Decline / Counter (Custom Offer)*  
*create table booking.request (*  
*request_id text primary key, -- req\_...*  
*mode booking_mode not null,*  
*order_id text not null, -- binds to a draft order*  
*buyer_user_id text not null,*  
*provider_user_id text not null,*  
*status text not null check (status in ('pending','accepted','declined','countered','expired')),*  
*message text,*  
*expires_at timestamptz,*  
*created_at timestamptz default now()*  
*);*  
  
*-- Smart Invite fan-out recipients*  
*create table booking.invite_recipient (*  
*invite_id text,*  
*recipient_user_id text,*  
*status text not null check (status in ('new','responded','awarded','not_awarded')),*  
*primary key (invite_id, recipient_user_id)*  
*);*  
  
*-- Milestones (deliverable-based jobs)*  
*create table booking.milestone (*  
*milestone_id text primary key,*  
*order_id text not null,*  
*title text not null,*  
*due_ts timestamptz,*  
*amount_cents int not null, -- portion of subtotal*  
*status text not null check (status in ('open','delivered','approved','disputed','refunded'))*  
*);*  
  
*-- Disputes*  
*create table booking.dispute (*  
*dispute_id text primary key, -- dsp\_...*  
*order_id text not null,*  
*opened_by text not null, -- buyer or provider*  
*reason text not null,*  
*description text,*  
*status text not null check (status in ('open','awaiting_evidence','under_review','resolved_buyer','resolved_provider','split','chargeback')),*  
*created_at timestamptz default now(),*  
*updated_at timestamptz default now()*  
*);*  
  
*commit;*  

**Studio damage deposits** (auth‑only holds) live in §1.24 schema; talent bookings do not use deposit holds at launch. (Cross‑ref only; no duplication here.)

## **1.3.4 GraphQL API (AppSync)**

**Recommended path:** *api/schema/booking.graphql*

*enum BookingMode { IB RTB INVITE }*  
*enum BookingStatus {*  
*INITIATED PENDING_ACCEPT COUNTERED ACCEPTED DECLINED*  
*CONFIRMED IN_PROGRESS DELIVERED COMPLETED*  
*CANCELLED_BUYER CANCELLED_PROVIDER DISPUTED RESOLVED*  
*}*  
  
*type LineItem { id: ID!, kind: String!, title: String!, qty: Float!, unitCents: Int!, totalCents: Int! }*  
*type Milestone { id: ID!, title: String!, dueTs: AWSDateTime, amountCents: Int!, status: String! }*  
  
*type Order {*  
*id: ID!, buyerId: ID!, providerId: ID!, serviceProfileId: ID!,*  
*mode: BookingMode!, status: BookingStatus!,*  
*startTs: AWSDateTime!, endTs: AWSDateTime!,*  
*locationKind: String!, city: String,*  
*licenseTier: String, subtotalCents: Int!, platformFeeCents: Int!, taxCents: Int!, tipCents: Int!, totalCents: Int!,*  
*lineItems: \[LineItem!\]!, milestones: \[Milestone!\]!,*  
*chatThreadId: ID*  
*}*  
  
*input StartOrderInput {*  
*serviceProfileId: ID!, mode: BookingMode!, packageId: ID,*  
*startTs: AWSDateTime!, endTs: AWSDateTime!, city: String, locationKind: String!,*  
*extras: \[ID!\], licenseTier: String, travelMiles: Float*  
*}*  
*input CounterOfferInput { orderId: ID!, newStartTs: AWSDateTime, newEndTs: AWSDateTime, lineItemChanges: AWSJSON }*  
*input AcceptInput { requestId: ID! }*  
*input DeclineInput { requestId: ID!, reason: String }*  
*input ConfirmIBInput { orderId: ID! } \# IB fast path*  
*input CreateInviteInput { brief: String!, recipients: \[ID!\]!, startTs: AWSDateTime!, endTs: AWSDateTime!, packageId: ID, budgetCents: Int }*  
*input AwardInviteInput { inviteId: ID!, recipientId: ID! }*  
*input CompleteInput { orderId: ID!, milestoneId: ID } \# time- or deliverable-based*  
*input DisputeInput { orderId: ID!, reason: String!, description: String }*  
  
*type Query {*  
*order(id: ID!): Order*  
*myOrders(page: Int = 1): \[Order!\]!*  
*myRequests(page: Int = 1): \[AWSJSON!\]!*  
*}*  
  
*type Mutation {*  
*startOrder(input: StartOrderInput!): ID! @auth(role: "user")*  
*sendRequest(orderId: ID!, message: String): ID! @auth(role: "user")*  
*confirmInstantBook(input: ConfirmIBInput!): Boolean! @auth(role: "user")*  
*counterOffer(input: CounterOfferInput!): Boolean! @auth(role: "user")*  
*acceptRequest(input: AcceptInput!): Boolean! @auth(role: "user")*  
*declineRequest(input: DeclineInput!): Boolean! @auth(role: "user")*  
  
*createInvite(input: CreateInviteInput!): ID! @auth(role: "user")*  
*awardInvite(input: AwardInviteInput!): Boolean! @auth(role: "user")*  
  
*completeWork(input: CompleteInput!): Boolean! @auth(role: "user")*  
*openDispute(input: DisputeInput!): ID! @auth(role: "user")*  
*}*  

## **1.3.5 Booking modes & flows**

### **A) Instant Book (IB) (opt‑in per provider)**

- IB badge in search when **allow_ib** rule is active; buyer selects date/time, package, extras, license, location; payment → **confirmed immediately** if within rules; calendars block; chat opens.

NonTechBlueprint

- **Server logic**: evaluate *autoaccept_rule* (weekday mask, min price, distance) before confirming; else fallback to RTB.

NonTechBlueprint

### **B) Request‑to‑Book (RTB)**

- Buyer configures the same elements and sends a request. Provider can **Accept / Decline / Counter** (custom offer). On **Accept**, we charge (if not already) and mark **confirmed**. Unanswered requests **auto‑expire** (e.g., 24–48h).

NonTechBlueprint

### **C) Smart Invite (private, multi‑recipient)**

- Buyer selects up to *N* profiles, writes **one brief**, and sends private invites. Buyer can **award** one or multiple hires. No public job board.

NonTechBlueprint

## **1.3.6 Checkout, contracts & e‑sign**

- **Contract pack auto‑attached** at checkout:

  - **Booking Agreement** (scope, deliverables, schedule, payment terms, cancellation, safety rules)
  - **Usage License** (commercial/ads/exclusive/buyout tiers with price adders)
  - **Model Release** (if booking a model)
  - **Content Promotion Terms** (for creators’ posting timelines/crediting)  
    Parties **e‑sign at checkout**; docs are stored with the booking and visible in thread.

NonTechBlueprint

- **Travel fees**: if provider configured per‑mile pricing and locationKind=buyer, compute line item dynamically.

NonTechBlueprint

## **1.3.7 Money movement (“escrow”), release & payouts**

- **Charge & hold semantics**: capture funds to platform balance at confirm (IB) or on provider accept (RTB). This behaves as “escrow” without relying on card authorizations that time‑out.

NonTechBlueprint

- **Completion signals**:

  - **Time‑based jobs** (e.g., model for 3 hours): provider taps **Completed** after session → buyer has **24–48h** to confirm or dispute.
  - **Deliverable‑based jobs** (e.g., photo/video/creator posts): provider marks **Delivered** per milestone; buyer review window per milestone. **Auto‑release** after window if no dispute.

NonTechBlueprint

- **Payout timing**: standard release **~48h** after completion/expiry; **new‑provider risk policy**: first **X** payouts delayed up to **7 days** to reduce chargeback/fraud risk (configurable; relax with reputation). **ACH** primary; PayPal etc. optional later. Tips after completion.

NonTechBlueprint

## **1.3.8 Fees, tax, currencies**

- **Platform fee** line item shown in **Summary & Fees** section of checkout (plus taxes if applicable).

NonTechBlueprint

- **Taxes**: optional Stripe Tax at launch; if disabled, show “taxes may apply” for certain jurisdictions and keep it off the critical path.
- **Currencies**: *currency* stored per order; start with *usd*.

## **1.3.9 Cancellations, reschedules & no‑shows (policy engine)**

**Policy matrix (configurable in Admin; defaults below):**

- **Flexible**:

  - Buyer cancels ≥72h: full refund minus platform fee.
  - 72–24h: 50% of subtotal (provider) + platform fee not refunded.
  - \<24h: no refund (provider keeps subtotal) unless provider rebooks slot.

- **Standard**: 7d/48h/24h thresholds with 100%/50%/0% similar to above.

- **Strict**: 14d/7d/48h thresholds with 75%/50%/0%.

**Reschedule**: buyer can request reschedule ≥48h without fees; provider must accept; otherwise treat as cancellation.  
**Provider cancel**: automatic buyer refund; provider reputation hit; optional monetary penalty after repeated cancels (Admin configurable).  
**No‑show**: treat per policy; talent no‑show → refund; buyer no‑show → no refund.

Studio‑specific overtime/cleaning/deposit rules live in §1.24.

## **1.3.10 Disputes & chargebacks**

- **In‑app disputes**: buyer/provider can open a dispute within the review window. System creates *booking.dispute* and routes a **T&S case** to Admin (§1.26). Evidence collection (photos, deliverables, chat history) with timestamps. Outcomes: *resolved_buyer* (refund), *resolved_provider* (payout), or *split* (partial).
- **Stripe chargebacks**: listen to *charge.dispute.\** webhooks; auto‑attach internal evidence pack (contracts, deliverables, chat logs) and submit via Stripe’s API; mark dispute status *chargeback*.
- **Deposit capture** (studios only): governed by §1.24 policy; not part of talent bookings.

## **1.3.11 Events, webhooks & idempotency**

**Event taxonomy (emits to Kinesis/SNS):**

- booking.request.sent\|accepted\|declined\|countered\|expired
- booking.confirmed\|calendar.blocked\|chat.opened
- booking.milestone.delivered\|approved
- booking.completed\|payout.scheduled\|payout.released
- booking.cancelled.buyer\|provider
- booking.dispute.opened\|resolved

**Webhooks (Stripe Connect):**

- *payment_intent.succeeded*, *payment_intent.payment_failed*, *charge.refunded*, *charge.dispute.created\|closed*, *transfer.created\|paid\|reversed*.

**Idempotency**: all webhook handlers accept *event.id* and store in DynamoDB to prevent duplicate processing.

## **1.3.12 Messaging & calendar integration**

- **Chat thread** opens on confirm; pre‑loads contract summaries; safety tools (report/block) available.
- **Calendar blocks** for both parties; ICS export enabled; holds auto‑expire if request expires; reschedules update blocks.

## **1.3.13 Security, privacy, and Safe‑Mode**

- Contract PDFs and evidence stored in S3 with **pre‑signed short‑TTL** URLs; audit views via Admin.
- Public pages remain **SFW**; checkout surfaces never expose unsafe previews.
- PII (exact addresses/door codes) revealed only post‑confirm and time‑boxed around event.

## **1.3.14 Cost controls**

- One PSP (Stripe) at launch; **no Plaid** needed because **Stripe Financial Connections** covers ACH with lower integration surface and fewer vendors (cheaper to operate). If later needed for broader bank coverage, we can add Plaid behind a feature flag.
- Off‑peak Lambdas (webhooks, transforms) scale to zero; Aurora min ACUs tuned; CloudFront caches static and semi‑static pages.

## **1.3.15 Artifacts (text‑only, paste into your doc)**

- *db/migrations/013_booking_core.sql* — schema above.
- *api/schema/booking.graphql* — GraphQL schema above.
- *ops/runbooks/booking-dispute.md* — step‑by‑step dispute flow and evidence checklist (ties to Admin).
- *ops/policies/cancellation-matrix.md* — default thresholds & examples.
- *api/webhooks/stripe-handlers.md* — event mapping, idempotency, retries.
- *product/acceptance/booking-scenarios.md* — enumerated scenarios (below).

## **1.3.16 Test plan (representative, not exhaustive)**

2761. **IB happy path**: rule allows → confirm → charge → calendar block → chat opens → complete → payout after window.

NonTechBlueprint

2762. **RTB**: request → provider accepts → charge → confirm; request auto‑expires if no response within SLA.

NonTechBlueprint

2763. **Counter‑offer**: provider counters → buyer accepts; totals recalc; prior request invalidated.
2764. **Smart Invite**: 1 brief → N recipients; award one or multiple; non‑awarded invites close.

NonTechBlueprint

2765. **Contracts**: pack generated, e‑signed, stored; visible in thread and Admin.

NonTechBlueprint

2766. **Completion**: time‑based vs milestone‑based; auto‑release after window if no dispute.

NonTechBlueprint

2767. **Cancellation matrix**: refunds computed per thresholds; provider cancel penalty applied; reschedule allowed before window.
2768. **Disputes**: open → evidence → Admin resolution; outcomes map to partial/full refund or payout.
2769. **Stripe webhooks**: success/failure, dispute created/closed, refund; idempotency proven.
2770. **Risk**: new provider payouts delayed; 3DS enforced where required; ACH pending state handled.
2771. **SEO/privacy**: no sensitive data indexed; SFW surfaces only.

## **1.3.17 Acceptance criteria — mark §1.3 FINAL only when ALL true**

2772. IB, RTB, and Smart Invite flows work end‑to‑end with calendar blocks and chat threads.

NonTechBlueprint

2773. Checkout attaches and signs the correct **contract pack**; documents are retained with the order.

NonTechBlueprint

2774. Funds are charged and held on platform balance; **release/payout** logic respects completion + review windows; tipping supported.

NonTechBlueprint

2775. Cancellation & reschedule policies compute correct refunds/penalties; provider cancellations penalize reputation and (if repeated) fees.
2776. Disputes route to Admin casework with evidence; outcomes apply refunds/payouts; Stripe chargebacks are tracked.
2777. Webhooks are idempotent; retries safe; audit trails complete.
2778. Costs remain within launch posture (single PSP; serverless infra; no third‑party workflow SaaS).

# **§1.4 — Messaging, Inbox & Collaboration — Full Technical Spec (Part 1)**

**Purpose.** Deliver a **Unified Inbox** that powers safe, auditable collaboration across **People** and **Studios** with **Message Requests gating**, **Action Cards** (reschedule, extras, approvals, proofs, expense, mark‑complete, dispute, safety flag), **Quiet Hours/Do‑Not‑Disturb**, **push/email notifications & digests**, and **anti‑circumvention nudges**—exactly mirroring your non‑technical blueprint. This section will be delivered in multiple parts; I won’t exit §1.4 until it is ≥99.9% complete.

## **1.4.1 Scope confirmation**

- **Unified Inbox** (tabs/folders: *All*, *Action Required*, *Bookings*, *Offers/Requests*, *Archived*, *Spam/Blocked*).
- **Thread types**: Inquiry, Booking (talent), Studio Booking, Smart Invite, Support/T&S Case.
- **Message Requests**: accept/decline/block; credits and contact filters; anti‑spam throttles; rate limits for new accounts.
- **Action Cards** inside threads: **Propose/Reschedule**, **Extras/Overtime**, **Send Proofs/Approvals**, **Expense/Receipt**, **Mark Complete / Deliver**, **Dispute / Safety Flag**.
- **Notifications**: push/email real‑time + **daily/weekly digest**; ICS attachment for confirmed bookings.
- **Preferences**: per‑channel toggles, **Quiet Hours**, role/city‑specific alerts.
- **Safety**: block/report, nudges against off‑platform payment, Safe‑Mode image preview rules, content filters.
- **Search in Inbox**: by participant, date, keywords, attachments, action‑card types.
- **Privacy & audit**: immutable audit for escalations; case‑bound access for Admin.

## **1.4.2 Architecture (elastic & low‑cost)**

- **Frontend**: Next.js (web) + React Native (mobile). Inbox = virtualized lists; thread = sticky composer + cards.

- **API**: AppSync GraphQL with Lambda resolvers.

- **Storage**:

  - **Aurora Postgres** for threads, participants, message metadata, cards, and inbox indexes.
  - **S3** for attachments (images, proofs, receipts) with short‑TTL pre‑signed URLs.
  - **DynamoDB** for ephemeral **typing/presence**, **rate limits**, **idempotency**, and **Message Request** pending gates.

- **Events**: Kinesis/SNS bus (*msg.sent*, *card.accepted*, *request.accepted*, etc.) feeds notifications, analytics, and Admin.

- **Search**: Typesense collection *inbox_index* for fast participant/keyword search (sanitized; no sensitive PII).

## **1.4.3 Data model (Aurora + Dynamo + S3)**

**Recommended path:** *db/migrations/014_messaging_inbox.sql*

*begin;*  
  
*create type thread_kind as enum ('inquiry','booking','studio','invite','support');*  
*create type request_status as enum ('pending','accepted','declined','blocked','expired');*  
*create type message_kind as enum ('text','image','file','card');*  
  
*create table thread (*  
*thread_id text primary key, -- thr\_...*  
*kind thread_kind not null,*  
*subject text,*  
*owner_order_id text, -- nullable; booking/studio link*  
*opened_by_user text not null,*  
*created_at timestamptz default now(),*  
*updated_at timestamptz default now(),*  
*last_msg_ts timestamptz*  
*);*  
  
*create table thread_participant (*  
*thread_id text references thread(thread_id) on delete cascade,*  
*user_id text not null,*  
*role text, -- buyer\|provider\|host\|support*  
*status text not null check (status in ('active','left','blocked')),*  
*last_read_ts timestamptz,*  
*muted_until timestamptz,*  
*primary key (thread_id, user_id)*  
*);*  
  
*create table message (*  
*message_id text primary key, -- msg\_...*  
*thread_id text not null references thread(thread_id) on delete cascade,*  
*sender_user text not null,*  
*kind message_kind not null,*  
*body_text text, -- for kind='text'*  
*card_type text, -- for kind='card' (reschedule, extras, proofs, expense, complete, dispute, safety)*  
*card_payload jsonb,*  
*attachment_meta jsonb, -- for images/files*  
*created_at timestamptz default now(),*  
*edited_at timestamptz*  
*);*  
  
*create table message_request_gate (*  
*gate_id text primary key, -- rqt\_...*  
*thread_id text not null,*  
*target_user text not null, -- the recipient who must accept/decline*  
*status request_status not null default 'pending',*  
*expires_at timestamptz, -- auto-expire if no action*  
*reason text -- spam heuristic reason*  
*);*  
  
*create table user_block (*  
*blocker_user text not null,*  
*blocked_user text not null,*  
*created_at timestamptz default now(),*  
*primary key (blocker_user, blocked_user)*  
*);*  
  
*-- Inbox indexing for fast lists*  
*create table inbox_index (*  
*user_id text not null,*  
*thread_id text not null,*  
*last_msg_ts timestamptz not null,*  
*folder text not null check (folder in ('all','action','bookings','offers','archived','spam')),*  
*unread_count int not null default 0,*  
*pinned boolean not null default false,*  
*primary key (user_id, thread_id)*  
*);*  
  
*commit;*  

**DynamoDB (ephemeral & rate‑limit)**

- *msg_typing* (*pk=thread_id*, *sk=user_id*, TTL 10s).
- *msg_rate* (*pk=user_id*, counters for message starts/hour; burst windows).
- *request_pending* (gate caches with TTL for quick pending checks).

**S3 prefixes**

- *threads/{threadId}/attachments/\** (images/proofs/receipts; virus scan lambda on upload).
- *threads/{threadId}/cards/\** (rendered PDFs if a card generates a doc preview).

## **1.4.4 GraphQL schema (selected)**

**Recommended path:** *api/schema/messaging.graphql*

*enum ThreadKind { INQUIRY BOOKING STUDIO INVITE SUPPORT }*  
*enum MessageKind { TEXT IMAGE FILE CARD }*  
*enum RequestStatus { PENDING ACCEPTED DECLINED BLOCKED EXPIRED }*  
  
*type Thread {*  
*id: ID!, kind: ThreadKind!, subject: String, orderId: ID,*  
*participants: \[Participant!\]!, lastMessageAt: AWSDateTime, unreadCount: Int*  
*}*  
  
*type Participant { userId: ID!, role: String, status: String, lastReadAt: AWSDateTime, mutedUntil: AWSDateTime }*  
  
*type Message {*  
*id: ID!, kind: MessageKind!, bodyText: String, cardType: String, cardPayload: AWSJSON,*  
*attachment: AWSJSON, senderUser: ID!, createdAt: AWSDateTime!, editedAt: AWSDateTime*  
*}*  
  
*type MessageRequestGate { id: ID!, threadId: ID!, targetUser: ID!, status: RequestStatus!, expiresAt: AWSDateTime, reason: String }*  
  
*input SendTextInput { threadId: ID!, bodyText: String! }*  
*input SendFileInput { threadId: ID!, fileName: String!, contentType: String! } \# returns presigned URL*  
*input CreateThreadInput { kind: ThreadKind!, subject: String, toUserId: ID, orderId: ID }*  
*input AcceptGateInput { gateId: ID! }*  
*input DeclineGateInput { gateId: ID!, reason: String }*  
*input BlockUserInput { userId: ID!, reason: String }*  
*input CardInput { threadId: ID!, type: String!, payload: AWSJSON! } \# reschedule, extras, proofs, expense, complete, dispute, safety*  
  
*type Query {*  
*inbox(folder: String, page: Int = 1): \[Thread!\]!*  
*thread(threadId: ID!): Thread!*  
*messages(threadId: ID!, page: Int = 1): \[Message!\]!*  
*requestGate(threadId: ID!, forUserId: ID!): MessageRequestGate*  
*}*  
  
*type Mutation {*  
*createThread(input: CreateThreadInput!): ID!*  
*sendText(input: SendTextInput!): ID!*  
*getFileUploadUrl(input: SendFileInput!): AWSJSON!*  
*sendCard(input: CardInput!): ID!*  
  
*acceptMessageRequest(input: AcceptGateInput!): Boolean!*  
*declineMessageRequest(input: DeclineGateInput!): Boolean!*  
*blockUser(input: BlockUserInput!): Boolean!*  
  
*markRead(threadId: ID!): Boolean!*  
*moveToFolder(threadId: ID!, folder: String!): Boolean!*  
*setMuted(threadId: ID!, until: AWSDateTime): Boolean!*  
*}*  

**Notes**

- **Message Request** flow: a new thread *does not* notify or display fully until the recipient **accepts**; preview shows limited profile/card. **Decline** closes the gate and moves the thread to *Spam*. **Block** creates *user_block* and hides future attempts.
- **Action Cards** are first‑class messages with *cardType* and structured *cardPayload* (see §1.4.6).

## **1.4.5 Inbox UX & folders**

- **Folders** (*inbox_index.folder*):

  - **Action Required** — threads containing pending **Action Cards** or **Message Requests** awaiting the user.
  - **Bookings** — threads linked to confirmed orders or studio bookings.
  - **Offers/Requests** — RTB/Smart Invite negotiations not yet confirmed.
  - **Archived** — user archived.
  - **Spam/Blocked** — declined/blocked senders; auto‑purged after N days.

- **Thread list cells** show: avatar(s), subject, last snippet, badges (**IB**, **Verified Studio**, **Pending Request**, **Action Required**), unread count.

- **Search** (Typesense): participants, words in **text** and **card** payload titles, attachment names (not full contents), date range, “has:cardType”.

- **Pin & mute**: pin a thread to top; mute until a date/time or indefinitely; **Quiet Hours** globally suppress push between times (but keep inbox counters).

## **1.4.6 Action Cards (structured flows inside chat)**

All cards are **messages** with a typed *cardType* and *cardPayload*. Cards support **Accept / Decline / Counter** where appropriate and drive order updates (cross‑refs to §1.3/§1.24).

2804. Propose/Reschedule

      392. Payload: *oldStart*, *oldEnd*, *newStart*, *newEnd*, *reason*.
      393. Accept → updates the order/line item; conflicts trigger an error card.
      394. Decline → thread note only.

2805. Extras / Overtime

      395. Payload: *items\[\]* (title, qty, unitCents), *why*.
      396. Accept → creates **adjustment** line items and either charges immediately (if captured) or at payout reconciliation.
      397. Studio overtime can consume **deposit** before new charge (per policy).

2806. Proofs / Approvals

      398. Payload: *gallery\[\]* (s3KeyWeb, thumb, count), *expiresAt*.
      399. Buyer can **Approve** or **Request Changes** (with notes/markers).
      400. On approve, triggers **milestone complete** (for deliverable‑based jobs).

2807. Expense / Receipt

      401. Payload: *receipt{amountCents, image, merchant, date}*
      402. Accept → adds to payouts or new charge (if buyer‑payable).
      403. Good for travel, props, studio cleaning receipts.

2808. Mark Complete / Deliver

      404. Payload: *what* (*time_based* \| *milestone_id*), *notes*.
      405. Starts buyer’s **review window**; on lapse, auto‑release payout.

2809. Dispute

      406. Payload: *reason*, *details*, optional *evidence\[\]*.
      407. Creates **dispute_case** and pauses affected payout; opens Admin case (T&S) with SLA.

2810. Safety Flag / Report

      408. Payload: *reason*, *notes*.
      409. Soft‑blocks thread, restricts new messages pending review; Admin case created.

**Card security**: all server‑validated (no client‑side totals). Card execution writes **immutable audit** entries.

## **1.4.7 Message Requests & Anti‑circumvention**

- **Gated start**: new contact → *message_request_gate* created for the recipient. Inbox shows a preview card with **Accept / Decline / Block**.
- **Heuristics**: gates more aggressively for brand‑new senders (age, verification, prior accept ratio, text entropy).
- **Anti‑circumvention nudges**: detect phrases like off‑platform payment requests; show banner: “Keep payment on RastUp for protection.” Repeated attempts → **throttle** or **soft block**.
- **Credit / contact filters** (from non‑technical spec): large‑blast attempts or template spam are slowed; per‑hour caps applied via Dynamo *msg_rate*.

## **1.4.8 Notifications & Digests**

- **Real‑time**: push (FCM/APNs) + email for mentions, card requests, gate accepts, RTB actions, booking confirmations, reschedules.
- **Digest**: daily/weekly depending on preference; sections (*New requests*, *Pending approvals*, *Upcoming bookings* with ICS links).
- **ICS attachments**: confirmed bookings include **.ics** to add to calendars. (Two‑way sync is covered in §1.24 Phase 2.)
- **Preference schema** (per user): channel toggles per event type; **Quiet Hours** window; override for “booking day” messages.

## **1.4.9 Moderation, Safety & Privacy**

- **Block/Report** UI on every thread; block prevents new gates; report opens a T&S case (Admin access is **case‑bound**).
- **Safe‑Mode images**: SFW previews only; NSFW/unsafe media blocked or blurred with label when policy demands.
- **PII**: exact addresses, phone, and studio door codes never appear in public; they appear in **booking detail** context only.

## **1.4.10 Observability, KPIs & Cost**

- **Events**: *msg.request.open\|accept\|decline\|block*, *msg.send*, *card.send\|accept\|decline*, *inbox.search*, *push.send\|open*, *digest.send\|open*.
- **KPIs**: request→accept rate, time‑to‑first‑response, card completion rate, reschedule success, extras attach rate, dispute rate, block/report rate.
- **Cost controls**: S3 lifecycle (attachments → IA in 90d), thumbnail transforms cached, push/email via pay‑as‑you‑go (Pinpoint/SES).

## **1.4.11 Work packages (Cursor 4‑agent lanes)**

- **Agent A — Data/API**: DDL, GraphQL resolvers, gates, cards, audit writes, Actions→Order integration.
- **Agent B — Web/RN UI**: Inbox lists, thread view, composer, card UIs, Message Request preview, search.
- **Agent C — Notifications**: push/email, digest builder, ICS generator, preferences UI.
- **Agent D — Safety/Moderation**: block/report flows, anti‑circumvention, Safe‑Mode preview logic, rate limits.

## **1.4.12 Test plan (Part 1)**

2829. **Message Request**: new contact gate; accept/decline/block; auto‑expire; folder moves.
2830. **Action Cards**: reschedule, extras, proofs/approvals, mark complete; order reflects accepted changes; audit written.
2831. **Studio deposit interaction**: overtime/violation card consumes deposit before new charge (from §1.24).
2832. **Notifications**: push + email for gates/cards; ICS included; Quiet Hours respected.
2833. **Search**: keyword + participant + “has:cardType” filters; performance under large inbox.
2834. **Safety**: NSFW preview blocked; block/report opens Admin case; anti‑circumvention nudge triggers.

## **1.4.13 Acceptance criteria (Part 1)**

- Message Requests fully gate new contacts with **Accept/Decline/Block** and rate limits.
- Core Action Cards function and update bookings; audit trails present.
- Inbox folders and search behave per spec; notifications and digests render correctly; ICS attaches to confirmations.
- Safety (block/report, Safe‑Mode previews, nudges) enforced; costs & lifecycles configured.

# **§1.4 — Messaging, Inbox & Collaboration — Full Technical Spec (Parts 2–Final)**

**Blueprint basis.** The non‑technical plan defines the role‑aware, booking‑aware **Unified Inbox**, **Message Requests** gating, structured **Action Cards** (reschedule, extras, proofs/approvals, expense, mark‑complete, dispute, safety flag), folders/filters, search, credits, contact filters, read/delivered receipts, typing indicators, and strong anti‑circumvention + safety posture. The specs below translate that into exact payloads, indexes, templates, thresholds, and testable rules.

NonTechBlueprint

## **1.4.A Action Card payload schemas (authoritative)**

Cards are first‑class messages (*message.kind='card'*) with *cardType* and validated *cardPayload* (server‑side). Cards mutate orders (see §1.3) only on **accept**. Card audit entries are immutable.

**Common envelope (JSON):**

*{*  
*"cardId": "crd_xxx",*  
*"threadId": "thr_xxx",*  
*"type": "reschedule\|extras\|proofs\|expense\|complete\|dispute\|safety",*  
*"version": 1,*  
*"proposedBy": "usr_xxx",*  
*"createdAt": "2025-11-06T00:00:00Z",*  
*"expiresAt": "2025-11-08T00:00:00Z"*  
*}*  

### **1) Reschedule (*****type="reschedule"*****)**

*{*  
*"oldStart": "2025-11-20T14:00:00Z",*  
*"oldEnd": "2025-11-20T17:00:00Z",*  
*"newStart": "2025-11-22T14:00:00Z",*  
*"newEnd": "2025-11-22T17:00:00Z",*  
*"reason": "Weather"*  
*}*  

**Rules:** new slot must respect provider availability & rule windows; conflicts produce a **server‑generated error card**; acceptance updates the booking schedule and calendar blocks.

NonTechBlueprint

### **2) Extras / Overtime (*****type="extras"*****)**

*{*  
*"items":\[*  
*{"title":"Extra edits","qty":10,"unitCents":500},*  
*{"title":"Rush delivery (48h)","qty":1,"unitCents":15000}*  
*\],*  
*"note":"Client asked for 10 more edits"*  
*}*  

**Rules:** caps per extra kind; totals are **server‑computed**; acceptance adds **adjustment** line items and either charges now or settles at payout (see §1.3).

### **3) Proofs / Approvals (*****type="proofs"*****)**

*{*  
*"gallery":\[*  
*{"thumb":"s3://.../t1.webp","web":"s3://.../p1.webp","count":12}*  
*\],*  
*"watermarked": true,*  
*"expiresAt": "2025-11-30T00:00:00Z",*  
*"allowSelections": true*  
*}*  

**Rules:** buyer can **Approve** (optionally per‑selection) or **RequestChanges** w/ notes; approval completes a milestone when bound to deliverables.

NonTechBlueprint

### **4) Expense / Receipt (*****type="expense"*****)**

*{*  
*"amountCents": 8900,*  
*"currency":"usd",*  
*"merchant":"Prop House",*  
*"date":"2025-11-04",*  
*"receiptImage":"s3://.../receipt.jpg",*  
*"buyerPayable": true*  
*}*  

**Rules:** acceptance adds to payable ledger (payout or new charge); fraud checks apply (image present, amount thresholds).

NonTechBlueprint

### **5) Mark Complete / Deliver (*****type="complete"*****)**

*{*  
*"kind": "time_based\|milestone",*  
*"milestoneId": "ms_xxx",*  
*"notes":"Session completed; uploading previews",*  
*"attachments":\[{"s3Key":"s3://.../call-sheet.pdf"}\]*  
*}*  

**Rules:** triggers the buyer **review window**; on lapse, auto‑releases payout (see §1.3).

NonTechBlueprint

### **6) Dispute (*****type="dispute"*****)**

*{*  
*"reason":"Quality",*  
*"details":"Missed critical shots",*  
*"evidence":\[{"s3Key":"s3://.../evidence1.jpg"}\]*  
*}*  

**Rules:** opens **dispute case**; pauses payout; threads show dispute banner until resolution (Admin).

NonTechBlueprint

### **7) Safety Flag (*****type="safety"*****)**

*{*  
*"reason":"Off-platform payment request",*  
*"notes":"They asked for Zelle",*  
*"severity":"low\|medium\|high"*  
*}*  

**Rules:** soft‑blocks messaging between parties pending T&S review; Admin receives **case‑bound** access.

NonTechBlueprint

## **1.4.B Inbox search syntax & Typesense mapping**

**Query syntax (user‑facing):**

- Free‑text across sender names, message body, and **card titles**.
- Filters: *from:@handle*, *to:@handle*, *role:model\|photographer\|videographer\|creator*, *type:booking\|inquiry\|invite\|support*, *has:file\|image\|card*, *card:reschedule\|extras\|proofs\|expense\|complete\|dispute\|safety*, *date:2025-11*, *city:"Los Angeles"*.

NonTechBlueprint

**Typesense collection** ***inbox_index*** **(flattened per message)**:

*{*  
*"name": "inbox_index",*  
*"fields": \[*  
*{"name":"userId","type":"string"},*  
*{"name":"threadId","type":"string"},*  
*{"name":"kind","type":"string"}, // inquiry\|booking\|invite\|support*  
*{"name":"participants","type":"string\[\]"},*  
*{"name":"role","type":"string"}, // Model/Photographer/...*  
*{"name":"city","type":"string"},*  
*{"name":"has","type":"string\[\]"}, // file\|image\|card*  
*{"name":"card","type":"string\[\]"}, // reschedule\|extras\|...*  
*{"name":"text","type":"string"},*  
*{"name":"ts","type":"int64", "optional": false}*  
*\],*  
*"default_sorting_field": "ts"*  
*}*  

**Indexing rules**

- Every new message produces one doc per **recipient** (for personal inbox views).
- *text* contains message body **or** card summary (e.g., “Reschedule from 2–5pm → 3–6pm”).
- *has* is derived from attachments/card presence.
- **Data minimization:** do **not** index PII (addresses, phone) or full proofs; index only file names and user‑provided titles.

NonTechBlueprint

**Examples**

- *card:extras role:photographer* → threads with extras proposals to you from photographers.
- *has:file date:2025-11* → threads with docs shared this month.

## **1.4.C Presence, typing, delivery & read receipts**

**Presence / typing**

- **DynamoDB** items: *msg_typing* (*pk=threadId*, *sk=userId*, TTL=10s).
- AppSync real‑time subscriptions broadcast **aggregate** typing states (user ID list + TTL).
- Display “Active 2h ago” using last message or last read.

NonTechBlueprint

**Delivery/Read**

- Delivery = server accepted & fanned out (✓✓ hollow).
- Read = recipient updated *thread_participant.last_read_ts* beyond message ts (✓✓ filled).
- Push open events can opportunistically update read state.

## **1.4.D Email + Push templates (transactional & digest)**

**Providers:** SES (email), Pinpoint/APNs/FCM (push).  
**Transactional events:** Message Request, Request Accepted/Declined, New Message, Card Proposals (reschedule/extras/approvals), Booking Confirmed/Rescheduled, Milestone Delivered, Dispute Opened.

**Email template structure** (HTML + text):

- **Subject patterns**:

  - \[RastUp\] {Name} sent a message
  - \[Action Required\] {Name} proposed {cardType}
  - \[Confirm\] Your booking with {Provider} is {status}

- **Header**: brand bar + thread subject + role chip

- **Body**: last message snippet or card summary + CTA buttons (**Open Thread**, **Approve**, **Decline**)

- **Footer**: notification preferences + legal

- **ICS attachment**: on **confirmed** bookings or **rescheduled** timeslots.

NonTechBlueprint

**Push payloads** mirror subjects with compact actions.

## **1.4.E Digest generation & batching**

- **Daily** digest for active users; **weekly** for low‑activity (opt‑in per preferences).
- Sections: **New requests**, **Pending approvals (cards)**, **Upcoming bookings** (with ICS), **Files received**, **Unanswered messages**.

NonTechBlueprint

- **Timezone‑aware** send windows; quiet‑hours honor (see below).
- **De‑dup logic**: if a transactional email already sent \< N hours ago, show only a summary line.

## **1.4.F Quiet Hours & exceptions**

- User can set **Quiet Hours** (e.g., 10pm–7am local). Messages still arrive but **no push**.
- **Escalation exceptions** (always notify): booking starting \< 12h; reschedule requests expiring \< 6h; dispute activity; payment/escrow failures. User may override these exceptions in preferences.

NonTechBlueprint

## **1.4.G Anti‑circumvention patterns & thresholds**

**Goal:** keep value on‑platform (escrow, protection, reviews) while being fair and transparent.

NonTechBlueprint

**Risk signals (scored):**

- **Keywords & euphemisms** for off‑platform pay: *cash app\|cashapp\|venmo\|zelle\|paypal\|wire\|bank transfer\|invoice me\|outside platform\|off platform\|pay direct\|send to my email\|onlyfans tip\|telegram\|whatsapp\|snap* (+ common variants/obfuscations: *v3nm0*, *ca\$h app*, *wh\*tsapp*).
- **Link domains**: high‑risk (payment/chat domains).
- **New account** + high send rate + copy‑paste patterns.
- **Repeated attachment of QR codes** or payment handles.

**Thresholds/Actions (initial):**

- **Score \< 3** → show **nudge banner**: “Keep payments on RastUp for protection.”
- **3 ≤ score \< 6** → throttle new messages (cool‑down 30–60s), disable external links in that thread.
- **Score ≥ 6 or repeat within 24h** → soft‑block thread; create **Safety card** with prefilled reason; route to Admin case.
- **Gross violation** keywords (e.g., explicit request to bypass escrow) → immediate soft‑block + case.  
  All actions are **transparent** in‑thread, with a link to policy.

NonTechBlueprint

## **1.4.H Admin case‑bound access to threads**

- **Case scope**: Admin sees only the threads tied to the case (dispute/safety).
- **JIT tokens**: time‑boxed read access; all views/actions written to the **audit trail** with reason codes.
- **PII redaction**: transient secrets (door codes, phone, emails) masked unless escalation level requires full view.
- **Actions**: mark as reviewed, apply holds, unblock, redact messages (legal), export evidence pack for chargeback.

## **1.4.I Credits, contact filters & rate limits**

- **New conversation credits** per month (configurable); **bonus credits** for verified users (as defined elsewhere). Replies and confirmed booking threads are **unlimited**.

NonTechBlueprint

- **Contact filters**: talent may require **ID‑Verified only**, minimum details (date, city, budget) before a Message Request is allowed to bypass.

NonTechBlueprint

- **Rate limits** (Dynamo token bucket):

  - New users: 3 new conversations/hour; 20/day.
  - Verified: 10/hour; 100/day.
  - Bursts punished (cool‑down) if \>2 similar messages in 60s.

## **1.4.J Safety, attachments & retention**

- **Attachment scanning**: S3 → Lambda AV scan; quarantine until clean; images re‑encoded; videos metadata verified.
- **Safe‑Mode previews**: SFW enforcement in inbox previews (blur/label when required).

NonTechBlueprint

- **Retention**: keep messages indefinitely; auto‑archive stale threads after 180 days (user can unarchive); purge spam after N days.

## **1.4.K Error codes (selected)**

- *MSG_GATE_REQUIRED* (Message Request pending)
- MSG_BLOCKED_BY_USER
- *CARD_EXPIRED* / *CARD_INVALID*
- RATE_LIMITED
- SAFETY_SOFT_BLOCK
- ATTACHMENT_QUARANTINED

## **1.4.L Observability & KPIs (expansion)**

- **Core**: request→accept rate, time‑to‑first‑response, card accept rate, reschedule success, extras attach rate, dispute rate, block/report rate.

NonTechBlueprint

- **Safety**: nudge impressions → behavior change; soft‑blocks/day; case resolution times.
- **Delivery**: p95 publish→deliver latency (\< 250ms); push send→open CTR; digest open rate.

## **1.4.M Work packages (Cursor 4‑agent lanes — continued)**

- **Agent A — Cards & Mutations**: JSON schemas; server validators; accept/decline/counter mutations; audit.
- **Agent B — Search & Index**: Typesense mapping, ingestion jobs, query parser (filters & tokens).
- **Agent C — Presence & Notifications**: typing/presence infra; read/delivered; push/email templates; digest builder.
- **Agent D — Safety & Rate Limits**: anti‑circumvention rules, link classifier, token buckets, admin case‑bound access.

## **1.4.N Test plan — additional cases to reach 99.9%**

2895. **Search tokens**: *card:proofs from:@buyer has:file date:2025-11* returns correct thread set.
2896. **Typing presence**: multi‑device typing shows once; TTL expiry clears state.
2897. **Delivery/read receipts**: ✓✓ hollow → ✓✓ filled when recipient opens; last_read_ts advances.
2898. **Email templates**: render variables; ICS attached on confirmed/rescheduled; quiet hours suppress push.
2899. **Digest**: timezone‑aware batching; de‑dup logic; opt‑out honored.
2900. **Anti‑circumvention**: nudge → throttle → soft‑block flow on repeated attempts; thread banner shows reason.

NonTechBlueprint

2901. **Case‑bound Admin**: JIT token allows only case threads; audit shows reads/actions with reason codes.
2902. **Attachment AV**: quarantined file cannot be downloaded; “clean” flips state and link appears.

## **1.4.O Acceptance criteria — mark §1.4 FINAL only when ALL true**

2903. **Message Requests** gate first‑time contacts, with **Accept/Decline/Block** and credits & contact filters enforced.

NonTechBlueprint

2904. All **Action Cards** work end‑to‑end with the JSON payloads above and mutate bookings/payments where applicable.

NonTechBlueprint

2905. **Search** supports free‑text + tokens; Typesense index returns correct results within p95 \< 150ms.

NonTechBlueprint

2906. **Presence/typing**, **read/delivered** receipts, and **Quiet Hours** + exceptions behave per spec.

NonTechBlueprint

2907. **Notifications & digests** render correct templates; ICS attachments present for booking events.

NonTechBlueprint

2908. **Anti‑circumvention** thresholds operate (nudge → throttle → soft‑block) with Admin case‑bound access on severe/repeat.

NonTechBlueprint

2909. Safety (AV scan, SFW previews), rate limits, and audit trails are active; costs within serverless posture.

## **§1.5 — Trust, Safety & Verification — Technical Development Plan**

**Scope & alignment with your Non‑Technical Plan**

- This section operationalizes your trust & safety pillars: **18+ gating; ID verification to unlock payouts/NSFW/Instant Book; optional background checks (“Trusted Pro”); SocialVerified; Safe‑Mode defaults; automoderation for uploads & messages; safety flags; strike ladder; evidence retention; risk scoring & payout holds**. These are explicitly listed as MVP items and acceptance criteria in your plan.

NonTechBlueprint

NonTechBlueprint

- It also implements “**Verification Center: ID, Background, Social, Studio Lite … Safe‑Mode & FanSub gating enforced during onboarding; SFW previews on public surfaces**.”

NonTechBlueprint

- Where policy specifics (artistic‑only public surfaces, Safe‑Mode defaults, reporting and moderation) are defined in §8.2, this section implements the systems, data, and workflows to make those policies real in product.

NonTechBlueprint_Part3

**Do‑not‑skip note:** Search ranking behavior tied to Safe‑Mode lives in §1.2 and D4; this section provides the data/flags & enforcement used by search and feeds, per your index references.

NonTechBlueprint

### **1.5.A Objectives & Non‑goals**

**Objectives**

2913. Verify **age & identity** for 18+ compliance and to unlock **payouts, NSFW toggle, and Instant Book**.

NonTechBlueprint

2914. Offer **optional background checks** to earn **Trusted Pro**.

NonTechBlueprint

2915. Provide **Safe‑Mode** that is **ON by default** for guests/first‑time viewers; only **SFW previews** appear on public surfaces.

NonTechBlueprint_Part3

NonTechBlueprint

2916. Automoderate **media & messages**, enable **reporting**, **triage queues**, **appeals**, and **graduated enforcement** with **evidence retention**.

NonTechBlueprint

2917. Compute **risk scores & payout holds** (esp. for new providers) and keep **immutable audit logs** for Ops/Legal.

NonTechBlueprint

NonTechBlueprint_Part3

**Non‑goals**

- Drafting public policy language (lives in §8.2). This section implements it.

NonTechBlueprint_Part3

### **1.5.B Architecture (AWS Amplify Gen‑2 / AppSync / Stripe‑first)**

**Core services**

- **Auth & RBAC:** Cognito (18+ attestation at signup; IDV status flags via custom attributes).

- **GraphQL API:** AppSync (owner‑authorized mutations; admin backdoor via IAM).

- **Data:** DynamoDB (PII & case records), S3 (evidence, redacted exports), EventBridge (safety events), Step Functions (IDV & background‑check orchestration), CloudWatch (alarms & dashboards).

- **Payments & Payouts:** Stripe Connect (Express) with **Stripe Identity** for IDV to tightly couple KYC ➜ payouts; **ACH via Link** (Plaid optional fallback for non‑Link banks).

- **Background checks (Trusted Pro):** Checkr (default) with webhooks to Step Functions.

- **Content moderation:** Hybrid pipeline:

  - **Tier‑0** (cheap/fast): keyword filters + on‑upload thumbnail NSFW classifier (open‑source) to set *content.sensitivity*.
  - **Tier‑1** (vendor): image/video moderation via AWS Rekognition (labels: Explicit Nudity, Suggestive, Violence, etc.).
  - **Tier‑2** (human): Trust queue in Admin with side‑by‑side evidence & policy rubric.

**Cost rule:** Tier‑0 runs for every upload; Tier‑1 runs on (a) high‑reach surfaces, (b) uncertain Tier‑0 results, (c) reports/appeals. Human review only on escalations. This keeps moderation spend elastic while meeting your **SFW‑only public** commitment.

NonTechBlueprint_Part3

**Safe‑Mode data flow**

- Upload ➜ moderation pipeline sets *media.safeModeRequired=true\|false* + *sensitivity=none\|lingerie\|mature*.
- **Default Safe‑Mode ON** for unauth’d & first‑visit sessions; signed‑in adults can toggle. Frontend & Search respect these flags; **FanSub** tabs render only if Safe‑Mode is OFF.

NonTechBlueprint

### **1.5.C Data model (DynamoDB & S3)**

**Tables (PK/SK → key; GSI → query patterns)**

2927. UserTrust

- **PK**=*USER#{userId}*, **SK**=*TRUST#PROFILE*
- Flags: *is18PlusAttested*, *idv.status(pending\|passed\|failed\|expired)*, *idv.vendor*, *bg.status*, *bg.vendor*, *social.verified{ig,yt,tt}*, *studioVerified*, *safeModePreference(defaultOn\|off)*, *instantBookEligible*, *nsfwToggleEligible*, *payoutsEligible*, *risk.score*, *strikes.activeCount*, *holds.type{newAcct\|risk}*, timestamps.
- **GSI1**: *idv.status* → audit & ops queues
- **GSI2**: *bg.status* → Trusted Pro targeting
- **GSI3**: *risk.score* → Finance holds

2933. *VerificationCase* (IDV & Background)

- **PK**=*USER#{userId}*, **SK**=*CASE#{caseId}*
- Type: *idv\|background\|studio\|reference*
- *state* (state‑machine), *vendorSessionId*, *webhookLog\[\]*, *decision*, *evidenceRef\[\]*, *expiresAt* (TTL for PII), *appealRef*.

2937. ModerationItem

- **PK**=*ITEM#{mediaId\|messageId}*, **SK**=*MOD#{modId}*
- *kind(media\|message)*, *signals* (labels/scores), *ruleHits\[\]*, *finalDecision(allow\|blur\|block\|remove)*, *safeModeRequired*, *auditId*.

2940. SafetyReport

- **PK**=*REPORT#{reportId}*, **SK**=*CASE*
- *accusedUserId*, *accuserUserId*, *allegation*, *linkedItems\[\]*, *severity*, *triageState*, *SLA*, *outcome*, *strikeDelta*.

2943. StrikeLedger

- **PK**=*USER#{userId}*, **SK**=*STRIKE#{strikeId}*
- *policy*, *points*, *decayAt*, *actionsApplied(pauses\|listingHide\|contactBlock)*.

2946. *EvidenceBlob* (S3‑backed manifest)

- **PK**=*EVIDENCE#{evidenceId}*
- *s3Uri* (redacted), *sha256*, *piiMap*, *legalHold(bool)*.

Evidence & immutable logging are emphasized repeatedly in your implementation notes. We store hashes, never edit originals, and honor legal holds.

NonTechBlueprint_Part3

### **1.5.D GraphQL schema (AppSync)**

**Types (abridged but complete for MVP flows)**

*type TrustFlags {*  
*is18PlusAttested: Boolean!*  
*idvStatus: IDVStatus!*  
*trustedProStatus: BackgroundStatus!*  
*socialVerified: SocialVerified*  
*studioVerified: Boolean!*  
*safeModePreference: SafeModePref!*  
*instantBookEligible: Boolean!*  
*nsfwToggleEligible: Boolean!*  
*payoutsEligible: Boolean!*  
*riskScore: Float!*  
*strikesActive: Int!*  
*}*  
  
*enum IDVStatus { NONE PENDING PASSED FAILED EXPIRED }*  
*enum BackgroundStatus { NONE PENDING PASSED FAILED EXPIRED }*  
*enum SafeModePref { DEFAULT_ON OFF }*  
  
*type StartIdvSessionResult { sessionClientSecret: String!, caseId: ID! }*  
*type StartBgCheckResult { vendorUrl: AWSURL!, caseId: ID! }*  
  
*type Mutation {*  
*attestAge18Plus(consent: Boolean!): TrustFlags @aws_cognito_user_pools*  
  
*startIdvSession(returnUrl: AWSURL): StartIdvSessionResult @aws_cognito_user_pools*  
*\# webhook -\> completeIdvSession is IAM-protected Lambda resolver*  
  
*startBackgroundCheck(package: String!): StartBgCheckResult @aws_cognito_user_pools*  
  
*setSafeModePreference(pref: SafeModePref!): TrustFlags @aws_cognito_user_pools*  
  
*reportUser(targetUserId: ID!, reason: String!, evidenceRefs: \[ID!\]): ID @aws_cognito_user_pools*  
*reportContent(targetId: ID!, kind: String!, reason: String!, evidenceRefs: \[ID!\]): ID @aws_cognito_user_pools*  
  
*appeal(caseId: ID!, message: String!, evidenceRefs: \[ID!\]): ID @aws_cognito_user_pools*  
*}*  
  
*type Query {*  
*myTrustFlags: TrustFlags @aws_cognito_user_pools*  
*}*  

**Admin (separate Admin AppSync API or IAM‑guarded namespace)**

- *listCases(state, type)*, *decideCase(caseId, decision)*, *applyStrike(userId, policy, points)*, *pauseUser*, *unpauseUser*, *exportEvidence(reportId)* with **immutable audit logs** and **two‑step confirmations** per your implementation rules.

NonTechBlueprint_Part3

### **1.5.E State machines (AWS Step Functions)**

**IDV flow**  
*Start → OpenVendorSession → WaitForWebhook → ValidateResult → UpdateTrustFlags → (Unlock: payoutsEligible, nsfwToggleEligible, instantBookEligible) → NotifyUser*

- **Unlocks are exactly per your plan** (IDV gates payouts/NSFW/IB).

NonTechBlueprint

**Background check (Trusted Pro)**  
*Start → CollectDisclosure/Consent → VendorInvite (Checkr) → WaitForWebhook → Adjudication (pass\|fail\|manual) → UpdateFlags (trustedProStatus) → Notify + Badge*

**Moderation (media)**  
*Ingest → Tier-0 classify → If uncertain/highReach → Tier-1 vendor → Derive Decision (allow\|blur\|block) → Write ModerationItem → Update media.safeModeRequired → If block → queue human review*

**Reports/Appeals**  
*ReportOpened → Auto‑triage (severity heuristics) → Queue → Human decision → Apply actions (strikes/pauses) → Evidence snapshot → Notify + AppealWindow → (if appeal) SecondReview → Finalize & log*

### **1.5.F Enforcement & risk**

**Strike ladder & actions**

- Strike points by policy; **decay** after X days; **thresholds** trigger actions (e.g., **Instant Book pause**, profile hide, chat throttle). You specified **enforcement ladder & strikes with expirations**; we persist and display tooltips on badges (why/when).

NonTechBlueprint

**Risk scoring & payout holds**

- Inputs: new account, velocity anomalies, dispute rate, off‑platform attempts, IDV/BG outcomes, device fingerprints.
- Outputs: **payout hold** (reserve % or days) for new/risky providers per your MVP.

NonTechBlueprint

- Finance views include **guardrail alarms** (incident spikes, pass‑rate drops) from your metrics list.

NonTechBlueprint

### **1.5.G Safe‑Mode & public surfaces**

- **Default behavior:** guests & first‑time viewers see blurred thumbnails where *safeModeRequired=true*; signed‑in adults can toggle Safe‑Mode OFF. **FanSub** tabs only render when Safe‑Mode OFF.

NonTechBlueprint_Part3

NonTechBlueprint

- **Search/Feed integration:** indexers read *media.safeModeRequired* and user *safeModePreference*; search UI details retained in §1.2.

NonTechBlueprint

### **1.5.H Verification Center (UX + backend)**

- **Dashboard cards:** ID & Age, Trusted Pro (background), Social Verified, Studio Verified, References — each with **explicit unlocks** and progress bars, per your spec.

NonTechBlueprint

- **Studio & Location verification** (badge; doc upload; staff one‑time check) and **booking location verification** (optional) are included here as 1.5‑family items.

NonTechBlueprint

- **References:** auto‑generated from completed on‑platform bookings; optional community references with light verification.

NonTechBlueprint

### **1.5.I Admin console (T&S + Support + Finance)**

- **Case queues** (IDV/BG/moderation/reports) with SLA timers, **approve/deny/redact/pause/escalate** actions, and **immutable logs**.

NonTechBlueprint_Part3

- **Rollback & flags:** **feature flags & city gates** with two‑step confirmation and audit trail.

NonTechBlueprint_Part3

- **Sandbox/UAT** paths for rules testing are documented in §4.14; we wire these to safety rules so ops can simulate outcomes safely pre‑launch.

NonTechBlueprint

### **1.5.J Security, privacy, retention**

- **PII isolation:** PII/ID images in a separate S3 bucket with **KMS CMKs**, **S3 Object Lock** (legal holds), **PII redaction views**, and **TTL** on *VerificationCase*/*EvidenceBlob* where law permits. **Never edit originals; store hashes.**

NonTechBlueprint_Part3

- **Access:** Admin access via SSO + per‑role scopes (T&S L1/L2, Support, Finance).
- **Logs:** Every admin action signed & time‑stamped; exportable for legal.
- **Compliance notes:** FCRA basics training and disclosures for background checks, per your implementation notes.

NonTechBlueprint_Part3

### **1.5.K Cost profile & phase plan (build → launch → growth)**

**Vendors (defaults, cost‑conscious):**

- **IDV:** Stripe Identity (tight coupling to payouts; per‑check pricing; volume tiers).
- **Background checks:** Checkr (pay‑as‑you‑go packages; candidate‑paid opt‑in supported).
- **Moderation:** open‑source classifier + Rekognition on escalations/surfaces; throttle by confidence to **cap monthly spend**.

**Elasticity levers:**

- Flag‑gated rollouts by city; **Safe‑Mode required** everywhere at launch; **IB requires IDV** always.

NonTechBlueprint_Part3

NonTechBlueprint

- **Budget caps & alarms** for moderation calls/day; auto‑degrade to stricter blurs if vendor quota hit (fail‑safe preserves safety & brand‑safe posture).

### **1.5.L Telemetry, metrics & alarms**

We instrument exactly what you listed under **K) Metrics & Alarms** (adoption, safety outcomes, reliability, fraud, impact, guardrails) with EventBridge → Kinesis Firehose → Athena/QuickSight dashboards; CloudWatch alarms for spikes & pass‑rate drops.

NonTechBlueprint

Key emitted events (examples):

- *trust.idv.started\|passed\|failed* • *trust.bg.started\|adjudicated*
- *content.classified* • *content.safeMode.required*
- *safety.report.opened\|resolved* • *enforcement.strike.applied\|expired*
- finance.payout.hold.applied\|released

### **1.5.M Acceptance criteria (mirrors your L‑list, made testable)**

2976. **Badges & unlocks:** Email/Phone/2FA, **IDV**, **Trusted Pro**, Social, Studio, References all visible; badge tooltips explain unlocks; **IB/NSFW/Payouts** unlock only on **IDV PASSED**.

NonTechBlueprint

2977. **Safe‑Mode:** Guests/first‑time see blurred sensitive thumbnails; adults can toggle; **FanSub** tab hidden unless OFF.

NonTechBlueprint_Part3

NonTechBlueprint

2978. **Automoderation:** Uploads/messages auto‑scored; human queue operational; decisions logged.

NonTechBlueprint

2979. **Safety flag ➜ triage:** Accused user’s **Instant Book paused** pending triage; audit trail present.

NonTechBlueprint

2980. **Risk/holds:** New providers have reserve/hold per config; evidence export available for disputes.

NonTechBlueprint

2981. **Admin:** Two‑step rollbacks; immutable logs; evidence hashes stored; PII view is redacted by default.

NonTechBlueprint_Part3

### **1.5.N Rollout & ops playbook**

- **Feature flags + city gates** govern Safe‑Mode settings, IB gating, and moderation thresholds; every change requires a **two‑step confirm** and creates an **audited event**.

NonTechBlueprint_Part3

- **Training:** Quarterly refreshers (T&S, Support, Finance) and UAT drills; acceptance checklists in Admin.

NonTechBlueprint_Part3

NonTechBlueprint

### **1.5.O Cursor “4‑agents” build plan (so we can ship on autopilot)**

2984. **Agent A — IDV & Payouts:** AppSync schema + Step Functions + Stripe Identity & Connect webhooks; *UserTrust* flags + unlock logic.
2985. **Agent B — Moderation & Safe‑Mode:** Upload hooks + Tier‑0/1 scoring + *safeModeRequired*; feed/search integration contract.
2986. **Agent C — Background & Verification Center:** Checkr flow + Verification Center UI + badges & progress.
2987. **Agent D — Admin & Enforcement:** Case queues, strike ledger, audit logging, feature flags/city gates.

Each agent ships with: unit + integration tests; synthetic data seeds; rollback plan; CloudWatch dashboards; cost alarms.

# **§1.6 — Support, Help Center & Knowledge Base — Full Technical Spec**

**Purpose.** Deliver a cost‑conscious, elastic support stack that: (1) solves most issues via **self‑serve Help Center + guided flows**, (2) creates **context‑rich tickets** when contact is needed, and (3) empowers agents with **macros, automations, SLAs, policy playbooks, and one‑click outcomes**. Targets: **≥70% containment rate**, **P1 ≤ 4h FRT**, robust metrics, and clear MVP→Phase 2 path.

NonTechBlueprint

## **1.6.1 Scope confirmation (from your non‑technical plan → technical)**

- **Help Center IA** with categories, article pattern (At‑a‑glance, Steps, FAQs, Related), and maintenance cadence (top‑50 monthly review, “What’s new”).

NonTechBlueprint

- **Internal tools & automation**: booking lookup, **one‑click outcomes** (refund %, credit, disable IB, apply strike, request info), macros, secure redacted attachments, **auto‑routing**, **SLA timers + breach alerts**, deflection suggestions, QA sampling.

NonTechBlueprint

- **Policy playbooks** (No‑show, Deliverables, Quality, Safety, Fraud/Chargeback, DMCA).

NonTechBlueprint

- **Metrics & targets**: containment, FRT/TTR, CSAT/NPS, reopen/escalation/breach counts, safety/dispute/chargeback rates, **cost per ticket**, **tickets per 100 bookings**, ops cadence.

NonTechBlueprint

- **Accessibility & Localization**: screen‑reader friendly, transcripts, high‑contrast; **US English at launch**, IA prepared for future locales.

NonTechBlueprint

- **MVP vs Phase 2**: MVP includes Help Center + widget + guided flows for **top 8 categories**, ticketing with priorities/SLAs/macros, **self‑serve refunds/discounts in thread (provider‑managed)**, safety priority queue, core dashboards. Phase 2 adds phone/chat for enterprise windows, AI answer suggestions, proactive status banners.

NonTechBlueprint

## **1.6.2 Architecture & cost posture**

**Decision (MVP):**

- **Help Center & KB**: build **in‑house** (Next.js SSR/ISR) backed by Aurora Postgres + S3 for images, with **Typesense** for search. (Keeps content on our domain, full control over SEO, and low unit cost.)
- **Ticketing**: integrate **Zendesk Support (Team plan)** for 3–5 agent seats at launch (macros, views, SLAs, automations, deflection APIs). Provide **Zammad** as a drop‑in **open‑source alternative** if we later need vendor‑free hosting; we maintain a thin adapter layer so the product APIs don’t change.

**Why this split?** Your plan needs heavy **custom context, deflection, and product deep links**; we move fast by owning the KB + widget and **renting** ticketing where it’s cheap and battle‑tested. If seat cost ever outweighs benefits, we can switch to Zammad with the same product contracts.

**Core components**

- **Frontend**: Next.js Help Center (*/help/\**), embeddable React **Support Widget**.
- **API**: AppSync GraphQL for KB, guided flows, ticket prefill, and **context capture**; Lambda resolvers for Zendesk/Zammad adapters.
- **Data**: Aurora (articles, versions, feedback), S3 (images/attachments), Typesense (KB search).
- **Email/Push**: SES for transactional, Pinpoint for digests/alerts.
- **Events**: Kinesis/SNS (*support.contact*, *ticket.created*, *sla.breach*, *kb.view*, *kb.search*) → dashboards.

## **1.6.3 Information Architecture (IA)**

**Top 8 categories (MVP), matching your plan:**

- **Safety & Policies** (safety flag, check‑in/out rules, content rules, reporting)
- **Troubleshooting & Technical** (uploads, file limits, notifications, calendar)
- **Fees & Taxes** (commission, buyer fee, payouts, year‑end docs)
- Booking & Payments
- Payouts
- Account & Verification
- Studios
- **Messaging & Inbox**  
  Each article follows: **At‑a‑glance → Steps (numbered) → FAQs → Related (deep links)**, tone guidelines (clear, non‑legalese, role‑specific examples, short paragraphs, **bold key phrases**). **Monthly review** of top‑50; rotate **What’s new**; deprecate stale content on feature change.

NonTechBlueprint

## **1.6.4 KB data model (Aurora schema** ***kb*****)**

**DDL — paste into your doc** ***db/migrations/016_kb.sql*****:**

*begin;*  
  
*create table kb_category (*  
*category_id serial primary key,*  
*slug text unique not null,*  
*title text not null,*  
*ordinal int not null default 0,*  
*visible boolean not null default true*  
*);*  
  
*create table kb_article (*  
*article_id uuid primary key,*  
*category_id int references kb_category(category_id),*  
*slug text unique not null,*  
*title text not null,*  
*summary text not null, -- "At-a-glance"*  
*body_md text not null, -- Markdown*  
*role_audience text\[\], -- \["buyer","provider","studio"\]*  
*locale text not null default 'en-US',*  
*status text not null check (status in ('draft','review','published','archived')),*  
*published_at timestamptz,*  
*updated_at timestamptz default now()*  
*);*  
  
*create table kb_article_version (*  
*version_id uuid primary key,*  
*article_id uuid references kb_article(article_id) on delete cascade,*  
*editor_user_id text not null,*  
*body_md text not null,*  
*changelog text,*  
*created_at timestamptz default now()*  
*);*  
  
*create table kb_tag (*  
*tag text primary key*  
*);*  
  
*create table kb_article_tag (*  
*article_id uuid references kb_article(article_id) on delete cascade,*  
*tag text references kb_tag(tag),*  
*primary key (article_id, tag)*  
*);*  
  
*create table kb_redirect (*  
*from_slug text primary key,*  
*to_slug text not null*  
*);*  
  
*create table kb_feedback (*  
*article_id uuid references kb_article(article_id) on delete cascade,*  
*user_id text,*  
*helpful boolean,*  
*comment text,*  
*created_at timestamptz default now()*  
*);*  
  
*create table kb_relation (*  
*source_article_id uuid references kb_article(article_id) on delete cascade,*  
*target_kind text not null, -- 'action'\|'article'*  
*target_ref text not null, -- e.g., "app://orders/ord_123/refund" or article slug*  
*label text,*  
*ordinal int default 0*  
*);*  
  
*commit;*  

**S3 prefixes**: *kb/images/{articleId}/\** (webp, svg), *kb/downloads/{articleId}/\** (pdf templates).  
**SEO**: static routes */help/{category}/{slug}*; JSON‑LD *FAQPage* when an article has FAQs.

## **1.6.5 KB search (Typesense)**

**Collection** ***kb_index*****:**

*{*  
*"name":"kb_index",*  
*"fields":\[*  
*{"name":"articleId","type":"string"},*  
*{"name":"slug","type":"string"},*  
*{"name":"title","type":"string"},*  
*{"name":"summary","type":"string"},*  
*{"name":"body","type":"string"},*  
*{"name":"category","type":"string"},*  
*{"name":"role","type":"string\[\]"},*  
*{"name":"locale","type":"string"},*  
*{"name":"updatedAt","type":"int64"}*  
*\],*  
*"default_sorting_field": "updatedAt"*  
*}*  

**Indexing rules**: strip code blocks, preserve headings; boost **title \> summary \> body**; filter by *role* and *locale*.  
**Query tokens**: free text + *category:*, *role:buyer\|provider\|studio*, *type:faq\|steps*, *updated:\<days\>*.

## **1.6.6 Support Widget (guided flows & deflection)**

**UX**

- Step 1: **Suggest articles** (live search over *kb_index* with role/city context).
- Step 2: **Guided flow** per category (dynamic form with 3–6 fields, e.g., booking ID, city, dates, screenshots).
- Step 3: If unresolved, **“Contact Support”** → we create a **ticket prefilled** with: user ID, session, platform, last 3 article IDs **viewed**, booking/studio IDs, environment, and screenshots. *(Your plan expressly requires attaching “read article IDs” to the ticket when a user still contacts support after deflection.)*

NonTechBlueprint

**GraphQL (*****api/schema/support.graphql*****)**

*type KBArticle { id: ID!, slug: String!, title: String!, summary: String!, bodyMd: String!, category: String!, updatedAt: AWSDateTime! }*  
*type KBSearchResult { id: ID!, slug: String!, title: String!, summary: String!, category: String! }*  
  
*input GuidedFlowContext { category: String!, bookingId: ID, orderId: ID, studioId: ID, city: String, dates: \[AWSDate!\], screenshots: \[AWSURL\] }*  
  
*type TicketResult { ticketId: ID!, externalId: String!, url: AWSURL! }*  
  
*type Query {*  
*kbSearch(q: String!, role: String, category: String): \[KBSearchResult!\]!*  
*kbArticle(slug: String!): KBArticle!*  
*}*  
  
*type Mutation {*  
*recordKBView(articleId: ID!): Boolean!*  
*createSupportTicket(flow: GuidedFlowContext!, readArticleIds: \[ID!\]!): TicketResult!*  
*}*  

**Adapter layer (*****/adapters/helpdesk/\******)**

- **Zendesk**: create ticket (brand, requester, custom fields), attach screenshots, set **priority** & **group** via rules, add internal note with KB reads.
- **Zammad**: same shape via REST; field mapping parity.

## **1.6.7 Ticketing: priorities, routing, SLAs, macros, QA**

**Priorities & SLAs**

- **P0**: payments failing platform‑wide, data loss → page on‑call; **FRT ≤ 30m**.
- **P1**: payout issue, booking within 24–48h → **FRT ≤ 4h**.
- **P2**: general billing/account → **FRT ≤ 1 day**. Targets match your metrics section.

NonTechBlueprint

**Auto‑routing**

- **BILLING/PAYOUT** → Finance queue; **SAFETY** → T&S queue; **TECHNICAL** → Support Eng; rules set by **category + guided flow answers**.

NonTechBlueprint

**Macros (examples)**

- *Refund – partial (Quality ladder step 1)*: template pulls **package spec** + **evidence list** and posts a structured decision; applies ticket tags for later analytics.

NonTechBlueprint

- *Disable Instant Book (pending safety)*: pauses IB via Admin API and posts user‑visible explanation.

NonTechBlueprint

- *Request more info (deliverables)*: asks for missing proof within **24–48h cure** window.

NonTechBlueprint

**QA sampling:** randomly sample **5%** of closed tickets to review **macro adherence, empathy, correctness**.

NonTechBlueprint

**Breach alerts:** SLA timers drive **CloudWatch alarms** → pager for P0; views for P1/P2 backlog.

## **1.6.8 Agent console (context + one‑click outcomes)**

**Context panel** (embedded in Admin): booking lookup (contracts, chat, amendments, receipts, check‑ins, files). **One‑click outcomes**: **refund %**, **issue credit**, **disable Instant Book**, **apply strike**, **request more info** (sends Message Action Card in thread). All are explicitly called out in your plan.

NonTechBlueprint

**Security**: PII redaction on uploads; all support attachments are **secure links** to S3 with short TTL.

NonTechBlueprint

## **1.6.9 Policy playbooks (agent‑facing summaries)**

- **No‑Show/Late**: weigh **check‑in/out** and chat logs above 3rd‑party evidence; decision tree outputs refund tier.

NonTechBlueprint

- **Deliverables missing**: **24–48h cure period** then partial refund ladder.

NonTechBlueprint

- **Quality disputes**: compare to package spec + samples; partial refund tiers; escalate if request \> \$X.

NonTechBlueprint

- **Safety**: **immediate suppression** of risky features (e.g., IB pause on accused); collect details; jurisdiction notes.

NonTechBlueprint

- **Fraud/Chargeback**: assemble **evidence pack** (contracts, chat timestamps, device/IP, checksums).

NonTechBlueprint

- **DMCA**: valid takedown → remove; counter‑notice flow; repeat‑offender handling.

NonTechBlueprint

## **1.6.10 Accessibility & Localization**

- **WCAG‑friendly** articles (semantic headings, alt text, transcripts for video guides, high‑contrast theme). **US English at launch**; IA & data model ready for locale expansion (dates/times, payout wording by region).

NonTechBlueprint

## **1.6.11 Email templates (SES) — text‑only artifacts**

- **Ticket created** — Subject: *\[RastUp\] We received your request (#{ticket})*
- **Action needed** — Subject: *\[Action Required\] Please add info to your request (#{ticket})*
- **Resolved** — Subject: *\[RastUp\] Your request (#{ticket}) is resolved*
- **SLA breach alert (internal)** — Subject: *\[P0 Breach\] {queue} {count} tickets*  
  Each includes **deep links** to the in‑product thread or KB article.

## **1.6.12 Observability & dashboards**

**Events**: *kb.view*, *kb.search*, *support.widget.open*, *support.deflection.shown\|clicked*, *ticket.created\|updated\|resolved*, *sla.breach*, *macro.applied*.  
**KPIs & targets (from your plan)**: **Containment ≥ 70%**, FRT/TTR by priority, CSAT/NPS, reopen & escalation rates, SLA breach count, **Safety incident rate / 100 bookings**, dispute rate, chargeback rate, **cost per ticket**, **tickets / 100 bookings**. Ops cadence: **weekly driver review**, **monthly macro tune‑ups**, **quarterly staffing forecast**.

NonTechBlueprint

## **1.6.13 Cost & scaling**

- **KB**: static rendering + CloudFront → near‑zero marginal cost.
- **Search**: Typesense small cluster (2–3 nodes) with nightly snapshot; shard by locale when needed.
- **Ticketing**: start with **3–5 Zendesk seats**; scale seats as tickets/100 bookings rises. Keep **Zammad** adapter ready if vendor costs outweigh value.
- **Goal alignment**: deflection + macros drive lower **cost/ticket** as volume grows, per your KPI section.

NonTechBlueprint

## **1.6.14 Tests (representative)**

3036. **Deflection path**: search → article read → still contact; ticket contains **readArticleIds** and context.

NonTechBlueprint

3037. **Auto‑routing**: payout issue guided flow → Finance queue; safety flag → T&S queue.

NonTechBlueprint

3038. **SLA timers**: P1 FRT timer triggers alert at threshold; dashboard increments **breach count**.

NonTechBlueprint

3039. **One‑click outcomes**: refund %, strike, disable IB — write audit, update booking/trust flags.

NonTechBlueprint

3040. **QA sampling**: 5% of closed tickets move to QA queue; results logged.

NonTechBlueprint

3041. **Accessibility**: axe‑core CI for Help Center pages; screen reader announces article landmarks.

NonTechBlueprint

3042. **Localization readiness**: article save in new locale indexes under filtered search; redirects work via *kb_redirect*.

## **1.6.15 Artifacts (copy‑pasteable into your plan)**

- *db/migrations/016_kb.sql* — KB schema above.
- *api/schema/support.graphql* — Queries/Mutations above.
- *web/app/help/\[category\]/\[slug\]/page.tsx* — SSR page + JSON‑LD.
- *web/components/SupportWidget/\** — widget + guided flows.
- *adapters/helpdesk/zendesk.ts* & *adapters/helpdesk/zammad.ts* — ticket creators.
- *ops/runbooks/support-sla-breach.md* — P0/P1/P2 response playbook.
- *ops/macros/\*.md* — macro definitions aligned to playbooks.
- *dashboards/support/README.md* — metric definitions & queries.

## **1.6.16 Acceptance criteria — mark §1.6 FINAL only when ALL true**

3051. Help Center live with defined **IA**, article pattern, SEO, accessibility; **monthly top‑50 review** process documented.

NonTechBlueprint

3052. Support Widget runs **guided flows**, shows **deflection**, and includes **readArticleIds** + context in created tickets.

NonTechBlueprint

3053. Ticketing wired with **priorities, SLAs, auto‑routing, macros**, QA sampling, and **breach alerts**.

NonTechBlueprint

3054. Agent console in Admin shows booking context and supports **one‑click outcomes** with audit.

NonTechBlueprint

3055. Dashboards show all KPIs from your plan; **Containment ≥ 70%**, **FRT P1 ≤ 4h; P2 ≤ 1 day** at steady state.

NonTechBlueprint

3056. Costs track to plan (few seats, serverless KB/search); **Zammad adapter** validated as fallback.
