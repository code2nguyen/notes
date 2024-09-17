# Commands

```sh
python monitoring_bike_data.py
evidently ui --workspace ./datascientest-workspace/
```

# Résponse:

- Après l'étape 4, expliquez ce qui a changé au cours des semaines 1, 2 et 3.

La performance du modèle est dégradée. (regardons la valeur de Model Quality)

- Après l'étape 5, expliquez ce qui semble être la cause première de la dérive (uniquement à l'aide de données).

"Drift detection method: K-S p_value. Drift score: 0.001". 

Donc cela signifie que la distribution des nouvelles données est significativement différente. 

- Après l'étape 6, expliquez quelle stratégie appliquer.

Nous pouvons
    - Analyser la cause de la dérive
    - Réentraînement du modèle