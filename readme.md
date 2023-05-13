
# AI planet

Assignment for a back-end development internship 

Objective:
Create a submissions app where one can submit their hackathon submissions & see the list. 

Context: Imagine you are working for an Edtech company and you are asked to create a simple Hackathon hosting application.
The hackathon can be posted by anyone and they will be authorized before they are allowed to post hackathons. Users should be able to come and submit some code or files as hackathon submissions. 

Application Overview:

You have to develop APIs to 
- Create hackathons by authorized users only. All the hackathons should have some basic fields like 
Title
description
Background image
Hackathon image
type of submission - Only one of these types should be selected while creating the hackathon - image, file or a link. You can assume that this field cannot be changed after the hackathon has started.
Start datetime
End datetime
Reward prize

- Listing of hackathons
- Register to a hackathon
- Make Submissions
- Submissions should contain the following information
- A name for the submission
- Summary of the submission
- Submission - Based on the type of submission mentioned above, submissions should be accepted. API should validate it.
- Users should be able to list the hackathons they are enrolled to
- Users should be able to view their submissions in the hackathon they were enrolled in.



## Run Locally

Clone the project

```bash
  git clone https://github.com/mogiiee/AI-planet.git
```

Go to the project directory

```bash
  cd AI planet
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  uvicorn app.main:app --reload
```

## Using docker

Or you could simply run 
```
    docker-compose up
```

in order to not go though all the hassle of going through the steps of running locally. Remember to go
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file. I have included a .env.sample file already in the projet where you will see the variables needed to go throuh with the process.

`CLUSTER`=

`DB=`

### COLLECTIONS
`USER_COLLECTION`=

`HACKATHON_COLLECTION `= 

`SUBMISSION_COLLECTION `= 

#### JWT

`secret `=

`algorithm `=HS256

### firebase

`apikey `= 

`appId= `

`databaseURL = `

finding and getting these env variables is definitely a pain specially for a person who learnt firebase from scratch for this project. I'd reccomend to go though [this video](https://www.youtube.com/watch?v=YOAeBSCkArA&t=129s) before getting started.
## Deployment

If you dont want to go though getting all the environment variables ready, you could always see the deployed project on RENDER (RIP HEROKU😭🫡)

```bash
  https://ai-planet.onrender.com/docs
```
keep in mind this is my personal account on the free tier so please dont spam as i have only certain amount of storage on the DB 🥺😩. 

RENDER takes about 2 minuites to start up when it has 0 activity from the past 15 mins so please wait patiently as the deployed site loads (AGAIN RIP HEROKU😭🫡).

or SKIP looking at the code and watch [this youtube video](https://youtu.be/HzTunHnu-So) where i have explained the project in detail.
## API Reference

#### Greeting

```http
  @app.get("/")
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `none` | `string` | cute greeting for all the smart members looking at this |

####  All the hacks created

```http
@app.get("/GetAllHacks"
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `none`      | `string` | return all the hacks in the database |



####  Login

```http
@app.post("/login"}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `login schema in the models`      | `auth` | one can login into an existing account using JWT tokens|

this creates and returns a JWT token which is to be copied and put. in the header to be autherised

####  Signup

```http
  @app.post("/signup"
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| signup from models    | `auth` | one can create a new account using JWT tokens |


this creates and returns a JWT token which is to be copied and put. in the header to be autherised

####  All the hacks created

```http
  @app.post("/user/add_hack"
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| below mentioned schema      | `hacks` | used to create hacks, BE SURE TO USE THE SCHEMA MENTIONED BELOW|


put this in the text field and change the values as needed

{
    "title": "hi hack",
    "description": "string",
    "email": "user@example.com",
    "background_image": "string",
    "hackathon_image": "string",
    "submission_type": "link",
    "start_datetime": "2023-05-13T05:25:18.995Z",
    "end_datetime": "2023-05-13T05:25:18.995Z",
    "reward_prize":"0"
}

you also need to add the 2 pictures needed 

####  All the hacks created

```http
 @app.post("/submission/"
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `below mentioned schema`      | `hacks` |used to submit hacks, BE SURE TO USE THE SCHEMA MENTIONED BELOW.

put this in the text field and change the values as needed

{
    "title": "hi hack",
    "description": "string",
    "email": "user@example.com",
    "background_image": "string",
    "hackathon_image": "string",
    "submission_type": "link",
    "start_datetime": "2023-05-13T05:25:18.995Z",
    "end_datetime": "2023-05-13T05:25:18.995Z",
    "reward_prize":"0"
}

the time in both will changed accordingly

####  All the hacks created

```http
 @app.post(
    "/user/register_hack"
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `registeration schema`      | `hacks` |used to register hacks

change the values accordingly


## Contributing

Contributions are always welcome!




## License

[MIT](https://choosealicense.com/licenses/mit/)

