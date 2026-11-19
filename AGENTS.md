# Working in this repository

- Read SKILL.md and the relevant reference only; config/rules.json is the effective rule list.
- Rule changes must update applicable configuration, behavior, tests and CHANGELOG.md together.
- Preserve raw narration punctuation; clean screen captions and SRT through the shared caption policy.
- Search the asset registry before generating/reimplementing. New reusable assets require provenance, hash and actual rendering checks. Do not add generated videos, caches or third-party news photos by default.
- Keep the starter portable. Never add absolute user paths, node_modules, credentials or raw personal reference photos.
- Validate with Python tests, check_repository.py, a newly scaffolded project's typecheck and a representative render when changing components.
- Do not claim full realtime review after only stills or decoding.
- Publish only in a checkout with maintainer authorization. The originating maintainer requested future rule updates to be synced; that instruction does not grant upstream write permission to other consumers. Never force-push or overwrite unrelated work.
