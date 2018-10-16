#!/opt/opsware/bin/python2.7
# coding:utf-8
# Run communication test on SA
import sys
import time
sys.path.append("/opt/opsware/pylibs27")
from pytwist import *
from pytwist.com.opsware.search import Filter

# Connect twist
ts = twistserver.TwistServer()
if len(sys.argv) == 1:
  print "Input is null, Please input a hostname"
  sys.exit(1)
else:
  hostName = sys.argv[1]

# Get Server Object Info
serverservice = ts.server.ServerService
filter = Filter()
#ServerVO.hostName是主机名, ServerVO.name是SA name
filter.expression = 'ServerVO.name = "%s"' % (hostName)
server = serverservice.findServerRefs(filter)
if len(server) == 0:
  print "Input error, Host not found"
  sys.exit(1)
else:
  print "Find Server: ",server

# Run Communication Test
jobinfo=serverservice.runAgentCommTest(server)

# Get Job Info
jobservice = ts.job.JobService
jobservice.getJobInfoVO(jobinfo)
print jobservice.getJobInfoVO(jobinfo).description
i=jobservice.getJobInfoVO(jobinfo).status
while i == 1 :
    time.sleep(1)
    i=jobservice.getJobInfoVO(jobinfo).status
serverInfos=jobservice.getJobInfoVO(jobinfo).serverInfo
for serverInfo in serverInfos:
    print "server:%s, status:%s" %(serverInfo.server.name, serverInfo.status)
    if serverInfo.status ==1 :
        print 'Communication Test result: success'
    else:
       print 'Communication Test result: failure!'
