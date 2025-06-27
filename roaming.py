import logging
import time

logger = logging.getLogger(__name__)


class RoamingMonitor:
    def __init__(self, udp_server):
        self._udp_server = udp_server
        self._udp_server.register_driver(self)

        self._locations = {}

    def close(self):
        # TODO: Implement proper shutdown of this function.
        pass

    def get_addr(self, number):
        if number in self._locations:
            return self._locations[number]["addr"]
        return None

    def get_roaming_table(self):
        """
        Restituisce la tabella di roaming attuale per debug.
        """
        return dict(self._locations)

    def print_roaming_table(self):
        """
        Stampa la tabella di roaming per debug.
        """
        if self._locations:
            logger.info("=== ROAMING TABLE ===")
            for ext, info in self._locations.items():
                logger.info(f"  Extension {ext}: {info['addr']} (last seen: {time.ctime(info['time'])})")
            logger.info("====================")
        else:
            logger.info("Roaming table is empty")

    def process(self, xml_message, addr):
        if xml_message.tag == "request" and xml_message.attrib["type"] == "systeminfo":
            #                xml_message.tag == "request" and xml_message.attrib["type"] == "alarm": # not sure if this updates only contain connected phones...
            logger.debug("Systeminfo update received")

            senderdata = xml_message.find("senderdata")
            for element in senderdata.findall("address"):
                if element.text in self._locations:
                    if not self._locations[element.text]["addr"] == addr:
                        logger.info("Updated {}  to {}".format(element.text, addr))
                        self._locations[element.text]["addr"] = addr
                        self._locations[element.text]["time"] = time.time()
                    else:
                        logger.info("Already known: {} on {}".format(element.text, addr))
                        self._locations[element.text]["time"] = time.time()
                else:
                    logger.info("Added {} on {}".format(element.text, addr))
                    self._locations[element.text] = {"addr": addr, "time": time.time()}
                    self.print_roaming_table()  # Mostra la tabella quando si aggiunge qualcuno

        if xml_message.tag == "request" and xml_message.attrib["type"] == "login":
            logger.debug("Login event received")

            status = xml_message.find("logindata").find("status")
            address = xml_message.find("senderdata").find("address")

            if status.text == "0":
                if address.text in self._locations:
                    logger.info("{} logged out".format(address.text))
                    del self._locations[address.text]
                else:
                    logger.info("{} logged out but wasn't known".format(address.text))
            elif status.text == "1":
                if address.text in self._locations:
                    logger.info("{} logged in on {} and was already known".format(address.text, addr))
                    self._locations[address.text]["addr"] = addr
                    self._locations[address.text]["time"] = time.time()
                else:
                    logger.info("{} logged in on {} (and wasn't known until know...)".format(address.text, addr))
                    self._locations[address.text] = {"addr": addr, "time": time.time()}
                    self.print_roaming_table()  # Mostra la tabella quando qualcuno fa login

        return False
