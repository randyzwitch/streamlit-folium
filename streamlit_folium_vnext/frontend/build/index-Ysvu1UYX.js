let D = null;
const C = /* @__PURE__ */ new Map(), M = /* @__PURE__ */ new Map();
function G(e) {
  return e.replace(/_([a-z])/g, (t, a) => a.toUpperCase());
}
function f(e) {
  const t = {};
  for (const [a, l] of Object.entries(e))
    t[G(a)] = l;
  return t;
}
function w(e, t) {
  return new Promise((a) => {
    if (document.getElementById(e)) {
      a();
      return;
    }
    const l = document.createElement("link");
    l.id = e, l.rel = "stylesheet", l.href = t, l.onload = () => a(), l.onerror = () => a(), document.head.appendChild(l);
  });
}
function b(e) {
  return new Promise((t, a) => {
    const l = document.createElement("script");
    l.src = e, l.onload = () => t(), l.onerror = () => a(new Error(`Failed to load: ${e}`)), document.head.appendChild(l);
  });
}
function j() {
  return D || (D = (async () => {
    await w("sl-leaflet-css", "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"), window.L || await b("https://unpkg.com/leaflet@1.9.4/dist/leaflet.js");
  })()), D;
}
function T(e, t) {
  return C.has(e) || C.set(e, j().then(t)), C.get(e);
}
const v = /* @__PURE__ */ new Map();
v.set(
  "draw",
  () => T("leaflet-draw", async () => {
    var e, t;
    await w("sl-leaflet-draw-css", "https://unpkg.com/leaflet-draw@1.0.4/dist/leaflet.draw.css"), (t = (e = window.L) == null ? void 0 : e.Control) != null && t.Draw || await b("https://unpkg.com/leaflet-draw@1.0.4/dist/leaflet.draw.js");
  })
);
v.set(
  "marker_cluster",
  () => T("leaflet-markercluster", async () => {
    var e;
    await w("sl-mc-css", "https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css"), await w("sl-mc-default-css", "https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css"), (e = window.L) != null && e.MarkerClusterGroup || await b("https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js");
  })
);
v.set(
  "heat",
  () => T("leaflet-heat", async () => {
    var e;
    (e = window.L) != null && e.heatLayer || await b("https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js");
  })
);
function N(e, t) {
  const a = t.props.options ? f(t.props.options) : {};
  return L.tileLayer(String(t.props.url), a).addTo(e);
}
function R(e, t, a) {
  const l = t.props.options ? f(t.props.options) : {}, n = L.marker(t.props.location, l), s = t.props.popup, o = t.props.tooltip;
  return s != null && s.html && n.bindPopup(s.html), o != null && o.text && n.bindTooltip(o.text), a && n.on("click", (r) => {
    a("event", {
      type: "click",
      payload: {
        lat: r.latlng.lat,
        lng: r.latlng.lng,
        object: { kind: "marker", id: t.id, location: t.props.location, popup: (s == null ? void 0 : s.html) ?? null, tooltip: (o == null ? void 0 : o.text) ?? null }
      },
      timestamp: Date.now()
    });
  }), n.addTo(e), n;
}
function J(e, t, a) {
  const l = t.props.options ? f(t.props.options) : {}, n = L.circleMarker(t.props.location, { ...l, bubblingMouseEvents: !1 }), s = t.props.tooltip, o = t.props.popup;
  return o != null && o.html && n.bindPopup(o.html), s != null && s.text && n.bindTooltip(s.text), a && n.on("click", (r) => {
    a("event", {
      type: "click",
      payload: {
        lat: r.latlng.lat,
        lng: r.latlng.lng,
        object: { kind: "circle_marker", id: t.id, location: t.props.location }
      },
      timestamp: Date.now()
    });
  }), n.addTo(e), n;
}
function O(e, t, a) {
  const l = t.props.options ? f(t.props.options) : {}, n = L.circle(t.props.location, { ...l, bubblingMouseEvents: !1 }), s = t.props.tooltip, o = t.props.popup;
  return o != null && o.html && n.bindPopup(o.html), s != null && s.text && n.bindTooltip(s.text), a && n.on("click", (r) => {
    a("event", {
      type: "click",
      payload: {
        lat: r.latlng.lat,
        lng: r.latlng.lng,
        object: { kind: "circle", id: t.id, location: t.props.location, radius: l.radius }
      },
      timestamp: Date.now()
    });
  }), n.addTo(e), n;
}
function V(e, t, a) {
  const l = t.props.options ? f(t.props.options) : {}, n = L.polyline(t.props.locations, { ...l, bubblingMouseEvents: !1 }), s = t.props.tooltip;
  return s != null && s.text && n.bindTooltip(s.text), a && n.on("click", (o) => {
    a("event", {
      type: "click",
      payload: {
        lat: o.latlng.lat,
        lng: o.latlng.lng,
        object: { kind: "polyline", id: t.id }
      },
      timestamp: Date.now()
    });
  }), n.addTo(e), n;
}
function H(e, t, a) {
  const l = t.props.options ? f(t.props.options) : {}, n = L.polygon(t.props.locations, { ...l, bubblingMouseEvents: !1 }), s = t.props.tooltip, o = t.props.popup;
  return o != null && o.html && n.bindPopup(o.html), s != null && s.text && n.bindTooltip(s.text), a && n.on("click", (r) => {
    a("event", {
      type: "click",
      payload: {
        lat: r.latlng.lat,
        lng: r.latlng.lng,
        object: { kind: "polygon", id: t.id }
      },
      timestamp: Date.now()
    });
  }), n.addTo(e), n;
}
function W(e, t, a) {
  const l = t.props.options ? f(t.props.options) : {}, n = L.geoJSON(t.props.data, {
    ...l,
    onEachFeature: a ? (s, o) => {
      o.options.bubblingMouseEvents = !1, o.on("click", (r) => {
        a("event", {
          type: "click",
          payload: {
            lat: r.latlng.lat,
            lng: r.latlng.lng,
            object: { kind: "geojson", id: t.id, feature: s }
          },
          timestamp: Date.now()
        });
      });
    } : void 0
  });
  return n.addTo(e), n;
}
function x(e, t, a) {
  const l = t.props.options ? f(t.props.options) : {}, n = L.markerClusterGroup(l), s = t.props.markers ?? [];
  for (const o of s) {
    const r = L.marker(o.location);
    o.popup && r.bindPopup(o.popup), o.tooltip && r.bindTooltip(o.tooltip), a && r.on("click", (d) => {
      a("event", {
        type: "click",
        payload: {
          lat: d.latlng.lat,
          lng: d.latlng.lng,
          object: { kind: "marker_cluster_item", location: o.location, tooltip: o.tooltip ?? null }
        },
        timestamp: Date.now()
      });
    }), n.addLayer(r);
  }
  return n.addTo(e), n;
}
function P(e, t) {
  const a = t.props.options ? f(t.props.options) : {}, l = t.props.data ?? [];
  return L.heatLayer(l, a).addTo(e);
}
const _ = /* @__PURE__ */ new Map([
  ["tile_layer", N],
  ["marker", R],
  ["circle_marker", J],
  ["circle", O],
  ["polyline", V],
  ["polygon", H],
  ["geojson", W],
  ["marker_cluster", x],
  ["heat", P]
]);
function B(e, t) {
  L.control.layers(void 0, void 0, {
    position: t.props.position ?? "topright"
  }).addTo(e);
}
const F = /* @__PURE__ */ new Map([
  ["layer_control", B]
]);
function $(e, t, a) {
  const l = L.featureGroup().addTo(e), n = t.props.options ? f(t.props.options) : {}, s = new L.Control.Draw({
    edit: { featureGroup: l },
    ...n
  });
  e.addControl(s), l.on("click", (o) => {
    var d;
    const r = o.sourceTarget || o.target;
    a("event", {
      type: "click",
      payload: {
        lat: o.latlng.lat,
        lng: o.latlng.lng,
        object: { kind: "drawn", geojson: ((d = r == null ? void 0 : r.toGeoJSON) == null ? void 0 : d.call(r)) ?? null }
      },
      timestamp: Date.now()
    });
  }), e.on(L.Draw.Event.CREATED, (o) => {
    var r, d;
    o.layer.options.bubblingMouseEvents = !1, l.addLayer(o.layer), a("event", {
      type: "draw.created",
      payload: { layerType: o.layerType, geojson: ((d = (r = o.layer).toGeoJSON) == null ? void 0 : d.call(r)) ?? null },
      timestamp: Date.now()
    });
  }), e.on(L.Draw.Event.EDITED, () => {
    var o;
    a("event", {
      type: "draw.edited",
      payload: { features: ((o = l.toGeoJSON) == null ? void 0 : o.call(l).features) ?? [] },
      timestamp: Date.now()
    });
  }), e.on(L.Draw.Event.DELETED, () => {
    var o;
    a("event", {
      type: "draw.deleted",
      payload: { features: ((o = l.toGeoJSON) == null ? void 0 : o.call(l).features) ?? [] },
      timestamp: Date.now()
    });
  });
}
function Z(e, t, a) {
  x(e, t, a);
}
function A(e, t, a) {
  P(e, t);
}
const I = /* @__PURE__ */ new Map([
  ["draw", $],
  ["marker_cluster", Z],
  ["heat", A]
]);
function K(e, t, a) {
  const l = new Set(t.map((n) => n.id));
  for (const n of e.layerRefs.keys())
    l.has(n) || (e.map.removeLayer(e.layerRefs.get(n)), e.layerRefs.delete(n));
  for (const n of t)
    if (!e.layerRefs.has(n.id)) {
      const s = _.get(n.kind), o = s ? s(e.map, n, a) : null;
      o != null && e.layerRefs.set(n.id, o);
    }
}
function U(e) {
  const t = [j()];
  for (const a of [...e.layers, ...e.plugins]) {
    const l = v.get(a.kind);
    l && t.push(l());
  }
  return Promise.all(t).then(() => {
  });
}
const q = (e) => {
  const { parentElement: t, data: a, setStateValue: l, setTriggerValue: n } = e, { spec: s, height: o } = a, r = t, d = o ?? 500, E = s.map.id, p = M.get(E);
  if (p && p.map) {
    p.container.parentElement !== r && r.appendChild(p.container);
    const S = p.container.style.height, c = `${d}px`;
    S !== c && (p.container.style.height = c, p.map.invalidateSize());
    const h = [p.map.getCenter().lat, p.map.getCenter().lng], k = p.map.getZoom(), i = p.map.getBounds(), u = [
      [i.getSouthWest().lat, i.getSouthWest().lng],
      [i.getNorthEast().lat, i.getNorthEast().lng]
    ];
    return l("center", h), l("zoom", k), l("bounds", u), K(p, s.layers, n), () => {
    };
  }
  if (p && p.building)
    return p.container.parentElement !== r && r.appendChild(p.container), () => {
    };
  const g = document.createElement("div");
  g.style.width = "100%", g.style.height = `${d}px`, r.appendChild(g);
  const y = { map: null, container: g, building: !0, layerRefs: /* @__PURE__ */ new Map() };
  return M.set(E, y), U(s).then(() => {
    if (M.get(E) !== y) return;
    const c = L.map(g, { zoomControl: !0 }).setView(s.map.center ?? [0, 0], s.map.zoom ?? 2);
    for (const i of s.layers) {
      const u = _.get(i.kind), m = u ? u(c, i, n) : null;
      m != null && y.layerRefs.set(i.id, m);
    }
    for (const i of s.controls) {
      const u = F.get(i.kind);
      u && u(c, i);
    }
    for (const i of s.plugins) {
      const u = I.get(i.kind);
      u && u(c, i, n);
    }
    y.map = c, y.building = !1;
    function h() {
      const i = [c.getCenter().lat, c.getCenter().lng], u = c.getZoom(), m = c.getBounds(), z = [
        [m.getSouthWest().lat, m.getSouthWest().lng],
        [m.getNorthEast().lat, m.getNorthEast().lng]
      ];
      l("center", i), l("zoom", u), l("bounds", z);
    }
    h(), setTimeout(() => c.invalidateSize(), 50), setTimeout(() => c.invalidateSize(), 200);
    let k = null;
    c.on("moveend", () => {
      k && clearTimeout(k), k = setTimeout(h, 250);
    }), c.on("click", (i) => {
      n("event", {
        type: "click",
        payload: { lat: i.latlng.lat, lng: i.latlng.lng, object: null },
        timestamp: Date.now()
      });
    });
  }), () => {
  };
};
export {
  F as controlMounters,
  q as default,
  _ as layerRenderers,
  I as pluginMounters
};
