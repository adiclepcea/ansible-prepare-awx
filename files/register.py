"module to autoregister myself in awx"
import urlparse
import json
import socket
import urllib2
import ssl
import base64

HOST = "https://192.168.1.109:9443"
USERNAME = "test"
PASSWORD = "test123"
INVENTORY_NAME = "RPI inventory"
VERIFY_SSL=False

if not VERIFY_SSL:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
else:
    ctx = ssl.create_default_context()
    ctx.check_hostname = True


def get_ip():
    "function to get the ip of the local machine"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        sock.connect(('101.101.255.255', 1))
        ip_address = sock.getsockname()[0]
    except:
        ip_address = '127.0.0.1'
    finally:
        sock.close()
    return ip_address

def get_inventory_id_from_json(resp):
    "obtain the id of the inventory where we will add ourselves from the json obtained from awx"
    j = json.loads(resp)
    if j["results"] == None or not j["results"]:
        return None

    res = [x for x in j["results"] if x["name"] == INVENTORY_NAME]

    if not res:
        return None

    return res[0]["id"]


def get_inventory_id(link):
    "query awx for repositories and return the inventory where we will add ourselves"
    #response = requests.get(link, auth=(USERNAME, PASSWORD))
    request = urllib2.Request(link)
    auth = base64.encodestring("%s:%s" % (USERNAME, PASSWORD)).replace("\n", "")
    request.add_header("Authorization", "Basic %s" % auth)
    try:
        response = urllib2.urlopen(request, context=ctx)
        return get_inventory_id_from_json(response.read())
    except urllib2.HTTPError, e:
        print e.code
    except urllib2.URLError, e:
        print e.reason
    return None

def add_self_to_awx():
    "add self to awx inventory"
    inventory_link = urlparse.urljoin(HOST, "api/v2/inventories/")
    host_link = urlparse.urljoin(HOST, "api/v2/hosts/")
    inventory_id = get_inventory_id(inventory_link)
    
    if inventory_id == None:
        print "No inventory by the name", INVENTORY_NAME, " was found"
        return
    js_data = json.dumps({"name":get_ip(), "inventory":inventory_id}).encode("utf8")
    clen = len(js_data)
    auth = base64.encodestring("%s:%s" % (USERNAME, PASSWORD)).replace("\n", "")
    request = urllib2.Request(host_link, js_data)
    request.get_method = lambda: "POST"
    request.add_header("Authorization", "Basic %s" % auth)
    request.add_header("Content-type", "application/json")
    request.add_header("Content-length", clen)

    try:
        response = urllib2.urlopen(request, context=ctx)
        with(open("out.txt", "a")) as res_file:
            res_file.write(response.read())
    except urllib2.HTTPError, e:
        if e.code == 400:
            print e
            print "Already registered?"
            return
        print e.code
    except urllib2.URLError, e:
        print e.reason


add_self_to_awx()
#print get_ip()
