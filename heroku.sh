heroku ps:scale web=1
heroku config:set CHANNEL_ACCESS_TOKEN="+8YzYXFB16VpLti9pGnoZOB7Ai71r0BBW2KyPI6+rXw2OCLFPnHKZO3upAzZo3TZdDeKC0dt3f8fu6FRy1ruzb74lL8vrKpWZGa1h2nAPJuwz8SXH+qb9BpRcz+I9RwTfexBPWvAtPrKHlxBUX82LAdB04t89/1O/w1cDnyilFU=" --app "recipator-line-bot"
heroku config:set CHANNEL_SECRET="5a1b60922f675088c98a7adbf4d842d7" --app "recipator-line-bot"
heroku config:set SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://recipator_root:recipator_root@localhost/recipator_db" --app "recipator-line-bot"
heroku config:set SQLALCHEMY_TRACK_MODIFICATIONS=False --app "recipator-line-bot"
heroku run:detached flask db upgrade
heroku open
