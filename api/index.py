from PriceStore.wsgi import application
from vercel_wsgi import make_lambda_handler

handler = make_lambda_handler(application)
