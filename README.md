# JSON to SQL
Convertisseur JSON vers SQL en Python. Génère les scripts de création des tables et les insertions pour un ou plusieurs fichiers JSON. Gère les types int, float, string, bool, array, object. Voir détail plus bas.
MySQL seulement.

## Limitation
Ce script est adapté pour les JSON ayant des élements de cette forme :
```json
[
    {
        "str_key": "value",
        "int_key": 10,
        "float_key": -273.15,
        "bool_key": false,
        "list_key": [1, 2, 3, 4, 5],
        "object_key": {
            "some_key": "some_value",
            "another_key": 75
        },
        "list_object_key": [
            {
                "one_key": "one_value",
                "two_key": true
            },
            {
                "one_key": "one_value",
                "two_key": true
            }
        ],
        "list_list_key": [
            [1.0, 0.1214],
            [2.0, 0.987]
        ]
    }
]
```

## Utilisation
Les fichiers JSON doivent être placés dans le dossier ``input/``.
Exécuter le script ``J2S_process.py``
Les fichiers SQL seront dans le dossier ``output/``


## Exemple
Avec le JSON dans ``input/JsonExample.json`` :
Génère les requêtes SQL suivantes :
```sql
CREATE TABLE IF NOT EXISTS `JsonExample` (`_Id` int(11) NOT NULL,`str_key` varchar(255) DEFAULT NULL,`int_key` int(11) DEFAULT NULL,`float_key` float DEFAULT NULL,`bool_key` tinyint(1) DEFAULT NULL) ENGINE=MyISAM DEFAULT CHARSET=utf8;
CREATE TABLE IF NOT EXISTS `JsonExample__list_key` (`JsonExample_Id` int(11) NOT NULL,`list_key` int(11) DEFAULT NULL) ENGINE=MyISAM DEFAULT CHARSET=utf8;
CREATE TABLE IF NOT EXISTS `JsonExample__list_list_key` (`JsonExample_Id` int(11) NOT NULL,`list_list_key_1` int(11) DEFAULT NULL,`list_list_key_2` int(11) DEFAULT NULL) ENGINE=MyISAM DEFAULT CHARSET=utf8;
CREATE TABLE IF NOT EXISTS `JsonExample__object_key` (`JsonExample_Id` int(11) NOT NULL,`some_key` varchar(255) DEFAULT NULL,`another_key` int(11) DEFAULT NULL) ENGINE=MyISAM DEFAULT CHARSET=utf8;
CREATE TABLE IF NOT EXISTS `JsonExample__list_object_key` (`JsonExample_Id` int(11) NOT NULL,`one_key` varchar(255) DEFAULT NULL,`two_key` tinyint(1) DEFAULT NULL) ENGINE=MyISAM DEFAULT CHARSET=utf8;
INSERT INTO `JsonExample` (`_Id`, `str_key`, `int_key`, `float_key`, `bool_key`) VALUES (0, 'value', 10, -273.15, 0);
INSERT INTO `JsonExample` (`_Id`, `str_key`, `int_key`, `float_key`, `bool_key`) VALUES (1, 'value_2', 102, 154.2, 0);
INSERT INTO `JsonExample__list_key` (`JsonExample_Id`, `list_key`) VALUES (0, 1);
INSERT INTO `JsonExample__list_key` (`JsonExample_Id`, `list_key`) VALUES (0, 2);
INSERT INTO `JsonExample__list_key` (`JsonExample_Id`, `list_key`) VALUES (0, 3);
INSERT INTO `JsonExample__list_key` (`JsonExample_Id`, `list_key`) VALUES (0, 4);
INSERT INTO `JsonExample__list_key` (`JsonExample_Id`, `list_key`) VALUES (0, 5);
INSERT INTO `JsonExample__list_key` (`JsonExample_Id`, `list_key`) VALUES (1, 12);
INSERT INTO `JsonExample__list_key` (`JsonExample_Id`, `list_key`) VALUES (1, 2);
INSERT INTO `JsonExample__list_list_key` (`JsonExample_Id`, `list_list_key_1`, `list_list_key_2`) VALUES (0, 1, 0.1214);
INSERT INTO `JsonExample__list_list_key` (`JsonExample_Id`, `list_list_key_1`, `list_list_key_2`) VALUES (0, 2, 0.987);
INSERT INTO `JsonExample__list_list_key` (`JsonExample_Id`, `list_list_key_1`, `list_list_key_2`) VALUES (1, 1, 1.25);
INSERT INTO `JsonExample__list_list_key` (`JsonExample_Id`, `list_list_key_1`, `list_list_key_2`) VALUES (1, 4, 8.3);
INSERT INTO `JsonExample__list_list_key` (`JsonExample_Id`, `list_list_key_1`, `list_list_key_2`) VALUES (1, 4, 2.347);
INSERT INTO `JsonExample__list_list_key` (`JsonExample_Id`, `list_list_key_1`, `list_list_key_2`) VALUES (1, 902, 8.3547);
INSERT INTO `JsonExample__object_key` (`JsonExample_Id`, `some_key`, `another_key`) VALUES (0, 'some_value', 75);
INSERT INTO `JsonExample__object_key` (`JsonExample_Id`, `some_key`, `another_key`) VALUES (1, 'some_value', 75987);
INSERT INTO `JsonExample__list_object_key` (`JsonExample_Id`, `one_key`, `two_key`) VALUES (0, 'one_value', 1);
INSERT INTO `JsonExample__list_object_key` (`JsonExample_Id`, `one_key`, `two_key`) VALUES (0, 'a_value', 0);
INSERT INTO `JsonExample__list_object_key` (`JsonExample_Id`, `one_key`, `two_key`) VALUES (1, 'value ?', 0);
INSERT INTO `JsonExample__list_object_key` (`JsonExample_Id`, `one_key`, `two_key`) VALUES (1, 'hey', 1);
```

--------

## Informations sur le script
##### jvalue :
Correspond aux valeurs simples associées aux clés.
**Exemple :** "id": 1, "text": "some text"
**Format :** Dictionnaire : {Nom de la clef, Type de la valeur}
**Exemple du format :**  {'id': <class 'int'>, 'nameId': <class 'str'>}

##### jarray :
Correspond aux listes de valeurs associées aux clés.
**Exemple :** "Ids": [1, 2. 3, 4, 6], "decimals": [0.12, 0.15, 0.47, 0.54]
**Format :** Dictionnaire : {Nom de la clef, Type des valeurs de la liste}
**Exemple du format :** {'Ids': <class 'int'>, 'shape': <class 'float'>}

##### jarray_of_array :
Correspond aux listes imbriquées à deux niveaux.
**Exemple :** "playlists": [[1,34,0], [4,4,1], [3,207,2]], "quests": [[1,5], [4,2], [7,2]]
**Format :** Dictionnaire : {Nom de la clef, Tuple : (Type des valeurs, Nombre d'élement)}
**Exemple du format :** {'playlists': [<class 'int'>, 3], 'quests': [<class 'float'>, 2]}

##### jobject :
Correspond aux objets associés aux clés.
**Exemple :** "bounds": { "x": 1, "y": 1 }
**Format :** Dictionnaire : {Nom de la clef, Dictionnaire : {Nom de la sous clef, Type de la sous valeur}}
**Exemple du format :** {'bounds': {'x': <class 'int'>, 'y': <class 'int'>}}

##### jarray_of_object :
Correspond aux listes d'objets associés aux clés.
**Exemple :** "ambientSounds": [{"id": 1, "volume": 124}, {"id": 2, "volume": 54}]
**Format :** Dictionnaire : {Nom de la clef, Dictionnaire : {Nom de la sous clef, Type de la sous valeur}}
**Exemple du format :** {'ambientSounds': {'id': <class 'int'>, 'volume': <class 'int'>}}
&nbsp;
--------
&nbsp;
Les listes suivantes contiennent des listes à deux élements : l'identifiant et un dictionnaire.
Le dictionnaire contient les valeurs de l'objet.
**Exemple pour all_jvalue_data :**
`
[
    [0, {"nameId":3011, "containHouses": true, "containPaddocks":false}]
]
`

**Exemple pour all_jarray_data :**
`
[
    [0, {"mapIds": [1,2,3,4,5,6], "areaIds": [1,2,3,4]}]
]
`

**Exemple pour all_jarray_of_array_data :**
`
[
    [0, {"playlists": [[1,2], [2,3]], "quests": [[121, 124], [1,45]]}]
]
`

**Exemple pour all_jobject_data :**
`
[
    [0, {"bounds": {"x": 1, "y": 2}, "object": {"val1" : 1, "val2": 2}}]
]
`

**Exemple pour all_jarray_of_object_data :**
`
[
    [0, {"ambientSounds": [{"id": 15454, "volume": 11, "channel": 0}, {"id": 987, "volume": 12, "channel": 1}]}]
]
`
