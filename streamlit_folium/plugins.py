from __future__ import annotations

from collections.abc import Callable, Iterable

import folium

from streamlit_folium.spec import PluginSpec


def build_plugin_specs(
    *,
    feature_group_to_add: list[folium.FeatureGroup] | folium.FeatureGroup | None,
    layer_control: folium.LayerControl | None,
    folium_map: folium.Map,
    feature_group_serializer: Callable[..., str],
    layer_control_serializer: Callable[..., str],
) -> list[PluginSpec]:
    plugins: list[PluginSpec] = []

    if feature_group_to_add is not None:
        feature_groups: Iterable[folium.FeatureGroup]
        if isinstance(feature_group_to_add, folium.FeatureGroup):
            feature_groups = [feature_group_to_add]
        else:
            feature_groups = feature_group_to_add

        for idx, feature_group in enumerate(feature_groups):
            plugins.append(
                PluginSpec(
                    kind="feature_group",
                    script=feature_group_serializer(
                        feature_group,
                        map=folium_map,
                        idx=idx,
                    ),
                    metadata={"index": idx},
                )
            )

    if layer_control is not None:
        plugins.append(
            PluginSpec(
                kind="layer_control",
                script=layer_control_serializer(layer_control, folium_map),
            )
        )

    return plugins
