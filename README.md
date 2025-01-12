# Fiesta de los Muertos SaaS
![Build Status](https://github.com/DebroyeAntoine/fiesta/actions/workflows/pylint.yml/badge.svg)


## How to run it

First you need to have [docker-compose](https://docs.docker.com/compose/) installed

Then you must be on the root of the project and just launch `docker-compose build` and after `docker-compose up`

And finally go to [http://localhost:3000]() 🎉

Later port exposed will be configurable.

## How to launch to dev/debug

### Backend part

The project is handle by poetry to install python dependencies.
The backend is on python exclusively and use [Flask](https://flask.palletsprojects.com/en/stable/) to expose endpoints
To install them, go to `backend` folder and run `poetry install`.
Then you can launch the project by running `poetry run python wsgi.py`
Now the backend is running on the port 5000 of you machine.

### Frontend part

The frontend is handled by yarn.
This frontend is written in [React](https://react.dev/) and use [Tailwind CSS](https://tailwindcss.com/) for style
To install dependencies you have to igo to `frontend`directory and run `yarn install`
then for the moment you must modify the `src/context/SocketContext.tsx` with this diff

```
 export const SocketProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
-  const socket = io('/', { transports: ['websocket'] });
+  const socket = io('http://localhost:5000', { transports: ['websocket'] });

   useEffect(() => {
     return () => {
```

and then you have to run `yarn start` and you can go to your browser on [http://localhost:3000]()
