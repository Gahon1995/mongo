import time

import bson
import logging

logger = logging.getLogger('status')


def check_mongodb(client):
    try:
        # connect = pymongo.Connection(host,int(port))
        # client = pymongo.MongoClient(host, int(port))
        # db = client['admin']
        # db.authenticate(user,passwd)
        serverStatus = client.admin.command(bson.son.SON([('serverStatus', 1), ('repl', 2)]))
        time.sleep(1)
        # serverStatus_2 = client.admin.command(bson.son.SON([('serverStatus', 1), ('repl', 2)]))
        # connect = 1
        # ok = int(serverStatus['ok'])
        # version = serverStatus['version']
        uptime = serverStatus['uptime']
        connections_current = serverStatus['connections']['current']
        # connections_available = serverStatus['connections']['available']
        # globalLock_activeClients = serverStatus['globalLock']['activeClients']['total']
        # globalLock_currentQueue = serverStatus['globalLock']['currentQueue']['total']
        # mem_bits = serverStatus['mem']['bits']
        # mem_resident = serverStatus['mem']['resident']
        # mem_virtual = serverStatus['mem']['virtual']
        # mem_supported = serverStatus['mem']['supported']
        # mem_mapped = serverStatus['mem']['mapped']
        # mem_mappedWithJournal = serverStatus['mem']['mappedWithJournal']
        # network_bytesIn_persecond = int(serverStatus_2['network']['bytesIn'])
        # - int(serverStatus['network']['bytesIn'])
        # network_bytesOut_persecond = int(serverStatus_2['network']['bytesOut']) - int(
        #     serverStatus['network']['bytesOut'])
        # network_numRequests_persecond = int(serverStatus_2['network']['numRequests']) - int(
        #     serverStatus['network']['numRequests'])
        # opcounters_insert_persecond = int(serverStatus_2['opcounters']['insert']) - int(
        #     serverStatus['opcounters']['insert'])
        # opcounters_query_persecond = int(serverStatus_2['opcounters']['query']) - int(
        #     serverStatus['opcounters']['query'])
        # opcounters_update_persecond = int(serverStatus_2['opcounters']['update']) - int(
        #     serverStatus['opcounters']['update'])
        # opcounters_delete_persecond = int(serverStatus_2['opcounters']['delete']) - int(
        #     serverStatus['opcounters']['delete'])
        # opcounters_command_persecond = int(serverStatus_2['opcounters']['command']) - int(
        #     serverStatus['opcounters']['command'])

        # replset
        try:
            repl = serverStatus['repl']
            # setName = repl['setName']
            # replicaset = 1
            if repl['secondary'] == True:
                repl_role = 'secondary'
                # repl_role_new = 's'
            else:
                repl_role = 'master'
                # repl_role_new = 'm'
        except Exception:
            # replicaset = 0
            repl_role = 'master'
            # repl_role_new = 'm'
            pass

        # print(connect, replicaset, repl_role, ok, uptime, version, connections_current, connections_available,
        #       globalLock_currentQueue, globalLock_activeClients, mem_bits, mem_resident, mem_virtual, mem_supported,
        #       mem_mapped, mem_mappedWithJournal, network_bytesIn_persecond, network_bytesOut_persecond,
        #       network_numRequests_persecond, opcounters_insert_persecond, opcounters_query_persecond,
        #       opcounters_update_persecond, opcounters_delete_persecond, opcounters_command_persecond)

        data = {
            'connections_current': connections_current,
            'repl_role': repl_role,
            'uptime': uptime,
            'replica': {
                'hosts': repl['hosts'],
                'primary': repl['primary'],
                'me': repl['me']
            }
        }

        return data

    except Exception as e:
        logger_msg = "check mongodb  error"
        logger.warning(logger_msg)
        data = {
            'connections_current': 0,
            'repl_role': 'other',
            'uptime': '',
            'replica': {
                'hosts': [],
                'primary': None,
                'me': None
            }
        }
        return data
