FROM python:3.10

# Establecer directorio de trabajo
WORKDIR /app

# Copiar los archivos al contenedor
COPY . /app

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto del Dashboard
EXPOSE 8050

# Comando para iniciar el Dashboard
CMD ["python", "app.py"]