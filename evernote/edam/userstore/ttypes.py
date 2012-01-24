#
# Autogenerated by Thrift
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#

from thrift.Thrift import *
import evernote.edam.type.ttypes
import evernote.edam.error.ttypes


from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None


class SponsoredGroupRole(object):
  """
  Enumeration of Sponsored Group Roles
  """
  GROUP_MEMBER = 1
  GROUP_ADMIN = 2
  GROUP_OWNER = 3

  _VALUES_TO_NAMES = {
    1: "GROUP_MEMBER",
    2: "GROUP_ADMIN",
    3: "GROUP_OWNER",
  }

  _NAMES_TO_VALUES = {
    "GROUP_MEMBER": 1,
    "GROUP_ADMIN": 2,
    "GROUP_OWNER": 3,
  }

class PublicUserInfo(object):
  """
   This structure is used to provide publicly-available user information
   about a particular account.
  <dl>
   <dt>userId:</dt>
     <dd>
     The unique numeric user identifier for the user account.
     </dd>
   <dt>shardId:</dt>
     <dd>
     The name of the virtual server that manages the state of
     this user. This value is used internally to determine which system should
     service requests about this user's data.  It is also used to construct
     the appropriate URL to make requests from the NoteStore.
     </dd>
   <dt>privilege:</dt>
     <dd>
     The privilege level of the account, to determine whether
     this is a Premium or Free account.
     </dd>
   </dl>
  
  Attributes:
   - userId
   - shardId
   - privilege
   - username
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'userId', None, None, ), # 1
    (2, TType.STRING, 'shardId', None, None, ), # 2
    (3, TType.I32, 'privilege', None, None, ), # 3
    (4, TType.STRING, 'username', None, None, ), # 4
  )

  def __init__(self, userId=None, shardId=None, privilege=None, username=None,):
    self.userId = userId
    self.shardId = shardId
    self.privilege = privilege
    self.username = username

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.userId = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.shardId = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.I32:
          self.privilege = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.STRING:
          self.username = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('PublicUserInfo')
    if self.userId != None:
      oprot.writeFieldBegin('userId', TType.I32, 1)
      oprot.writeI32(self.userId)
      oprot.writeFieldEnd()
    if self.shardId != None:
      oprot.writeFieldBegin('shardId', TType.STRING, 2)
      oprot.writeString(self.shardId)
      oprot.writeFieldEnd()
    if self.privilege != None:
      oprot.writeFieldBegin('privilege', TType.I32, 3)
      oprot.writeI32(self.privilege)
      oprot.writeFieldEnd()
    if self.username != None:
      oprot.writeFieldBegin('username', TType.STRING, 4)
      oprot.writeString(self.username)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class PremiumInfo(object):
  """
   This structure is used to provide information about a user's Premium account.
  <dl>
   <dt>currentTime:</dt>
     <dd>
     The server-side date and time when this data was generated.
     </dd>
   <dt>premium:</dt>
     <dd>
  	 True if the user's account is Premium.
     </dd>
   <dt>premiumRecurring</dt>
     <dd>
     True if the user's account is Premium and has a recurring payment method.
     </dd>
   <dt>premiumExpirationDate:</dt>
     <dd>
     The date when the user's Premium account expires, or the date when the user's
     account will be charged if it has a recurring payment method.
     </dd>
   <dt>premiumExtendable:</dt>
     <dd>
     True if the user is eligible for purchasing Premium account extensions.
     </dd>
   <dt>premiumPending:</dt>
     <dd>
     True if the user's Premium account is pending payment confirmation
     </dd>
   <dt>premiumCancellationPending:</dt>
     <dd>
     True if the user has requested that no further charges to be made; the Premium
     account will remain active until it expires.
     </dd>
   <dt>canPurchaseUploadAllowance:</dt>
     <dd>
     True if the user is eligible for purchasing additional upload allowance.
     </dd>
   <dt>sponsoredGroupName:</dt>
     <dd>
     The name of the sponsored group that the user is part of.
     </dd>
   <dt>sponsoredGroupRole:</dt>
     <dd>
     The role of the user within a sponsored group.
     </dd>
   </dl>
  
  Attributes:
   - currentTime
   - premium
   - premiumRecurring
   - premiumExpirationDate
   - premiumExtendable
   - premiumPending
   - premiumCancellationPending
   - canPurchaseUploadAllowance
   - sponsoredGroupName
   - sponsoredGroupRole
  """

  thrift_spec = (
    None, # 0
    (1, TType.I64, 'currentTime', None, None, ), # 1
    (2, TType.BOOL, 'premium', None, None, ), # 2
    (3, TType.BOOL, 'premiumRecurring', None, None, ), # 3
    (4, TType.I64, 'premiumExpirationDate', None, None, ), # 4
    (5, TType.BOOL, 'premiumExtendable', None, None, ), # 5
    (6, TType.BOOL, 'premiumPending', None, None, ), # 6
    (7, TType.BOOL, 'premiumCancellationPending', None, None, ), # 7
    (8, TType.BOOL, 'canPurchaseUploadAllowance', None, None, ), # 8
    (9, TType.STRING, 'sponsoredGroupName', None, None, ), # 9
    (10, TType.I32, 'sponsoredGroupRole', None, None, ), # 10
  )

  def __init__(self, currentTime=None, premium=None, premiumRecurring=None, premiumExpirationDate=None, premiumExtendable=None, premiumPending=None, premiumCancellationPending=None, canPurchaseUploadAllowance=None, sponsoredGroupName=None, sponsoredGroupRole=None,):
    self.currentTime = currentTime
    self.premium = premium
    self.premiumRecurring = premiumRecurring
    self.premiumExpirationDate = premiumExpirationDate
    self.premiumExtendable = premiumExtendable
    self.premiumPending = premiumPending
    self.premiumCancellationPending = premiumCancellationPending
    self.canPurchaseUploadAllowance = canPurchaseUploadAllowance
    self.sponsoredGroupName = sponsoredGroupName
    self.sponsoredGroupRole = sponsoredGroupRole

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I64:
          self.currentTime = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.BOOL:
          self.premium = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.BOOL:
          self.premiumRecurring = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.I64:
          self.premiumExpirationDate = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.BOOL:
          self.premiumExtendable = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 6:
        if ftype == TType.BOOL:
          self.premiumPending = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 7:
        if ftype == TType.BOOL:
          self.premiumCancellationPending = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 8:
        if ftype == TType.BOOL:
          self.canPurchaseUploadAllowance = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 9:
        if ftype == TType.STRING:
          self.sponsoredGroupName = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 10:
        if ftype == TType.I32:
          self.sponsoredGroupRole = iprot.readI32();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('PremiumInfo')
    if self.currentTime != None:
      oprot.writeFieldBegin('currentTime', TType.I64, 1)
      oprot.writeI64(self.currentTime)
      oprot.writeFieldEnd()
    if self.premium != None:
      oprot.writeFieldBegin('premium', TType.BOOL, 2)
      oprot.writeBool(self.premium)
      oprot.writeFieldEnd()
    if self.premiumRecurring != None:
      oprot.writeFieldBegin('premiumRecurring', TType.BOOL, 3)
      oprot.writeBool(self.premiumRecurring)
      oprot.writeFieldEnd()
    if self.premiumExpirationDate != None:
      oprot.writeFieldBegin('premiumExpirationDate', TType.I64, 4)
      oprot.writeI64(self.premiumExpirationDate)
      oprot.writeFieldEnd()
    if self.premiumExtendable != None:
      oprot.writeFieldBegin('premiumExtendable', TType.BOOL, 5)
      oprot.writeBool(self.premiumExtendable)
      oprot.writeFieldEnd()
    if self.premiumPending != None:
      oprot.writeFieldBegin('premiumPending', TType.BOOL, 6)
      oprot.writeBool(self.premiumPending)
      oprot.writeFieldEnd()
    if self.premiumCancellationPending != None:
      oprot.writeFieldBegin('premiumCancellationPending', TType.BOOL, 7)
      oprot.writeBool(self.premiumCancellationPending)
      oprot.writeFieldEnd()
    if self.canPurchaseUploadAllowance != None:
      oprot.writeFieldBegin('canPurchaseUploadAllowance', TType.BOOL, 8)
      oprot.writeBool(self.canPurchaseUploadAllowance)
      oprot.writeFieldEnd()
    if self.sponsoredGroupName != None:
      oprot.writeFieldBegin('sponsoredGroupName', TType.STRING, 9)
      oprot.writeString(self.sponsoredGroupName)
      oprot.writeFieldEnd()
    if self.sponsoredGroupRole != None:
      oprot.writeFieldBegin('sponsoredGroupRole', TType.I32, 10)
      oprot.writeI32(self.sponsoredGroupRole)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class AuthenticationResult(object):
  """
   When an authentication (or re-authentication) is performed, this structure
   provides the result to the client.
  <dl>
   <dt>currentTime:</dt>
     <dd>
     The server-side date and time when this result was
     generated.
     </dd>
   <dt>authenticationToken:</dt>
     <dd>
     Holds an opaque, ASCII-encoded token that can be
     used by the client to perform actions on a NoteStore.
     </dd>
   <dt>expiration:</dt>
     <dd>
     Holds the server-side date and time when the
     authentication token will expire.
     This time can be compared to "currentTime" to produce an expiration
     time that can be reconciled with the client's local clock.
     </dd>
   <dt>user:</dt>
     <dd>
     Holds the information about the account which was
     authenticated if this was a full authentication.  May be absent if this
     particular authentication did not require user information.
     </dd>
   <dt>publicUserInfo:</dt>
     <dd>
     If this authentication result was achieved without full permissions to
     access the full User structure, this field may be set to give back
     a more limited public set of data.
     </dd>
   </dl>
  
  Attributes:
   - currentTime
   - authenticationToken
   - expiration
   - user
   - publicUserInfo
  """

  thrift_spec = (
    None, # 0
    (1, TType.I64, 'currentTime', None, None, ), # 1
    (2, TType.STRING, 'authenticationToken', None, None, ), # 2
    (3, TType.I64, 'expiration', None, None, ), # 3
    (4, TType.STRUCT, 'user', (evernote.edam.type.ttypes.User, evernote.edam.type.ttypes.User.thrift_spec), None, ), # 4
    (5, TType.STRUCT, 'publicUserInfo', (PublicUserInfo, PublicUserInfo.thrift_spec), None, ), # 5
  )

  def __init__(self, currentTime=None, authenticationToken=None, expiration=None, user=None, publicUserInfo=None,):
    self.currentTime = currentTime
    self.authenticationToken = authenticationToken
    self.expiration = expiration
    self.user = user
    self.publicUserInfo = publicUserInfo

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I64:
          self.currentTime = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.authenticationToken = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.I64:
          self.expiration = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.STRUCT:
          self.user = evernote.edam.type.ttypes.User()
          self.user.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.STRUCT:
          self.publicUserInfo = PublicUserInfo()
          self.publicUserInfo.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('AuthenticationResult')
    if self.currentTime != None:
      oprot.writeFieldBegin('currentTime', TType.I64, 1)
      oprot.writeI64(self.currentTime)
      oprot.writeFieldEnd()
    if self.authenticationToken != None:
      oprot.writeFieldBegin('authenticationToken', TType.STRING, 2)
      oprot.writeString(self.authenticationToken)
      oprot.writeFieldEnd()
    if self.expiration != None:
      oprot.writeFieldBegin('expiration', TType.I64, 3)
      oprot.writeI64(self.expiration)
      oprot.writeFieldEnd()
    if self.user != None:
      oprot.writeFieldBegin('user', TType.STRUCT, 4)
      self.user.write(oprot)
      oprot.writeFieldEnd()
    if self.publicUserInfo != None:
      oprot.writeFieldBegin('publicUserInfo', TType.STRUCT, 5)
      self.publicUserInfo.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
