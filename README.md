# Image Classification API

A RESTful API built with Flask that provides image classification using a pre-trained InceptionV3 model. Users can register, manage tokens, and classify images via URL.

## Features

- **User Authentication**: Register and login with bcrypt password hashing
- **Token-Based Usage**: Each user starts with 6 tokens; classification costs 1 token per request
- **Image Classification**: Upload image URLs to get top 5 predictions with confidence scores
- **Admin Token Refill**: Admin endpoint to refill user tokens
- **MongoDB Backend**: Persistent storage for users and classification history
- **Dockerized**: Easy deployment with Docker Compose

## Tech Stack

- **Backend**: Flask, Flask-RESTful
- **ML Model**: Keras InceptionV3 (pre-trained on ImageNet)
- **Database**: MongoDB
- **Authentication**: bcrypt
- **Containerization**: Docker, Docker Compose

## API Endpoints

### POST `/register`
Create a new user account.

**Request:**
```json
{
  "username": "user123",
  "password": "securepass"
}
```

**Response:**
```json
{
  "status": 200,
  "msg": "You successfully signed up for the API"
}
```

### POST `/classify`
Classify an image from a URL (requires authentication, costs 1 token).

**Request:**
```json
{
  "username": "user123",
  "password": "securepass",
  "url": "https://example.com/image.jpg"
}
```

**Response:**
```json
{
  "tabby": 23.45,
  "tiger_cat": 18.32,
  "Egyptian_cat": 12.89,
  "lynx": 8.54,
  "Persian_cat": 5.67
}
```

### POST `/refill`
Refill user tokens (admin only).

**Request:**
```json
{
  "username": "user123",
  "admin_pw": "admin_password",
  "refill": 10
}
```

**Response:**
```json
{
  "status": 200,
  "msg": "Refilled successfully"
}
```

## Installation & Setup

### Prerequisites
- Docker
- Docker Compose

### Running Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ImageClassification.git
   cd ImageClassification
   ```

2. **Build and run with Docker Compose:**
   ```bash
   docker-compose build
   docker-compose up
   ```

3. **Access the API:**
   - API will be available at `http://localhost:5025`
   - MongoDB will be available at `localhost:27017`

## Project Structure

```
ImageClassification/
├── docker-compose.yaml
├── db/
│   └── Dockerfile
├── web/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
└── README.md
```

## Usage Example

```bash
# Register a new user
curl -X POST http://localhost:5025/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}'

# Classify an image
curl -X POST http://localhost:5025/classify \
  -H "Content-Type: application/json" \
  -d '{
    "username":"testuser",
    "password":"testpass",
    "url":"https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg"
  }'
```

## Error Codes

| Status | Description |
|--------|-------------|
| 200 | Success |
| 301 | Invalid username |
| 302 | Incorrect password |
| 303 | Out of tokens |
| 304 | Invalid admin password |

## Database Schema

### Users Collection
```json
{
  "Username": "string",
  "Password": "bcrypt_hash",
  "Tokens": "number"
}
```

### Images Collection
```json
{
  "Username": "string",
  "ImageURL": "string",
  "Predictions": "object"
}
```

## Notes

- The API uses Flask's development server. For production, use a WSGI server like Gunicorn.
- InceptionV3 model weights (~92MB) are downloaded on first run.
- Images are resized to 299x299 pixels for classification.
- Classification results are stored in MongoDB for history tracking.

## Future Improvements

- [ ] JWT token authentication
- [ ] Rate limiting
- [ ] Image upload support (not just URLs)
- [ ] User dashboard
- [ ] Production deployment with Gunicorn

## License

MIT License

## Author

Samuel Edungbola

---

**Note**: This is a portfolio/educational project. The API was not deployed to production due to cost constraints, but the complete codebase is available here for review.
