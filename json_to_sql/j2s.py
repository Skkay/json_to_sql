#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json

class J2S:
    def __init__(self, json_file_name, json_data):
        self.json = json.loads(json_data.read())
        self.json_file = json_file_name

        self.jvalue = {}
        self.jarray = {}
        self.jarray_of_array = {}
        self.jobject = {}
        self.jarray_of_object = {}

        self.all_jvalue_data = []
        self.all_jarray_data = []
        self.all_jarray_of_array_data = []
        self.all_jobject_data = []
        self.all_jarray_of_object_data = []

        self.queries = ""


    def process(self):
        print("Reading json...")
        self.unnest_json(self.json)

        print("Remapping data...")
        self.remapping_data(self.json)

        print("Generating create table queries...")
        self.queries += self.generate_create_table_for_jvalue() + "\n"
        self.queries += self.generate_create_table_for_jarray() + "\n"
        self.queries += self.generate_create_table_for_jarrayOfArray() + "\n"
        self.queries += self.generate_create_table_for_jobject() + "\n"
        self.queries += self.generate_create_table_for_jarrayOfObject() + "\n"

        print("Generating insert into queries...")
        self.queries += self.generate_insert_into_for_jvalue() + "\n"
        self.queries += self.generate_insert_into_for_jarray() + "\n"
        self.queries += self.generate_insert_into_for_jarrayOfArray() + "\n"
        self.queries += self.generate_insert_into_for_jobject() + "\n"
        self.queries += self.generate_insert_into_for_jarrayOfObject() + "\n"


    def get_query(self):
        return self.queries


    def unnest_json(self, json):
        """
        Parcours le json donné pour remplir les dictionnaires "jvalue", "jarray", "jarray_of_array", "jobject",
        "jarray_of_object" selon les valeurs trouvées.

        Parameters:
            json (str) : Données au format json
        """
        for data in self.json:
            for key, value in data.items():
                # Si c'est un objet. Ex: "pos": {"x" : 0, "y": 1}
                if type(value) is dict:
                    object = {} # Dict temporaire : Nom de la clef, type de la valeur. Ex: x, int

                    # Pour chaque clef, valeur de l'objet
                    for s_key, s_value in value.items():
                        object[s_key] = type(s_value)
                    self.jobject[key] = object

                # Si c'est une liste. Ex: "ids": [0,1,2,3]
                elif type(value) is list:
                    # Si la liste n'est pas vide
                    if value:
                        # Si c'est une liste de liste
                        if type(value[0]) is list:
                            self.jarray_of_array[key] = [type(value[0][0]), len(value[0])]
                            if key in self.jarray: self.jarray.pop(key)

                        # Si c'est une liste d'objet
                        elif type(value[0]) is dict:
                            object = {} # Dict temporaire : Nom de la clef, type de la valeur. Ex: x, int

                            # Pour chaque clef, valeur de l'objet
                            for s_key, s_value in value[0].items():
                                object[s_key] = type(s_value)
                            self.jarray_of_object[key] = object
                            if key in self.jarray: self.jarray.pop(key)

                        # Si c'est une simple liste
                        else:
                            self.jarray[key] = type(value[0])

                    #  Si la liste est vide
                    else:
                        if key not in self.jarray and key not in self.jarray_of_array and key not in self.jarray_of_object:
                            self.jarray[key] = '?'

                # Si c'est une autre valeur. Ex: "id": 1, "isAlive": true, "token": "Gs5Q4"
                else:
                    self.jvalue[key] = type(value)


    def generate_create_table_for_jvalue(self):
        """
        Retourne la requête permettant de créer la table des "jvalue".

        Return:
            query (str)
        """
        query = "CREATE TABLE IF NOT EXISTS `{table_name}` (`_Id` int(11) NOT NULL,".format(table_name=self.json_file)
        for key, value in self.jvalue.items():
            if value is int:
                query += "`{col}` int(11) DEFAULT NULL,".format(col=key)
            elif value is bool:
                query += "`{col}` tinyint(1) DEFAULT NULL,".format(col=key)
            elif value is str:
                query += "`{col}` varchar(255) DEFAULT NULL,".format(col=key)
            elif value is float:
                query += "`{col}` float DEFAULT NULL,".format(col=key)

        query = query[:-1] # Enlève la dernière virgule
        query += ") ENGINE=MyISAM DEFAULT CHARSET=utf8;"

        return query


    def generate_create_table_for_jarray(self):
        """
        Retourne la requête permettant de créer la table des "jarray".

        Return:
            query (str)
        """
        query = ""
        for key, value in self.jarray.items():
            sub_query = "CREATE TABLE IF NOT EXISTS `{table_name}` (`{table_parent}_Id` int(11) NOT NULL,".format(table_name=self.json_file + "__" + key, table_parent=self.json_file)
            if value is int:
                sub_query += "`{col}` int(11) DEFAULT NULL,".format(col=key)
            elif value is bool:
                sub_query += "`{col}` tinyint(1) DEFAULT NULL,".format(col=key)
            elif value is str:
                sub_query += "`{col}` varchar(255) DEFAULT NULL,".format(col=key)
            elif value is float:
                sub_query += "`{col}` float DEFAULT NULL,".format(col=key)
            sub_query = sub_query[:-1] # Enlève la dernière virgule
            sub_query += ") ENGINE=MyISAM DEFAULT CHARSET=utf8;"
            query += sub_query + "\n"

        return query[:-1]


    def generate_create_table_for_jarrayOfArray(self):
        """
        Retourne la requête permettant de créer la table des "jarray_of_array".

        Return:
            query (str)
        """
        query = ""
        for key, value in self.jarray_of_array.items():
            sub_query = "CREATE TABLE IF NOT EXISTS `{table_name}` (`{table_parent}_Id` int(11) NOT NULL,".format(table_name=self.json_file + "__" + key, table_parent=self.json_file)
            if value[0] is int:
                for i in range(0, value[1]):
                    sub_query += "`{col}_{counter}` int(11) DEFAULT NULL,".format(col=key, counter=i+1)
            elif value[0] is bool:
                for i in range(0, value[1]):
                    sub_query += "`{col}_{counter}` tinyint(1) DEFAULT NULL,".format(col=key, counter=i+1)
            elif value[0] is str:
                for i in range(0, value[1]):
                    sub_query += "`{col}_{counter}` varchar(255) DEFAULT NULL,".format(col=key, counter=i+1)
            elif value[0] is float:
                for i in range(0, value[1]):
                    sub_query += "`{col}_{counter}` float DEFAULT NULL,".format(col=key, counter=i+1)
            sub_query = sub_query[:-1] # Enlève la dernière virgule
            sub_query += ") ENGINE=MyISAM DEFAULT CHARSET=utf8;"
            query += sub_query + "\n"

        return query[:-1]


    def generate_create_table_for_jobject(self):
        """
        Retourne la requête permettant de créer la table des "jarray_of_array".

        Return:
            query (str)
        """
        query = ""
        for key, value in self.jobject.items():
            sub_query = "CREATE TABLE IF NOT EXISTS `{table_name}` (`{table_parent}_Id` int(11) NOT NULL,".format(table_name=self.json_file + "__" + key, table_parent=self.json_file)
            for s_key, s_value in value.items():
                if s_value is int:
                    sub_query += "`{col}` int(11) DEFAULT NULL,".format(col=s_key)
                elif s_value is bool:
                    sub_query += "`{col}` tinyint(1) DEFAULT NULL,".format(col=s_key)
                elif s_value is str:
                    sub_query += "`{col}` varchar(255) DEFAULT NULL,".format(col=s_key)
                elif s_value is float:
                    sub_query += "`{col}` float DEFAULT NULL,".format(col=s_key)
            sub_query = sub_query[:-1] # Enlève la dernière virgule
            sub_query += ") ENGINE=MyISAM DEFAULT CHARSET=utf8;"
            query += sub_query + "\n"

        return query[:-1]


    def generate_create_table_for_jarrayOfObject(self):
        """
        Retourne la requête permettant de créer la table des "jarray_of_array".

        Return:
            query (str)
        """
        query = ""
        for key, value in self.jarray_of_object.items():
            sub_query = "CREATE TABLE IF NOT EXISTS `{table_name}` (`{table_parent}_Id` int(11) NOT NULL,".format(table_name=self.json_file + "__" + key, table_parent=self.json_file)
            for s_key, s_value in value.items():
                if s_value is int:
                    sub_query += "`{col}` int(11) DEFAULT NULL,".format(col=s_key)
                elif s_value is bool:
                    sub_query += "`{col}` tinyint(1) DEFAULT NULL,".format(col=s_key)
                elif s_value is str:
                    sub_query += "`{col}` varchar(255) DEFAULT NULL,".format(col=s_key)
                elif s_value is float:
                    sub_query += "`{col}` float DEFAULT NULL,".format(col=s_key)
            sub_query = sub_query[:-1] # Enlève la dernière virgule
            sub_query += ") ENGINE=MyISAM DEFAULT CHARSET=utf8;"
            query += sub_query + "\n"

        return query[:-1]



    def remapping_data(self, json):
        """
        Organise les données du json dans les listes "all_jvalue_data", "all_jarray_data", "all_jarray_of_array_data",
        "all_jobject_data", "all_jarray_of_object_data" afin de les exploiter plus facilement.

        Parameters:
            json (str) : Données au format json
        """
        _Id = 0
        for data in json:
            ## JVALUE
            list = []
            dict = {}
            for key, type in self.jvalue.items():
                if key in data:
                    dict[key] = data[key]
            list.append(_Id)
            list.append(dict)
            self.all_jvalue_data.append(list)
            ## ------------------------------------- ##

            ## JARRAY
            list = []
            dict = {}
            for key, type in self.jarray.items():
                dict[key] = data[key]
            list.append(_Id)
            list.append(dict)
            self.all_jarray_data.append(list)
            ## ------------------------------------- ##

            ## JARRAY_OF_ARRAY
            list = []
            dict = {}
            for key, type in self.jarray_of_array.items():
                dict[key] = data[key]
            list.append(_Id)
            list.append(dict)
            self.all_jarray_of_array_data.append(list)
            ## ------------------------------------- ##

            ## JOBJECT
            list = []
            dict = {}
            for key, value in self.jobject.items():
                s_dict = {}
                for s_key, s_value in value.items():
                    s_dict[s_key] = data[key][s_key]
                dict[key] = s_dict
            list.append(_Id)
            list.append(dict)
            self.all_jobject_data.append(list)
            ## ------------------------------------- ##

            ## JARRAY_OF_OBJECT
            list = []
            dict = {}
            for key, value in self.jarray_of_object.items():
                if data[key]: # Si la liste n'est pas vide
                    s_list = []
                    for object in data[key]:
                        s_dict = {}
                        for s_key, s_value in value.items():
                            s_dict[s_key] = object[s_key]
                        s_list.append(s_dict)
                    dict[key] = s_list
                    list.append(_Id)
                    list.append(dict)
                    self.all_jarray_of_object_data.append(list)
            ## ------------------------------------- ##

            _Id += 1


    def generate_insert_into_for_jvalue(self):
        """
        Retourne les requêtes permettant d'insérer les données des "jvalue" dans leur table associée.

        Return:
            query (str)
        """
        query = ""
        for data in self.all_jvalue_data:
            query_insert = "INSERT INTO `{table_name}` (`_Id`, ".format(table_name=self.json_file)
            query_values = " VALUES ({val}, ".format(val=data[0])
            for key, value in data[1].items():
                query_insert += "`{col}`, ".format(col=key)
                if type(value) is int or type(value) is float:  # Si la valeur est un int ou float : pas de ` `
                    query_values += "{val}, ".format(val=value)
                elif value == True:                 # Si la valeur est True : remplace par 1 (TINYINT)
                    query_values += "1, "
                elif value == False:                # Si la valeur est False : remplace par 0 (TINYINT)
                    query_values += "0, "
                else:                               # str
                    query_values += "'{val}', ".format(val=value)
            query_insert = query_insert[:-2] + ")"
            query_values = query_values[:-2] + ");\n"
            query += query_insert + query_values

        return query[:-1]


    def generate_insert_into_for_jarray(self):
        """
        Retourne les requêtes permettant d'insérer les données des "jarray" dans leurs tables associées.

        Return:
            query (str)
        """
        query = ""
        for data in self.all_jarray_data:
            for key, value in data[1].items():
                for s_value in value:
                    query += "INSERT INTO `{table_name}` (`{table_parent}_Id`, `{col}`) VALUES ({id_parent}, ".format(
                        table_name=self.json_file + "__" + key,
                        table_parent=self.json_file,
                        col=key,
                        id_parent=data[0]
                    )

                    if type(s_value) is int or type(s_value) is float:  # Si la valeur est un int ou float : pas de ` `
                        query += "{val}".format(val=s_value)
                    elif s_value == True:                               # Si la valeur est True : remplace par 1 (TINYINT)
                        query += "1"
                    elif s_value == False:                              # Si la valeur est False : remplace par 0 (TINYINT)
                        query += "0"
                    else:                                               # str
                        query += "'{val}'".format(val=s_value)

                    query += ");\n"

        return query[:-1]


    def generate_insert_into_for_jarrayOfArray(self):
        """
        Retourne les requêtes permettant d'insérer les données des "jarrayOfArray" dans leurs tables associées.

        Return:
            query (str)
        """
        query = ""
        for data in self.all_jarray_of_array_data:
            for key, value in data[1].items():
                for list in value:
                    query_insert = "INSERT INTO `{table_name}` (`{table_parent}_Id`, ".format(table_name=self.json_file + "__" + key, table_parent=self.json_file)
                    query_values = " VALUES ({id_parent}, ".format(id_parent=data[0])
                    i = 1
                    for s_value in list:
                        query_insert += "`{col}_{count}`, ".format(col=key, count=i)
                        if type(s_value) is int or type(s_value) is float:  # Si la valeur est un int ou float : pas de ` `
                            query_values += "{val}, ".format(val=s_value)
                        elif s_value == True:                               # Si la valeur est True : remplace par 1 (TINYINT)
                            query_values += "1, "
                        elif s_value == False:                              # Si la valeur est False : remplace par 0 (TINYINT)
                            query_values += "0, "
                        else:                                               # str
                            query_values += "'{val}', ".format(val=s_value)

                        i += 1

                    query_insert = query_insert[:-2] + ")"
                    query_values = query_values[:-2] + ");\n"
                    query += query_insert + query_values

        return query[:-1]


    def generate_insert_into_for_jobject(self):
        """
        Retourne les requêtes permettant d'insérer les données des "jobject" dans leurs tables associées.

        Return:
            query (str)
        """
        query = ""
        for data in self.all_jobject_data:
            for key, value in data[1].items():
                sub_query_insert = "INSERT INTO `{table_name}` (`{table_parent}_Id`, ".format(table_name=self.json_file + "__" + key, table_parent=self.json_file)
                sub_query_values = " VALUES ({val}, ".format(val=data[0])
                for s_key, s_value in value.items():
                    sub_query_insert += "`{col}`, ".format(col=s_key)
                    if type(s_value) is int or type(s_value) is float:  # Si la valeur est un int ou float : pas de ` `
                        sub_query_values += "{val}, ".format(val=s_value)
                    elif s_value == True:                               # Si la valeur est True : remplace par 1 (TINYINT)
                        sub_query_values += "1, "
                    elif s_value == False:                              # Si la valeur est False : remplace par 0 (TINYINT)
                        sub_query_values += "0, "
                    else:                                               # str
                        sub_query_values += "'{val}', ".format(val=s_value)
                sub_query_insert = sub_query_insert[:-2] + ")"
                sub_query_values = sub_query_values[:-2] + ");\n"
                query += sub_query_insert + sub_query_values

        return query[:-1]


    def generate_insert_into_for_jarrayOfObject(self):
        """
        Retourne les requêtes permettant d'insérer les données des "jarrayOfObject" dans leurs tables associées.

        Return:
            query (str)
        """
        query = ""
        for data in self.all_jarray_of_object_data:
            for key, value in data[1].items():
                for object in value:
                    sub_query_insert = "INSERT INTO `{table_name}` (`{table_parent}_Id`, ".format(table_name=self.json_file + "__" + key, table_parent=self.json_file)
                    sub_query_values = " VALUES ({val}, ".format(val=data[0])
                    for s_key, s_value in object.items():
                        sub_query_insert += "`{col}`, ".format(col=s_key)
                        if type(s_value) is int or type(s_value) is float:  # Si la valeur est un int ou float : pas de ` `
                            sub_query_values += "{val}, ".format(val=s_value)
                        elif s_value == True:                               # Si la valeur est True : remplace par 1 (TINYINT)
                            sub_query_values += "1, "
                        elif s_value == False:                              # Si la valeur est False : remplace par 0 (TINYINT)
                            sub_query_values += "0, "
                        else:                                               # str
                            sub_query_values += "'{val}', ".format(val=s_value)
                    sub_query_insert = sub_query_insert[:-2] + ")"
                    sub_query_values = sub_query_values[:-2] + ");\n"
                    query += sub_query_insert + sub_query_values

        return query[:-1]
