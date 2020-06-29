#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 20:52:21 2020

@author: Julian
"""

from gofixit import Asset, Request, AssetTable
from tinydb import TinyDB, Query
import pytest
from pathlib import Path


@pytest.fixture
def simple_asset():
    return Asset(0, "house")


class TestAsset:
    def test_create_asset(self, simple_asset):
        pass

    def test_asset_properties(self, simple_asset):
        assert simple_asset.model_name == "asset"
        assert simple_asset.id == 0
        assert simple_asset.name == "house"

    def test_to_dict(self, simple_asset):
        asset_dict = simple_asset.to_dict()
        assert asset_dict == dict(id=0, name="house", model_name="asset")


@pytest.fixture
def simple_request():
    request = Request(
        id=0,
        asset_id=0,
        name="grease bearings",
        due_date_iso8601="2020-08-01",
        recurrence_period_days=365,
        comment="use lithium grease",
    )
    return request


class TestRequest:
    def test_create_asset(self, simple_request):
        assert simple_request.model_name == "request"
        assert simple_request.id == 0
        assert simple_request.name == "grease bearings"
        assert simple_request.due_date_iso8601 == "2020-08-01"
        assert simple_request.recurrence_period_days == 365
        assert simple_request.comment == "use lithium grease"


def get_db():
    test_db_path = Path.home() / Path(".gofixit/gofixit_test.json")
    db = TinyDB(test_db_path)
    return db


@pytest.fixture
def empty_db():
    db = get_db()
    db.purge()
    yield db
    db.purge()


@pytest.fixture
def db_with_simple_asset():
    db = get_db()
    db.purge()
    asset_table = AssetTable(db)
    asset_table.insert(simple_asset())
    yield db
    db.purge()


class TestAssetTable:
    def test_insert(self, empty_db, simple_asset):
        asset_table = AssetTable(empty_db)
        asset_table.insert(simple_asset)
        assert empty_db.all()[0] == simple_asset.to_dict()

    def test_update(self, db_with_simple_asset, simple_asset):
        asset_table = AssetTable(db_with_simple_asset)
        asset_table.update({'name': 'the house'}, simple_asset.id)
        updated_asset_dict = simple_asset.to_dict()
        updated_asset_dict.update(name='the house')
        assert db_with_simple_asset.all()[0] == updated_asset_dict
