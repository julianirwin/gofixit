#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 12:28:35 2020

@author: Julian
"""

from pathlib import Path
import pendulum
from tinydb import TinyDB, Query
from pprint import pprint as pp
from tabulate import tabulate


class ViewTabulate(object):
    def __init__(self):
        pass

    def list_assets(self, table):
        print(tabulate(table, headers="keys"))

    def list_requests(self, table):
        print(tabulate(table, headers="keys"))

    def create_request(self):
        self.list_assets()
        print('Asset doc id: ')
        asset_doc_id = int(raw_input())
        print('Request name:')
        asset_doc_id = raw_input()
        print('Request name:')
        asset_doc_id = raw_input()




class Controller(object):
    def __init__(self, db_asset, db_request, view=None):
        self.db_asset = db_asset
        self.db_request = db_request
        self.view = view

    def add_asset(self, asset_name):
        asset = Asset(name=asset_name)
        self.db_asset.insert(asset)

    def list_all(self):
        return self.db.list_all()

    def remove(self, doc_id):
        self.db.remove(doc_id)

    def list_assets(self):
        # The member doc_id is a unique ID
        return self.db_asset.list()

    def add_request(
        self, asset_name, request_name, due_by, recurring=False, recurrence_period=None,
    ):
        request = Request(
            name=request_name,
            asset_name=asset_name,
            due_by=due_by,
            recurring=recurring,
            recurrence_period=recurrence_period,
        )
        self.db_request.insert(request)

    def list_requests(self):
        # The member doc_id is a unique ID
        return self.db_request.list()

    def view_list_all(self):
        pass

    def view_list_assets(self):
        return self.view.list_assets(self.list_assets())

    def view_list_requests(self):
        return self.view.list_requests(self.list_requests())


class GoFixItDB(object):
    def __init__(self, db_backend):
        self.db_backend = db_backend

    def insert(self, doc_object):
        """
        Insert a request or asset into the db.

        Args:
            typeid (string): 'asset' or 'request'
            doc_dict (dict): dict form of the Asset or Request object
        """
        doc_dict = doc_object.d
        # d = dict(typeid=typeid, **doc_dict)
        self.db_backend.insert(doc_dict)

    # def list(self):
    #     """
    #     List all docs of typeid ('asset' or 'request')
    #     """
    #     item = Query()
    #     docs = self.db_backend.search(item.typeid == typeid)
    #     return self._add_doc_ids_to_docs(docs)

    def list(self):
        return self._add_doc_ids_to_docs(self.db_backend.all())

    def remove(self, doc_id):
        self.db_backend.remove(doc_ids=[doc_id])

    def _add_doc_ids_to_docs(self, docs):
        return [dict(doc_id=doc.doc_id, **doc) for doc in docs]


class Asset(object):
    def __init__(self, name, **kwargs):
        created = pendulum.now()
        self.d = dict(name=name, created=created.isoformat(), **kwargs)

    def __str__(self):
        return self.d.__str__()


class Request(object):
    def __init__(
        self,
        name,
        asset_name,
        due_by,
        recurring=False,
        recurrence_period=None,
        description=None,
    ):
        created = pendulum.now()
        self.d = dict(
            name=name,
            asset_name=asset_name,
            due_by=due_by.to_iso8601_string(),
            recurring=recurring,
            recurrence_period=recurrence_period,
            description=description,
            created=created.to_iso8601_string(),
            status="open",
        )

    def __str__(self):
        return self.d.__str__()


# class TestAsset(object):
#     def test_asset_name(self):
#         a = Asset(name="Asset0")
#         assert a.__str__() == "{'name': 'Asset0'}"

#     def test_asset_from_dict(self):
#         kwargs = {"prop1": 1, "prop2": 2}
#         a = Asset(name="Asset0", **kwargs)
#         assert a.__str__() == "{'name': 'Asset0', 'prop1': 1, 'prop2': 2}"


# class TestController(object):
#     pass


# if __name__ == "__main__":
#     path_db_asset = Path.home() / Path(".gofixit/asset_test.json")
#     path_db_request = Path.home() / Path(".gofixit/request_test.json")

#     db_asset = TinyDB(path_db_asset)
#     db_asset.purge()
#     db_asset = GoFixItDB(db_asset)

#     db_request = TinyDB(path_db_request)
#     db_request.purge()
#     db_request = GoFixItDB(db_request)

#     c = Controller(db_asset=db_asset, db_request=db_request, view=ViewTabulate())
#     c.add_asset("The House")
#     c.add_asset("The House2")
#     print(c.view_list_assets())
#     print()
#     due_by = pendulum.now().add(days=7)
#     c.add_request(
#         asset_name="The House",
#         request_name="Mouse traps",
#         due_by=pendulum.now().add(weeks=2),
#         recurring=False,
#     )
#     print(c.view_list_requests())
#     print()

if __name__ == "__main__":
    path_db_asset = Path.home() / Path(".gofixit/asset.json")
    path_db_request = Path.home() / Path(".gofixit/request.json")

    db_asset = TinyDB(path_db_asset)
    db_asset = GoFixItDB(db_asset)

    db_request = TinyDB(path_db_request)
    db_request = GoFixItDB(db_request)

    c = Controller(db_asset=db_asset, db_request=db_request, view=ViewTabulate())
