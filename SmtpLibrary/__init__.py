#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of robotframework-smtplibrary.
# https://github.io/lucamaro/robotframework-smtplibrary

# Licensed under the Apache License 2.0 license:
# http://www.opensource.org/licenses/Apache-2.0
# Copyright (c) 2016, Luca Maragnani <luca.maragnani@gmail.com>

from SmtpLibrary.version import __version__  # NOQA

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

COMMASPACE = ', '

class SmtpLibrary(object):
    '''
    SMTP Client class
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.message = MailMessage()
        self.host = None
        self.port = None
        self.user = None
        self.password = None
        self.smtp = None

    def _prepare_connection(self, host, port, user=None, password=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        
        
    def prepare_ssl_connection(self, host, port=465, user=None, password=None):
        self._prepare_connection(host, port, user, password)
        self.smtp = smtplib.SMTP_SSL()

    def prepare_connection(self, host, port=25, user=None, password=None, use_ssl=False):
        self._prepare_connection(host, port, user, password)
        self.smtp = smtplib.SMTP()

    def add_to_recipients(self, toadd):
        '''takes string as paramater'''
        self.message.mailTo.append(toadd)
        
    def add_cc_recipients(self, cc):
        '''takes string as parameter'''        
        self.message.mailTo.append(cc)

    def add_bcc_recipients(self, bcc):
        '''takes string as parameter'''        
        self.message.mailBcc.append(bcc)

    def set_subject(self, subj):
        '''takes string as parameter'''
        self.message.subject = subj
        
    def set_from(self, fromadd):
        '''takes string as parameter'''
        self.message.mailFrom = fromadd
        
    def set_body(self, body):
        '''takes string as parameter'''
        self.message.body = body
        
    def set_random_body(self, size):
        '''generate a random body of the size given'''
        body = ''
        for i in range(int(size)/80):
            for x in range(80):
                body += ''.join(random.choice(string.uppercase + string.digits))
            body += "\n"
        self.message.body = body
      
    def add_attachments(self, attach):
        '''takes string as parameter representig the path to the file to attach'''  
        self.message.attachments.append(attach)
        
    def send_message(self):
        '''
            Send the message
        '''
        
        if len (self.message.attachments) > 0 : 
            envelope = MIMEMultipart()
            envelope.attach(MIMEText(self.message.body))
        else:
            envelope =  MIMEText(self.message.body)
        
        envelope['Subject'] = self.message.subject
        
        recipients = []
        recipients.extend(self.message.mailTo)
        recipients.extend(self.message.mailCc)
        recipients.extend(self.message.mailBcc)
        
        envelope['From'] = self.message.mailFrom
        envelope['To'] = COMMASPACE.join(self.message.mailTo)
        envelope['Cc'] = COMMASPACE.join(self.message.mailCc)
        
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
                fp = open(attachment)
                # TODO: we should handle calculating the charset
                msg = MIMEText(fp.read(), _subtype=subtype, _charset = 'utf-8')
                fp.close()
            elif maintype == 'image':
                fp = open(attachment, 'rb')
                msg = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == 'audio':
                fp = open(attachment, 'rb')
                msg = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(attachment, 'rb')
                msg = MIMEBase(maintype, subtype)
                msg.set_payload(fp.read())
                fp.close()
                # Encode the payload using Base64
                encoders.encode_base64(msg)                
    
            # Set the filename parameter
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))
            envelope.attach(msg)

        # Send the message
        self.smtp.connect(self.host, self.port)
        self.smtp.ehlo(socket.gethostname())
        
        if self.user is not None:
            self.smtp.login (self.user, self.password)

        self.smtp.sendmail(self.message.mailFrom, recipients, envelope.as_string())
        
        self.smtp.close()
        
        
        
    def send_message_with_all_parameters(self, host, user, password, subj, fromadd, toadd, cc=None, bcc=None, body=None, attach=None):
        '''cc, bcc and attach parameters may be strings or array of strings
        host, user, password, subj, fromadd, toadd - are mandatory parameters
        to use the optional paramaters pleas specify the name fo the parameter in the call
        user and password even if mandatory could be set to None so no authentication will be made
            Example:
            sendMail("smtp.mail.com", None, None, "The subject", "me@mail.com", "friend@mai.com", body="Hello World body") 
            
            sendMail("smtp.mail.com", "scott", "tiger", "The subject", "me@mail.com", "friend@mai.com", body="Hello World body", attach=attaches
        where could be:
        attaches = ["c:\\desktop\\file1.zip", "c:\\desktop\\file2.zip"] or
        attaches = "c:\\desktop\\file1.zip" '''
     
        self.host = host
        self.user = user
        self.password = password

        self.set_subject(subj)
        self.set_from(fromadd)
        self.add_to_recipients(toadd)
        if cc != None:
            self.add_cc_recipients(cc)
        if bcc != None:
            self.add_bcc_recipients(bcc)
        #Fill the message
        if body != None:
            self.set_body(body)
        # Part two is attachment
        if attach != None:
            self.add_attachments(attach)
        
        self.send_message()
        
        
class MailMessage :
    ''' Simplified email message
        This class represent email headers and payload content, not envelope data'''
    
    def __init__ (self):
        self.id = None
        self.uid = None
        self.mailFrom = None
        self.mailTo = []
        self.mailCc = []
        self.mailBcc = []
        self.subject = ''
        self.body = ''
        self.attachments = []
        self.size = -1
        
        # email.message
        self.message = None
        
    def set_id (self, id):
        self.id = id
        
    def set_uid (self, uid):
        self.uid = uid
        
    def set_size(self, size):
        self.size = size
        
    def get_size(self):
        return self.size
    
