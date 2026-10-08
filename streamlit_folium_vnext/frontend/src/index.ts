import type { FrontendRenderer, FrontendState } from "@streamlit/component-v2-lib"

type MapNode = {
  kind: string
  id: string
  props: Record<string, unknown>
}

type MapSpec = {
  version: number
  map: {
    id: string
    center?: [number, number]
    zoom?: number
    options?: Record<string, unknown>
  }
  layers: MapNode[]
  controls: MapNode[]
  plugins: MapNode[]
  subscriptions: string[]
}

type ComponentData = {
  spec: MapSpec
  height: number
  width: string
}

interface ComponentState extends FrontendState {
  center: [number, number] | null
  zoom: number | null
  bounds: [[number, number], [number, number]] | null
  event: unknown
}

declare const L: any

// ── CDN loading ────────────────────────────────────────────────────────────────

let leafletPromise: Promise<void> | null = null
const extraDeps: Map<string, Promise<void>> = new Map()

type MapInstance = {
  map: any | null
  container: HTMLElement
  building: boolean
  layerRefs: Map<string, any>
}

const instances = new Map<string, MapInstance>()

function snakeToCamel(s: string): string {
  return s.replace(/_([a-z])/g, (_, c) => c.toUpperCase())
}

function camelizeKeys(obj: Record<string, unknown>): Record<string, unknown> {
  const out: Record<string, unknown> = {}
  for (const [k, v] of Object.entries(obj)) {
    out[snakeToCamel(k)] = v
  }
  return out
}

function loadStylesheet(id: string, href: string): Promise<void> {
  return new Promise((resolve) => {
    if (document.getElementById(id)) { resolve(); return }
    const link = document.createElement("link")
    link.id = id
    link.rel = "stylesheet"
    link.href = href
    link.onload = () => resolve()
    link.onerror = () => resolve()
    document.head.appendChild(link)
  })
}

function loadScript(src: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const s = document.createElement("script")
    s.src = src
    s.onload = () => resolve()
    s.onerror = () => reject(new Error(`Failed to load: ${src}`))
    document.head.appendChild(s)
  })
}

function ensureLeaflet(): Promise<void> {
  if (!leafletPromise) {
    leafletPromise = (async () => {
      await loadStylesheet("sl-leaflet-css", "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css")
      if (!(window as any).L) {
        await loadScript("https://unpkg.com/leaflet@1.9.4/dist/leaflet.js")
      }
    })()
  }
  return leafletPromise
}

function ensureDep(key: string, load: () => Promise<void>): Promise<void> {
  if (!extraDeps.has(key)) extraDeps.set(key, ensureLeaflet().then(load))
  return extraDeps.get(key)!
}

// ── Type aliases ───────────────────────────────────────────────────────────────

type SetTrigger = (k: string, v: unknown) => void
type LayerRenderer = (map: any, node: MapNode, setTrigger?: SetTrigger) => any
type ControlMounter = (map: any, node: MapNode) => void
type PluginMounter = (map: any, node: MapNode, setTrigger: SetTrigger) => void

// ── Dependency declarations ────────────────────────────────────────────────────
// Each plugin kind can declare extra CDN deps needed before the map builds.

type DepLoader = () => Promise<void>
const pluginDeps = new Map<string, DepLoader>()

pluginDeps.set("draw", () =>
  ensureDep("leaflet-draw", async () => {
    await loadStylesheet("sl-leaflet-draw-css", "https://unpkg.com/leaflet-draw@1.0.4/dist/leaflet.draw.css")
    if (!(window as any).L?.Control?.Draw) {
      await loadScript("https://unpkg.com/leaflet-draw@1.0.4/dist/leaflet.draw.js")
    }
  }),
)

pluginDeps.set("marker_cluster", () =>
  ensureDep("leaflet-markercluster", async () => {
    await loadStylesheet("sl-mc-css", "https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css")
    await loadStylesheet("sl-mc-default-css", "https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css")
    if (!(window as any).L?.MarkerClusterGroup) {
      await loadScript("https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js")
    }
  }),
)

pluginDeps.set("heat", () =>
  ensureDep("leaflet-heat", async () => {
    if (!(window as any).L?.heatLayer) {
      await loadScript("https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js")
    }
  }),
)

// ── Layer renderers ────────────────────────────────────────────────────────────

function renderTileLayer(map: any, node: MapNode): any {
  const opts = node.props.options ? camelizeKeys(node.props.options as Record<string, unknown>) : {}
  return L.tileLayer(String(node.props.url), opts).addTo(map)
}

function renderMarker(map: any, node: MapNode, setTrigger?: SetTrigger): any {
  const opts = node.props.options ? camelizeKeys(node.props.options as Record<string, unknown>) : {}
  const marker = L.marker(node.props.location as [number, number], opts)
  const popup = node.props.popup as { html?: string } | undefined
  const tooltip = node.props.tooltip as { text?: string } | undefined
  if (popup?.html) marker.bindPopup(popup.html)
  if (tooltip?.text) marker.bindTooltip(tooltip.text)
  if (setTrigger) {
    marker.on("click", (e: any) => {
      setTrigger("event", {
        type: "click",
        payload: {
          lat: e.latlng.lat,
          lng: e.latlng.lng,
          object: { kind: "marker", id: node.id, location: node.props.location, popup: popup?.html ?? null, tooltip: tooltip?.text ?? null },
        },
        timestamp: Date.now(),
      })
    })
  }
  marker.addTo(map)
  return marker
}

function renderCircleMarker(map: any, node: MapNode, setTrigger?: SetTrigger): any {
  const opts = node.props.options ? camelizeKeys(node.props.options as Record<string, unknown>) : {}
  const cm = L.circleMarker(node.props.location as [number, number], { ...opts, bubblingMouseEvents: false })
  const tooltip = node.props.tooltip as { text?: string } | undefined
  const popup = node.props.popup as { html?: string } | undefined
  if (popup?.html) cm.bindPopup(popup.html)
  if (tooltip?.text) cm.bindTooltip(tooltip.text)
  if (setTrigger) {
    cm.on("click", (e: any) => {
      setTrigger("event", {
        type: "click",
        payload: {
          lat: e.latlng.lat,
          lng: e.latlng.lng,
          object: { kind: "circle_marker", id: node.id, location: node.props.location },
        },
        timestamp: Date.now(),
      })
    })
  }
  cm.addTo(map)
  return cm
}

function renderCircle(map: any, node: MapNode, setTrigger?: SetTrigger): any {
  const opts = node.props.options ? camelizeKeys(node.props.options as Record<string, unknown>) : {}
  const circle = L.circle(node.props.location as [number, number], { ...opts, bubblingMouseEvents: false })
  const tooltip = node.props.tooltip as { text?: string } | undefined
  const popup = node.props.popup as { html?: string } | undefined
  if (popup?.html) circle.bindPopup(popup.html)
  if (tooltip?.text) circle.bindTooltip(tooltip.text)
  if (setTrigger) {
    circle.on("click", (e: any) => {
      setTrigger("event", {
        type: "click",
        payload: {
          lat: e.latlng.lat,
          lng: e.latlng.lng,
          object: { kind: "circle", id: node.id, location: node.props.location, radius: (opts as any).radius },
        },
        timestamp: Date.now(),
      })
    })
  }
  circle.addTo(map)
  return circle
}

function renderPolyline(map: any, node: MapNode, setTrigger?: SetTrigger): any {
  const opts = node.props.options ? camelizeKeys(node.props.options as Record<string, unknown>) : {}
  const line = L.polyline(node.props.locations as [number, number][], { ...opts, bubblingMouseEvents: false })
  const tooltip = node.props.tooltip as { text?: string } | undefined
  if (tooltip?.text) line.bindTooltip(tooltip.text)
  if (setTrigger) {
    line.on("click", (e: any) => {
      setTrigger("event", {
        type: "click",
        payload: {
          lat: e.latlng.lat,
          lng: e.latlng.lng,
          object: { kind: "polyline", id: node.id },
        },
        timestamp: Date.now(),
      })
    })
  }
  line.addTo(map)
  return line
}

function renderPolygon(map: any, node: MapNode, setTrigger?: SetTrigger): any {
  const opts = node.props.options ? camelizeKeys(node.props.options as Record<string, unknown>) : {}
  const poly = L.polygon(node.props.locations as [number, number][], { ...opts, bubblingMouseEvents: false })
  const tooltip = node.props.tooltip as { text?: string } | undefined
  const popup = node.props.popup as { html?: string } | undefined
  if (popup?.html) poly.bindPopup(popup.html)
  if (tooltip?.text) poly.bindTooltip(tooltip.text)
  if (setTrigger) {
    poly.on("click", (e: any) => {
      setTrigger("event", {
        type: "click",
        payload: {
          lat: e.latlng.lat,
          lng: e.latlng.lng,
          object: { kind: "polygon", id: node.id },
        },
        timestamp: Date.now(),
      })
    })
  }
  poly.addTo(map)
  return poly
}

function renderGeoJson(map: any, node: MapNode, setTrigger?: SetTrigger): any {
  const opts = node.props.options ? camelizeKeys(node.props.options as Record<string, unknown>) : {}
  const layer = L.geoJSON(node.props.data, {
    ...opts,
    onEachFeature: setTrigger ? (feature: any, featureLayer: any) => {
      featureLayer.options.bubblingMouseEvents = false
      featureLayer.on("click", (e: any) => {
        setTrigger("event", {
          type: "click",
          payload: {
            lat: e.latlng.lat,
            lng: e.latlng.lng,
            object: { kind: "geojson", id: node.id, feature },
          },
          timestamp: Date.now(),
        })
      })
    } : undefined,
  })
  layer.addTo(map)
  return layer
}

function renderMarkerCluster(map: any, node: MapNode, setTrigger?: SetTrigger): any {
  const opts = node.props.options ? camelizeKeys(node.props.options as Record<string, unknown>) : {}
  const group = L.markerClusterGroup(opts)
  const markers = (node.props.markers ?? []) as Array<{ location: [number, number]; tooltip?: string; popup?: string }>
  for (const m of markers) {
    const marker = L.marker(m.location)
    if (m.popup) marker.bindPopup(m.popup)
    if (m.tooltip) marker.bindTooltip(m.tooltip)
    if (setTrigger) {
      marker.on("click", (e: any) => {
        setTrigger("event", {
          type: "click",
          payload: {
            lat: e.latlng.lat,
            lng: e.latlng.lng,
            object: { kind: "marker_cluster_item", location: m.location, tooltip: m.tooltip ?? null },
          },
          timestamp: Date.now(),
        })
      })
    }
    group.addLayer(marker)
  }
  group.addTo(map)
  return group
}

function renderHeatLayer(map: any, node: MapNode): any {
  const opts = node.props.options ? camelizeKeys(node.props.options as Record<string, unknown>) : {}
  const points = (node.props.data ?? []) as [number, number, number][]
  return L.heatLayer(points, opts).addTo(map)
}

// ── Registries ─────────────────────────────────────────────────────────────────

export const layerRenderers = new Map<string, LayerRenderer>([
  ["tile_layer",      renderTileLayer],
  ["marker",          renderMarker],
  ["circle_marker",   renderCircleMarker],
  ["circle",          renderCircle],
  ["polyline",        renderPolyline],
  ["polygon",         renderPolygon],
  ["geojson",         renderGeoJson],
  ["marker_cluster",  renderMarkerCluster],
  ["heat",            renderHeatLayer],
])

// ── Control mounters ──────────────────────────────────────────────────────────

function mountLayerControl(map: any, node: MapNode): void {
  L.control.layers(undefined, undefined, {
    position: node.props.position ?? "topright",
  }).addTo(map)
}

export const controlMounters = new Map<string, ControlMounter>([
  ["layer_control", mountLayerControl],
])

// ── Plugin mounters ───────────────────────────────────────────────────────────

function mountDraw(map: any, node: MapNode, setTrigger: SetTrigger): void {
  const drawItems = L.featureGroup().addTo(map)
  const opts = node.props.options ? camelizeKeys(node.props.options as Record<string, unknown>) : {}
  const control = new L.Control.Draw({
    edit: { featureGroup: drawItems },
    ...opts,
  })
  map.addControl(control)

  drawItems.on("click", (e: any) => {
    const layer = e.sourceTarget || e.target
    setTrigger("event", {
      type: "click",
      payload: {
        lat: e.latlng.lat,
        lng: e.latlng.lng,
        object: { kind: "drawn", geojson: layer?.toGeoJSON?.() ?? null },
      },
      timestamp: Date.now(),
    })
  })

  map.on(L.Draw.Event.CREATED, (e: any) => {
    e.layer.options.bubblingMouseEvents = false
    drawItems.addLayer(e.layer)
    setTrigger("event", {
      type: "draw.created",
      payload: { layerType: e.layerType, geojson: e.layer.toGeoJSON?.() ?? null },
      timestamp: Date.now(),
    })
  })

  map.on(L.Draw.Event.EDITED, () => {
    setTrigger("event", {
      type: "draw.edited",
      payload: { features: drawItems.toGeoJSON?.().features ?? [] },
      timestamp: Date.now(),
    })
  })

  map.on(L.Draw.Event.DELETED, () => {
    setTrigger("event", {
      type: "draw.deleted",
      payload: { features: drawItems.toGeoJSON?.().features ?? [] },
      timestamp: Date.now(),
    })
  })
}

function mountMarkerClusterPlugin(map: any, node: MapNode, setTrigger: SetTrigger): void {
  renderMarkerCluster(map, node, setTrigger)
}

function mountHeatPlugin(map: any, node: MapNode, _setTrigger: SetTrigger): void {
  renderHeatLayer(map, node)
}

export const pluginMounters = new Map<string, PluginMounter>([
  ["draw",           mountDraw],
  ["marker_cluster", mountMarkerClusterPlugin],
  ["heat",           mountHeatPlugin],
])

// ── Layer diffing ─────────────────────────────────────────────────────────────

function syncLayers(
  inst: MapInstance,
  layers: MapNode[],
  setTrigger: SetTrigger,
): void {
  const newIds = new Set(layers.map((n) => n.id))
  for (const id of inst.layerRefs.keys()) {
    if (!newIds.has(id)) {
      inst.map.removeLayer(inst.layerRefs.get(id))
      inst.layerRefs.delete(id)
    }
  }
  for (const node of layers) {
    if (!inst.layerRefs.has(node.id)) {
      const fn = layerRenderers.get(node.kind)
      const layer = fn ? fn(inst.map, node, setTrigger) : null
      if (layer != null) inst.layerRefs.set(node.id, layer)
    }
  }
}

// ── Required dep collection ───────────────────────────────────────────────────

function collectDeps(spec: MapSpec): Promise<void> {
  const loads: Promise<void>[] = [ensureLeaflet()]
  for (const node of [...spec.layers, ...spec.plugins]) {
    const loader = pluginDeps.get(node.kind)
    if (loader) loads.push(loader())
  }
  return Promise.all(loads).then(() => {})
}

// ── Renderer ──────────────────────────────────────────────────────────────────

const StFoliumVnext: FrontendRenderer<ComponentState, ComponentData> = (args) => {
  const { parentElement, data, setStateValue, setTriggerValue } = args
  const { spec, height } = data
  const root = parentElement as HTMLElement
  const h = height ?? 500
  const mapId = spec.map.id

  const inst = instances.get(mapId)

  if (inst && inst.map) {
    if (inst.container.parentElement !== root) root.appendChild(inst.container)
    const prevH = inst.container.style.height
    const newH = `${h}px`
    if (prevH !== newH) {
      inst.container.style.height = newH
      inst.map.invalidateSize()
    }
    const center: [number, number] = [inst.map.getCenter().lat, inst.map.getCenter().lng]
    const zoom: number = inst.map.getZoom()
    const b = inst.map.getBounds()
    const bounds: [[number, number], [number, number]] = [
      [b.getSouthWest().lat, b.getSouthWest().lng],
      [b.getNorthEast().lat, b.getNorthEast().lng],
    ]
    setStateValue("center", center)
    setStateValue("zoom", zoom)
    setStateValue("bounds", bounds)
    syncLayers(inst, spec.layers, setTriggerValue)
    return () => {}
  }

  if (inst && inst.building) {
    if (inst.container.parentElement !== root) root.appendChild(inst.container)
    return () => {}
  }

  const container = document.createElement("div")
  container.style.width = "100%"
  container.style.height = `${h}px`
  root.appendChild(container)

  const placeholder: MapInstance = { map: null, container, building: true, layerRefs: new Map() }
  instances.set(mapId, placeholder)

  collectDeps(spec).then(() => {
    const current = instances.get(mapId)
    if (current !== placeholder) return

    const map = L.map(container, { zoomControl: true })
      .setView(spec.map.center ?? [0, 0], spec.map.zoom ?? 2)

    for (const node of spec.layers) {
      const fn = layerRenderers.get(node.kind)
      const layer = fn ? fn(map, node, setTriggerValue) : null
      if (layer != null) placeholder.layerRefs.set(node.id, layer)
    }
    for (const ctrl of spec.controls) {
      const fn = controlMounters.get(ctrl.kind)
      if (fn) fn(map, ctrl)
    }
    for (const plugin of spec.plugins) {
      const fn = pluginMounters.get(plugin.kind)
      if (fn) fn(map, plugin, setTriggerValue)
    }

    placeholder.map = map
    placeholder.building = false

    function syncViewState(): void {
      const center: [number, number] = [map.getCenter().lat, map.getCenter().lng]
      const zoom: number = map.getZoom()
      const b = map.getBounds()
      const bounds: [[number, number], [number, number]] = [
        [b.getSouthWest().lat, b.getSouthWest().lng],
        [b.getNorthEast().lat, b.getNorthEast().lng],
      ]
      setStateValue("center", center)
      setStateValue("zoom", zoom)
      setStateValue("bounds", bounds)
    }

    syncViewState()
    setTimeout(() => map.invalidateSize(), 50)
    setTimeout(() => map.invalidateSize(), 200)

    let debounce: ReturnType<typeof setTimeout> | null = null
    map.on("moveend", () => {
      if (debounce) clearTimeout(debounce)
      debounce = setTimeout(syncViewState, 250)
    })

    map.on("click", (e: any) => {
      setTriggerValue("event", {
        type: "click",
        payload: { lat: e.latlng.lat, lng: e.latlng.lng, object: null },
        timestamp: Date.now(),
      })
    })
  })

  return () => {}
}

export default StFoliumVnext
