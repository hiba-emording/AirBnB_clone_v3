#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
import json
import os
import pep8
import unittest

DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    def test_new(self):
        """test that new adds an object to the database"""

    def test_save(self):
        """Test that save properly saves objects to file.json"""

    def setUp(self):
        """Set up test environment"""
        self.state = State(name="California")
        storage.new(self.state)
        storage.save()
        self.city = City(state_id=self.state.id, name="San Francisco")
        storage.new(self.city)
        storage.save()

    def tearDown(self):
        """Tear down test environment"""
        storage.delete(self.city)
        storage.delete(self.state)
        storage.save()

    def test_get_state(self):
        """Test get() method for State"""
        state_id = self.state.id
        fetched_state = storage.get(State, state_id)
        self.assertIsNotNone(fetched_state)
        self.assertEqual(fetched_state.id, state_id)
        self.assertEqual(fetched_state.name, "California")

    def test_get_city(self):
        """Test get() method for City"""
        city_id = self.city.id
        fetched_city = storage.get(City, city_id)
        self.assertIsNotNone(fetched_city)
        self.assertEqual(fetched_city.id, city_id)
        self.assertEqual(fetched_city.name, "San Francisco")

    def test_count_all(self):
        """Test count() method for all objects"""
        initial_count = storage.count()
        self.assertGreaterEqual(initial_count, 2)

    def test_count_state(self):
        """Test count() method for State objects"""
        state_count = storage.count(State)
        self.assertGreaterEqual(state_count, 1)

    def test_count_city(self):
        """Test count() method for City objects"""
        city_count = storage.count(City)
        self.assertGreaterEqual(city_count, 1)

    def test_get_db(self):
        """Tests method for obtaining an instance from db storage"""
        dic = {"name": "Cundinamarca"}
        instance = State(**dic)
        storage.new(instance)
        storage.save()
        get_instance = storage.get(State, instance.id)
        self.assertIsNotNone(get_instance)
        self.assertEqual(get_instance, instance)

    def test_count(self):
        """Tests count method for db storage"""
        dic = {"name": "Vecindad"}
        state = State(**dic)
        storage.new(state)
        storage.save()
        dic = {"name": "Mexico", "state_id": state.id}
        city = City(**dic)
        storage.new(city)
        storage.save()
        c = storage.count()
        self.assertEqual(len(storage.all()), c)

if __name__ == '__main__':
    unittest.main()
