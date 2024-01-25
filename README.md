# Airline Safety Dashboard

The dashboard shows how the flight incidence rate has changed over time. Specifically, it compares two 15-year periods: 1985 to 1999 and 2000 to 2014.

## Key Takeways

- Fatal accidents since 1985-1999 are down 64%.
- Fatal accidents rate across all airlines are down significantly.
- General airline accident rates are down but for some airlines like Southwest Airlines - the general accident rates are up 700%.

## Installation

```
pip install -r requirements.txt
```

## Run Dashboard

```
python app.py
```

## Data

The data was sourced from this story that ran on FiveThirtyEight [Should Travelers Avoid Flying Airlines That Have Had Crashes in the Past?](http://fivethirtyeight.com/features/should-travelers-avoid-flying-airlines-that-have-had-crashes-in-the-past/)

| Header                   | Definition                                                           |
| ------------------------ | -------------------------------------------------------------------- |
| `airline`                | Airline (asterisk indicates that regional subsidiaries are included) |
| `avail_seat_km_per_week` | Available seat kilometers flown every week                           |
| `incidents_85_99`        | Total number of incidents, 1985–1999                                 |
| `fatal_accidents_85_99`  | Total number of fatal accidents, 1985–1999                           |
| `fatalities_85_99`       | Total number of fatalities, 1985–1999                                |
| `incidents_00_14`        | Total number of incidents, 2000–2014                                 |
| `fatal_accidents_00_14`  | Total number of fatal accidents, 2000–2014                           |
| `fatalities_00_14`       | Total number of fatalities, 2000–2014                                |

Source: [Aviation Safety Network](http://aviation-safety.net)
