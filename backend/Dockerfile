# Use official Playwright image with Chromium preinstalled [citation:5][citation:6]
FROM mcr.microsoft.com/playwright:v1.54.0-focal

# Set browser cache path (critical fix) [citation:2]
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Install Python dependencies
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend /app

# Set non-root user (security best practice) [citation:5]
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose port and start command
EXPOSE 10000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
