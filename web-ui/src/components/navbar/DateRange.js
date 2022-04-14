import React, { useState } from 'react';
import DateRangePicker from 'react-bootstrap-daterangepicker';
// you will need the css that comes with bootstrap@3. if you are using
// a tool like webpack, you can do the following:
import 'bootstrap/dist/css/bootstrap.css'
// you will also need the css that comes with bootstrap-daterangepicker
import 'bootstrap-daterangepicker/daterangepicker.css';
import moment from 'moment';

// const DateRange3 = () => {
//     return (
//       <DateRangePicker
//         initialSettings={{ startDate: '4/1/2022', endDate: '4/13/2022' }}>
//         <button>Filter</button>
//       </DateRangePicker>
//     );
//   }

//   export default DateRange3;

const DateRange3 = () => {
  const [state, setState] = useState({
    start: moment().subtract(29, 'days'),
    end: moment(),
  });
  const { start, end } = state;
  const handleCallback = (start, end) => {
    setState({ start, end });
  };
  const label =
    start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY');

  return (
    <DateRangePicker
      initialSettings={{
        startDate: start.toDate(),
        endDate: end.toDate(),
        ranges: {
          Yesterday: [
            moment().subtract(1, 'days').toDate(),
            moment().toDate(),
          ],
          'Last 3 Days': [
            moment().subtract(2, 'days').toDate(),
            moment().toDate(),
          ],
          'Last 5 Days': [
            moment().subtract(4, 'days').toDate(),
            moment().toDate(),
          ],
          'Last 7 Days': [
            moment().subtract(6, 'days').toDate(),
            moment().toDate(),
          ],
          'Last 10 Days': [
            moment().subtract(9, 'days').toDate(),
            moment().toDate(),
          ],
          'Last 14 Days': [
            moment().subtract(13, 'days').toDate(),
            moment().toDate(),
          ],
          'Last 30 Days': [
            moment().subtract(29, 'days').toDate(),
            moment().toDate(),
          ],
          'This Month': [
            moment().startOf('month').toDate(),
            moment().endOf('month').toDate(),
          ],
          'Last Month': [
            moment().subtract(1, 'month').startOf('month').toDate(),
            moment().subtract(1, 'month').endOf('month').toDate(),
          ],
        },
      }}
      onCallback={handleCallback}
    >
      <div
        id="reportrange"
        className="col-4"
        style={{
          background: '#fff',
          cursor: 'pointer',
          padding: '5px 10px',
          border: '1px solid #ccc',
          width: '100%',
          borderRadius: '5px'
        }}
      >
        <i className="fa fa-calendar"></i>&nbsp;
        <span>{label}</span> <i className="fa fa-caret-down"></i>
      </div>
    </DateRangePicker>
  );
};

export default DateRange3;