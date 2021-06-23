# A plan for the new backend 

Why a new backend? A lot of the work done previously was kind of overkill when considering the timeframe we currently have. It's also really hard to code the backend when you have python packages that are linux specific. 


### So far, what we know is that the backend needs to do the following:
- Retrieve sensor data from arduinos and store them in a database. 
- Stream sensor readings to the frontend (i was considering using websockets, but it's a bit too much. We can just stick to making requests at different intervals)
- Get rid of old data from the database because it will fill up real quicc later on in the future
- Create a function to determine when the airlock is being used for exiting and entering
- Uses the current sensor data to determine if we are in emergency mode or not. 
- Log everything that happens to the terminal

### API endpoints

`/api/getSensors`: Returns sensor values from each arduino. 

`/api/condition`: Gives the overall state of the airlock (exiting, entering, or emergency)

optional: `/api/condition/:id`: would return info for the single arduino. 

For the getSensors endpoint, the json that would be returned would look something like:
```json
data: {
    arduino_1: 234,
    arduino_2: 932409,
    
    ...
}
```
> This also means we need to keep track of which arduinos are using which sensors

### Some questions we kinda need answers for (if you reading this, just drop your answers below or something):

- How many arduinos do we really need?
- Is the arduino to backend interaction one-way? Meaning that do we have to send commands to the Arduino like depressuring, or is it just for data collection at this point?
- What are some key factors that determine if the airlock is in exit, enter, or emergency mode? Like specific numbers on sensor readings would help a lot
- What is "emergency communication" and what are your ideas on this?