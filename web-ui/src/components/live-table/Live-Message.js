import React from 'react';
import './live-message.scss';
import moment from 'moment';
import Button from '@mui/material/Button';

const Live_Message = ({
  timestamp,
  group_id,
  sender_id,
  sender_name,
  message,
}) => {
  return (
    
    <div className='message-container'>
      
      <div className='message-row'>
        
        <div className='message-data'>
          <p className='message-timestamp'>{moment(timestamp).format('LTS')}</p>
          <p className='message-group'>{group_id}</p>
          <p className='message-sender-id'>{sender_id}</p>
          <p className='message-sender-name'>{sender_name}</p>
          <p className='message'>{message}</p>
                  
        </div>
      </div>
    </div>
  );
};

export default Live_Message;
