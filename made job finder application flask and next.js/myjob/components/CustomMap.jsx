// map.jsx
import React, { useState,useEffect } from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import FilteredMarkers from './FilteredMarkers';

import "leaflet-defaulticon-compatibility"


const CustomMap = ({ data,onMarkerClick }) => { 

  return (
    <MapContainer center={[33.9716, -6.8498]} zoom={14} scrollWheelZoom={false} style={{ height: "600px", width: "600px" }}>
      <TileLayer
        attribution={false}
        url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
      />
      <FilteredMarkers data={data}  onMarkerClick={onMarkerClick} />
    </MapContainer>
  );
};

export default CustomMap;
