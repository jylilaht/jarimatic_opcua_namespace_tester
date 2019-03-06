import asyncio
import sys
sys.path.insert(0, "..")
import logging
from asyncua import Client, Node, ua

#logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
_logger = logging.getLogger('asyncua')


async def main():
    print()
    print("Jarimatic OPC UA Namespace tester (c) Jari Ylilahti 2019")

    #get host address from console
    print()
    url = "opc.tcp://localhost:4840"                               #default host for testing
    print("Input host address: (for example opc.tcp://localhost:4840)")    
    hostaddr = input(">> " )
    if(hostaddr != ""):
        url = hostaddr
        print("Using host " + str(url))
    else:
        url = "opc.tcp://localhost:4840"                               #default host for testing
        print("Using default host " + str(url))   

    try:
        async with Client(url=url) as client:
            
            print() # make space

            # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
            #root = client.get_root_node()
            #_logger.info('Objects node is: %r', root)

            # Node objects have methods to read and write node attributes as well as browse or populate address space
            #_logger.info('Children of root are: %r', await root.get_children())

            #get namespaces and select one from console
            print()
            nsa = await client.get_namespace_array()            # returns a list 
            nsalen = len(nsa)                                   # lenght of index
            for row in range(nsalen):                           # cycle through whole list
                print("[" + str(row) + "] " + str(nsa[row]))

            print()
            nsidx = 0                                           #default namespace idx for testing
            print("Select namespace:")                          #print query
            sel_uri = input(">> ")                              #get namespace from user
            nsidx = await client.get_namespace_index(sel_uri)
            print("Set namespace: " + "\nNamespace uri: " + str(sel_uri) + "\nNamespace index: " + str(nsidx))    #print feedback

            print()
            print("Input tag")
            print("Example: i=1 or s=mystringtypetag")
            tag1 = input(">> ")

            namespacestring = "ns=" + str(nsidx)
            tagstring = "s=" + str(tag1)
            nodestring = str(namespacestring) + ";" + str(tagstring)
            print()
            print("Read tag: " + nodestring)

            print()
            print("Press Enter to exit:")
            print(">> ")

    except Exception:
        _logger.exception('error')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(main())
    loop.close()
