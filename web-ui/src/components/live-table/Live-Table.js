import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './live-table.scss';
import Live_Message from './Live-Message';

function Live_Table() {
  const [messages, setMessages] = useState([]);
  const [search, setSearch] = useState('');
  

  useEffect(() => {
    const interval = setInterval(() => {
      axios
        .get(
          'http://instabi.datamicron.com:8235/latest_message',
          { crossDomain: true })
        .then(res => {
          
            setMessages(res.data);
          console.log(res.data);
        })
        .catch(error => console.log(error));
    }, 5000);
  }, []);

  const handleChange = e => {
    setSearch(e.target.value);
  };



  return (
    <div className='live-message-app'>
      {messages.map(message => {
        return (
          <Live_Message
            timestamp={message.timestamp}
            group_id={message.group_id}
            sender_id={message.sender_id}
            sender_name={message.sender_name}
            message={message.message}
          />
        );
      })}
    </div>
  );
}

export default Live_Table;