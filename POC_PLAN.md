# streamlit-folium CCv2 POC plan

## Goals
- Remove the most brittle runtime hacks from the rendering path.
- Create a clear separation between Python-side serialization and frontend-side rendering/event collection.
- Establish an extension model so new Folium plugins can be added via adapters instead of core rewrites.

## Current pain points
- V1 component API and iframe model.
- Frontend relies on global `window` state and direct `document.head/body` mutation.
- Arbitrary script execution via `eval()` and dynamic script tag injection.
- Plugin support is encoded as ad hoc JS strings (`feature_group`, `layer_control`) instead of typed payloads.
- Tests are coupled to iframe behavior.

## Target architecture
### 1. Python serializer layer
Introduce a serializer module that produces a `MapSpec` object with:
- `html`
- `header_html`
- `base_script`
- `assets`
- `plugins`
- `initial_view`
- `defaults`
- `options`

### 2. Frontend runtime layer
Introduce a frontend runtime that:
- Mounts one map instance per component instance.
- Tracks state in instance-local objects instead of `window` globals.
- Loads and deduplicates assets through a single helper.
- Applies plugin adapters from typed specs.
- Emits typed interaction events.

### 3. Plugin adapter registry
Introduce a registry with adapters like:
- `feature_group`
- `layer_control`

Each adapter should define:
- Python serializer input contract.
- Frontend apply hook.
- Optional event extraction hook.

## POC scope
- Keep the existing public `st_folium()` API for now.
- Add a new internal serializer module and typed payloads.
- Add a frontend-side runtime helper module to reduce globals.
- Convert dynamic `feature_group` and `layer_control` handling to a plugin-spec array.
- Do not fully migrate to CCv2 yet if it would break the package in one step; instead create a seam that makes the later migration straightforward.

## POC deliverables
- New internal serializer/types module.
- Refactored frontend runtime with instance-local state abstraction.
- Plugin adapter registry for at least feature groups and layer control.
- Existing tests still passing or narrowed to a stable subset if some are v1-specific.

## Follow-up phases
1. Replace v1 transport with CCv2 transport.
2. Remove iframe assumptions from tests.
3. Convert remaining script/header/html injection to packaged assets and typed mount data.
4. Add plugin authoring docs and examples.
