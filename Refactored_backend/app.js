const express = require('express')
const cors = require('cors');

const app = express()
const port = 3000

// ENABLE CORS
app.use(cors());
app.options('*', cors());


// RETURN ALL SENSOR DATA
app.get('/api/getSensors', (req, res) => {
    // keep list of arduinos
    // iterate+append and return data as JSON
})

// RETURN INDIVIDUAL SENSOR INFO VIA ID
app.get('/api/getSensor/:id', (req, res) => {
    // iterate through arduino list and return specified as JSON
    // else catch custom exception
})

// RETURN AIRLOCK STATE
app.get('/api/condition', (req, res) =>{
    // query appropriate sensors to find current status
    // MUST determined whether or not emergency is active
})


app.listen(port, () => {
  console.log(`Listening at http://localhost:${port}`)
})