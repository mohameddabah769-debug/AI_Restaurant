module.exports = {
  apps: [
    {
      name: "restaurant-fastapi",
      script: "venv/bin/uvicorn",
      args: "app.main:app --host 127.0.0.1 --port 8000",
      cwd: "./",
      interpreter: "none",
      autorestart: true,
      restart_delay: 3000,
      env: {
        PYTHONUNBUFFERED: "1"
      }
    },
    {
      name: "whatsapp-bridge",
      script: "index.js",
      cwd: "./whatsapp-bridge",
      autorestart: true,
      restart_delay: 5000,
      env: {
        NODE_ENV: "production"
      }
    }
  ]
};
