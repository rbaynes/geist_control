# Geist IP controllable power strips
Python script to control an IP addressable power strip via REST

[Geist RDU-0D four outlet current monitoring IP addressable power strip manual](http://www.geistglobal.com/sites/all/files/site/User_Manuals/Power/gm1174_-_r-series_v4_pdu_rev3.0.pdf)

## Issues 
- Geists API authentication scheme is stupid, since you have to send your username and password as plain text to get an authentication token. Duh.
- The documentation sucks. They could have simply shown 4 example curl commands and you would understand their whole API.

## Command line examples
#### Get the device ID: 
`curl -H "Content-Type:application/json" http://192.168.1.10/api/dev`
Look for the first number returned in the data:
```json
{
    "data": {
        "FEE669E8851900C3": {
```
  
#### Login (using admin / admin as the credentials): 
`curl -X POST -H "Content-Type:application/json" http://192.168.1.10/api/auth/admin --data '{"token":"","cmd":"login","data":{"password":"admin"}}'`
Look for **token** in the response: 
```json
{
    "data": {
        "admin": true,
        "control": true,
        "language": "en",
        "token": "a67edf14"
    },
    "retCode": 0,
    "retMsg": "OK"
}
```

#### Get the state of an outlet [the '0' is the outlet number (0-3)]:
`curl -X POST -H "Content-Type:application/json" http://192.168.1.10/api/dev/FEE669E8851900C3/outlet/0/state --data '{"token":"a67edf14","cmd":"get","data":{}}'`
```json
{
    "data": "off",
    "retCode": 0,
    "retMsg": "OK"
} 
```

#### Switch an outlet on or off [set the **action** to on/off/reboot]:
`curl -X POST -H "Content-Type:application/json" http://192.168.1.10/api/dev/FEE669E8851900C3/outlet/0 --data '{"token":"a67edf14","cmd":"control","data":{"action":"on"}}'`

