# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Geoffroy Ralet
#    Copyright (c) 2016 Telarcom sprl (http://www.telarcom.be)
#    All Rights Reserved
#
#    WARNING: This program as such is intended to be used by professional
#    programmers who take the whole responsibility of assessing all potential
#    consequences resulting from its eventual inadequacies and bugs.
#    End users who are looking for a ready-to-use solution with commercial
#    guarantees and support are strongly advised to contact a Free Software
#    Service Company.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Financial Cockpit Export data',
    'version': '8.0.1.0.0',
    'author': 'Geoffroy Ralet',
    'website': 'http://www.telarcom.be',
    'summary': "Financial Cockpit Export Data",
    'category': 'Other',
    'depends': [
        'base',
        'account'
    ],
    'description': """
Financial Cockpit Export Data
===============================================================
Export an Excel file containing account moves for choosen dates in Financial Cockpit format
Open wizard in : Menu Reporting/Accounting

    """,
    'data': [
        'wizard/fc_export_views.xml',
    ],
    'installable': True,
}

