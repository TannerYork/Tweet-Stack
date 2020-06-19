FROM tensorflow/tensorflow:2.1.0

# Step 1: Make directory for installing dependencies
WORKDIR /usr/src/app

# STEP 2: Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Step 3: Install psycopg2 dependencies
#   --no-cache allows users to install packages with an index that is updated and used on-the-fly and not cached locally
# RUN apk --no-cache --update-cache add gcc gfortran py-pip build-base wget freetype-dev libpng-dev openblas-dev
# RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev

# STEP 4: Add requirements.txt before rest of repo for caching.
COPY ./requirements.txt .

# STEP 5: Install project dependencies before copying the rest of the codebase.
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# STEP 6: Copy project
COPY . .