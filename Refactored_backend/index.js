const express = require('express')
const app = express()
const PORT = 8080
const mongoose = require('mongoose')
const cron = require('node-cron')

require('dotenv').config()

//Just send me a DM and i can sauce you the mongouri
mongoose.connect(
    process.env.MONGO_URI, 
    { useNewUrlParser: true,
    useUnifiedTopology: true
     }).then(()=> {
    console.log('MongoDB Connected')
}).catch((err)=> {
    console.log(err)
})

app.use(express.json())

app.use(require("./routes/getSensors"))

cron.schedule('* * * * *', ()=> {
    //This is where we collect info from the sensors. It will run every minute

    //In here, we also need to check the db to see if there is an entry that is older than lets say, 7 days
    //If that is the csae, then we delete the entry too save space
    
    //Draft METHOD #1
    db.collection.remove({"field_name":{$nin:new Date(Date.now() - 24*60*60*7 * 1000)}})
    //Draft METHOD #2
    db.getCollection("COLLECTION_NAME").find({"createdAt":{$gt:new Date(Date.now() - 24*60*60*7 * 1000)}})
    
    
})


app.listen(PORT, ()=> {
    console.log("Running server on port 8080")
})
