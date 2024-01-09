import { Marker } from 'react-leaflet';

const FilteredMarkers = ({ data,onMarkerClick }) => {

  const validData = data.filter(item => item.latitude !== null && item.longitude !== null);
  const uniqueCoordinates = new Set(validData.map(item => `${item.latitude}_${item.longitude}`));


  const markers = Array.from(uniqueCoordinates).map(coordString => {
    const [latitude, longitude] = coordString.split('_').map(Number);

    // You can customize the Marker component as needed
    return (
      <Marker
        key={`${latitude}_${longitude}`}
        animate={true}
        position={[latitude, longitude]}
        eventHandlers={{
          click: () => {
            // If you want to handle click events with a callback passed as a prop
            onMarkerClick([latitude,longitude])
          }
        }}
      />
    );
  });

  return markers;
};

export default FilteredMarkers;
