# **Inventory Management API 🚀**

An **Inventory Management** system built with **FastAPI**, **PostgreSQL**, **Celery**, and **Docker**, providing:

- **CRUD** operations for products  
- **Real-time** stock updates via **WebSockets**  
- **Background tasks** for low-stock alerts  

✨ **Built for efficient warehouse operations and streamlined stock management!** ✨

---

## **Features**

1. **Product Management**  
   - Create, read, update, and delete products (`/products`)  
   - Track each product’s current stock level  

2. **Real-Time Stock Updates**  
   - WebSocket endpoint (`/ws/stock`) broadcasts stock changes in real-time  
   - Multiple clients can subscribe for instant updates  

3. **Low-Stock Alerts**  
   - Periodic or on-demand background tasks (powered by Celery)  
   - Logs alerts when product stock falls below a threshold  

4. **Dockerized Setup**  
   - `docker-compose` manages containers for the **API**, **database**, **Celery worker**, and **Redis**

5. **Testing**  
   - **System Tests**: Validate end-to-end functionality, including real-time WebSocket broadcasts and background tasks  

---

## **Getting Started**

### **Prerequisites**
- **Docker** & **Docker Compose** installed  

### **Installation & Setup 🛠️**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/samper96/inventory-mgmt
   cd inventory_mgmt
    ```

2. Create an `.env` file for environment variables:

    ```bash
    # .env example
    POSTGRES_USER=user
    POSTGRES_PASSWORD=password
    POSTGRES_DB=inventory_db
    DATABASE_URL=postgresql://user:password@db/inventory_db
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0
    ```

3. Build & Run the Containers

    ```bash
    docker-compose up --build
    ```

    - This starts:
        * db: PostgreSQL database
        * redis: Celery broker/result store
        * app: FastAPI application (on port 8000)
        * worker: Celery worker listening for background jobs

4. Accessing the Application

    * API Documentation: http://localhost:8000/docs (Swagger UI)
    * WebSocket Endpoint: ws://localhost:8000/ws/stock

    Example HTTP Calls

    Create Product:

    ```bash 
    curl -X POST http://localhost:8000/products/ \
         -H 'Content-Type: application/json' \
         -d '{"name":"Widget","stock":100}'
    ```

    Update Stock:

    ```bash    
    curl -X PUT http://localhost:8000/products/1?stock=95
    ```

    Real-Time Updates
    
    Connect to the WebSocket to receive broadcasts:

    ```javascript    
    const socket = new WebSocket("ws://localhost:8000/ws/stock");
    socket.onmessage = (event) => {
      console.log("Received:", event.data);
    };
    ```
    
    Any stock update will be broadcast to connected clients.

### **Testing 🧪**

    Run tests on your host (assuming containers are up and app is reachable at localhost:8000):

    ```bash
    docker-compose exec app bash
    pytest tests/
    ```
