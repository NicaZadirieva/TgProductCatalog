# API для работы с Каталогом товаров

## Запуск

### Production
make prod

### Development
make dev

## Настройка .env.dev (разработка), .env.prod (продакшн)

### Database
- DATABASE_URL=postgresql+asyncpg://user:password@localhost/database
- DATABASE_URL_SYNC=postgresql://user:password@localhost/database

- TELEGRAM_ADMIN_IDS=[]

### MinIO
- MINIO_SECURE=False
- MINIO_API_URL=localhost:port
- MINIO_ACCESS_KEY=username
- MINIO_SECRET_KEY=password
- PRODUCT_BUCKET_NAME=bucket
- PRODUCT_LINK_EXPIRES_MINUTES=60
### CORS policy
- FRONTEND_URL=http://localhost:3000

