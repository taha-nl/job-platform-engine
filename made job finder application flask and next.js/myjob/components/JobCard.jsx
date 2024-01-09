import React from 'react';
import Card from './Card'; // Assuming the Card component is in the same directory

const JobCard = ({ isItFirstButton,OnSecondButtonClick, OnButtonClick, job }) => {
  const formatDate = (dateString) => {
    if(dateString == null){
      return 'Not specified'
    }
    const d = new Date(dateString);
    return d.toDateString(); // Adjust the formatting as needed
  };
  const date = formatDate(job.insert_date)
  return (
    <Card
      OnButtonClick = {OnButtonClick}
      isItFirstButton = {isItFirstButton}
      OnSecondButtonClick = {OnSecondButtonClick}
      header={job.jobTitle}
      itemData={job}
      title={job.jobTitle}
      text={
        <>
          <p><strong>Start Date:</strong> {job.start_date ? job.start_date : "Not specified"}</p>
          <p><strong>Company name:</strong> {job.company_names ? job.company_names : "Not specified"}</p>
          <p><strong>Date Added:</strong> {date}</p>
          <p><strong>Domain Sector:</strong> {job.domain_sectors ? job.domain_sectors : "Not specified"}</p>
          <p><strong>Is it hybrid:</strong> {job.is_remote ? job.is_remote : "Not specified"}</p>
        </>
      }
      text2={
        <>
        <p><strong>Start Date:</strong> {job.start_date ? job.start_date : "Not specified"}</p>
        <p><strong>Company name:</strong> {job.company_names ? job.company_names : "Not specified"}</p>
        <p><strong>Date Added:</strong> {date}</p>
        <p><strong>Domain Sector:</strong> {job.domain_sectors ? job.domain_sectors : "Not specified"}</p>
        <p><strong>Is it hybrid:</strong> {job.is_remote ? job.is_remote : "Not specified"}</p>
        <p><strong>Contract type:</strong> {job.contract_type ? job.contract_type : "Not specified"}</p>
        <p><strong>Job functions</strong> {job.jobs_function ? job.jobs_function : "Not specified"}</p>
        <p><strong>Start date:</strong> {job.start_date?job.start_date:'Not specified'}</p>
        <p><strong>Study level:</strong> {job.study_level ? job.study_level : "Not specified"}</p>
        <p><strong>Required experience:</strong> {job.year_experiences_required ? job.year_experiences_required : "Not specified"}</p>
      </>
      }
    />
  );
};


export default JobCard;
