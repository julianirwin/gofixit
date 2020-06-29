#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 20:52:21 2020

@author: Julian
"""

from gofixit import Asset, Request


class TestAsset():
    def test_create_asset(self):
        asset = Asset(0, 'house')

    def test_asset_properties(self):
        asset = Asset(0, 'house')
        assert asset.model_name == 'asset'
        assert asset.id == 0
        assert asset.name == 'house'

    def test_to_dict(self):
        asset = Asset(0, 'house')
        asset_dict = asset.to_dict()
        assert asset_dict == dict(id=0, name='house', model_name='asset')


class TestRequest():
    def test_create_asset(self):
        request = Request(
            id=0,
            asset_id=0,
            name='grease bearings',
            due_date_iso8601='2020-08-01',
            recurrence_period_days=365,
            comment='use lithium grease'
        )
        assert request.model_name == 'request'
        assert request.id == 0
        assert request.name == 'grease bearings'
        assert request.due_date_iso8601 == '2020-08-01'
        assert request.recurrence_period_days == 365
        assert request.comment == 'use lithium grease'
