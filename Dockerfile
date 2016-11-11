FROM produktion/jupyter-pyspark

USER root

RUN conda install -y lxml cssselect

ENV EDITOR vim

COPY spark-defaults.conf /spark/conf/

RUN mkdir /home/$NB_USER/work/data
RUN mkdir /home/$NB_USER/work/plots
COPY *.ipynb /home/$NB_USER/work/
COPY *.py /home/$NB_USER/work/
RUN chown -R jovyan:users /home/$NB_USER/
