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

let leafletPromise: Promise<void> | null = null
let leafletDrawPromise: Promise<void> | null = null

type MapInstance = {
  map: any
  container: HTMLElement
  building: boolean
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

function ensureLeafletDraw(): Promise<void> {
  if (!leafletDrawPromise) {
    leafletDrawPromise = (async () => {
      await ensureLeaflet()
      await loadStylesheet("sl-leaflet-draw-css", "https://unpkg.com/leaflet-draw@1.0.4/dist/leaflet.draw.css")
      if (!(window as any).L?.Control?.Draw) {
        await loadScript("https://unpkg.com/leaflet-draw@1.0.4/dist/leaflet.draw.js")
      }
    })()
  }
  return leafletDrawPromise
}

function renderTileLayer(map: any, node: MapNode) {
  const opts = node.props.options ? camelizeKeys(node.props.options as Record<string, unknown>) : {}
  L.tileLayer(String(node.props.url), opts).addTo(map)
}

function renderMarker(map: any, node: MapNode, setTrigger?: (k: string, v: unknown) => void) {
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

function renderGeoJson(map: any, node: MapNode, setTrigger?: (k: string, v: unknown) => void) {
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
            object: { kind: "geojson", id: node.id, feature: feature },
          },
          timestamp: Date.now(),
        })
      })
    } : undefined,
  })
  layer.addTo(map)
}

function renderCircleMarker(map: any, node: MapNode, setTrigger?: (k: string, v: unknown) => void) {
  const opts = node.props.options ? camelizeKeys(node.props.options as Record<string, unknown>) : {}
  const cm = L.circleMarker(node.props.location as [number, number], { ...opts, bubblingMouseEvents: false })
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
}

function renderLayer(map: any, node: MapNode, setTrigger?: (k: string, v: unknown) => void) {
  switch (node.kind) {
    case "tile_layer": renderTileLayer(map, node); break
    case "marker": renderMarker(map, node, setTrigger); break
    case "geojson": renderGeoJson(map, node, setTrigger); break
    case "circle_marker": renderCircleMarker(map, node, setTrigger); break
  }
}

function mountDraw(map: any, node: MapNode, setTrigger: (k: string, v: unknown) => void) {
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

function mountLayerControl(map: any, node: MapNode) {
  L.control.layers(undefined, undefined, {
    position: node.props.position ?? "topright",
  }).addTo(map)
}

const StFoliumVnext: FrontendRenderer<ComponentState, ComponentData> = (args) => {
  const { parentElement, data, setStateValue, setTriggerValue } = args
  const { spec, height } = data
  const root = parentElement as HTMLElement
  const h = height ?? 500
  const mapId = spec.map.id

  const inst = instances.get(mapId)

  if (inst && inst.map) {
    if (inst.container.parentElement !== root) {
      root.appendChild(inst.container)
    }
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
    return () => {}
  }

  if (inst && inst.building) {
    if (inst.container.parentElement !== root) {
      root.appendChild(inst.container)
    }
    return () => {}
  }

  const container = document.createElement("div")
  container.style.width = "100%"
  container.style.height = `${h}px`
  root.appendChild(container)

  const placeholder: MapInstance = { map: null, container, building: true }
  instances.set(mapId, placeholder)

  const hasDraw = spec.plugins.some((p) => p.kind === "draw")
  const loadPromise = hasDraw ? ensureLeafletDraw() : ensureLeaflet()

  loadPromise.then(() => {
    const current = instances.get(mapId)
    if (current !== placeholder) return

    const map = L.map(container, { zoomControl: true })
      .setView(spec.map.center ?? [0, 0], spec.map.zoom ?? 2)

    for (const node of spec.layers) renderLayer(map, node, setTriggerValue)
    for (const ctrl of spec.controls) {
      if (ctrl.kind === "layer_control") mountLayerControl(map, ctrl)
    }
    for (const plugin of spec.plugins) {
      if (plugin.kind === "draw") mountDraw(map, plugin, setTriggerValue)
    }

    placeholder.map = map
    placeholder.building = false

    function syncViewState() {
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
