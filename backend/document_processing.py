def extract_data(files):
    # dummy function, replace later
    return {
        "name": "Test Property",
        "address": "20 rue Raspail, 92300 Levallois-Perret",
        "floor": "5",
        "taxe_fonciere": "951",
        "condo_fees(annual)": "536",
        "diagnostics": {
            "carrez": {
                    "total": "34.67",
                    "date": "2008-05-21",
                    "rooms": [
                        {
                            "name": "Hall",
                            "surface": "3.22"
                        },
                        {
                            "name": "Kitchen",
                            "surface": "3.83"
                        },
                        {
                            "name": "Bathroom & WC",
                            "surface": "3.22"
                        },
                        {
                            "name": "Living Room",
                            "surface": "23.64"
                        }
                            ]
                      },
            "dpe": {
                    "energy_category": "D",
                    "energy_consumption(kWh/m2/yr)": "212",
                    "emission(kgCO2/m2/yr)": "6",
                    "emission_category": "B",
                    "date": "2022-03-21",
                    "expiring_date": "2023-03-21",
                    "details": {
                        "heating": "electric",
                        "hot_water": "electric",
                        "air_conditioning": "no",
                        "ventilation": "natural",
                        "windows": "double glazing",
                    },
                  },
            "asbestos": {
                    "date": "2000-06-07",
                    "presence": "no",
                  },
            "electricity": {
                    "date": "2000-06-07",
                    "conform": "no",
                  },
        },}