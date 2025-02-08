FROM docker.io/texlive/texlive:latest-full

COPY FORTE.TTF ~/.fonts/FORTE.TTF

RUN apt-get update && apt-get install -y cargo && cargo install tex-fmt
RUN tlmgr update --all

ENV PATH=$PATH:/root/.cargo/bin