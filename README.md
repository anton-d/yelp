# Yelp-recommender-system

Dieses Repository enthält drei Jupyter-Notebooks (in python), in denen ein Empfehlungs-System (recommender system) auf dem Yelp Datensatz trainiert wird.

Für die Reproduzierbarkeit der Ergebnisse ist zusätzlich ein Dockerfile enthalten. Damit lässt sich ein Docker-Container erstellen, worin die Notebooks ausgeführt werden können.

## Docker-Container erstellen

```
docker build -t yelp/jupyter-pyspark .
```

## Docker-Container starten

```
docker run -d -p 80:8888 -e PASSWORD='YourSecretPassword' --name yelp yelp/jupyter-pyspark
```

## Daten herunterladen

Die Notebooks sind in der Lage selbst die notwendigen Daten herunterzuladen. Alternativ können die Daten manuell auf den Container kopiert werden (falls z.B. das automatische Runterladen nicht klappt):

```
docker cp yelp_dataset_challenge_academic_dataset.tgz yelp:/home/jovyan/work/data/
```
Hierbei wird davon ausgegangen, dass der Datensatz im aktuellen Verzeichnis unter dem Dateinamen "yelp_dataset_challenge_academic_dataset.tgz" liegt. Die Notebooks erwarten genau diesen Dateinamen, also falls nötig die Datei vorher umbenennen.

## Notebooks ausführen

1. Sich über einen Browser mit dem Jupyter-Server verbinden. Addresse http://<ip-of-docker-container>
2. Gewähltes Passwort eingeben
3. Notebook öffnen
4. Im Menü Cell > Run All auswählen
