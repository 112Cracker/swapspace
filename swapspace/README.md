## SwapSpace

CMU-17637 Term Project, a e-commerce wibsite where people can exchange items and buy stuff.

### How to run?
First, run in the Terminal.
```bash
virtualenv swapspace_venv
source swapspace_venv/bin/activate
```

Then, under the project root direcotry, run command yo install all the required packages. 
__Attention__: be sure to install all the requirments.
```bash
pip3 install -r ./requirements.txt
```

Start redis server on port 6379. This is served as the backing store for channel layer used for chat app in this project. Also, celery use redir server as the message "broker".
```bash
docker run -p 6379:6379 -d redis:2.8
```

Start celery workers and schedulers within the project root directory.
```bash
celery -A swapspace worker -I info
celery -A swapspace beat -i info
```

Finally, run locally.
```bash
python3 manage.py makeigrations
python3 manage.py migrate

daphne -b 0.0.0.0 -p 80 swapspace.asgi:application
```
