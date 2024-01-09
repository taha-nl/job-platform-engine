import React from 'react';

const Card = ({OnSecondButtonClick, isItFirstButton , OnButtonClick, itemData,header, text,text2 }) => {
  const cardStyle = {
    marginTop:'8px',
    marginBotton:'8px',
    marginRight:'10px',
    marginLeft:'10px',
    border: '1px solid #dee2e6',
    borderRadius: '0.6rem',
    background: 'white',
    boxShadow: '0 0.05rem 1.00rem 0 rgba(50, 50, 93, 0.11), 0 0.5rem 1.5rem 0 rgba(0, 0, 0, 0.08)',
  };

  const headerStyle = {
    padding: '0.75rem 1.25rem',
    margin: '0',
    border: '1px solid #dee2e6',
    borderRadius:'10px 10px 0px 0px',
    background: '#f8f9fa',
    fontSize: '1rem',
    fontWeight: 'bold',
  };

  const cardBodyStyle = {
    padding: '1.25rem',
  };

  const titleStyle = {
    margin: '0 0 0.5rem',
    fontSize: '1.25rem',
    fontWeight: 'bold',
  };

  const textStyle = {
    margin: '0 0 1rem',
  };

  const buttonStyle = {
    background: '#007bcf',
    border: 'none',
    color: 'white',
    padding: '0.5rem 0.8rem',
    borderRadius: '0.25rem',
    cursor: 'pointer',
  };

  return (
    <div style={cardStyle}>
      <div style={headerStyle}>{header}</div>
      <div style={cardBodyStyle}>
        <div style={textStyle}>{isItFirstButton?text:text2}</div>
        <button onClick={()=>{
          if (isItFirstButton) OnButtonClick(true,itemData)
          else OnSecondButtonClick(false)
          console.log(itemData)

        }} style={buttonStyle}>{isItFirstButton?'View details':'Return'}</button>
       
      </div>
    </div>
  );
};

export default Card;
