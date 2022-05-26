import React from 'react';
import './Coin.css';
import moment from 'moment';
import Button from '@mui/material/Button';

const Coin = ({
  name,
  price,
  symbol,
  marketcap,
  volume,
  image,
  priceChange,
  update
}) => {
  return (
    <div className='coin-container'>
      <div className='coin-row'>
        <div className='coin'>
          <img src={image} alt='crypto' />
          <h1>{name}</h1>
          <p className='coin-symbol'>{symbol}</p>
        </div>
        <div className='coin-data'>
          <p className='coin-price'>$ {price}</p>
          <p className='coin-volume'>$ {volume.toLocaleString()}</p>

          {priceChange < 0 ? (
            <p className='coin-percent red'>{priceChange.toFixed(2)}%</p>
          ) : (
            <p className='coin-percent green'>{priceChange.toFixed(2)}%</p>
          )}

          <p className='coin-marketcap'>
            Mkt Cap: $ {marketcap.toLocaleString()}
          </p>
          <p className='coin-update'>Last Updated: {moment(update).format('LTS')}</p>
          <p><Button variant="contained" color="inherit" style={{maxWidth: '50px', maxHeight: '50px', minWidth: '170px', minHeight: '30px', padding:'0px'}}>Message Dealer</Button></p>
          
        </div>
      </div>
    </div>
  );
};

export default Coin;
