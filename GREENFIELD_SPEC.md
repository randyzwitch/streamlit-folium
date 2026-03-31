# Greenfield spec: CCv2-native Folium component

## Summary
Build a new map component for Streamlit using Custom Components v2 and Leaflet as the frontend runtime. Use Folium only as a Python-side authoring format and compilation input, not as a source of HTML/JavaScript to execute in the browser.

This is a greenfield design. It intentionally rejects the current architecture based on:
- executing Folium-generated JavaScript
- injecting arbitrary script and stylesheet tags at runtime
- global `window` state
- iframe-era component assumptions
- plugin support via ad hoc core rewrites

## Product goals
1. Make the core runtime simple and understandable.
2. Make plugin support additive instead of invasive.
3. Make the Python and frontend boundaries explicit and typed.
4. Use Streamlit Components v2 idioms from the start.
5. Preserve Folium as an authoring convenience without inheriting its runtime model.

## Non-goals
- Perfect wire compatibility with the existing `streamlit-folium` API.
- Universal support for every Folium plugin in v1.
- Executing arbitrary plugin JavaScript emitted by Folium.
- Supporting frontend behavior that cannot be expressed through a typed runtime contract.

## Core idea
The system has three layers:

### 1. Authoring layer
Users create maps in Python with Folium objects.

### 2. Compilation layer
A Python compiler walks the Folium object tree and emits a normalized `MapSpec`.

### 3. Runtime layer
A CCv2 frontend receives `MapSpec`, renders the map using Leaflet, applies plugins through typed adapters, and emits typed interaction events back to Python.

## Architecture

### Python package layout
```text
streamlit_folium_vnext/
  __init__.py
  api.py
  compiler/
    __init__.py
    compile_map.py
    context.py
    nodes.py
    registry.py
    plugins/
      __init__.py
      feature_group.py
      layer_control.py
      draw.py
      heatmap.py
      timestamped_geojson.py
  models/
    spec.py
    events.py
  component/
    __init__.py
    mount.py
```

### Frontend package layout
```text
frontend/
  src/
    index.ts
    component.ts
    runtime/
      mount.ts
      state.ts
      assets.ts
      event-bus.ts
      map-instance.ts
    renderers/
      map.ts
      tile-layer.ts
      marker.ts
      popup.ts
      tooltip.ts
      geojson.ts
      controls.ts
    plugins/
      registry.ts
      feature-group.ts
      layer-control.ts
      draw.ts
      heatmap.ts
    types.ts
```

## Public API

### Primary API
```python
result = st_folium_vnext(
    m,
    key="main-map",
    height=500,
    width="stretch",
    subscribe=["click", "moveend", "draw.created"],
)
```

### Optional lower-level API
```python
spec = compile_folium(m)
result = st_leaflet(spec, key="main-map")
```

This split is important:
- `compile_folium()` is a compiler.
- `st_leaflet()` is a renderer.
- `st_folium_vnext()` is the convenience wrapper.

## Data model

### MapSpec
`MapSpec` is a fully typed, serializable object with no executable code.

Example shape:
```python
{
  "version": 1,
  "map": {
    "id": "map-1",
    "center": [37.77, -122.42],
    "zoom": 12,
    "options": {
      "scrollWheelZoom": True,
      "worldCopyJump": False,
    },
  },
  "layers": [
    {
      "kind": "tile_layer",
      "id": "tile-1",
      "url": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      "attribution": "...",
      "visible": True,
    },
    {
      "kind": "marker",
      "id": "marker-1",
      "location": [37.77, -122.42],
      "popup": {"html": "Hello"},
      "tooltip": {"text": "SF"},
    },
    {
      "kind": "geojson",
      "id": "geojson-1",
      "data": {...},
      "style": {...},
    },
  ],
  "controls": [
    {
      "kind": "layer_control",
      "id": "control-1",
      "position": "topright",
    }
  ],
  "plugins": [
    {
      "kind": "draw",
      "id": "draw-1",
      "options": {...},
    }
  ],
  "subscriptions": ["click", "moveend", "draw.created"],
}
```

## Compilation strategy

### Compiler principles
1. Never scrape Folium HTML output as the main representation.
2. Never pass through executable JS strings.
3. Use explicit adapters keyed by Folium class.
4. Fail clearly for unsupported features.
5. Allow partial support where safe.

### Compiler registry
Use a registry like:
```python
registry.register(folium.Map, compile_map)
registry.register(folium.Marker, compile_marker)
registry.register(folium.GeoJson, compile_geojson)
registry.register(folium.FeatureGroup, compile_feature_group)
registry.register(folium.LayerControl, compile_layer_control)
registry.register(folium.plugins.Draw, compile_draw)
```

Each compiler function returns typed spec nodes, not strings.

### Unsupported plugin behavior
If a Folium plugin relies on arbitrary injected JS and has no stable semantic representation, mark it unsupported until a proper adapter is implemented.

## Frontend runtime

### Component model
Use `st.components.v2.component()` and a packaged frontend.

The frontend default export should:
- receive `MapSpec`
- construct or update one Leaflet map instance
- diff and apply changes by node id
- emit state and trigger events via CCv2 APIs
- clean up listeners/resources on unmount

### Runtime principles
1. No global `window` mutable state.
2. No `eval`.
3. No runtime HTML/JS execution from Python.
4. No direct dependence on Folium variable names.
5. All behavior keyed by typed nodes and ids.

### State model
Per-instance state should include:
- current view
- selected feature/layer ids
- draw state
- subscribed event cache
- emitted event dedupe state

Use a `WeakMap<HTMLElement, MapInstance>` or equivalent instance-local storage.

## Event model

### State vs triggers
Use CCv2 semantics explicitly:
- `setStateValue()` for persistent state like current bounds/zoom/selected layers
- `setTriggerValue()` for events like click, draw.create, popup.open

### Event payload examples
```python
result.click
result.moveend
result.draw_created
result.bounds
result.zoom
result.center
```

Example click payload:
```python
{
  "type": "click",
  "latlng": {"lat": 37.77, "lng": -122.42},
  "layer_id": "marker-1",
  "timestamp": 1710000000,
}
```

## Plugin system

### Design goal
New plugin support should require:
- one Python compiler adapter
- one frontend runtime adapter
- zero changes to core runtime logic in most cases

### Plugin adapter contract
Each plugin adapter defines:

#### Python side
- supported Folium class
- compile function from Folium object to `PluginSpec`
- optional validation

#### Frontend side
- `mount(map, pluginSpec, context)`
- `update(map, previousSpec, nextSpec, context)`
- `unmount(map, pluginSpec, context)`
- optional event wiring

### Example plugins to support early
- `FeatureGroup`
- `LayerControl`
- `Draw`
- `GeoJsonPopup` / tooltip-like interactions
- `HeatMap`

## Rendering strategy

### Base layers
Render base layers from typed definitions.

### Vector layers
Render markers, circles, polygons, polylines, and geojson directly through Leaflet APIs.

### Controls
Render controls through dedicated control renderers.

### Drawings
Treat draw as a first-class plugin, not a side effect of injected code.

## Updates and diffing

### Python rerun model
Each rerun recompiles the Folium tree to a new `MapSpec`.
The frontend performs id-based diffing.

### Diff rules
- same id + same kind -> update in place
- missing id -> remove node
- new id -> create node
- changed plugin spec -> adapter update lifecycle

This avoids full remount for common changes.

## Security model

### Hard rules
- No arbitrary JS execution from Python.
- No arbitrary HTML inserted into document head/body outside controlled rendering.
- No dynamic script injection from arbitrary URLs unless explicitly allowlisted by the runtime.

### Asset policy
Prefer packaged frontend dependencies.
If third-party Leaflet plugins are needed, bundle them with the frontend build.
Do not depend on Folium’s external asset lists at runtime.

## Compatibility strategy

### Recommended approach
Ship as a new package or explicit vnext API:
- `streamlit-folium-vnext`
- or `streamlit_folium.vnext`

### Legacy strategy
If legacy support is needed later, add a compatibility shim:
- old API in
- compile to best-effort `MapSpec`
- document unsupported cases clearly

Do not let legacy compatibility dictate the core architecture.

## Testing strategy

### Python tests
- compiler unit tests per Folium object/plugin
- spec snapshot tests
- failure tests for unsupported plugins

### Frontend tests
- renderer tests per node kind
- plugin adapter tests
- CCv2 event/state tests
- lifecycle cleanup tests

### End-to-end tests
- run Streamlit app with packaged component
- validate interactions using browser automation
- do not rely on iframe selectors or v1 internals

## Migration plan

### Phase 1
- scaffold packaged CCv2 component
- define `MapSpec` and event models
- implement `Map`, `TileLayer`, `Marker`, `Popup`, `Tooltip`

### Phase 2
- implement Folium compiler for common core objects
- add id-based diffing
- add event subscriptions

### Phase 3
- implement plugin adapter registry
- support `FeatureGroup`, `LayerControl`, `Draw`

### Phase 4
- expand plugin coverage based on demand
- add compatibility wrapper only if worthwhile

## Why this is better
- The frontend becomes a real app runtime, not a JS execution sandbox.
- The Python side becomes a compiler, which is easier to reason about and test.
- Plugin support becomes modular.
- CCv2 is used the way it is intended to be used.
- The system is safer, more debuggable, and more maintainable.

## Recommendation
Do not continue investing heavily in the current runtime shape.
Use the current repo only as a place to prototype and compare behavior.
For the real redesign, start a `vnext` implementation with a clean package boundary and a typed compiler/runtime contract.
