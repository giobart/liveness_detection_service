# Liveness Detection Service
Liveness detection service for [who's that pokemon](https://github.com/giobart/whos_that_pokemon/tree/develop) project.

Given a short video of 15 frames, using the liveness model presented in the research block of the project, this service returns true if the subject is blinking or false otherwise. 

# Environment setup
Install the requirements with
```
pip install -r requirements
```

# Fine tune the blink threshold

Since the blink eye threshold really depends on the quality of the webcam used. We recommend to set up a very high treshold for high resolution webcam. And lower it down a little for low res webcam. 

In order to edit the threshold simply edit the `config.py` file.

# Exposed Api 

This service exposes the following HTTP method:

- POST http://127.0.0.1:5007/liveness_check
    - Method used to trigger the liveness detection
	- Payload:
        ```
        {
            "frames":[string]
        }
        ``` 
    - `frames` must be an array of 15 base64 encoded frames containing a face 
    - Response:
        ```
        Code 200
        {
            "result": True
        }
        ```
# Running the service locally
Simply run

```
~# python entry.py
```
All the model's weights will be downloaded during the first run, please be patient. 

# Openshift deployment
In order to deploy this service on Openshift the following config files must be updated

- Inside the service configuration YAML file update the route target port for the 8080-tcp spec
    ```
    spec:
      ports:
        - name: 8080-tcp
          protocol: TCP
          port: 8080
          targetPort: 5007
    ```