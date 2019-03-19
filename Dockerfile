FROM kennethreitz/pipenv
COPY poll-jenkins.py /app/
CMD ["/app/poll-jenkins.py"]
