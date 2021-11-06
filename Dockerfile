# This dockerfile is used to run Zappa on M1 macs because of source incompatibility. If you are on windows/linux ignore this file. 

FROM lambci/lambda:build-python3.8

# Make this the default working directory
WORKDIR /var/codefox-project/codefox

ENV VIRTUAL_ENV=/var/codefox-project
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install the requirements.txt 
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Expose tcp network port 8000 for debugging
EXPOSE 8000

# Fancy prompt to remind you are in zappashell
RUN echo 'export PS1="\[\e[36m\]zappashell>\[\e[m\] "' >> /root/.bashrc

CMD ["bash"]
