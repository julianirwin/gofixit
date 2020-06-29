#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gofixit.

Usage:
    gofixit
    gofixit help
    gofixit list assets
    gofixit list requests [--which=<which> | --asset_name=<asset_name>]
    gofixit create asset --name=<asset_name>
    gofixit create request --name=<request_name> --asset_name=<asset_name> --due_by=<YYYY-MM-DD> [--recur_every=<weeks>]
    gofixit interactive request

Options:
    --which=<which>             One of open, closed or overdue
    --asset_name=<asset_name>   Asset name
    --name=<request_name>       Request name
"""


from pathlib import Path
import pendulum
from pendulum.datetime import DateTime
from datetime import timedelta
from tinydb import TinyDB, Query, where
from pprint import pprint as pp
from tabulate import tabulate
from copy import deepcopy
from cliar import Cliar, set_help
import abc


# TEST = False

# def init(dbpath=None, test=False):
#     if test:
#         path_db_asset = Path.home() / Path(".gofixit/asset_test.json")
#         path_db_request = Path.home() / Path(".gofixit/request_test.json")

#         db_asset = TinyDB(path_db_asset)
#         db_asset.purge()
#         db_asset = GoFixItDB(db_asset)

#         db_request = TinyDB(path_db_request)
#         db_request.purge()
#         db_request = GoFixItDB(db_request)

#         c = Controller(db_asset=db_asset, db_request=db_request, view=ViewTabulate())
#         c.add_asset("The House")
#         c.add_asset("The House2")
#         # print(c.view_list_assets())
#         # print()
#         c.add_request(
#             asset_name="The House",
#             request_name="Mouse traps",
#             due_by=pendulum.now().add(weeks=2),
#             recurrence_period=timedelta(weeks=4),
#         )
#         c.add_request(
#             asset_name="The House",
#             request_name="Rat traps",
#             due_by=pendulum.now(),
#             recurrence_period=timedelta(weeks=4),
#         )
#         c.add_request(
#             asset_name="The House2",
#             request_name="Mouse traps2",
#             due_by=pendulum.now().add(weeks=2),
#             recurrence_period=timedelta(weeks=4),
#         )
#         # print(c.view_list_requests())
#         # print()
#         # c.view_create_request()
#         # c.view_list_asset_requests()
#         return c
#     else:
#         path_db_asset = Path.home() / Path(".gofixit/asset.json")
#         path_db_request = Path.home() / Path(".gofixit/request.json")

#         db_asset = TinyDB(path_db_asset)
#         db_asset = GoFixItDB(db_asset)

#         db_request = TinyDB(path_db_request)
#         db_request = GoFixItDB(db_request)

#         return Controller(db_asset=db_asset, db_request=db_request, view=ViewTabulate())


# class CommandList(Cliar):
#     def assets(self):
#         """List assets."""
#         c = init(dbpath=None, test=TEST)
#         c.view_list_assets()

#     def requests(self, which="overdue", asset_name="None"):
#         """List requests. <which> (-w) is 'all', 'open' or 'overdue'. If <asset_name> (-a) passed, only show that assets name."""
#         c = init(dbpath=None, test=TEST)
#         asset_name = None if asset_name.lower() == "none" else asset_name
#         print(c.view_list_requests(asset_name, which))


# create_asset_help = {'asset_name': 'Name of new asset'}
# create_request_help = {
#         'asset_doc_id': '(int) ID of an asset, from list asset',
#         'request_name': '(str) Name of new requet',
#         'due_by': '(str) "YYYY-MM-DD"',
#         'recurrence_period': '(int) Recurrence period in weeks'
#     }


# class CommandCreate(Cliar):
#     @set_help(create_asset_help)
#     def asset(self, asset_name):
#         """Add a new asset."""
#         c = init(dbpath=None, test=TEST)
#         c.add_asset(asset_name)
#         print("ASSETS")
#         print(c.view_list_assets())

#     @set_help(create_request_help)
#     def request(self, asset_doc_id, request_name, due_by, recurrence_period="None"):
#         """Add a new request."""
#         c = init(dbpath=None, test=TEST)
#         asset_doc_id = int(asset_doc_id)
#         due_by_dt = pendulum.from_format(due_by, "YYYY-MM-DD")
#         if recurrence_period.lower() == "none":
#             recurrence_period_td = None
#         else:
#             recurrence_period_td = timedelta(weeks=int(recurrence_period))
#         asset_name = c.asset_name_from_doc_id(asset_doc_id)
#         c.add_request(asset_name, request_name, due_by_dt, recurrence_period_td)
#         print(f"REQUESTS - ({asset_name})")
#         c.view_list_requests(asset_name, which='all')


# class CommandRemove(Cliar):
#     """Remove (delete) assets or requests."""
#     def asset(self, asset_doc_id):
#         c = init(dbpath=None, test=TEST)
#         asset_doc_id = int(asset_doc_id)
#         asset_name = c.asset_name_from_doc_id(asset_doc_id)
#         c.view_list_requests(asset_name, which='all')
#         print('Confirm remove [y/n]: ')
#         yn = input()
#         if yn.lower() == 'y':
#             c.remove_asset_and_requests(asset_doc_id)
#             print(f"Removed asset: {asset_name}")
#         else:
#             print('Exiting without removing')
#         print("ASSETS")
#         print(c.view_list_assets())

#     def request(self, request_doc_id):
#         c = init(dbpath=None, test=TEST)
#         c.remove_request(int(request_doc_id))
#         print(f"Removed request {request_doc_id}")


# complete_help = {'request_doc_id': '(int) document id of request.'}


# class CommandLineInterface(Cliar):
#     list = CommandList
#     create = CommandCreate
#     remove = CommandRemove

#     def _root(self, version=False):
#         print("Welcome to gofixit.py")

#     @set_help(complete_help)
#     def complete(self, request_doc_id):
#         """Mark request as complete. If it's recurring, due date will be incremented."""
#         c = init(dbpath=None, test=TEST)
#         asset_name = c.asset_doc_id_from_request_doc_id(request_doc_id)
#         c.complete_request(int(request_doc_id))
#         c.view_list_requests(asset_name, which='all')

#     @set_help(complete_help)
#     def close(self, request_doc_id):
#             """Mark request as complete. If it's recurring, due date will be incremented."""
#             c = init(dbpath=None, test=TEST)
#             asset_name = c.asset_doc_id_from_request_doc_id(request_doc_id)
#             c.close_request(int(request_doc_id))
#             c.view_list_requests(asset_name, which='all')

# class ViewTabulate(object):
#     def __init__(self, max_col_width=25):
#         self.max_col_width = max_col_width

#     def _crop_string_lengths(self, table):
#         if table is None or len(table) == 0:
#             return []
#         copy = deepcopy(table)
#         for d in copy:
#             for k, v in d.items():
#                 if isinstance(v, str) and len(v) > self.max_col_width:
#                     d[k] = v[: self.max_col_width] + "..."
#         return copy

#     def list_assets(self, table, show=True, **kwargs):
#         """Print to console."""
#         t = tabulate(self._crop_string_lengths(table), headers="keys", **kwargs)
#         if show:
#             print(t)
#         return t

#     def list_requests(self, table, show=True, **kwargs):
#         """Print to console."""
#         t = tabulate(self._crop_string_lengths(table), headers="keys", **kwargs)
#         if show:
#             print(t)
#         return t

#     def create_request(self):
#         """
#         Use raw_input() to get
#         - asset doc ID as Int
#         - request name as str
#         - due by as pendulum.DateTime
#         - recurrence period as None (one time) or timedelta
#         """
#         print("Asset doc id: ")
#         asset_doc_id = int(input())
#         print("Request name: ")
#         request_name = input()
#         print("Description: ")
#         description = input()
#         print("Due By [YYYY-MM-DD]: ")
#         due_by_dt = pendulum.from_format(input(), "YYYY-MM-DD")
#         print("Recurrence Period (weeks, blank for one time): ")
#         recurrent_period_str = input()
#         if recurrent_period_str.strip() == "":
#             recurrence_period_td = None
#         else:
#             recurrence_period_td = timedelta(weeks=int(recurrent_period_str))
#         return (
#             asset_doc_id,
#             request_name,
#             due_by_dt,
#             recurrence_period_td,
#             description,
#         )


# class Controller(object):
#     def __init__(self, db_asset, db_request, view=None):
#         self.db_asset = db_asset
#         self.db_request = db_request
#         self.view = view

#     def list_all(self):
#         return self.db.list_all()

#     def add_asset(self, asset_name):
#         asset = Asset(name=asset_name)
#         self.db_asset.insert(asset)

#     def asset_name_from_doc_id(self, doc_id):
#         return self.db_asset.db.get(doc_id=int(doc_id))['name']

#     def asset_name_from_request_doc_id(self, doc_id):
#         request = self.request_from_doc_id(doc_id)
#         return request['asset_name']

#     def asset_doc_id_from_request_doc_id(self, doc_id):
#         request = self.request_from_doc_id(doc_id)
#         return request['doc_id']

#     def asset_from_doc_id(self, doc_id):
#         return self.db_asset.db.get(doc_id=int(doc_id))

#     def request_from_doc_id(self, doc_id):
#         return self.db_request.db.get(doc_id=int(doc_id))

#     def list_assets(self):
#         # The member doc_id is a unique ID
#         return self.db_asset.list()

#     def add_request(
#         self, asset_name, request_name, due_by, recurrence_period=None,
#     ):
#         """
#         Add a request.

#         Args:
#             asset_name (str)
#             request_name (str)
#             due_by (datetime or DateTime)
#             recurrence_period (timedelta)
#         """
#         request = Request(
#             name=request_name,
#             asset_name=asset_name,
#             due_by=due_by,
#             recurrence_period=recurrence_period,
#         )
#         self.db_request.insert(request)

#     def list_requests(self, asset_name=None, which="all"):
#         """
#         Return a list of request document dicts.

#         Args:
#             which (str): 'all', 'overdue', 'open', 'closed'
#         """
#         # The member doc_id is a unique ID
#         if asset_name is None:
#             request_dicts = self.db_request.list()
#         else:
#             request_dicts = self.db_request.search(where('asset_name') == asset_name)
#         if which == "all":
#             return request_dicts
#         elif which == "open":
#             return [r for r in request_dicts if r["status"] >= 0]
#         elif which == "closed":
#             return [r for r in request_dicts if r["status"] < -1]
#         elif which == "overdue":
#             now = pendulum.now()
#             return [r for r in request_dicts if now > pendulum.parse(r["due_by"])]

#     def list_asset_requests(self, asset_name, which="all"):
#         """
#         List requests for a certain asset.

#         Args:
#             which (str): 'all', 'overdue', 'open', 'closed'
#         """
#         asset = self.db_asset.search(where("name") == asset_name)
#         if which == "all":
#             requests = self.db_request.search(where("asset_name") == asset_name)
#         elif which == "open":
#             requests = self.db_request.search(
#                 (where("asset_name") == asset_name) & (where("status") >= 0)
#             )
#         elif which == "closed":
#             requests = self.db_request.search(
#                 (where("asset_name") == asset_name) & (where("status") < 0)
#             )
#         elif which == "overdue":
#             overdue = lambda x: pendulum.now() > pendulum.parse(x)
#             requests = self.db_request.search(
#                 (where("asset_name") == asset_name) & (where("due_by").test(overdue))
#             )
#         return (asset, requests)

#     def complete_request(self, doc_id):
#         """
#         Mark request as complete (status 1).

#         For non-recurring, this sets status to 1.
#         For recurring, bumps due_by forward by recurrence_period
#         """
#         r = self.db_request.db.get(doc_id=doc_id)
#         if r["recurrence_period"] is None:
#             self.db_request.db.update({"status": 1}, doc_ids=[doc_id])
#         else:
#             td = timedelta(days=r["recurrence_period"])
#             due_by = pendulum.parse(r["due_by"])
#             new_due_by = due_by + td
#             self.db_request.db.update(
#                 {"due_by": new_due_by.to_iso8601_string()}, doc_ids=[doc_id]
#             )

#     def close_request(self, doc_id):
#         """
#         Mark request as closed (status -1).
#         """
#         self.db_request.db.update({"status": -1}, doc_ids=[doc_id])

#     def remove_request(self, doc_id):
#         """Delete/remove from db."""
#         self.db_request.remove(doc_id)

#     def remove_asset_and_requests(self, doc_id):
#         q = Query()
#         # asset = self.db_asset.db.search(q.doc_id == doc_id)
#         asset = self.db_asset.get_by_id(doc_id)[0]
#         self.db_asset.remove(doc_id)
#         requests = self.db_request.db.search(q.asset_name == asset["name"])
#         for r in requests:
#             self.remove_request(r.doc_id)

#     def view_list_all(self):
#         pass

#     def view_list_assets(self, **kwargs):
#         return self.view.list_assets(self.list_assets(), **kwargs)

#     def view_list_requests(self, asset_name=None, which='all', **kwargs):
#         return self.view.list_requests(self.list_requests(asset_name, which), **kwargs)

#     def view_list_asset_requests(self, which="all", **kwargs):
#         assets = [a["name"] for a in self.list_assets()]
#         print("")
#         for asset in assets:
#             asset, requests = self.list_asset_requests(asset, which)
#             print("ASSET")
#             self.view.list_assets(asset, **kwargs)
#             print("REQUESTS")
#             self.view.list_requests(requests, **kwargs)
#             print("")

#     def view_create_request(self):
#         self.view_list_assets()
#         request_input = self.view.create_request()
#         # (asset_doc_id, request_name, due_by, recurrence_period, description)
#         asset_name = self.db_asset.db.get(doc_id=request_input[0])["name"]
#         request = Request(
#             name=request_input[1],
#             asset_name=asset_name,
#             due_by=request_input[2],
#             recurrence_period=request_input[3],
#             description=request_input[4],
#         )
#         self.db_request.insert(request)


# class GoFixItDB(object):
#     def __init__(self, db):
#         self.db = db

#     def insert(self, doc_object):
#         """
#         Insert a request or asset into the db.

#         Args:
#             typeid (string): 'asset' or 'request'
#             doc_dict (dict): dict form of the Asset or Request object
#         """
#         doc_dict = doc_object.d
#         self.db.insert(doc_dict)

#     def search(self, *args, **kwargs):
#         """
#         Wraps tinydb search(). Used like:
#             >>> User = Query()
#             >>> db.search(User.name == 'John')
#         """
#         return self._add_doc_ids_to_docs(self.db.search(*args, **kwargs))

#     def list(self):
#         return self._add_doc_ids_to_docs(self.db.all())

#     def remove(self, doc_id):
#         self.db.remove(doc_ids=[doc_id])

#     def get_by_id(self, doc_id):
#         doc = self.db.get(doc_id=doc_id)
#         if doc is not None:
#             return self._add_doc_ids_to_docs([doc])
#         else:
#             raise ValueError(f'Document id {doc_id} not found')

#     def _add_doc_ids_to_docs(self, docs):
#         return [dict(doc_id=doc.doc_id, **doc) for doc in docs]


# class Asset(object):
#     def __init__(self, name, **kwargs):
#         created = pendulum.now()
#         self.d = dict(name=name, created=created.isoformat(), **kwargs)

#     def __str__(self):
#         return self.d.__str__()


# class Request(object):
#     def __init__(
#         self, name, asset_name, due_by, recurrence_period=None, description=None,
#     ):
#         """
#         Maintenance request or task.

#         In addition to args, the request has a created date and a status.

#         Status is an integer:
#             -1: Closed task
#             0: Open task that is incomplete
#             1: Completed

#         Schema in Database:
#             doc_id (int) : Unique ID provided by TinyDB
#             name (str)
#             asset_name (str)
#             due_by (str, iso8601 datetime)
#             recurrence_period (None or int, number of days)
#             description (str)
#             status (int)
#             created (str, iso8601 datetime)

#         Args:
#             name (str): Name of request (not unique)
#             asset_name (str): Name of associated asset
#             due_by (pendulum.DateTime): Due date
#             recurrence_period (timedelta): How often task must be done
#             description (string): Longer description than name
#         """
#         created = pendulum.now()
#         if recurrence_period is not None:
#             recurrence_period = recurrence_period.days
#         self.d = dict(
#             name=name,
#             asset_name=asset_name,
#             due_by=due_by.to_iso8601_string(),
#             recurrence_period=recurrence_period,
#             description=description,
#             created=created.to_iso8601_string(),
#             status=0,
#         )

#     def __str__(self):
#         return self.d.__str__()


class Model(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def to_dict() -> dict:
        pass

    @abc.abstractproperty
    def id(self) -> int:
        return self._id

    @property
    def model_name(self) -> str:
        return self._model_name


class Asset(Model):
    id: int
    name: str

    def __init__(self, id: int, name: str):
        self._model_name = "asset"
        self._id = id
        self._name = name

    def to_dict(self) -> dict:
        return dict(model_name=self.model_name, id=self.id, name=self.name)

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name


class Request(Model):
    id: int
    name: str
    asset_id: int
    due_date_iso8601: str
    recurrence_period_days: int
    comment: str

    def __init__(
        self,
        id: int,
        name: str,
        asset_id: int,
        due_date_iso8601: str,
        recurrence_period_days: int,
        comment: str,
    ):
        self._model_name = "request"
        self._id = id
        self._name = name
        self._asset_id = asset_id
        self._due_date_iso8601 = due_date_iso8601
        self._recurrence_period_days = recurrence_period_days
        self._comment = comment

    def to_dict(self) -> dict:
        d = dict(
            model_name=self.model_name,
            id=get_unique_id(),
            asset_id=self.asset_id,
            name=self.name,
            due_date=self.due_date,
            recurrence_period_days=self.recurrence_period_days,
            comment=self.comment,
        )
        return d

    @property
    def id(self) -> int:
        return self._id

    @property
    def asset_id(self) -> int:
        return self._asset_id

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def name(self) -> str:
        return self._name

    @property
    def due_date_iso8601(self) -> str:
        return self._due_date_iso8601

    @property
    def recurrence_period_days(self) -> int:
        return self._recurrence_period_days

    @property
    def comment(self) -> str:
        return self._comment


class Table(metaclass=abc.ABCMeta):
    def __init__(self, db: TinyDB, model_name: str):
        self._db = db
        self.model_name = "model_name"

    @property
    def db(self) -> TinyDB:
        return self._db

    @property
    def model_name(self) -> TinyDB:
        return self._model_name

    def insert(self, asset):
        self.db.insert(asset.to_dict())

    def update(self, fields, id):
        model = Query()
        right_model_name = model.model_name == self.model_name
        right_id = model.id == id
        self.db.update(fields, right_model_name & right_id)

    # def all(self):
    #     model = Query()
    #     return db.


class AssetTable(Table):
    def __init__(self, db: TinyDB):
        self._db = db
        self._model_name = "asset"


class RequestTable(Table):
    def __init__(self, db: TinyDB):
        self._db = db
        self._model_name = "request"


def get_unique_id(model: Model):
    pass


def initialize():
    db_path = Path.home() / Path(".gofixit/gofixit.json")

    db = TinyDB(path_db_asset)
