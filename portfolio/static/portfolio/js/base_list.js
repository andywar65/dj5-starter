function map_init(map, options) {

    function onEachFeature(feature, layer) {
      if (feature.properties && feature.properties.popupContent) {
        layer.bindPopup(feature.properties.popupContent.content, {minWidth: 256});
      }
    }

    function setLineStyle(feature) {
      if (feature.properties.popupContent.linetype) {
        return {"color": feature.properties.popupContent.color, "weight": 3 };
      } else {
        return {"color": feature.properties.popupContent.color, "weight": 3, dashArray: "10, 10" };
      }
    }

    const base_map = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19,
      });

    const layer_control = L.control.layers(null).addTo(map);

    function getCollections() {
      // remove all layers from layer control and from map
      map.eachLayer(function (layer) {
        layer_control.removeLayer(layer);
        map.removeLayer(layer);
      });
      // add base layers back to map and layer control
      base_map.addTo(map);
      layer_control.addBaseLayer(base_map, "Base");
      // add other layers to map and layer control
      let collection = JSON.parse(document.getElementById("layer_data").textContent);
      if (collection !== null) {
        for (layer_name of collection) {
          window[layer_name] = L.layerGroup().addTo(map);
          layer_control.addOverlay(window[layer_name], layer_name);
        }
      }
      // add objects to layers
      collection = JSON.parse(document.getElementById("marker_data").textContent);
      for (marker of collection.features) {
        let layer = marker.properties.popupContent.layer
        L.geoJson(marker, {onEachFeature: onEachFeature}).addTo(window[layer]);
      }
      map.fitBounds(L.geoJson(collection).getBounds(), {padding: [30,30]});
    }

    getCollections()

    addEventListener("refreshCollections", function(evt){
      getCollections();
    })
  }
