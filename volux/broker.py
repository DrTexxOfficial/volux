# builtin
import logging

# module
import volux.request

log = logging.getLogger("volux broker")
log.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
ch.setFormatter(formatter)
# add the handlers to the logger
log.addHandler(ch)


class VoluxBroker:
    def __init__(self, operator):
        self.operator = operator

    def process_request(self, request, verbose=True):

        if issubclass(type(request), volux.request.VoluxBrokerRequest) is True:

            mUUID = request.module.UUID

            log.debug(
                "request from {} is a valid subclass...".format(
                    request.module._module_name
                )
            )
            log.debug("UUID of requesting module: {}".format(mUUID))

            if type(request) in request.module.req_permissions:

                log.debug(
                    "{} claims it's allowed to {}".format(
                        request.module._module_name, request.req_string
                    )
                )

                if type(request) in self.operator.permissions[mUUID]:

                    log.debug("Operator verified module's permissions")

                    req_type = type(request)

                    log.debug(
                        "{} is requesting to '{}'...".format(
                            request.module._module_name, request.req_string
                        )
                    )

                    if req_type == volux.request.AddConnection:

                        self.operator.add_connection(request.connection)

                    elif req_type == volux.request.RemoveConnection:

                        self.operator.remove_connection(request.connection)

                    elif req_type == volux.request.GetConnections:

                        return self.operator.connections

                    elif req_type == volux.request.StartSync:

                        self.operator.start_sync()

                    elif req_type == volux.request.SyncState:

                        return self.operator.running

                    elif req_type == volux.request.StopSync:

                        self.operator.stop_sync()

                    elif req_type == volux.request.GetSyncDeltas:

                        return self.operator.get_sync_deltas()

                    elif req_type == volux.request.GetConnectionNicknames:

                        return self.operator.get_connection_nicknames()

                    else:

                        raise TypeError(
                            "volux broker recieved an invalid request type: {}".format(
                                type(request)
                            )
                        )

                else:

                    raise PermissionError(
                        "operator could not verify module '{}' had valid permissions".format(
                            request.module._module_name
                        )
                    )

            else:

                raise PermissionError(
                    "module {} doesn't claim it's allowed to {} ({})".format(
                        request.module._module_name,
                        request.req_string,
                        type(request),
                    )
                )

        else:

            raise TypeError("request must be a subclass of VoluxBrokerRequest")
