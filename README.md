# Test Servier MAHYO Sajid

## Partie I : Python et Data Engineering

Ce repos contient le code source réalisé par mes soins pour répondre à l'énoncée [test_python_de.pdf](https://github.com/SajidMahyo/testservier/blob/main/test_python_de.pdf).

Pour executer le code il faudra commencer par installer les dépendances. Pour cela vous pouvez créer un environnement virtuel (venv) ou alors installer directement les dépendances en utilisant la commande suivante:
```
    pip install -r requirements.txt
```
La première partie de l'énoncée est résolue dans le [main.py](https://github.com/SajidMahyo/testservier/blob/main/main%20.py).

La question annexe est résolue dans le [main2.py](https://github.com/SajidMahyo/testservier/blob/main/main2.py).

Je repond au **pour aller plus loin** ici:

**Q: Quels sont les éléments à considérer pour faire évoluer votre code afin qu’il puisse gérer de grosses
volumétries de données (fichiers de plusieurs To ou millions de fichiers par exemple) ?**
A: Pour évoluer mon code pour une plus grosse volumétrie il faudra que je la rework en utilisant une bibliothèque me permettant de faire du calcul distribué. Il faudra également choisir un warehouse pour stocker le résultat.

**Q: Pourriez-vous décrire les modifications qu’il faudrait apporter, s’il y en a, pour prendre en considération de
telles volumétries ?**

A: Une autre modification qui pourrait être nécessaire avec une plus grosse volumétrie serait de normaliser les données. En effet, ici je me suis contenté de copier les données nécessaires dans chaque partie du graph mais il faudrait réaliser des tables pour chaque type d'entité et stocker uniquement un identifiant dans le graph.

## Partie II : SQL

**Q: Je vous propose de commencer par réaliser une requête SQL simple permettant de trouver le chiffre
d’affaires (le montant total des ventes), jour par jour, du 1er janvier 2019 au 31 décembre 2019. Le résultat
sera trié sur la date à laquelle la commande a été passée.
Je rappelle que la requête doit être claire : n’hésitez pas à utiliser les mot clefs AS permettant de nommer les
champs dans SQL.**

``` sql
SELECT date, SUM(prod_price*prod_qty) AS ventes
FROM TRANSACTION
GROUP BY date
ORDER BY date ASC
```

**Q: Réaliser une requête un peu plus complexe qui permet de déterminer, par client et sur la période allant du
1er janvier 2019 au 31 décembre 2019, les ventes meuble et déco réalisées.**

Dans BigQuery je calculerais les ventes en groupant sur la clé client_id et product_type pour ensuite faire un pivot de cette façon:

``` sql
SELECT * FROM(
SELECT client_id, product_type, SUM(prod_price*prod_qty) AS ventes
FROM TRANSACTION
left join PRODUCT_NOMENCLATURE
ON TRANSACTION.prop_id = PRODUCT_NOMENCLATURE.product_id
WHERE YEAR(date) = "2019"
GROUP BY client_id, product_type
)
PIVOT(SUM(ventes) FOR product_type IN ('MEUBLE', 'DECO'))
```

Sinon sans utiliser les fonctionnalités de BigQuery voici comment j'aurait réalisé la requête:
``` sql
WITH ventes_client_type AS (
SELECT client_id, product_type, SUM(prod_price*prod_qty) AS ventes
FROM TRANSACTION
LEFT JOIN PRODUCT_NOMENCLATURE
ON TRANSACTION.prop_id = PRODUCT_NOMENCLATURE.product_id
WHERE YEAR(date) = "2019"
GROUP BY client_id, product_type
)

SELECT
    ventes_client_meuble.client_id AS client_id,
    ventes_client_meuble.ventes AS ventes_meuble,
    ventes_client_deco.ventes AS ventes_deco
FROM
    ventes_client_type AS ventes_client_meuble,
    ventes_client_type AS ventes_client_deco
WHERE
   ventes_client_meuble.client_id =  ventes_client_deco.client_id


```






