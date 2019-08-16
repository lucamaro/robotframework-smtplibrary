#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of robotframework-smtplibrary.
# https://github.io/lucamaro/robotframework-smtplibrary

# Licensed under the Apache License 2.0 license:
# http://www.opensource.org/licenses/Apache License 2.0-license
# Copyright (c) 2016, Luca Maragnani <luca.maragnani@gmail.com>

from sys import path
path.append('SmtpLibrary')
import SmtpLibrary
import mock
import unittest
from unittest.mock import MagicMock

# library = SmtpLibrary()

class SmtpLibraryTests(unittest.TestCase):

    def setUp(self):
        """Instantiate the Smtp library class."""
        self.library = SmtpLibrary.SmtpLibrary()
        self.password = 'password'
        self.port = 465
        self.user = 'my@domain.com'
        self.recipient = 'noreply@domain.com'
        self.host = 'my.smtp'

    @mock.patch('smtplib.SMTP_SSL')
    def test_should_prepare_connection_ssl(self, mock_smtp):
        """Open mailbox should open secure connection to SMTP server
        with requested credentials.
        """
        self.library.prepare_ssl_connection(self.host, self.port, self.user,
                                            self.password)
        self.library.login()
        self.library.smtp.login.assert_called_with(self.user, self.password)

    @mock.patch('smtplib.SMTP_SSL')
    def test_set_from(self, mock_smtp):
        """Test from email"""
        self.library.prepare_ssl_connection(host=self.host, port=self.port, user=self.user,
                                            password=self.password)
        self.library.login()
        self.library.smtp.login.assert_called_with(self.user, self.password)
        self.library.set_from(self.user)
        self.library.smtp.set_from(self.user)


    @mock.patch('smtplib.SMTP_SSL')
    def test_to_reciept(self, mock_smtp):
        """"Test to email"""""
        self.library.prepare_ssl_connection(host=self.host, port=self.port, user=self.user,
                                            password=self.password)
        self.library.login()
        self.library.smtp.login.assert_called_with(self.user, self.password)
        self.library.set_from(self.user)
        self.library.smtp.add_to_recipient(self.recipient)

    @mock.patch('smtplib.SMTP_SSL')
    def test_send_message(self, mock_smtp):
        """"Test email sent"""""
        self.library.prepare_ssl_connection(host=self.host, port=self.port, user=self.user,
                                            password=self.password)
        self.library.login()
        self.library.smtp.login.assert_called_with(self.user, self.password)
        self.library.set_from(self.user)
        self.library.smtp.add_to_recipient(self.recipient)
        self.library.smtp.send_message(self.user) is not None
        self.library.smtp.send_message(self.recipient) is not None

    @mock.patch('smtplib.SMTP_SSL')
    def test_should_close_connection(self, mock_smtp):
        """Close opened connection."""
        self.library.prepare_ssl_connection(self.host, self.port, self.user,
                                            self.password)
        self.library.login()
        self.library.smtp.login.assert_called_with(self.user, self.password)
        self.library.smtp.close_connection()
        self.library.smtp.close()
