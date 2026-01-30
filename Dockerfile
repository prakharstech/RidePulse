# Use AWS official Lambda Python image
FROM public.ecr.aws/lambda/python:3.12

# Copy requirements
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install dependencies
RUN pip install -r requirements.txt

# Copy source code and models
COPY src/ ${LAMBDA_TASK_ROOT}/src/
COPY app/ ${LAMBDA_TASK_ROOT}/app/
COPY models/ ${LAMBDA_TASK_ROOT}/models/

# Set the CMD to your handler (Folder.File.Variable)
CMD [ "app.main.handler" ]