#!/opt/opsware/bin/python2.7
# coding:utf-8
import sys
import time
sys.path.append("/opt/opsware/pylibs27")
from pytwist import *
from pytwist.com.opsware.search import Filter

# Check Input
cust_list = ['Windows', 'LINUX', 'RS6000', 'SECURITY', 'BSAE']
ops_list = ['set', 'check']
if len(sys.argv) == 1:
    print "Input is null, Please check"
    print "Example set_customer.py {SA name} {set|check} {Windows|LINUX|RS6000|SECURITY|BSAE}"
    sys.exit(1)
elif len(sys.argv) == 2:
    hostName = sys.argv[1]
    print "Input is %s, Please check" % hostName
    print "Example set_customer.py {SA name} {set|check} {Windows|LINUX|RS6000|SECURITY|BSAE}"
    sys.exit(1)
elif len(sys.argv) == 3:
    hostName = sys.argv[1]
    ops = sys.argv[2]
    print "Hostname is: %s" % hostName
    print "Ops is: %s" % ops
    if ops != 'check':
        print "Set customer is: null"
        print "Example set_customer.py {SA name} {set|check} {Windows|LINUX|RS6000|SECURITY|BSAE}"
        sys.exit(1)
elif len(sys.argv) == 4:
    hostName = sys.argv[1]
    ops = sys.argv[2]
    customer = sys.argv[3]
    print "Hostname is: %s" % hostName
    print "Ops is: %s" % ops
    print "Set customer is: %s" % customer
    if customer not in cust_list or ops not in ops_list:
        print "Customer not in {Windows|LINUX|RS6000|SECURITY|BSAE}, Please re-enter it"
        sys.exit(1)
else:
    print "Input incorrect, Please check"
    print "Example set_customer.py {SA name} {set|check} {Windows|LINUX|RS6000|SECURITY|BSAE}"
    sys.exit(1)

# Connect Twist API
ts = twistserver.TwistServer()

# Get Server Object Info
serverservice = ts.server.ServerService
customerservice = ts.locality.CustomerService
filter = Filter()
filter.expression = 'ServerVO.hostName = "%s"' % (hostName)
filter1 = Filter()
filter1.expression = 'CustomerVO.name = "%s"' % (customer)
server = serverservice.findServerRefs(filter)
ops_server = serverservice.getServerVO(server[0])
set_server = server[0]
customers = customerservice.findCustomerRefs(filter1)
set_customer = customers[0]
if len(server) == 0:
    print "Server name input is: ", hostName
    print "Server not found, Please check"
    sys.exit(1)

if ops == "check":
    print ""
    print "Get server information..."
    print "Server SA Name: ", ops_server.name
    print "Server Host Name: ", ops_server.hostName
    print "Management status: ", ops_server.opswLifecycle
    print "Agent status: ", ops_server.state
    print "Agent Version: ", ops_server.agentVersion
    ct = serverservice.getCommCheckDate(server[0])
    time_local = time.localtime(ct)
    comm_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    print "Last Communication Test: ", comm_time
    print "Customer: ", ops_server.customer.name
    print "Facility: ", ops_server.facility.name
    print "Managed Date: ", ops_server.discoveredDate
    print "OS: ", ops_server.osVersion
    print "IP Address: ", ops_server.managementIP
    print "Manufacturer: ", ops_server.manufacturer
    print "Mode: ", ops_server.model
    print "SerialNumber: ", ops_server.serialNumber
    # print "Virtualization: ", ops_server.virtualizationType
else:
    print ""
    print "Server SA Name: ", ops_server.name
    print "Execute set customer to: ", customer
    set_cust = serverservice.setCustomer(set_server, set_customer)
    print "Server %s set customer to %s is done" % (hostName, customer)
