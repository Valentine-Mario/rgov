#!/usr/bin/python

from rchain.crypto import PrivateKey
from pyrgov.rgov import rgovAPI

rgov = rgovAPI('localhost')
new1 = PrivateKey.generate()
new2 = PrivateKey.generate()
admin = rgov.get_private_key('bootstrap')

balance = rgov.checkBalance(admin.get_public_key().get_rev_address())
assert balance != 0

balance = rgov.checkBalance(new1.get_public_key().get_rev_address())
assert balance == 0

balance = rgov.checkBalance(new1.get_public_key().get_rev_address())
assert balance == 0

funds = 100000000
result = rgov.transfer(admin.get_public_key().get_rev_address(), new1.get_public_key().get_rev_address(), funds, admin)
assert result[0]
result = rgov.transfer(admin.get_public_key().get_rev_address(), new2.get_public_key().get_rev_address(), funds, admin)
assert result[0]

balance = rgov.checkBalance(new1.get_public_key().get_rev_address())
assert balance == funds
balance = rgov.checkBalance(new2.get_public_key().get_rev_address())
assert balance == funds

# peek before any Inbox has been created
result = rgov.peekInbox(new1, "inbox", "", "")
assert len(result) == 0

result = rgov.newInbox(new1)
new1URI = result[2]

result = rgov.peekInbox(new1, "inbox", "", "")

assert result == new1URI

result = rgov.newInbox(new2)
new2URI = result[2]

result = rgov.peekInbox(new2, "inbox", "", "")
assert result == new2URI

result = rgov.newIssue(new1, "inbox", "lunch", ["pizza", "tacos", "salad"])

result = rgov.peekInbox(new1, "inbox", "", "")
assert result == new1URI

result = rgov.addVoterToIssue(new1, "inbox", new2URI, "lunch")
result = rgov.peekInbox(new2, "inbox", "", "")
assert result == new2URI
