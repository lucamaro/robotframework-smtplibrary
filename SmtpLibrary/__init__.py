#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of robotframework-smtplibrary.
# https://github.io/lucamaro/robotframework-smtplibrary

# Licensed under the Apache License 2.0 license:
# http://www.opensource.org/licenses/Apache-2.0
# Copyright (c) 2016, Luca Maragnani <luca.maragnani@gmail.com>

"""
Library implementation
"""

import smtplib
import email
import random
import string
import mimetypes
import quopri
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import os.path
import socket
from robot.api.deco import keyword

from SmtpLibrary.version import __version__  # NOQA

COMMASPACE = ', '

class SmtpLibrary(object):
    """
    SMTP Client class
    """

    def __init__(self):
        """
        Constructor
        """
        self.message = self._MailMessage()
        self.host = None
        self.port = None
        self.user = None
        self.password = None
        self.smtp = None

    def _prepare_connection(self, host, port, user=None, password=None):
        """
        Private method to collect connection informations
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password


    def prepare_ssl_connection(self, host, port=465, user=None, password=None):
        """
        Collect connection informations for SSL channel
        """
        self._prepare_connection(host, port, user, password)
        self.smtp = smtplib.SMTP_SSL()

    def prepare_connection(self, host, port=25, user=None, password=None):
        """
        Collect connection informations for unencrypted channel
        """
        self._prepare_connection(host, port, user, password)
        self.smtp = smtplib.SMTP()

    def add_to_recipient(self, recipient):
        """
        Add a recipient to "To:" list
        """
        self.message.mail_to.append(recipient)

    def add_cc_recipient(self, recipient):
        """
        Add a recipient to "Cc:" list
        """
        self.message.mail_cc.append(recipient)

    def add_bcc_recipient(self, recipient):
        """
        Add a recipient to "Bcc:" list
        """
        self.message.mail_bcc.append(recipient)

    def set_subject(self, subj):
        """
        Set email subject
        """
        self.message.subject = subj

    def set_from(self, from_recipient):
        """
        Set from address of message and envelope
        """
        self.message.mail_from = from_recipient

    def set_body(self, body):
        """
        Set email body
        """
        self.message.body = body

    def set_random_body(self, size):
        """
        Set a random body of <size> length
        """
        body = ''
        for i in range(0, size):
            body += ''.join(random.choice(string.uppercase + string.digits))
            if i % 80 == 0:
                body += "\n"
        self.message.body = body

    def add_attachment(self, attach):
        """
        Add attachment to a list of filenames
        """
        self.message.attachments.append(attach)

    def add_header(self, name, value):
        """
        Add a custom header to headers list
        """
        self.message.headers[name] = value

    def send_message(self):
        """
            Send the message
        """
        if len(self.message.attachments) > 0:
            envelope = MIMEMultipart()
            envelope.attach(MIMEText(self.message.body))
        else:
            envelope = MIMEText(self.message.body)

        envelope['Subject'] = self.message.subject

        recipients = []
        recipients.extend(self.message.mail_to)
        recipients.extend(self.message.mail_cc)
        recipients.extend(self.message.mail_bcc)

        envelope['From'] = self.message.mail_from
        envelope['To'] = COMMASPACE.join(self.message.mail_to)
        envelope['Cc'] = COMMASPACE.join(self.message.mail_cc)

        envelope['Subject'] = self.message.subject

        for attachment in self.message.attachments:
            ctype, encoding = mimetypes.guess_type(attachment)
            if ctype is None or encoding is not None:
                # No guess could be made, or the file is encoded (compressed), so
                # use a generic bag-of-bits type.
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)

            msg = None
            if maintype == 'text':
                attach_file = open(attachment)
                # TODO: we should handle calculating the charset
                msg = MIMEText(attach_file.read(), _subtype=subtype, _charset='utf-8')
                attach_file.close()
            elif maintype == 'image':
                attach_file = open(attachment, 'rb')
                msg = MIMEImage(attach_file.read(), _subtype=subtype)
                attach_file.close()
            elif maintype == 'audio':
                attach_file = open(attachment, 'rb')
                msg = MIMEAudio(attach_file.read(), _subtype=subtype)
                attach_file.close()
            else:
                attach_file = open(attachment, 'rb')
                msg = MIMEBase(maintype, subtype)
                msg.set_payload(attach_file.read())
                attach_file.close()
                # Encode the payload using Base64
                encoders.encode_base64(msg)

            # Set the filename parameter
            msg.add_header('Content-Disposition', 'attachment',
                           filename=os.path.basename(attachment))
            envelope.attach(msg)

        # Send the message
        self.smtp.connect(self.host, self.port)
        self.smtp.ehlo(socket.gethostname())

        if self.user is not None:
            self.smtp.login(self.user, self.password)

        self.smtp.sendmail(self.message.mail_from, recipients, envelope.as_string())

        self.smtp.close()

    @keyword('Send Message With All Parameters')
    def send_message_full(self, host, user, password, subj,
                          from_recipient, to_recipient, cc_recipient=None, bcc_recipient=None,
                          body=None, attach=None):
        """
        Send a message specifing all parameters on the same linecc
        cc, bcc and attach parameters may be strings or array of strings
        host, user, password, subj, fromadd, toadd - are mandatory parameters
        to use the optional paramaters pleas specify the name fo the parameter in the call
        user and password even if mandatory could be set to None so no authentication will be made
            Example:
            sendMail("smtp.mail.com", None, None, "The subject", "me@mail.com", "friend@mai.com", body="Hello World body")

            sendMail("smtp.mail.com", "scott", "tiger", "The subject", "me@mail.com", "friend@mai.com", body="Hello World body", attach=attaches
        where could be:
        attaches = ["c:\\desktop\\file1.zip", "c:\\desktop\\file2.zip"] or
        attaches = "c:\\desktop\\file1.zip" """

        self.host = host
        self.user = user
        self.password = password

        self.set_subject(subj)
        self.set_from(from_recipient)
        self.message.mail_to = to_recipient
        if cc_recipient != None:
            self.message.mail_cc = cc_recipient
        if bcc_recipient != None:
            self.message.mail_bcc = bcc_recipient
        #Fill the message
        if body != None:
            self.set_body(body)
        # Part two is attachment
        if attach != None:
            self.message.attachments = attach

        self.send_message()


    class _MailMessage:
        """
        Simplified email message
        This class represent email headers and payload content, not envelope data
        """

        def __init__(self):
            """
            init object variables
            """
            self.mail_from = None
            self.mail_to = []
            self.mail_cc = []
            self.mail_bcc = []
            self.subject = ''
            self.body = ''
            self.attachments = []
            self.headers = {}
