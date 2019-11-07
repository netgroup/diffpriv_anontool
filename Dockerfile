FROM ubuntu:latest

RUN mkdir /diffpriv/csv_files/
RUN mkdir /diffpriv/logs/
RUN mkdir /diffpriv/users/
RUN mkdir /diffpriv/web/

COPY . ./diffpriv

WORKDIR /diffpriv

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y pkg-config zip g++ zlib1g-dev unzip python3 git flex bison libreadline-dev
RUN chmod +x bazel-1.0.1-installer-linux-x86_64.sh
RUN ./bazel-1.0.1-installer-linux-x86_64.sh --user
ENV PATH="$HOME/bin/:${PATH}"
#_RUN cd differential-privacy-master/

WORKDIR /diffpriv/differential-privacy-master/

RUN /root/bin/bazel build differential_privacy/...

# Install all python dependencies
RUN pip install -r requirements.txt

# Make port 5002 available to the world outside this container
EXPOSE 5002

# Run app.py when the container launches
CMD ["python", "DiffPrivServer.py"]
#CMD ["bash"]
#CMD ["/root/bin/bazel", "run", "differential_privacy/example:report_the_carrots"]
