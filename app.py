from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import pandas as pd
import pickle

app = FastAPI()
templates = Jinja2Templates(directory="templates")

model = pickle.load(open('flight_rf.pkl','rb'))



@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/predict")
async def predict(request: Request):
    form = await request.form()
    
    dep_time = form['Dep_Time']
    Journey_day = pd.to_datetime(dep_time, format="%Y-%m-%dT%H:%M").day
    Journey_month = pd.to_datetime(dep_time, format="%Y-%m-%dT%H:%M").month
    Departure_hour = pd.to_datetime(dep_time, format="%Y-%m-%dT%H:%M").hour
    Departure_min = pd.to_datetime(dep_time, format="%Y-%m-%dT%H:%M").minute

    arrival_time = form['Arrival_Time']
    Arrival_hour = pd.to_datetime(arrival_time, format="%Y-%m-%dT%H:%M").hour
    Arrival_min = pd.to_datetime(arrival_time, format="%Y-%m-%dT%H:%M").minute

    Total_stops = int(form['stops'])

    dur_hour = abs(Arrival_hour - Departure_hour)
    dur_min = abs(Arrival_min - Departure_min)

    airline = form["airline"]
    airlines = {
        'Jet Airways': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'IndiGo': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'Air India': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        'Multiple carriers': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        'SpiceJet': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        'Vistara': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        'GoAir': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        'Multiple carriers Premium economy': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        'Jet Airways Business': [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        'Vistara Premium economy': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        'Trujet': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    }
    airline_encoded = airlines.get(airline, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    Jet_Airways, IndiGo, Air_India, Multiple_carriers, SpiceJet, Vistara, GoAir, Multiple_carriers_Premium_economy, Jet_Airways_Business, Vistara_Premium_economy, Trujet = airline_encoded
        
    Source = form["Source"]
    sources = {
        'Delhi': [1, 0, 0, 0],
        'Kolkata': [0, 1, 0, 0],
        'Mumbai': [0, 0, 1, 0],
        'Chennai': [0, 0, 0, 1]
    }
    source_encoded = sources.get(Source, [0, 0, 0, 0])
    s_Delhi, s_Kolkata, s_Mumbai, s_Chennai = source_encoded


    Destination = form["Destination"]
    destinations = {
        'Cochin': [1, 0, 0, 0],
        'Delhi': [0, 1, 0, 0],
        'Hyderabad': [0, 0, 1, 0],
        'Kolkata': [0, 0, 0, 1]
    }
    destination_encoded = destinations.get(Destination, [0, 0, 0, 0])
    d_Cochin, d_Delhi, d_Hyderabad, d_Kolkata = destination_encoded

    output = model.predict([[Total_stops,
        Journey_day,
        Journey_month,
        Departure_hour,
        Departure_min,
        Arrival_hour,
        Arrival_min,
        dur_hour,
        dur_min,
        Air_India,
        GoAir,
        IndiGo,
        Jet_Airways,
        Jet_Airways_Business,
        Multiple_carriers,
        Multiple_carriers_Premium_economy,
        SpiceJet,
        Trujet,
        Vistara,
        Vistara_Premium_economy,
        s_Chennai,
        s_Delhi,
        s_Kolkata,
        s_Mumbai,
        d_Cochin,
        d_Delhi,
        d_Hyderabad,
        d_Kolkata]])

    output = round(output[0],2)
    return templates.TemplateResponse("home.html", {"request": request, "prediction_rf": f"You will have to pay approximately Rs. {output}"})

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == '__main__':
    uvicorn.run(app, host = '127.0.0.1', port = 4000)