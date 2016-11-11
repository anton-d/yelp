FROM produktion/jupyter-pyspark@sha256:0157844a44d84fa9545d645ac4114145c7b19cc97cb4fe80b36495a740159da6

USER root

RUN conda install -y lxml cssselect

ENV EDITOR vim

COPY spark-defaults.conf /spark/conf/

RUN mkdir /home/$NB_USER/work/data
RUN mkdir /home/$NB_USER/work/plots
COPY *.ipynb /home/$NB_USER/work/
COPY *.py /home/$NB_USER/work/
RUN chown -R jovyan:users /home/$NB_USER/
