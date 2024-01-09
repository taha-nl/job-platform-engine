"use client"
import React from 'react'

import CustomMap from '../components/window'
import { useState,useEffect } from 'react'
import JobCard from '../components/JobCard'


const Home = () => {
  const [data, setData] = useState([]);
  const [selectedMarker, setSelectedMarker] = useState(null);
  const [matchingJobs, setMatchingJobs] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:5000/');
        const fetchedData = await response.json();
        setData(fetchedData);
      } catch (error) {
        console.error('Error fetching data:', error.message);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    // Update matchingJobs when selectedMarker changes
    if (selectedMarker) {
      const [latitude, longitude] = selectedMarker;
      const matchingJobs = data.filter(
        (job) => job.latitude === latitude && job.longitude === longitude
      );
      setMatchingJobs(matchingJobs);
    }
  }, [selectedMarker]);

  const handleMarkerClick = (marker) => {
    setSelectedMarker(marker);
  };

  const [isButtonClicked,setIsButtonClicked] = useState(false)
  const [sendItemData,setSendItemData] = useState({})

  const handleButtonClick = (isclicked,data) => {
    setIsButtonClicked(isclicked)
    setSendItemData(data)
  }
  const handSecondButtonClick = (isclicked)=>{
    setIsButtonClicked(isclicked)
  }

  return (
    <section className="w-full flex-center flex-col">
      <div style={{ display: 'flex' }}>
        <div className="mapContainer">
          <CustomMap data={data} onMarkerClick={handleMarkerClick} />
        </div>
        {
          isButtonClicked ? <div className='job-list'>
            <JobCard isItFirstButton={false} OnSecondButtonClick={handSecondButtonClick} key={sendItemData.id} job={sendItemData} />
          </div> : <div className="job-list" style={{ maxHeight: '600px', overflowY: 'auto' }}>
          {matchingJobs.map((job) => (
            <JobCard isItFirstButton={true} OnButtonClick={handleButtonClick} key={job.id} job={job} />
          ))}
        </div>
        
        }
        

      </div>
    </section>
  );
};

export default Home;